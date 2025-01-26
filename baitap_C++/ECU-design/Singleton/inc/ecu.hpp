#ifndef __ECU_H
#define __ECU_H
#include <iostream>
#include <vector>
#include <string>
#include <stdbool.h>
#include <ctime>
#include "record.hpp"
#define PATH ".//database//ECU_data.csv"
using namespace std;


typedef enum{
    relase,
    press,
    limit_brake_status
}brake_status;
class EngineControlUnit
{
private:
    vector<int> rpm_history;            //biến lưu trữ tốc độ
    vector<float> temperature_history;  //biến lưu trữ nhiệt độ
    int rpm;                    //tốc đỗ -> số vòng quay
    float temperature;          //nhiệt độ
    float fuel_rate;            //mức nhiên liệu cung cấp
    float throttle_input;       //phản hồi bàn đạp ga
    float brake_input;          //phản hồi bàn đạp phanh
    brake_status isbrake;       //trạnh thái phanh 
    static EngineControlUnit *Instance; // luu trữ instance duy nhất
    
    // private constructor ngăn chặn việc khởi tạo bên ngoài
    EngineControlUnit();  //được dùng để khởi tạo đối tượng duy nhất và các thông số mặc định ban đầu
    
    int getEngineSpeed()const {return rpm;}
    float getEngineTemperature()const {return temperature;}
    float getFuelRate() const {return fuel_rate;}                //đọc về mức nhiên liệu
    brake_status getBrakestatus() const {return isbrake;}        //đọc về trạng thái phanh

    //các hàm sau đây được gọi bởi GenerateRandomData để cài đặt các thuộc tính tương ứng
    void setBrakestatus(const brake_status& isbrake_){isbrake = isbrake_;}                   //cài đặt trạng thái phanh
    void setThrottlePosition(const float& position){throttle_input = position;} //cài đặt phản hồi bàn đạp phanh
    void setBrakePosition(const float& position){brake_input = position;}       //cài đặt phản hồi bản đạp phanh
    void setEngineSpeed(const int& speed);                                         //cài đặt tốc độ và lưu vào lịch sử
    void setEngineTemperature(const float& temp);                                  //cài đặt nhiệt độ và lưu vào lịch sử
    
    //2 hàm sau đây được gọi bởi calculateFuelRate
    void setFuelRate(const float& rate){fuel_rate = rate;}  //cài đặt mức nhiên liệu 
    void AdjustFactor(float& k_rpm,float& k_temp);          //điều chỉnh hệ số ảnh hưởng đến mức tăng giảm nhiên liệu
    
    //được gọi bởi setFuelInjectionRate
    void CalculateFuelRate();           //tính toán mức nhiên liệu hiệu chỉnh

    void LimitFuelbyBrake(const brake_status& isbrake);

    
    //2 hàm sau đây được gọi bởi ECU_Read
    bool isOverheadting();       //cảnh báo quá nhiệt
    void GenerateRandomData();   //hàm tạo ngẫu nhiên các giá trị mô phỏng việc đọc dữ liệu từ cảm biến
public:
    static EngineControlUnit *ECUInit()
    {
        if (Instance == NULL)
        {
            Instance = new EngineControlUnit;
        }
        return Instance;
    }
    //Hàm để ECU cài đặt các giá trị sau khi nhận dữ liệu từ hàm mô phỏng ngãu nhiên
    void ECU_Read();
    //hàm lưu trữ tốc độ và nhiệt độ vào file csv
    void ECU_SaveData();
    //hàm in ra chuẩn đoán các giá trị đã lưu trong file csv của các lần chạy
    void ECU_Diagnostic();
    //hàm cài đặt mức nhiên liệu dựa trên mức độ đạp gas và tỉ lệ hòa khí
    void setFuelInjectionRate();
    //hàm để tương tác với hệ thống phanh dựa vào mức độ đap phanh và điều chỉnh lại mức nhiên liệu thức tế cung cấp cho xe
    void brakeControlInteraction();
};
#endif
