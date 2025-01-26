#ifndef RTE_TORQUECONTROL_H
#define RTE_TORQUECONTROL_H

#include "Std_Types.h" // Bao gồm các kiểu dữ liệu tiêu chuẩn
#include <stddef.h>    // Định nghĩa NULL

#define VEHICLE_LOAD		600
#define MAX_SPEED			250
#define MIN_SPEED			0
#define DRIVER_MAX_TORQUE 	300
#define DRIVER_MIN_TORQUE 	0

/* INITIALIZED VALUE */
#define SENSOR_SPEED_VALUE 350
#define SENSOR_LOAD_VALUE 1000
#define SENSOR_TORQUE_VALUE 500




// API để đọc dữ liệu từ cảm biến bàn đạp ga
Std_ReturnType Rte_Read_RpThrottleSensor_ThrottlePosition(float *ThrottlePosition);

// API để đọc dữ liệu từ cảm biến tốc độ
Std_ReturnType Rte_Read_RpSpeedSensor_Speed(float *Speed);

// API để đọc dữ liệu từ cảm biến tải trọng
Std_ReturnType Rte_Read_RpLoadSensor_LoadWeight(float *LoadWeight);

// API để đọc mô-men xoắn thực tế từ cảm biến mô-men xoắn
Std_ReturnType Rte_Read_RpTorqueSensor_ActualTorque(float *ActualTorque);

// API để ghi dữ liệu mô-men xoắn yêu cầu tới bộ điều khiển động cơ
Std_ReturnType Rte_Write_PpMotorDriver_SetTorque(float TorqueValue);

// API khởi tạo cảm biến bàn đạp ga
Std_ReturnType Rte_Call_RpThrottleSensor_Init(void);

// API khởi tạo cảm biến tốc độ
Std_ReturnType Rte_Call_RpSpeedSensor_Init(void);

// API khởi tạo cảm biến tải trọng
Std_ReturnType Rte_Call_RpLoadSensor_Init(void);

// API khởi tạo cảm biến mô-men xoắn
Std_ReturnType Rte_Call_RpTorqueSensor_Init(void);

// API khởi tạo bộ điều khiển mô-men xoắn
Std_ReturnType Rte_Call_PpMotorDriver_Init(void);

typedef struct{
	//PID parameter
	double kp,ki,kd;
	float error_value,error_pre1,error_pre2;
	float output_pwm,last_output_pwm;
}motor_name;
#endif // RTE_TORQUECONTROL_H
