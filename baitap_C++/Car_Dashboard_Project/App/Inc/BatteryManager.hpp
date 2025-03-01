#ifndef BATTERYMANAGER_HPP
#define BATTERYMANAGER_HPP

#include "SpeedCalculator.hpp"
#include "VehicleConfig.hpp"

// Lớp BatteryManager quản lý mức pin và tính toán quãng đường di chuyển dựa trên các yếu tố vận hành
class BatteryManager {
public:
    // Constructor và Destructor
    BatteryManager(SpeedCalculator* speedAccess_);
    ~BatteryManager(){};

    // Phương thức tính toán mức tiêu hao pin tức thời -> KWh/s
    double calculateBatteryDrain(int acLevel, int windLevel) const; // Tính toán tiêu hao pin

    // Phương thức dự đoán quãng đường còn lại
    double calculateRemainingRange() const;    // Tính toán quãng đường dự đoán dựa trên mức pin hiện tại

    // Phương thức cập nhật mức pin 
    void updateBatteryLevel(int acLevel, int windLevel); // Cập nhật mức pin dựa trên các yếu tố vận hành

    // Getter cho mức pin % hiện tại
    double getBatteryLevel() const {return batteryLevel;}       // Lấy mức pin hiện tại

    // Getter cho mức năng lượng kWh hiện tại
    double getBatterykWh() const {return current_kWh;}

    //nhiệt độ pin
    float calculateBatteryTemp();
    
private:
    //con trỏ đến module tính toán tốc độ để lấy dữ liệu cho việc tính toán quãng đường di chuyển còn lại
    SpeedCalculator* speedAccess;
    double batteryLevel;                       // Mức pin hiện tại của xe tính theo %
    double batteryCapacity;                    // Dung lượng pin tối đa
    double drainPerKm;                         // Mức tiêu hao pin trên mỗi km (cơ bản)
    double current_kWh;                        // Mức pin hiện tại tính theo kWm 
    double battery_temp;                       // nhiệt độ pin
};

#endif // BATTERYMANAGER_HPP