#include "BatteryManager.hpp"
#include "VehicleConfig.hpp"

float environment_temp = 35.0f;  //giả sử nhiệt độ môi trường -> ảnh hưởng đến nhiệt độ ban đầu của pin khi xe khởi động

BatteryManager::BatteryManager(SpeedCalculator* speedAccess_){
    //khởi tạo địa chỉ cho con trỏ tới các module cần thiết để lấy dữ liệu khi chạy chương trình
    this->speedAccess = speedAccess_;
    drainPerKm = 0.0f;
    battery_temp = environment_temp;    //giả sử nhiệt độ pin cân bằng với môi trường khi xe khởi động
    batteryCapacity =  (double)ElectricVehicle_Init::getDesignValue(vehicle_Attribute::BATTERY_CAPACITY);;
    current_kWh = batteryCapacity;//lưu trữ năng lượng pin và cập nhật dựa trên giá trị trước đó
    cout << "Khởi tạo thành công hệ thống quản lý pin" << endl;
}
float BatteryManager::calculateBatteryTemp(){
    double P_engine = speedAccess->getPowerEngineConsumption();
    battery_temp = VehicleCalculation::getBatteryTemp(battery_temp,environment_temp,P_engine);
    return battery_temp;
}
double BatteryManager::calculateBatteryDrain(int acLevel, int windLevel) const
{
    //lấy thông số về công suất tối đa của điều hòa
    static const int maxAcPower = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::MAX_AC_POWER);

    //tính toán tiêu hao do công suất động cơ -> Wh
    double P_engine = speedAccess->getPowerEngineConsumption();

    //tính toán tiêu hao do điều hòa -> Wh
    int P_ac = VehicleCalculation::getPowerAC(environment_temp,acLevel,maxAcPower);

    //tính toán tiêu hao do mức gió -> Wh
    int P_wind = VehicleCalculation::getPowerWind(windLevel);

    //tổng tiêu hao -> đổi từ Wh sang kWh
    double Drain_kWh = (P_engine + P_ac + P_wind)/1000.0f;

    //test only
    /* cout << "drain: " << Drain_kWh << " kWh" 
         << " - P_engine:  " << P_engine << " Wh" 
         << " - P_ac:  " << P_ac << " Wh"
         << " - P_wind:  " << P_wind << " Wh" 
         << " - Wind level: " << windLevel 
         << " - Ac temp: " << acLevel; */
   
    return Drain_kWh / 3600.0f; //trả về kWh/s để tính mức pin hiện tại theo giây
}
double BatteryManager::calculateRemainingRange() const
{ 
    double current_battery = getBatterykWh();
    double remaining_range = current_battery / drainPerKm;
    /* cout << "quãng đường còn lại: " << remaining_range << " km" 
         << "  - tiêu hao trên km: " << drainPerKm << " kWh/km" << endl; */
    return remaining_range;
}
void BatteryManager::updateBatteryLevel(int acLevel, int windLevel){        
    static auto previousTime = steady_clock::now(); // Thời gian trước đó
    auto currentTime = steady_clock::now();
    duration<double> elapsedTime = currentTime - previousTime;
    double deltaT = elapsedTime.count();  //số giây theo thời gian thực giữa mỗi lần cập nhật
    
    //mức tiêu hao năng lượng trong 1s
    double Drain_kWh_per_second = calculateBatteryDrain(acLevel,windLevel);

    //mức tiêu hao theo thời gian thực tính bằng đơn vị giây 
    current_kWh -=  Drain_kWh_per_second*deltaT; 
    
    //% pin còn lại
    batteryLevel = (current_kWh / batteryCapacity) * 100.0f; 

    /* cout << " - mức pin %: " << batteryLevel 
            << " - dung lượng còn lại: " << current_kWh << endl; */

    //quãng đường tối đa đi được trên lý thuyết 
    static const int max_range = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::MAX_RANGE);
    
    //quãng đường đi được thực tế
    float current_distance_traveled = speedAccess->getTotalDistanceTraveling();

    //khi xe mới khởi động và chưa đi được quãng đường dài -> giả sử tiêu hao trên km là 0.14 kWh/km
    if(current_distance_traveled < 10){
        drainPerKm = 0.14f; 
    } 
    //khi xe đi được quãng đường đủ dài chuyển sang sử dụng công thức hiệu chỉnh thực tế
    else{
        static double alpha = 0.009f;   //hệ số dùng để hiệu chỉnh mức tiêu hao pin trung bình dựa trên quãng đường đi được so với quãng đường tối đa theo lý thuyết
        drainPerKm = (batteryCapacity - current_kWh)/(current_distance_traveled + alpha * (double)max_range);   
    }
    previousTime = currentTime;     //cập nhật thời gian trước đó
}