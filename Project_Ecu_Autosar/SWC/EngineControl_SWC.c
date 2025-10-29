#include "EngineControl_SWC.h"

static SensorData data;

static void HandleCriticalError(){
   //logic kiểm tra và điều chỉnh giới hạn lại giá trị
   printf("- đang xử lý lỗi\n");
   return;
}
static int16_t ComputePWM(float rpm , float current, float voltage){
   //logic xử lý
   int PWM = 0;
   printf(" - Đang tính toán duty cycle\n");
   return PWM;
}
void Runnable_ProcessSensorData(void) {

    //Nhận dữ liệu cảm biến từ Sensor_SWC thông qua Rte
    Std_ReturnType Status = Rte_Read_EngineControl_SWC_SensorData(&data);
    if(Status == E_NOT_OK){
        printf(" -Lỗi khi nhận dữ liệu cảm biến\n");
        return;
    }
    printf(" - đã nhận dữ liệu cảm biến\n");

    //logic lọc nhiễu,  tính toán giá trị trung bình

    //logic tính toán mo-men xoắn dựa trên rpm
    printf(" - Bắt đầu tính toán Pwm\n");
    ControlCmd cmd;
    cmd.PWM_DutyCycle = ComputePWM(data.RPM, data.current, data.voltage);
    cmd.status = MOTOR_RUN;

    //Ghi dữ liệu cho EngineControl_SWC
    if(Rte_Write_EngineControl_SWC_ControlCmd(&cmd) == E_OK){
        //LOGIC xử lý
        printf(" - Đang gửi tín hiệu pwm để điều khiển driver \n");
    }
    return;
}

bool Runnable_CheckError(void) {
    bool errorDetected;
    //Yêu cầu Diagnostic_SWC xử lý lỗi
    if(Rte_Call_Diagnostic_SWC_CheckCriticalError(&errorDetected) == E_OK){
        //LOGIC xủ lý
    }
    if(errorDetected) {
        HandleCriticalError(); //xử lý lỗi quá dòng, quá nhiệt , rpm (quá cao/thấp)
    }
    return errorDetected;
}