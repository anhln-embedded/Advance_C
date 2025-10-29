#include "Actuator_SWC.h"

void Runnable_InitActuator(){
    Std_ReturnType Status;
    printf("khởi tạo driver điều khiển đông cơ...\n");
    Status =  Rte_Call_MotorDriver_SWC_Init();
    if(Status == E_OK){
        printf("khởi tạo thành công driver điều khiển động cơ\n");
    }
    else{
        printf("Khởi tạo thất bại driver điều khiển động cơ\n");
        return;
    }
    flagECU.ActuatorInitFlag = SUCCESS;
}

void Runnable_ExecuteActuator(){
   printf(" - đang điều khiển động cơ\n");
}
