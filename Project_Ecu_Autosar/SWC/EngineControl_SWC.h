//Đọc dữ liệu từ các cảm biến (dòng, áp, tốc độ RPM, nhiệt độ).
#ifndef ENGINE_CONTROL_SWC_H
#define ENGINE_CONTROL_SWC_H
#include "Rte.h"


//hàm tính toán mo-men,tốc độ theo tải động cơ
void Runnable_ProcessSensorData(); 

//hàm kiểm tra và giám sát thông số hoạt động của động cơ
bool Runnable_CheckError();
#endif
