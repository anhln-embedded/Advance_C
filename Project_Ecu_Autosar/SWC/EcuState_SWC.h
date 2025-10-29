#ifndef ECUSTATE_SWC_H
#define ECUSTATE_SWC_H
#include "Rte.h"
#include "Os_Cfg.h"
//enum lưu trữ các biến statemachine
typedef enum {
    STATE_INIT,             //trạng thái khởi tạo hệ thống (cảm biến,actuator)
    STATE_NORMAL,           //trạng thái bình thường (đọc cảm biến -> tính toán -> điều khiển motor) và kiểm tra lỗi
    STATE_ERROR_HANDLING,   //trạng thái xử lý lỗi
    STATE_EMERGENCY_STOP,   //trạng thái tắt hệ thống khẩn cấp tự động
    STATE_SHUTDOWN          //trạng thái tắt hệ thống (bởi người dùng)
}ECU_State;

//enum định nghĩa trạng thái nguồn hệ thống
typedef enum{
    ON,
    OFF
}Ignition_status;

//enum lưu trữ trạng thái xử lý của các Runnable
typedef enum{
    SUCCESS,
    FAIL
}Runnable_status;

//cấu trúc lưu trữ các cờ trạng thái xử lý của ECU -> cập nhật bởi các Runable
typedef struct{
    Runnable_status SensorInitFlag;       
    Runnable_status CanInitFlag;
    Runnable_status DiagnoseInitFlag;
    Runnable_status ActuatorInitFlag;
    Runnable_status SensorErrorDetectFlag; 
    Runnable_status ActuatorStateFlag;    
    Runnable_status newCriticalErrorFlag;  
    Ignition_status IgnitionFlag;
}ECU_Flag;

//hàm quản lý trạng thái hệ thống
void ECU_StateMachine(void);

//hàm kiểm tra khởi tạo nguồn hệ thống, cảm biến và động cơ
bool AllSystemsOK();

//hàm cập nhật trạng thái nguồn hệ thống -> gọi bởi task keyboard
void IgnitionSet(Ignition_status state,ECU_State currentState);

//biến toàn cục chia sẻ giữa các Swc để cập nhật trạng thái xử lý của Runnable
extern ECU_Flag flagECU;

#endif