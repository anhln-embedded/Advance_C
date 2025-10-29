#include "Os_Cfg.h"

//khóa mutex để cho phép các luồng lần lượt truy cập tài nguyên chung
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;  

//mảng chứa các giá biến conditional tương ứng với các event để thông báo khi 1 luồng thực hiện xong
pthread_cond_t  triggerd_events[TASK_ID_Max]; 

//biến toàn cục lưu trữ các task Event và trạng thái hệ thống 
uint8_t Task_Events = 0; 

void setEvent(uint8_t eventMask) {
    Task_Events |= eventMask;
}

void clearEvent(uint8_t EventMask){
    Task_Events &= ~EventMask; 
}
//hàm cho phép 1 luống đợi điều kiện kích hoạt từ lường khác
void waitEvent(TaskIDType Id,uint8_t EventMask){
    //kiểm tra EventMask của task tương ứng có được kích hoạt không cùng với điều kiện dừng lường 
    while(!(Task_Events & EventMask) && !(Task_Events & evSystemStop)){
        pthread_cond_wait(&triggerd_events[Id],&mutex);
    }
}
bool IsEventSet(uint8_t EventMask){
    return (Task_Events & EventMask);
}
//hàm cho phép 1 luồng truy cập vào tài nguyên chung để thao tác
void GetResource(){
    pthread_mutex_lock(&mutex);
}
//hàm cho phép 1 luồng dừng thao tác trên tài nguyên chung
void LeaveResource(){
    pthread_mutex_unlock(&mutex);
}

//hàm cho phép 1 luồng thông báo kết quả đến luồng khác
void notify_event(TaskIDType Id){
    pthread_cond_signal(&triggerd_events[Id]); 
}
bool check_stop_condition(TaskIDType Id){
    //kiểm tra nếu cờ được set thì lần lượt thông báo đến các luồng để dừng xử lý
    if(Task_Events & evSystemStop){
            //thông báo đến luồng phụ thuộc tiếp theo 
            if(Id == TASK_ID_Sensor){
                pthread_cond_signal(&triggerd_events[TASK_ID_EngineControl]);
            }
            else if(Id == TASK_ID_EngineControl){
                pthread_cond_signal(&triggerd_events[TASK_ID_Actuator]);
                pthread_cond_signal(&triggerd_events[TASK_ID_Diagnostic]);
            }
            else if(Id == TASK_ID_Diagnostic || Id == TASK_ID_Actuator){
                return true;
            }
        return true;    //trả về kết quả để thục hiện thoát khỏi luồng hiện tại
    }
    else {
        return false;   //trả về kết quả tiếp tục thực thi luồng
    }
}

