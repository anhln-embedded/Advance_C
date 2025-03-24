#ifndef DISPLAYMANAGER_HPP
#define DISPLAYMANAGER_HPP

#include "DashboardController.hpp" //truy cập DashboardController để lấy dữ liệu
#include <stdint.h>
#include <stdbool.h>

/**
 * @brief Lớp quản lý việc hiển thị thông tin lên giao diện
 * @details Lớp này cung cấp API để hiển thị dữ liệu cập nhật từ module DashboardController sau 
 *          khi đọc từ file csv
 */
class DisplayManager : public Observer {
public:
    /**
    * @brief hàm tạo để đăng ký observer cho module DashboardController để lắng nghe mỗi 
    *       khi có dữ liệu mới được cập nhật
    */
    DisplayManager(DashboardController* dashboardController); //đăng ký làm observer cho dashboardController ngay khi khởi tạo
     /**
    * @brief hàm hủy đổi tượng DisplayManager
    */
    ~DisplayManager(){};

    /**
    * @brief    phương thức hiển thị dữ liệu lên terminal 
    * @details  nhận dữ liệu từ DashboardController và cập nhật giao diện
    */
    void updateDisplay();  

    /**
    * @brief            phương thức hiển thị tốc độ
    * @param[in] speed  tốc độ cập nhật từ dashboardController 
    */
    void showSpeed(const uint16_t& speed);                
    /**
    * @brief            phương thức hiển thị mức pin 
    * @param[in] batteryLevel  % mức pin cập nhật từ dashboardController 
    */
    void showBatteryStatus(const uint8_t& batteryLevel); // Hiển thị mức pin còn lại
    /**
    * @brief                  phương thức hiển thị nhiệt độ/trạng thái điều hòa, mức gió
    * @param[in] AC_status    trạng thái điều hòa cập nhật từ dashboardController 
    * @param[in] climateTemp  nhiệt độ điều hòa cập nhật từ dashboardController 
    * @param[in] windLevel    mức gió cập nhật từ dashboardController 
    */
    void showClimateStatus(const bool& AC_status,const uint8_t& climateTemp,const uint8_t& windlevel);  
    /**
    * @brief            phương thức hiển thị chế độ lái
    * @param[in] mode   chế độ lái cập nhật từ dashboardController 
    * - 'ECO' chế độ tiết kiệm nhiên liệu
    * - 'SPORT' chế độ thể thao
    */
    void showDriveMode(const string& mode);        

    /**
    * @brief                     phương thức hiển thị quãng đường còn lại 
    * @param[in] remainingRange  quãng đường còn lại cập nhật từ dashboardController 
    */
    void showRemainingRange(const uint16_t& remainingRange); 
    /**
    * @brief                     phương thức hiển thị tín hiệu rẽ
    * @param[in] remainingRange  tín hiệu rẽ cập nhật từ dashboardController 
    * - '0' xi nhan tắt
    * - '1' xi nhan trái
    * - '2' xi nhan phải
    */
    void showTurnSignal(const string& turnSignal);
    /**
    * @brief                     phương thức hiển thị trạng thái chân phanh
    * @param[in] remainingRange  trạng thái phanh cập nhật từ dashboardController 
    * - '0' chưa nhấn
    * - '1' đang nhấn
    */
    void showBrakePedal(const bool& IsBraking);
    /**
    * @brief                     phương thức hiển thị trạng thái chân gas
    * @param[in] remainingRange  trạng thái gas cập nhật từ dashboardController 
    * - '0' chưa nhấn
    * - '1' đang nhấn
    */
    void showGasPedal(const bool& IsAccelerating);
    /**
    * @brief    phương thức hiển thị trạng thái an toàn/nguy hiểm của xe
    * @details  hiển thị trạng thái an toàn/nguy hiểm dựa trên biến toàn cục IsSafeAction định nghĩa bởi module SafetyManager 
    */
    void showWarningAction();

    /**
    * @brief  phương thức từ Observer - được gọi khi có thay đổi dữ liệu
    */
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

extern int outputPower;             //biến toàn cục hiển thị công suất tối đa theo chế độ lái trên terminal dùng bởi displayManager
extern float update_odometer;       //biến toàn cục hiển thị quãng đường đi được ở dạng float trên terminal so với kiểu int trên server dùng bởi displayManager
extern float update_battery_temp;   //biến toàn cục hiển thị mức pin ở dạng float trên terminal so với kiểu int trên server dùng bởi displayManager
extern bool IsSafetyAction;         //biến toàn cục hiển thị thông báo khi có hành động nguy hiểm 
extern int gasLevel_display;
extern int brakeLevel_display;
#endif // DISPLAYMANAGER_HPP