#ifndef __ECU_H
#define __ECU_H
#include <iostream>
#include <vector>
#include <string>
#include <stdbool.h>
#include "record.hpp"
#define PATH ".//database//ECU_data.csv"
using namespace std;
class EngineControlUnit
{
private:
    vector<int> speed_history;
    vector<float> temp_history;
    int update_speed;
    float update_temp;
    static EngineControlUnit *Instance; // luu trữ instance duy nhất
    // private constructor ngăn chặn việc khởi tạo bên ngoài
    EngineControlUnit()
    {
        cout << "Initialized successfully" << endl;
    }
    ~EngineControlUnit()
    {
        cout << "call destructor" << endl;
    }
    //cài đặt và đọc dữ liệu tốc độ,nhiệt độ 
    int getEngineSpeed();
    float getEngineTemperature();
    void setEngineSpeed(int speed);
    void setEngineTemperature(float temp);
    
    //cảnh báo quá nhiệt
    bool isOverheadting();
    
    //tương tác với hệ thống điểu chỉnh mức nhiên liệu và phanh
    void setFuelInjectionRate();
    void brakeControlInteraction();

public:
    static EngineControlUnit *ECUInit()
    {
        if (Instance == NULL)
        {
            Instance = new EngineControlUnit;
        }
        // Emptyfile(PATH);
        return Instance;
    }
    void display_ECU();
    void readsensor_ECU();
    void DataRecord_ECU();
    void diagnostics_ECU();
};
#endif
