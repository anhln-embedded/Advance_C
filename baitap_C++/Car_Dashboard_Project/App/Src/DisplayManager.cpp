#include "DisplayManager.hpp"
//#include "SpeedCalculator.hpp"      
//#include "SafetyManager.hpp"
#define ENVIRONMENT_TEMP        35
#define WARNING_BATTERY_LEVEL   20

int outputPower;
float update_odometer;
float update_battery_temp;
bool IsSafetyAction;
int gasLevel_display;
int brakeLevel_display;


bool UnsafeAction = false;
DisplayManager :: DisplayManager(DashboardController* dashboardController){
    this->dashboardController = dashboardController;
    dashboardController->registerObserver(this);
    cout << "Khởi tạo thành công hệ thống hiển thị dữ liệu" << endl;
}
void DisplayManager::update( 
    const uint16_t& speed,
    const uint16_t& remaining_range,
    const uint8_t& battery_level, 
    const uint8_t& climate_temp,
    const uint8_t& wind_level,
    const string& turnSignal,
    const string& drivemode, 
    const bool& IsBraking,
    const bool& IsAccelerating,
    const bool& AC_status)
{    
    //đảm bảo dữ liệu luôn được cập nhật lên giao diện kể cả dashboard chưa được khởi tạo
    if(dashboardController == NULL){
        showSpeed(speed);
        showBatteryStatus(battery_level);
        showClimateStatus(AC_status,climate_temp,wind_level);
        showDriveMode(drivemode);
        showRemainingRange(remaining_range);
        showTurnSignal(turnSignal);
        showBrakePedal(IsBraking);
        showGasPedal(IsAccelerating);
    }
    return;
}
void DisplayManager::updateDisplay(){
        showSpeed(dashboardController->getSpeed());
        showBatteryStatus(dashboardController->getBatteryLevel());
        showClimateStatus(dashboardController->getACstatus(),dashboardController->getClimatStatus(),dashboardController->getWindLevel());
        showDriveMode(dashboardController->getDriveMode());
        showRemainingRange(dashboardController->getRemainingRange());
        showTurnSignal(dashboardController->getTurnSignal());
        showBrakePedal(dashboardController->getBrakeStatus());
        showGasPedal(dashboardController->getGasStatus());
}
void DisplayManager::showSpeed(const uint16_t& speed){
    if(IsSafetyAction){
        cout << "phát hiện nhấn gas và phanh cùng lúc -> ưu tiên giảm tốc độ" << endl;
    }
    cout << "tốc độ: " << speed << " km/h" 
         << " - công suất tối đa: " << outputPower <<" kW" << endl;
    
}
void DisplayManager::showBatteryStatus(const uint8_t& batteryLevel){
    cout << "mức pin: " << static_cast<int>(batteryLevel) << " %"
         << " - nhiệt độ pin: " << setprecision(3) << update_battery_temp << "\u00B0C - " << "nhiệt độ môi trường: " << ENVIRONMENT_TEMP << "\u00B0C"; 
    if(static_cast<int>(batteryLevel) < WARNING_BATTERY_LEVEL){
        cout << " - Pin sắp hết";
    }
    cout << endl;
}
void DisplayManager::showClimateStatus(const bool& AC_status,const uint8_t& climateTemp,const uint8_t& windlevel){
    auto ac_status = [AC_status]() -> string {return AC_status ? "điều hòa đang bật" : "điều hòa đang tắt";};
    cout << ac_status() << " - nhiệt độ: " <<  static_cast<int>(climateTemp) << "\u00B0C - mức gió: " <<  static_cast<int>(windlevel) << endl;
}
void DisplayManager::showDriveMode(const string& drivemode){
    auto drivemode_status = [drivemode]()-> string {return drivemode == "ECO" ? "đang kích hoạt chế độ lái ECO" : "đang kích hoạt chế độ lái SPORT";};
    cout << drivemode_status() << endl;
}
void DisplayManager::showRemainingRange(const uint16_t& remainingRange){
    cout << "Quãng đường còn lại: " << remainingRange << " Km" 
         <<  " - Quảng đường đã đi: " << setprecision(3) << update_odometer << " Km" << endl; 
}
void DisplayManager::showTurnSignal(const string& turnSignal){
    auto turn_status = [turnSignal]() -> string{
        if(turnSignal == "0")      return "xi nhan đang tắt";
        else if(turnSignal == "1") return "đã bật xi nhan trái";
        else                       return "đã bật xi nhan phải";
    };
    cout << turn_status() << endl;

}
void DisplayManager::showBrakePedal(const bool& IsBraking){
    if(IsBraking) cout << "đang đạp phanh ";
    else          cout << "đang nhả phanh ";
    cout << " - cường độ phanh: " << brakeLevel_display << " %" <<endl;
}
void DisplayManager::showGasPedal(const bool& IsAccelerating){
    if(IsAccelerating) cout << "đang đạp Gas ";
    else               cout << "đang nhả Gas ";
    cout << " - cường độ gas: " << gasLevel_display << " %" <<endl;
    cout << ".................................................." << endl;
}