#include "..//inc//ecu.hpp"

#define MAX_RPM 6000                    //số vòng quay tối đa
#define MAX_TEMP 120                    //nhiệt độ tối đa
#define MAX_PEDAL_APPLY 100             //mức bàn đạp tối đa
#define WARNING_TEMP 100                //nhiệt độ cảnh báo
#define OPTIMAL_TEMP 90                 //nhiệt độ lý tưởng
#define BASE_FUEL    10                 //mức nhiên liệu cơ bản 

//khởi tạo giá trị ban đầu cho biến static
EngineControlUnit *EngineControlUnit ::Instance = NULL;


EngineControlUnit::EngineControlUnit()
{
    throttle_input = 0.0f;
    brake_input = 0.0f;
    isbrake = brake_status::relase;
    rpm = 0;
    temperature = OPTIMAL_TEMP;   
    cout << "ECU Đã được khởi tạo với các thông số mặc định" << endl;
}
/* PUBLIC INTERFACE */
void EngineControlUnit::GenerateRandomData(){
    int rpm = rand() % (MAX_RPM + 1);
    float temperature = 40 + rand() % 81; // mô phỏng nhiệt độ trong khoảng 40 - 120 độ C
    float throttle_position = rand() % (MAX_PEDAL_APPLY + 1);
    float brake_position = rand() % (MAX_PEDAL_APPLY + 1);
    brake_status isbrake = static_cast<brake_status>(rand() % static_cast<int>(limit_brake_status));

    setEngineSpeed(rpm);
    setEngineTemperature(temperature);
    setThrottlePosition(throttle_position);
    setBrakePosition(brake_position);
    setBrakestatus(isbrake);
}

void EngineControlUnit::ECU_Diagnostic()
{
    cout << "======Kết quả chuẩn đoán======" << endl;
    if (dataRead(PATH) == FAIL)
    {
        cout << "Đọc dữ liệu thất bại" << endl;
        return;
    }
}
void EngineControlUnit::ECU_SaveData()
{
    if ((dataRecord(PATH, rpm_history, temperature_history)) == FAIL)
    {
        cout << "Lưu trữ dữ liệu thất bại" << endl;
        return;
    }
}
void EngineControlUnit::ECU_Read()
{
    GenerateRandomData();
    cout << "Tốc độ: " << getEngineSpeed() << " rpm\tnhiệt độ: " << getEngineTemperature() << " °C"<<endl;
    if (isOverheadting())
        cout << "CẢNH BÁO ĐỘNG CƠ QUÁ NHIỆT" << endl;
}


void EngineControlUnit::setFuelInjectionRate()
{
    CalculateFuelRate();
    cout << "Mức nhiên liệu: " << getFuelRate() << " %" << endl; 
}
void EngineControlUnit::brakeControlInteraction()
{
    auto isbrake = getBrakestatus();
    LimitFuelbyBrake(isbrake);
    if(isbrake == brake_status::press) cout << "đang đạp phanh" << endl;
    else if(isbrake == brake_status::relase) cout << "phanh chưa được nhấn" << endl;
}

/* PRIVATE INTERFACE */

void EngineControlUnit::CalculateFuelRate() {
    //các hệ số hiệu chỉnh nhiên liệu theo tốc độ và nhiệt độ
    float k_rpm = 0.0f,k_temp = 0.0f;

    //hiệu chỉnh các hệ số
    AdjustFactor(k_rpm,k_temp);

    //tính toán mức nhiên liệu
    float fuel_Adjust = throttle_input + k_rpm * (rpm/MAX_RPM) + k_temp * (temperature / MAX_TEMP);

    //duy trì mức nhiên liệu ở mức tối thiểu khi tốc độ giảm về 0 
    if(fuel_rate < BASE_FUEL) fuel_rate = BASE_FUEL;   
    setFuelRate(fuel_Adjust);
}

void EngineControlUnit::LimitFuelbyBrake(const brake_status& isbrake){
    if(isbrake == brake_status::press){
        if(getEngineSpeed() < 1500){
            float fuel_reduction = 1.0f - (brake_input/MAX_PEDAL_APPLY);
            fuel_rate -= fuel_reduction;
        }
        else    
            cout << "phanh đã được kích hoạt để hãm bớt tốc độ" << endl;
    }
}
void EngineControlUnit::AdjustFactor(float& k_rpm,float& k_temp){
    //điều chỉnh hệ số nhiên liệu dựa trên tốc độ
    if(rpm >= 1500 && rpm <= 3000){
        k_rpm = 1.5f;  //tăng nhẹ đối với tốc độ vừa phải
    }
    else if(rpm <= 5000){
        k_rpm = 2.0f; //tăng mạnh đối với tốc độ cao
    }
    else if(rpm > 5000){
        k_rpm = 2.5f;
    }
    //điều chỉnh hệ số nhiên liệu dựa trên nhiệt độ
    if(temperature < OPTIMAL_TEMP){
        k_temp = 1.2f; //tăng mức nhiên liệu khi nhiệt độ dưới mức lý tưởng
    }
    else if(temperature > WARNING_TEMP){
        k_temp = 0.8f; //giảm mức nhiên liệu khi nhiệt độ quá cao
    }
}

void EngineControlUnit::setEngineSpeed(const int& speed)
{
    rpm = speed;
    rpm_history.push_back(speed);
    if (speed > MAX_RPM)
    {
        cout << "CẢNH BÁO TỐC ĐỘ PHẢI NHỎ HƠN 6000 RPM" << endl;
    }
}
void EngineControlUnit::setEngineTemperature(const float& temp)
{
    temperature = temp;
    temperature_history.push_back(temp);
    if (temp > 120 || temp < -20)
    {
        cout << "CẢNH BÁO, NHIỆT ĐỘ PHẢI NẰM TRONG KHOẢNG TỪ -20 - 120 °C" << endl;
    }
}
bool EngineControlUnit::isOverheadting()
{
    if (temperature > WARNING_TEMP)
        return true;
    return false;
}
