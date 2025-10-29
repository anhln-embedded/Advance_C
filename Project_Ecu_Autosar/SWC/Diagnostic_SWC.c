#include "Diagnostic_SWC.h"

//Khởi tạo mặc định các trạng thái lỗi ban đầu
ErrorFlags flags = {.overCurrent = false,
                    .overVoltage = false,
                    .overTemperature = false,
                    .speedError = false};


void Runnable_InitDiagnostic(){
    //Khởi tạo hệ thống quản lý sự kiện chuẩn đoán
    Dem_Init();
    //Khởi tạo hệ thống xử lý chuẩn đoán
    Dcm_Init();

    flagECU.DiagnoseInitFlag = SUCCESS;
}
void Runnable_InitCan(){
    PduR_Init();
    flagECU.CanInitFlag = SUCCESS;
}
static ErrorFlags CheckErrors(){
    float current = 0.0f,volatage = 0.0f,temperature = 0.0f,rpm = 0.0f;
    ErrorFlags flags;
    if(Rte_Read_CurrentSensor_current(&current) == E_OK){
        if(current > MAX_CURRENT){
            flags.overCurrent = SUCCESS;
            printf("dòng điện vượt mức cho phép\n");
        }
    }
    /* 
        logic kiểm tra Rpm, nhiệt độ, áp 
    */

}
Std_ReturnType Runnable_CheckCriticalErrors(bool *errorDetected) {
    ErrorFlags flags = CheckErrors();
    if(flags.overCurrent || flags.overVoltage || flags.overTemperature || flags.speedError) {
        *errorDetected = TRUE;
    } else {
        *errorDetected = FALSE;
    }
    return E_OK;
}
void Runnable_ReportErrors(){
    //lưu trữ mã lỗi vào DEM

    //gửi thông tin lỗi lên BUS can qua DCM
}