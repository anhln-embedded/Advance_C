#ifndef SPEEDCALCULATOR_HPP
#define SPEEDCALCULATOR_HPP
#include "SafetyManager.hpp"     //được gọi để truy cập Api quản lý các chức năng an toàn hỗ trợ cho việc điều chỉnh mức gas và phanh 
#include "DriveModeManager.hpp"  //được gọi để truy cập Api lấy chế độ lái hỗ trợ cho việc điều chỉnh tóc độ hiện tại
#include "VehicleConfig.hpp"
using namespace std::chrono;

/**
 * @brief Lớp quản lý việc tính toán tốc độ
 * @details Lớp này cung cấp API để tính toán và điều chỉnh tốc độ dựa trên chế độ lái,mức gas, phanh
 */

class SpeedCalculator {
private:
    //con trỏ đến module quản lý chế độ lái và quản lý an toàn để lấy dữ liệu
    DriveModeManager* drivemodeGet;
    SafetyManager* safetyGet;
    float distance_travel;       // quãng đường đi được (kmkm)
    double EngineConsumption;    // công suất tiêu thụ tức thời của động cơ (Watt)
    int currentSpeed;            // Vận tốc hiện tại của xe (km/hh)
    int maxSpeedSport;           // Giới hạn vận tốc tối đa cho chế độ SPORT
    int maxSpeedEco;             // Giới hạn vận tốc tối đa cho chế độ ECO

     /**
     * @brief   phương thức điều chỉnh mức gas và phanh 
     * @details tự động hiệu chỉnh mức gas và phanh dựa trên trạng thái gas và phanh
     * @param[in] isGasApplied     trạng thái bàn chân gas
     * @param[in] isBrakeApplied   trạng thái chân phanh
     * - 'true' đang nhấn 
     * - 'false' đang nhả
     * @note được gọi trong phương thức calculateSpeed trước khi thực hiện tính toán tốc độ
     */
    void AdjustGasBrakeLevel(bool isGasApplied, bool isBrakeApplied);
    /**
     * @brief   phương thức điều chỉnh tốc độ dựa trên chế độ lái
     * @param[in] driveMode chế độ lái
     *              + "ECO":    chế độ lái tiết kiệm nhiên liệu
     *              + "SPORT":  chế độ lái thế thao
     * @note được gọi trong phương thức calculateSpeed trước khi thực hiện tính toán tốc độ
     */
    void adjustSpeedForDriveMode(const std::string& driveMode); 
public:
    /**
     * @brief   phương thức tạo để khởi tạo các thông số mặc định của module SpeedCalculator
     * @details Khởi tạo tốc độ ban đầu,quãng đường đã đi,các giá trị ngưỡng tốc độ cho từng chế độ lái,
     *          và khởi tạo con trỏ đến các module SafetyManager và DriveModeManager
     * @param[in] drivemodeGet_  con trỏ tới DriveModeManager để lấy dữ liệu
     * @param[in] safetyGet_     con trỏ tới SafetyManager để lấy dữ liệu
     */
    SpeedCalculator(DriveModeManager* drivemodeGet_,SafetyManager* safetyGet_); 
    /**
     * @brief phương thức hủy đối tượng SpeedCalculator
     */

    ~SpeedCalculator(){};
    /**
     * @brief   phương thức tính toán tóc độ dựa trên trạng thái chân phanh và gas
     * @param[in] isAccelerating  trạng thái chân gas
     * @param[in] isAccelerating  trạng thai chân phanh 
     *              + true: đang nhấn
     *              + false: không nhấn
     * @return int: tốc độ tính bằng km/h
     */
    int calculateSpeed(bool isAccelerating, bool isBraking); 
    
    /**
     * @brief  Getter cho quãng đường đi được (km)
     * @note   được truy cập bởi module BatteryManager thông qua 
     *         phương thức updateBatteryLevel
     */
    float getTotalDistanceTraveling() const {return distance_travel;}

    /**
     * @brief  Getter cho công suất tiêu thụ do đông cơ (watt)
     * @note   được truy cập bởi module BatteryManager thông qua 
     *         phương thức calculateBatteryDrain
     */
    double getPowerEngineConsumption() const {return EngineConsumption;}
    
    /**
     * @brief  Getter cho tôc độ tối đa (km/h) dựa trên chế độ lái hiện tại
     */
    int getMaxSpeed(const std::string& driveMode) const;    

    /**
     * @brief  Getter cho tốc độ hiện tại (km/h)
     */
    int getCurrentSpeed() const {return currentSpeed;} 
};

#endif // SPEEDCALCULATOR_HPP

