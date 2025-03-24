#ifndef BATTERYMANAGER_HPP
#define BATTERYMANAGER_HPP

#include "SpeedCalculator.hpp"

/**
 * @brief Lớp quản lý các chức năng tính toán mức pin, quãng đường còn lại
 * @details Lớp này cung cấp API để tính mức tiêu thụ pin, và dự đoán quãng đường đi được còn lại của xe
 */
class BatteryManager {
public:
    /**
     * @brief hàm khởi tạo các thông số mặc định
     * @details khởi tạo dung lượng ban đầu của pin,nhiệt độ pin ban đầu, và con trỏ tới module SpeedCalculator
     */
    BatteryManager(SpeedCalculator* speedAccess_);
    /**
    * @brief hàm hủy đối tượng BatteryManager
    */
    ~BatteryManager(){};

     /**
     * @brief phương thức dự đoán quãng đường còn lại dựa trên
     *          mức pin còn lại (kWh) và mức tiêu hao trên km
     * @return double : quãng đường còn lại tính bằng km
     */
    double calculateRemainingRange() const;  

    /**
     * @brief phương thức Cập nhật mức pin dựa trên các yếu tố vận hành
     * @param[in] acLevel   nhiệt độ điều hòa trong khoảng 18 - 28 độ c
     * @param[in] windLevel mức gió trong khoảng 0 - 5 
     */
    void updateBatteryLevel(int acLevel, int windLevel); 

    // Getter cho mức pin % hiện tại
    double getBatteryLevel() const {return batteryLevel;}       // Lấy mức pin hiện tại

    /**
     * @brief   phương thức Cập nhật nhiệt độ pin 
     * @details tính toán dựa trên con trỏ tới module SpeedCalculator để truy cập 
     *          Api getPowerEngineConsumption lấy ra công suất tiêu hao do động cơ
     *          két hợp với nhiệt độ môi trường để tính ra nhiệt độ pin hiện tại
     * @return float : nhiệt độ pin tính bằng độ C
     */
    float calculateBatteryTemp();
    
private:
    //con trỏ đến module tính toán tốc độ để lấy dữ liệu cho việc tính toán quãng đường di chuyển còn lại
    SpeedCalculator* speedAccess;
    double batteryLevel;                       // Mức pin hiện tại của xe tính theo %
    double batteryCapacity;                    // Dung lượng pin tối đa
    double drainPerKm;                         // Mức tiêu hao pin trên mỗi km (cơ bản)
    double current_kWh;                        // Mức pin hiện tại tính theo kWm 
    double battery_temp;                       // nhiệt độ pin

     /**
     * @brief   phương thức tính toán mức tiêu hao pin tức thời 
     * @details 
     * @param[in] acLevel   nhiệt độ điều hòa trong khoảng 18 - 28 độ c
     * @param[in] windLevel mức gió trong khoảng 0 - 5 
     * @return double : mức tiêu hao tức thời tính bằng kWH/s
     */
    double calculateBatteryDrain(int acLevel, int windLevel) const; // Tính toán tiêu hao pin
    
    /**
     * @brief getter cho mức pin hiện tại kWh
     */
    double getBatterykWh() const {return current_kWh;}

};

#endif // BATTERYMANAGER_HPP