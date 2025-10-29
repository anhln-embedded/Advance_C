#include "task.h"
#include "Os.h"
#include <stdlib.h>

void* Task_Sensor(void* arg) {
    //khởi tạo các cảm biến -> cập nhật trạng thái cho state machine
    Runnable_InitSensors();
    while(1){
        //cơ chế khóa tài nguyên (đảm bảo 1 thời điểm chỉ có 1 luồng được phép truy cập)
        GetResource();   
    
        //Đợi điệu kiện kích hoạt task sensor 
        waitEvent(TASK_ID_Sensor,evSystemRunning);

        //kiểm tra điều kiện dừng nếu user nhấn stop
        if(check_stop_condition(TASK_ID_Sensor)){
            LeaveResource();
            break;  //stop luồng thực thi
        }
        printf("\n----------------------------\n");
        printf("\n[TASK_Sensor]: Processing...\n");
        //dọc cảm biến và cập nhật state machine
        Runnable_ReadSensors();        
        
        //kích hoạt sự kiện xử lý sensor data
        setEvent(evSensorDataReady);  
        notify_event(TASK_ID_EngineControl); //thông báo cho task_EngineControl

        //mở khóa tài nguyên (cho phép các luòng khác được can thiệp)
        LeaveResource();

        //thực thi sau mỗi chu kỳ nhất định
        Os_Delay(1000);
    }
    printf("[TASK_Sensor] đã bị hủy\n");
    return NULL;
}
void* Task_EngineControl(void* arg) {
    while(1){
        GetResource();;
        
        //Đợi event kích hoạt từ task sensor
        waitEvent(TASK_ID_EngineControl,evSensorDataReady);

        if(check_stop_condition(TASK_ID_EngineControl)){
            LeaveResource();
            break;  //stop luồng thực thi
        }

        printf("\n[TASK_EngineControl]: Processing...\n");
        //xử lý dữ liệu cảm biến
        Runnable_ProcessSensorData();

        //mô phỏng trạng thái lỗi
        uint8_t errorStatus = rand() % 2;

        if(errorStatus == 1){
            //kích hoạt xự kiện cho task Diagnostic
            setEvent(evErrorDetected);
            notify_event(TASK_ID_Diagnostic);  //thông báo kết quả cho task_Diagnostic   
        }
    
        //kích hoạt sự kiện cho task actuator
        setEvent(evControlCmdReady);
        notify_event(TASK_ID_Actuator);    //thông báo kết quả cho task Actuator

        //reset trạng thái event
        clearEvent(evSensorDataReady);
        LeaveResource();
    }
    printf("[TASK_EngineControl]: đã bị hủy\n");
    return NULL;
}
void* Task_Actuator(void* arg) {
    //khởi tạo driver motor -> cập nhật trạng thái cho state machine
    Runnable_InitActuator();
    while(1){
        //khóa tài nguyên
        GetResource();
    
        //đợi điều kiện kích họat task
        waitEvent(TASK_ID_Actuator,evControlCmdReady);

         //kiểm tra điều kiện dừng luồng
        if(check_stop_condition(TASK_ID_Actuator)){
            LeaveResource();
            break;
        }


        printf("\n[TASK_Actuator]: Processing...\n");
        Runnable_ExecuteActuator();

        //reset event
        clearEvent(evControlCmdReady);

        //mỏ khóa tài nguyên
        LeaveResource();
    }
    printf("[TASK_Actuator]: đã bị hủy\n");
    return NULL;
}
void* Task_Diagnostic(void* arg) {
    //khởi tạo hệ thống chuẩn đoán -> cập nhật trạng thái cho state machine
    Runnable_InitDiagnostic();
    while(1){
        GetResource();

        waitEvent(TASK_ID_Diagnostic,evErrorDetected);

        if(check_stop_condition(TASK_ID_Diagnostic)){
            LeaveResource();
            break;
        }

        printf("\n[TASK_Diagnostic]: Processing...\n");
        Runnable_ReportErrors();

        clearEvent(evErrorDetected);
        LeaveResource();
    }
    printf("[TASK_Diagnostic]: đã bị hủy\n");
    return NULL;
}
void* ISR_CAN_RX(void* arg) {
   /* 
       Triển khai phần xử lý tín hiệu ngắt từ CAN
   */
}
void* Task_Keyboard(void* arg){
    static char choice;
    printf("nhấn 'r' để CHẠY ĐỘNG CƠ , 's' để TẠM DỪNG ĐỘNG CƠ , 'q' để TẮT NGUỒN HỆ THỐNG  \n");
    while(1){
        scanf("%c",&choice);
        GetResource();

        if (choice == 'r')
        {
            printf("đang khởi động hệ thống\n");
            //cập nhật trạng thái khởi động hệ thống 
            IgnitionSet(ON,STATE_INIT);

            //kiểm tra khởi tạo hệ thống và kích hoạt các luồng
            if(AllSystemsOK()){
                Os_Delay(1000);
                setEvent(evSystemRunning);      //kích hoạt sự kiện khởi động hệ thống
                notify_event(TASK_ID_Sensor);   //thông báo cho phép kích hoạt task sensor
            }
            else{
                goto handle_shutdown;  //Dừng tất cả các luồng ngay lập tức Nếu hệ thống khởi tạo thất bại
            }
        }
        else if(choice == 's')
        {
           //cập nhật trạng thái dừng khẩn cấp
           IgnitionSet(ON,STATE_EMERGENCY_STOP);
           clearEvent(evSystemRunning);
        }
        else if(choice == 'q'){
            handle_shutdown:    //label được dùng để xác định vị trí nhảy đến xử lý khi được gọi

            //cập nhật trạng thái tắt nguồn hệ thống
            IgnitionSet(OFF,STATE_SHUTDOWN); 

            //kích hoạt sự kiện dừng hệ thống
            setEvent(evSystemStop);
            
            //thông báo đến luồng đọc cảm biến để lần lượt dừng các luồng còn lại
            notify_event(TASK_ID_Sensor);
            printf("động cơ đã tắt\n");
            LeaveResource(); 
            break;
        }
        ECU_StateMachine(); //Thực hiện cập nhật trạng thái hệ thống
        LeaveResource();

        //delay để giảm tải hệ thống
        Os_Delay(50);
    }
    printf("[TASK_Keyboard]: đã bị hủy\n");
    return NULL;
}