#include "EcuState_SWC.h"
#include "Diagnostic_SWC.h"

//định nghĩa trạng thái ban đầu của hệ thống
ECU_State currentState = STATE_SHUTDOWN;

//định nghĩa trạng thái ban đầu của các cờ 
ECU_Flag flagECU = {
    .ActuatorInitFlag = FAIL,
    .CanInitFlag = FAIL,
    .ActuatorStateFlag = FAIL,
    .SensorErrorDetectFlag = FAIL,
    .SensorInitFlag = FAIL,
    .IgnitionFlag = OFF
};

//hàm kiểm tra lỗi hệ thống
static bool CriticalErrorDetected(){
    return (flags.overCurrent || flags.overTemperature || flags.overVoltage || flags.speedError) ? true : SUCCESS;
}

//hàm kiểm tra nguồn hệ thống
static bool IgnitionOFF(){
   return flagECU.IgnitionFlag == ON ? false : true;
}

//hàm kiểm tra cảm biến lỗi cảm biến
static bool SensorErrorDetected(){
   return flagECU.SensorErrorDetectFlag;
}

//hàm kiểm tra lỗi mới
static bool NewCriticalError(){
    /* 
        logic kiểm tra trạng thái lỗi mới nhất (phân biệt với lỗi trước đó)
    */
}

//hàm kiểm tra kết quả xử lý lỗi
static bool ErrorRecovered(){
    /* 
        logic cập nhật lại trạng thái bình thường sau khi xử lý lỗi cho phép động cơ hoạt động bình thường trở lại
    */
}

//hàm thực thi các thao tác tắt nguồn hệ thống
static void PerformShutdown(){
    //gọi Runnable để dừng động cơ và tắt xe
    return;
}

//hàm thực thi lưu trữ dữ liệu hệ thống khi tắt nguồn
static void  SaveShutdownState(){
    //gọi Runnable để lưu trạng thái hệ thóng (tốc độ, nhiệt độ, dòng , áp)
    printf("đã lưu trạng thái hệ thống\n");
    return;
}

//hàm thực thi dừng khẩn cấp hệ thống (không tắt nguồn)
static void ExecuteEmergencyStop(){
    //gọi Runnable để dừng động cơ
   
    printf("đọng cơ đã dừng\n");
    return;
}

bool AllSystemsOK() {
    if(flagECU.ActuatorInitFlag == SUCCESS && 
        //flagECU.CanInitFlag &&
        flagECU.DiagnoseInitFlag == SUCCESS && 
        flagECU.SensorInitFlag == SUCCESS &&
        flagECU.IgnitionFlag == ON){
            printf("hệ thống khởi tạo thành công\n");
            return true;
    }
    else{
        printf("hệ thống khởi tạo thất bại\n");
        /* printf("sensor: %d\nActuator: %d\nDiagnostic: %d\nIgnition: %d\n",
        flagECU.SensorInitFlag,flagECU.ActuatorInitFlag,flagECU.DiagnoseInitFlag,flagECU.IgnitionFlag); */
        return false;
    }
}
void IgnitionSet(Ignition_status Ignition_state,ECU_State StateECU){
    flagECU.IgnitionFlag = Ignition_state;
    currentState = StateECU;
    /* printf("Ignition: %s\n",flagECU.IgnitionFlag == ON ? "ON" : "OFF");
    if(currentState == STATE_INIT) printf("INIT STATE\n");
    else if(currentState == STATE_NORMAL) printf("INIT NORMAL\n");
    else if(currentState == STATE_EMERGENCY_STOP) printf("STATE EMERENCY STOP\n");
    else if(currentState == STATE_SHUTDOWN) printf("STATE SHUTDOWN\n"); */
}

void ECU_StateMachine(void) {
    switch (currentState) {
        case STATE_INIT:    
        //nếu khởi tạo hardware và software thành công 
            if (AllSystemsOK()){ 
                currentState = STATE_NORMAL; // chuyển sang trạng thái bình thường (đọc cảm biến -> tính toán -> điều khiển)
                printf("đã chuyển sang STATE_NORMAL\n");
            }
            break;
        case STATE_NORMAL:
        //Nếu lỗi nghiêm trọng -> quá dòng/nhiệt -> mất điều khiển động cơ
            if (CriticalErrorDetected()){
                //xử lý dừng động cơ khẩn cấp
                currentState = STATE_EMERGENCY_STOP; //chuyển trạng thái khẩn cáp
            }
            
            //nếu giá trị cảm biến không hợp lệ
            else if (SensorErrorDetected()){
                currentState = STATE_ERROR_HANDLING; //chuyển sang trạng thái xử lý lỗi
                printf("đã chuyển sang STATE_ERROR_HANDLING\n");
            }

            //nếu hệ thống hoạt động bình thường nhưng xe được tắt
            else if (IgnitionOFF()){
                SaveShutdownState(); //ECU lưu trạng thái (file csv)
                currentState = STATE_SHUTDOWN;
            }
            break;
        case STATE_ERROR_HANDLING:
            //Nếu cảm biến ổn định trở lại
            if (ErrorRecovered()){
                ExecuteEmergencyStop(); // dừng động cơ
                currentState = STATE_NORMAL; //khôi phục trạng thái bình thường của hệ thống
            }
            //nếu có lỗi mới nghiệm trọng
            else if (NewCriticalError()) {
                currentState = STATE_EMERGENCY_STOP; //chuyển trạng thái dừng khẩn cấp
            }
            break;
        case STATE_EMERGENCY_STOP:
            //nếu có lệnh tắt xe 
            if (IgnitionOFF()){
                SaveShutdownState(); //ECU lưu trạng thái (file csv)
                currentState = STATE_SHUTDOWN; 
                printf("đã chuyển sang STATE_SHUTDOWN\n");
            }
            ExecuteEmergencyStop(); // dừng động cơ
            break;
        case STATE_SHUTDOWN:
            PerformShutdown(); //ngắt hệ thống (dừng động cơ) , tát nguồn
            break;
    }
}

