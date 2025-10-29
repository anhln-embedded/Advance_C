#include "sensor_SWC.h"

static int16_t ADC_ReadCurrentSensor(){
   /* 
        triển khai gọi Rte Interface để xử lý
   */
}
static int16_t ADC_ReadVoltageSensor(){
    /* 
        triển khai gọi Rte Interface để xử lý
   */
}
static int16_t ADC_ReadTempSensor(){
    /* 
        triển khai gọi Rte Interface để xử lý
   */
}
static int16_t Encoder_ReadRPM(){
    int rpm = 0;
    Std_ReturnType Status = Rte_Read_CurrentSensor_current(&rpm);
    if(Status == E_OK){
        printf("- tốc độ hiện tại là: %d rpm\n");
    }
    else{
        printf("- lỗi khi đọc cảm biến encoder\n");
        flagECU.SensorErrorDetectFlag = FAIL; //cập nhật trạng thái lỗi cho statemachine
    }
}

void Runnable_InitSensors(){
    Std_ReturnType Init_status;
    printf("Khởi tạo cảm biến dòng điện...\n");

    Init_status = Rte_Call_CurrentSensor_SWC_Init();
    if (Init_status == E_OK) {
        printf("Cảm biến dòng điện đã được khởi tạo thành công.\n");
    }else {
        printf("Lỗi khi khởi tạo cảm biến dòng điện.\n");
        return;
    }
    /* 
        khởi tạo các cảm biến còn lại
    */
    flagECU.SensorInitFlag = SUCCESS;  //cập nhật trạng thái khởi tạo thành công cho statemachine
}
void Runnable_ReadSensors(void) {
    SensorData data;
    printf(" - đang đọc dữ liệu sensor\n");
    data.current = ADC_ReadCurrentSensor();
    data.voltage = ADC_ReadVoltageSensor();
    data.temperature = ADC_ReadTempSensor();
    data.RPM = Encoder_ReadRPM();

    //Gửi dữ liệu cảm biến đến EngineControl_SWC thông qua RTE.
    if(Rte_Write_Sensor_SWC_SensorData(&data) == E_OK){
        printf(" - Đã gửi dữ liệu sensor để xử lý tính toán\n");
    }
}
