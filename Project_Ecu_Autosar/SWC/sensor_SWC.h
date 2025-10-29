#ifndef SENSOR_SWC_H
#define SENSOR_SWC_H
#include "Rte.h"
#include "EcuState_SWC.h"


//hàm khởi tạo các cảm biến dòng , áp , nhiệt độ , encoder
void Runnable_InitSensors();

//hàm đọc dũ liệu cảm biến 
void Runnable_ReadSensors();

#endif
