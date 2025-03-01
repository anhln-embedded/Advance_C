#ifndef SAFETYMANAGER_HPP
#define SAFETYMANAGER_HPP

#include <iostream>
using namespace std;

// Lớp SafetyManager quản lý các yếu tố an toàn khi điều khiển xe
class SafetyManager {
public:
    // Constructor và Destructor
    SafetyManager();
    ~SafetyManager(){};

    // Phương thức kiểm tra xem có đang đạp ga và phanh cùng lúc không
    bool checkBrakeAndAccelerator(bool isAccelerating, bool isBraking); // Kiểm tra hành vi nguy hiểm

    // Phương thức kích hoạt phanh
    void applyBrake();                       // Giảm tốc độ dần dần khi phanh được nhấn

    //phương thức kích hoạt bàn đạp gas
    void applyGas();

    // Phương thức giải phóng phanh
    void releaseBrake();                     // Giải phóng phanh khi nhả ra

    // Phương thức giải phóng bàn đạp gas
    void releaseGas();                     // Giải phóng gas khi nhả ra

    // Kiểm tra trạng thái của phanh
    bool isBrakeApplied() const {return brakeApplied;}  // Trả về trạng thái phanh có đang được nhấn hay không

    //getter cập nhật mức gas và phanh
    int getGasLevel() const {return gasIntensity;}
    int getBrakeLevel() const {return brakeIntensity;}
private:
    bool brakeApplied;                       // Biến lưu trạng thái phanh (đang được nhấn hay không)
    int gasIntensity;
    int brakeIntensity;                      // Cường độ giảm tốc khi phanh (đơn vị giảm tốc mỗi lần)
    int currentSpeed;                        // Tốc độ hiện tại của xe (được cập nhật khi phanh)
};
//định nghĩa biến toàn cục thể hiện trạng thái thực hiện hành động an toàn/nguy hiểm
extern bool IsSafeAction;                   
#endif // SAFETYMANAGER_HPP

