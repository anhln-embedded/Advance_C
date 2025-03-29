#ifndef SAFETYMANAGER_HPP
#define SAFETYMANAGER_HPP

using namespace std;

/**
 * @brief Lớp quản lý các chức năng an toàn
 * @details Lớp này cung cấp API để kiểm soát và điều chỉnh mức gas,phanh,
 *          cũng như cho phép kích hoạt/vô hiệu hóa phanh thông qua việc liên tục 
 *          kiểm các điều kiện an toàn
 */

class SafetyManager {
public:
    /**
    * @brief Hàm tạo để cài đặt giá trị mức gas và phanh ban đầu
    */
    SafetyManager();

     /**
    * @brief hàm hủy đối tượng SafetyManager
    */
    ~SafetyManager(){};
     /**
     * @brief   phương thức kiểm tra xem có đang đạp ga và phanh cùng lúc không
     * @details dựa trên trạng thái phanh và gas để xác định liệu người lái có đang 
     *          thực hiện hành vi nguy hiểm như đạp gas và phanh cùng lúc
     * @param[in] isAccelerating trạng thái chân gas
     * @param[in] isBraking      trạng thái chân phanh
     * - 'true' đang nhấn 
     * - 'false' đang nhả
     * @return bool: trạng thái xe hiện tại
     * @retval 'true'  Xe đang ở trạng thái nguy hiểm (vừa đạp ga vừa phanh).
     * @retval 'false' Xe đang ở trạng thái an toàn.
     */
    bool checkBrakeAndAccelerator(bool isAccelerating, bool isBraking); 

    /**
     * @brief   phương thức kích hoạt phanh
     * @details giá trị cường độ phanh sẽ tăng dần khi phương thức được gọi để giảm tốc
     * @note được gọi bởi module SpeedCalculator  thông qua Api adjustSpeedForDriveMode
     */
    void applyBrake();       

    /**
     * @brief   phương thức kích hoạt chân gas
     * @details giá trị cường độ gas sẽ tăng dần khi phương thức được gọi để tăng tốc
     * @note được gọi bởi module SpeedCalculator thông qua Api adjustSpeedForDriveMode
     */

    void applyGas();

    /**
     * @brief   phương thức giải phóng chân phanh
     * @details giá trị cường độ phanh sẽ giảm dần khi người lái nhả chân phanh
     * @note được gọi bởi module SpeedCalculator thông qua Api adjustSpeedForDriveMode
     */
    void releaseBrake();                    

    /**
     * @brief   phương thức giải phóng bàn đạp gas
     * @details giá trị cường độ gas sẽ giảm dần khi người lái nhả chân gas
     * @note được gọi bởi module SpeedCalculator thông qua Api adjustSpeedForDriveMode
     */
    void releaseGas();               

    // Kiểm tra trạng thái của phanh
    //bool isBrakeApplied() const {return brakeApplied;}  // Trả về trạng thái phanh có đang được nhấn hay không

    /**
     * @brief getter cho giá trị mức gas
     * @note được gọi bởi module SpeedCalculator thông qua Api adjustSpeedForDriveMode
     */
    int getGasLevel() const {return gasIntensity;}
     
    /**
     * @brief getter cho giá trị mức phanh
     * @note được gọi bởi module SpeedCalculator thông qua Api adjustSpeedForDriveMode
     */
    int getBrakeLevel() const {return brakeIntensity;}
private:
    //bool brakeApplied;                     // Biến lưu trạng thái phanh (đang được nhấn hay không)
    int gasIntensity;                        // Cường độ tăng tốc khi nhấn gas (đơn vị tăng tốc mỗi lần)
    int brakeIntensity;                      // Cường độ giảm tốc khi phanh (đơn vị giảm tốc mỗi lần)
    //int currentSpeed;                      // Tốc độ hiện tại của xe (được cập nhật khi phanh)
};

//biến toàn cục lưu trữ trạng thái an toàn/nguy hiểm của xe truy cập bới module DisplayManager 
extern bool IsSafeAction;                   
#endif // SAFETYMANAGER_HPP

