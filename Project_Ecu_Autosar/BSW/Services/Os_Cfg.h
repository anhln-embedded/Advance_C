#ifndef OS_CFG_H
#define OS_CFG_H

#include <pthread.h>
#include "Std_Types.h"

//định nghĩa danh sách chứa ID tương ứng cho từng task
typedef enum {
    TASK_ID_Sensor,
    TASK_ID_EngineControl,   
    TASK_ID_Actuator,        
    TASK_ID_Diagnostic,     
    ID_ISR_CAN_RX,
    TASK_ID_Max
}TaskIDType;

//Định nghĩa bitmask tương ứng với event kích hoạt task
#define evSystemRunning     (1U << 0)   //event kích hoạt bởi người dùng khi muốn chạy/tạm ngưng hệ thống
#define evSystemStop        (1U << 1)   //event kích hoạt bởi người dùng khi muốn dừng hê thống
#define evSensorDataReady   (1U << 2)   //event kích hoạt mỗi khi có dữ liệu cảm biến
#define evControlCmdReady   (1U << 3)   //event kích hoạt mỗi khi tính toán xong dữ liệu
#define evErrorDetected     (1U << 4)   //event kích hoạt mổi khi phát hiện lỗi

//biến toàn cục lưu trữ danh sách các task triggered event băng cơ chế conditional
extern pthread_cond_t  triggerd_events[TASK_ID_Max]; 

//biến toàn cục mutex quản lý việc chia sẻ tải nguyên chung giữa các luồng
extern pthread_mutex_t mutex;

//hàm kích hoạt event 
void setEvent(uint8_t bitmask);

//hàm đợi event
void waitEvent(TaskIDType current_TaskId,uint8_t EventMask);

//hàm xóa event
void clearEvent(uint8_t bitmask);

//hàm kiểm tra event có được set 
bool IsEventSet(uint8_t EventMask);

//hàm trửu tượng việc khóa tài nguyên
void GetResource();

//hàm trừu tượng việc mở khóa tài nguyên
void LeaveResource();

//hàm đánh thức luồng khi có điều kiện xảy ra
void notify_event(TaskIDType current_TaskId);

//hàm kiểm tra điều kiện dừng xử lý luồng
bool check_stop_condition(TaskIDType current_TaskId);


#endif
