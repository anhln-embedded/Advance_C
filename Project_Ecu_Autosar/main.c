#include "task.h"
#include "Os.h"
int main(){
    //Khởi tạo hệ điều hành
    Os_Init();
    //khởi tạo và chạy các luồng 
    Os_CreateTask(Task_Sensor,"Task Sensor");
    Os_CreateTask(Task_EngineControl,"Task EngineControl");
    Os_CreateTask(Task_Actuator,"Task Actuator");
    Os_CreateTask(Task_Diagnostic,"Task Diagnostic");
    Os_CreateTask(Task_Keyboard,"Task Keyboard");

    Os_Shutdown();
    return 0;
}
