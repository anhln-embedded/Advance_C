#ifndef DRIVEMODEMANAGER_HPP
#define DRIVEMODEMANAGER_HPP

/**
 * @brief kiểu cấu trúc để định nghĩa các hệ số điều chỉnh tương ứng với chế độ lái
 */

struct drivemode_factor{
    float f_ECO = 0.85;
    float f_SPORT = 1.2;
};
/**
 * @brief Lớp quản lý các chế độ lái của xe
 * @details Lớp này cung cấp API điều chỉnh giới hạn tốc độ, công suất theo chế độ lái
 */

class DriveModeManager {
public:
    // Enum để xác định các chế độ lái
    enum class Mode { SPORT, ECO };
    /**
    * @brief hàm tạo để cài đặt chế độ lái,công suất mặc định ban đầu
    */
    DriveModeManager();
    /**
    * @brief phương thức hủy đối tượng DriveModeManager
    */
    ~DriveModeManager(){};

    /**
    * @brief phương thức thiết lập chế độ lái
    * @param[in] driveMode
    * - 'SPORT' chế độ lái thể thao
    * - 'ECO'   chế độ lái tiết kiệm nhiên liệu
    */
    void setDriveMode(Mode driveMode);   
    
    /**
    * @brief phương thức lấy công suất đầu ra dựa trên chế độ lái
    * @details  Trả về công suất phù hợp với chế độ lái hiện tại 
    */
    int getPowerOutput() const;           

    /**
    * @brief phương thức giới hạn tốc độ khi ở chế độ ECO
    * @details  Trả về tốc độ được giới hạn nếu chế độ ECO đang kích hoạt
    */
    int limitSpeedForEcoMode(int currentSpeed); 

    /**
    * @brief Getter cho chế độ lái hiện tại
    * @details  Trả về tốc độ được giới hạn nếu chế độ ECO đang kích hoạt
    * @return Mode chế độ lái
    * @retval ECO   chế độ tiết kiệm nhiên liệu
    * @retval SPORT chế độ thể thao
    */
    Mode getCurrentDriveMode() const{return currentDriveMode;}     // Trả về chế độ lái hiện tại

private:
    Mode currentDriveMode;                // Chế độ lái hiện tại của xe
    int powerOutputSport;                 // Công suất đầu ra cho chế độ SPORT
    int powerOutputEco;                   // Công suất đầu ra cho chế độ ECO
    int maxEcoSpeed;                      // Giới hạn tốc độ tối đa khi ở chế độ ECO
};

#endif // DRIVEMODEMANAGER_HPP