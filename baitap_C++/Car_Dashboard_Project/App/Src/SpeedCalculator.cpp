#include "SpeedCalculator.hpp"


#define LOAD  120   //giả sử tải trọng là 120 kg

//điều chỉnh cường độ gas và phanh dựa trên trạng thái bàn đạp 
void SpeedCalculator::AdjustGasBrakeLevel(bool isGasApplied, bool isBrakeApplied){
    if(isGasApplied && !isBrakeApplied) {
        safetyGet->applyGas();
        safetyGet->releaseBrake();
    }
    else if(!isGasApplied && isBrakeApplied){
        safetyGet->releaseGas();
        safetyGet->applyBrake();
    }
    else if(!isBrakeApplied && !isBrakeApplied){
        safetyGet->releaseGas();
        safetyGet->releaseBrake();
    }
    else{
         safetyGet->releaseBrake();
         safetyGet->releaseGas();
    }
}
SpeedCalculator::SpeedCalculator(DriveModeManager* drivemodeGet_,SafetyManager* safetyGet_){
    //khởi tạo địa chỉ cho con trỏ tới DrivemodeManager để lấy chế độ lái và SafetyManager để láy phương thức điều chỉnh mức gas và phanh
    this->drivemodeGet = drivemodeGet_;
    this->safetyGet = safetyGet_;
    currentSpeed = 0;
    distance_travel = 0.0f;
    //cài đặt các ngưỡng tốc độ cho từng chế độ lái
    maxSpeedEco = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::MAX_SPEED_ECO);
    maxSpeedSport = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::MAX_SPEED_SPORT);
}
int SpeedCalculator::calculateSpeed(bool isAccelerating, bool isBraking){
    //các thông số để tính toán
    static const int MaxRpm =ElectricVehicle_Init::getDesignValue(vehicle_Attribute::MAX_RPM);
    static const int maxTorque = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::MAX_TORQUE);
    static const int wheelRadius = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::WHEEL_RADIUS);
    static const int vehicleWeight = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::WEIGHT);
    static const int totalWeight = vehicleWeight + LOAD;    // tổng trọng lượng của xe

    static float speed_ms = 0;                      // lưu trữ và cập nhật lại tốc độ m/s
    static float distance_ms = 0;                   // lưu trữ quãng đường cập nhật theo mét   
    static auto previousTime = steady_clock::now(); // Thời gian trước đó
    
    auto currentTime = steady_clock::now();
    duration<double> elapsedTime = currentTime - previousTime;
    double deltaT = elapsedTime.count();  //số giây theo thời gian thực giữa mỗi lần cập nhật
    
    //điều chỉnh cường độ gas và phanh 
    AdjustGasBrakeLevel(isAccelerating,isBraking);

    //truy cập SafetyManager để lấy mức gas và phanh
    int gasLevel = safetyGet->getGasLevel();
    int brakeLevel = safetyGet->getBrakeLevel();
 
    int rpm = VehicleCalculation::getRpm(speed_ms,wheelRadius,MaxRpm);   //tính số vòng quay của động cơ
    float Torque = VehicleCalculation::getTorque(rpm,MaxRpm,gasLevel,maxTorque);  //tính mo-men xoắn dựa trên rpm và cường độ gas
    float angularSpeed = VehicleCalculation::getAngularSpeed(rpm);      //tính tốc độ góc

    //tính toán tiêu hao do công suất động cơ  -> sử dụng cho batteryManager
    EngineConsumption = VehicleCalculation::getPowerEngine(Torque,angularSpeed);

    //tính lực kéo dựa trên bán kính bánh xe và mo-men xoắn
    float F_traction = VehicleCalculation::getTractionForce(wheelRadius,Torque);

    //tính gia tốc dựa trên tốc độ trước đó,lực kéo hiện tại,trọng lượng xe và cường độ phanh
    float a = VehicleCalculation::getAcceleration(speed_ms,F_traction,totalWeight,brakeLevel);

    //tính tốc độ xe 
    speed_ms = speed_ms + a*deltaT;
    currentSpeed = static_cast<int>(speed_ms * 3.6); //đổi ra km/h

    string mode = drivemodeGet->getCurrentDriveMode() == DriveModeManager::Mode::ECO ? "ECO" : "SPORT";
    //chỉ điều chỉnh tốc độ theo chế độ lái nếu đang nhấn phanh
    if(isAccelerating){
        adjustSpeedForDriveMode(mode); //được gọi liên tục để diều chỉnh phản hồi và ngưỡng tốc độ trong phạm vi cho phép của chế độ lái
    }
    //nếu nhấn phanh hoặc thả gas thì giới hạn tốc độ trong phạm vi cho phép
    else{
        if(currentSpeed >= getMaxSpeed(mode)) currentSpeed = getMaxSpeed(mode);
        if(speed_ms <= 0){
            currentSpeed = 0;
            speed_ms = 0;
        }
    }
    
    //tính toán quãng đường đi được
    distance_ms = distance_ms + speed_ms * deltaT + 0.5f * a * (deltaT*deltaT);
    distance_travel = distance_ms/1000.0f; //đổi ra km
    //test only
    /* cout << "current mode: " << mode  << 
            " - km/h: " << currentSpeed <<
            //" - distance travel: " << distance_travel << " Km" <<
            //" - a: " << a << " m/s^2" << 
            //" - F_traction: " << F_traction << " N.m" << 
            " - Torque: " << Torque << "N.m" <<
            //" - omega: " << angularSpeed << " rad/s" << 
            //" - Pengine: " << EngineConsumption << " Watt" << 
            " - rpm : " << rpm <<  
            " - gas: " << gasLevel << 
            " - brake: " << brakeLevel << endl; */
    previousTime = currentTime;     //cập nhật thời gian trước đó
    return currentSpeed;
}
int SpeedCalculator::getMaxSpeed(const std::string& driveMode) const{
    if(driveMode == "ECO") return maxSpeedEco;
    else return maxSpeedSport;
}
void SpeedCalculator::adjustSpeedForDriveMode(const std::string& driveMode){
    drivemode_factor f_factor;
    //trả về tốc độ tối đa cho mỗi chế độ nếu giá trị hiện tại lớn hơn tốc độ cài đặt cho từng chế độ lái
    if(driveMode == "ECO"){
        currentSpeed *= f_factor.f_ECO; //điều chỉnh tăng tốc chậm hơn
        if(currentSpeed > maxSpeedEco){
            currentSpeed = maxSpeedEco; //giới hạn tốc độ ECO tối đa
        }
    }
    else{
        currentSpeed *= f_factor.f_SPORT; //điều chỉnh tăng tốc nhanh hơn
        if(currentSpeed > maxSpeedSport){
            currentSpeed = maxSpeedSport;   //giới hạn tốc độ sport tối đa
        }
    }
    
}
