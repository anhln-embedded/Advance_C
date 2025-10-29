#include "Rte.h"


Std_ReturnType Rte_Write_Sensor_SWC_SensorData(SensorData* data){
    return E_OK;
}
Std_ReturnType Rte_Read_EngineControl_SWC_SensorData(SensorData* data){
    return E_OK;
}

Std_ReturnType Rte_Write_EngineControl_SWC_ControlCmd(ControlCmd* cmd){
    return E_OK;
}

// API kiểm tra lỗi nghiêm trọng gọi bởi EngineControl_SWC (Client)
Std_ReturnType Rte_Call_Diagnostic_SWC_CheckCriticalError(bool* error_status){
    return E_OK;
}

// API khởi tạo cảm biến dòng điện
Std_ReturnType Rte_Call_CurrentSensor_SWC_Init(void){
    return E_OK;
}

// API khởi tạo cảm biến điện áp
Std_ReturnType Rte_Call_VoltageSensor_SWC_Init(void){
    return E_OK;
}

// API khởi tạo cảm biến nhiệt độ
Std_ReturnType Rte_Call_TemperatureSensor_SWC_Init(void){
    return E_OK;
}


// API khởi tạo Driver PWM điểu khiển tốc độ
Std_ReturnType Rte_Call_MotorDriver_SWC_Init(void){
    return E_OK;
}

// API để đọc dữ liệu từ cảm biến tốc độ (Encoder)
Std_ReturnType Rte_Read_EncoderSensor_ActualSpeed(float *ActualRpm){
    return E_OK;
}

// API để đọc dữ liệu dòng điện từ cảm biến dòng điện
Std_ReturnType Rte_Read_CurrentSensor_current(float *current){
    return E_OK;
}

// API để đọc dữ liệu dòng điện từ cảm biến điện áp
Std_ReturnType Rte_Read_VolatageSensor_voltage(float *voltage){
    return E_OK;
}

// API để đọc dữ liệu dòng điện từ cảm biến điện áp
Std_ReturnType Rte_Read_TemperatureSensor_Temperature(float *temperature){
    return E_OK;
}

