#ifndef DISPLAYMANAGER_HPP
#define DISPLAYMANAGER_HPP

#include "DashboardController.hpp" // Để lấy dữ liệu từ DashboardController
#include "SpeedCalculator.hpp"
#include "SafetyManager.hpp"
// Lớp DisplayManager chịu trách nhiệm hiển thị thông tin lên giao diện
class DisplayManager : public Observer {
public:
    // Constructor và Destructor;
    DisplayManager(DashboardController* dashboardController); //đăng ký làm observer cho dashboardController ngay khi khởi tạo
    ~DisplayManager(){};

    // Phương thức cập nhật giao diện tổng quát
    void updateDisplay();  // Nhận dữ liệu từ DashboardController và cập nhật giao diện

    // Phương thức hiển thị cụ thể cho từng thông số
    void showSpeed(const uint16_t& speed);                // Hiển thị tốc độ
    void showBatteryStatus(const uint8_t& batteryLevel); // Hiển thị mức pin còn lại
    void showClimateStatus(const bool& AC_status,const uint8_t& climateTemp,const uint8_t& windlevel);  // Hiển thị nhiệt độ điều hòa
    void showDriveMode(const string& mode);          // Hiển thị chế độ lái
    void showRemainingRange(const uint16_t& remainingRange); // Hiển thị quãng đường đi chuyển còn lại
    void showTurnSignal(const string& turnSignal);
    void showBrakePedal(const bool& IsBraking);
    void showGasPedal(const bool& IsAccelerating);
    void showWarningAction();

    // Phương thức từ Observer - được gọi khi có thay đổi dữ liệu
    void update(
        const uint16_t& speed,
        const uint16_t& remaining_range,
        const uint8_t& battery_level, 
        const uint8_t& climate_temp,
        const uint8_t& wind_level,
        const string& turnSignal,
        const string& drivemode, 
        const bool& IsBraking,
        const bool& IsAccelerating,
        const bool& AC_status
    )  override;

private:
    // Con trỏ tới DashboardController để lấy dữ liệu
    DashboardController* dashboardController;
};

extern int outputPower;  //biến toàn cục hiển thị công suất tối đa theo chế độ lái trên terminal dùng bởi displayManager
extern float update_odometer;  //biến toàn cục hiển thị quãng đường đi được ở dạng float trên terminal so với kiểu int trên server dùng bởi displayManager
extern float update_battery_temp; //biến toàn cục hiển thị mức pin ở dạng float trên terminal so với kiểu int trên server dùng bởi displayManager
extern bool IsSafetyAction; ////biến toàn cục hiển thị thông báo khi có hành động nguy hiểm 
extern int gasLevel_display;
extern int brakeLevel_display;
#endif // DISPLAYMANAGER_HPP