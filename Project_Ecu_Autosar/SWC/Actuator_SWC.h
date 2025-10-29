//Đọc dữ liệu từ các cảm biến (dòng, áp, tốc độ RPM, nhiệt độ).
#ifndef ACTUATOR_H
#define ACTUATOR_H
#include "Rte.h"
#include "EcuState_SWC.h"

//hàm khởi tạo driver điều khiển động cơ
void Runnable_InitActuator();

//Hàm băm xung PWM điều khiển tốc độ
void Runnable_PWMadjustActuator();

//hàm điều khiển động cơ 
void Runnable_ExecuteActuator();

#endif
