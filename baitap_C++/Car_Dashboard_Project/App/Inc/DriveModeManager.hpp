#ifndef DRIVEMODEMANAGER_HPP
#define DRIVEMODEMANAGER_HPP
#include "VehicleConfig.hpp"

// Lớp DriveModeManager quản lý chế độ lái của xe, gồm các chế độ như SPORT và ECO
struct drivemode_factor{
    float f_ECO = 0.85;
    float f_SPORT = 1.2;
};
class DriveModeManager {
public:
    // Enum để xác định các chế độ lái
    enum class Mode { SPORT, ECO };
    // Constructor và Destructor
    DriveModeManager();
    ~DriveModeManager(){};

    // Phương thức thiết lập chế độ lái
    void setDriveMode(Mode driveMode);    // Đặt chế độ lái hiện tại (SPORT hoặc ECO)

    // Phương thức lấy công suất đầu ra dựa trên chế độ lái
    int getPowerOutput() const;           // Trả về công suất phù hợp với chế độ lái hiện tại

    // Phương thức giới hạn tốc độ khi ở chế độ ECO
    int limitSpeedForEcoMode(int currentSpeed); // Giới hạn tốc độ nếu chế độ ECO đang kích hoạt

    //phương thức giới hạn lại mức gas nếu quá lớn ở chế độ SPORT
    void limitGasForSportMode();  // -> tránh tốc độ tăng quá nhanh khi vừa kích hoạt SPORT
    // Getter cho chế độ lái hiện tại
    Mode getCurrentDriveMode() const{return currentDriveMode;}     // Trả về chế độ lái hiện tại

private:
    Mode currentDriveMode;                // Chế độ lái hiện tại của xe
    int powerOutputSport;                 // Công suất đầu ra cho chế độ SPORT
    int powerOutputEco;                   // Công suất đầu ra cho chế độ ECO
    int maxEcoSpeed;                      // Giới hạn tốc độ tối đa khi ở chế độ ECO
};

#endif // DRIVEMODEMANAGER_HPP