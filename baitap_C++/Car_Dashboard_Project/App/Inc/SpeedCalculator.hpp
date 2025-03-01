#ifndef SPEEDCALCULATOR_HPP
#define SPEEDCALCULATOR_HPP
#include "SafetyManager.hpp"
#include "DriveModeManager.hpp"
#include "VehicleConfig.hpp"
using namespace std::chrono;

class DriveModeManager;

// Lớp SpeedCalculator chịu trách nhiệm tính toán và điều chỉnh vận tốc của xe

class SpeedCalculator {
private:
    //con trỏ đến module quản lý chế độ lái và quản lý an toàn để lấy dữ liệu
    DriveModeManager* drivemodeGet;
    SafetyManager* safetyGet;
    float distance_travel;       // quãng đường đi được
    double EngineConsumption;     // công suất tiêu thụ tức thời của động cơ Wat
    int currentSpeed;            // Vận tốc hiện tại của xe
    int maxSpeedSport;           // Giới hạn vận tốc tối đa cho chế độ SPORT
    int maxSpeedEco;             // Giới hạn vận tốc tối đa cho chế độ ECO
    void AdjustGasBrakeLevel(bool isGasApplied, bool isBrakeApplied);
public:
    // Constructor và Destructor
    SpeedCalculator(DriveModeManager* drivemodeGet_,SafetyManager* safetyGet_); 
    ~SpeedCalculator(){};
    // Phương thức tính toán vận tốc
    int calculateSpeed(bool isAccelerating, bool isBraking); // Tính toán vận tốc dựa trên ga và phanh
    // Phương thức điều chỉnh vận tốc theo chế độ lái hiện tại
    void adjustSpeedForDriveMode(const std::string& driveMode); // Điều chỉnh vận tốc khi thay đổi chế độ lái
    
    //Getter cho quãng đường đi được 
    float getTotalDistanceTraveling() const {return distance_travel;}

    //Getter cho công suất tiêu thụ -> sử dụng bởi batteryManager để tính tiêu hao năng lượng 
    double getPowerEngineConsumption() const {return EngineConsumption;}
    
    // Getter cho vận tốc tối đa tùy theo chế độ lái
    int getMaxSpeed(const std::string& driveMode) const;     // Lấy giới hạn vận tốc theo chế độ lái

    // Getter cho vận tốc hiện tại
    int getCurrentSpeed() const {return currentSpeed;} // Lấy giá trị vận tốc hiện tại
};

#endif // SPEEDCALCULATOR_HPP

