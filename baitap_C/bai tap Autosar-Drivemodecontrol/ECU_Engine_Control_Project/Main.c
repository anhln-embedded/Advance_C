#include "BSW/Services/Os.h"
#include "SWC/Torque_Control.h"
#include <stdio.h>
// Task để khởi tạo và cập nhật hệ thống điều khiển mô-men xoắn
void *Task_TorqueControl(void *arg)
{
    // Gọi hàm khởi tạo Torque Control
    TorqueControl_Init();

    // Liên tục cập nhật hệ thống điều khiển mô-men xoắn
    while (1)
    {
        TorqueControl_Update();
        printf("\n1s passed........\n");
        // Tạm dừng 1 giây trước khi cập nhật tiếp
        Os_Delay(1000);
    }

    return NULL;
}
void *Task_DriveModeControl(void *arg)
{
    DriveMode_Init();
    while (1)
    {
        DriveMode_Update();
        Os_Delay(100);
    }
}
int main(void)
{
    // Khởi tạo hệ điều hành
    Os_Init();
    // Tạo task chung cho Torque Control (khởi tạo + cập nhật)
    Os_CreateTask(Task_TorqueControl, "Torque Control");
    Os_CreateTask(Task_DriveModeControl, "Drive Mode Control");

    // Chờ các task hoàn thành
    Os_Shutdown();

    return 0;
}
