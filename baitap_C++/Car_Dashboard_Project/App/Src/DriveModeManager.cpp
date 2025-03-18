#include "DriveModeManager.hpp"
#include "VehicleConfig.hpp"
DriveModeManager::DriveModeManager(){
    //cập nhật chế độ lái ban đầu
    this->currentDriveMode = Mode::ECO;
    //lấy thông số công suất thực tế của xe
    const int maxPower = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::MAX_ENGINE_POWER);
    drivemode_factor f_mode;
    //khởi tạo các giới hạn công suất theo chế độ lái
    powerOutputEco = f_mode.f_ECO*maxPower;
    powerOutputSport = maxPower;
    cout << "Khởi tạo thành công hệ thống quản lý chế độ lái" << endl;
}
void DriveModeManager::setDriveMode(Mode Drivemode){
    if(Drivemode == Mode::ECO){
        this->currentDriveMode = Mode::ECO;            
        
    }
    else if(Drivemode == Mode::SPORT){
        this->currentDriveMode = Mode::SPORT;
    }
}

int DriveModeManager::getPowerOutput() const{
    //giới hạn công suất đầu ra theo chế độ lái
    if(currentDriveMode == Mode::ECO){
        return powerOutputEco;
    }
    else if(currentDriveMode == Mode::SPORT){
        return powerOutputSport;
    }
}
int DriveModeManager::limitSpeedForEcoMode(int currentSpeed){
    currentSpeed*= 0.99; //giảm dần tốc độ
    return currentSpeed;
}
