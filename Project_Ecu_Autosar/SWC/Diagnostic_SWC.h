//Đọc dữ liệu từ các cảm biến (dòng, áp, tốc độ RPM, nhiệt độ).
#ifndef DIAGNOSTIC_SWC_H
#define DIAGNOSTIC_SWC_H
#include "Rte.h"
#include "EcuState_SWC.h"
#include "Pdu_Router.h"
#include "Dcm.h"
#include "Dem.h"

typedef struct{
    bool overCurrent;
    bool overVoltage;
    bool overTemperature;
    bool speedError;
 }ErrorFlags; 
 
void Runnable_InitDiagnostic();
void Runnable_InitCan();
//hàm phát hiện lỗi quá nhiệt,dòng,áp,PWM
Std_ReturnType Runnable_CheckCriticalErrors(bool* errorDetected);

//Hàm lưu trữ mã lỗi và gửi trạng thái lỗi qua CAN
void Runnable_ReportErrors();

//biến toàn cục để cập nhật mã lỗi 
extern ErrorFlags flags;

#endif
