#ifndef TORQUE_CONTROL_H
#define TORQUE_CONTROL_H
#include "DriveMode_Control.h"
#include "PID.h"
 // Hàm khởi tạo hệ thống điều khiển mô-men xoắn
void TorqueControl_Init(void);  
// Hàm cập nhật hệ thống điều khiển mô-men xoắn
void TorqueControl_Update(void);
#endif // TORQUE_CONTROL_H
