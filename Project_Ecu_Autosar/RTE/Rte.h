#ifndef RTE_H
#define RTE_H
#include "Std_Types.h"
#include "IoHwAb_MotorDriver.h"

//Gỉả lập các giá trị giới hạn
#define MAX_CURRENT 100
#define MAX_VOLTAGE 200
#define MAX_TEMP    100
#define MAX_RPM     300
#define MIN_RPM     50

typedef enum{
    MOTOR_RUN,
    MOTOR_OFF
}Motor_status;

typedef struct{
    int16_t       PWM_DutyCycle;
    Motor_status  status;
}ControlCmd;

typedef struct{
    float current;
    float voltage;
    int RPM;
    float temperature;
}SensorData;


// API để ghi dữ liệu từ Sensor_SWC -> EngineControl_SWC  (Sender-Receiver Interface)
Std_ReturnType Rte_Write_Sensor_SWC_SensorData(SensorData* data);

//API để EngineControl_SWC đọc đữ liệu gữi từ Sensor_SWC 
Std_ReturnType Rte_Read_EngineControl_SWC_SensorData(SensorData* data);

// API để ghi giá trị PWM từ EngineControl_SWC → Actuator_SWC (Sender-Receiver Interface)
Std_ReturnType Rte_Write_EngineControl_SWC_ControlCmd(ControlCmd* cmd);

// API kiểm tra lỗi nghiêm trọng gọi bởi EngineControl_SWC (Client)
Std_ReturnType Rte_Call_Diagnostic_SWC_CheckCriticalError(bool* error_status);

// API khởi tạo cảm biến dòng điện
Std_ReturnType Rte_Call_CurrentSensor_SWC_Init(void);

// API khởi tạo cảm biến điện áp
Std_ReturnType Rte_Call_VoltageSensor_SWC_Init(void);

// API khởi tạo cảm biến nhiệt độ
Std_ReturnType Rte_Call_TemperatureSensor_SWC_Init(void);

// API khởi tạo Driver PWM điểu khiển tốc độ
Std_ReturnType Rte_Call_MotorDriver_SWC_Init(void);

// API để đọc dữ liệu từ cảm biến tốc độ (Encoder)
Std_ReturnType Rte_Read_EncoderSensor_ActualSpeed(float *ActualRpm);

// API để đọc dữ liệu dòng điện từ cảm biến dòng điện
Std_ReturnType Rte_Read_CurrentSensor_current(float *current);

// API để đọc dữ liệu dòng điện từ cảm biến điện áp
Std_ReturnType Rte_Read_VolatageSensor_voltage(float *voltage);

// API để đọc dữ liệu dòng điện từ cảm biến điện áp
Std_ReturnType Rte_Read_TemperatureSensor_Temperature(float *temperature);


#endif