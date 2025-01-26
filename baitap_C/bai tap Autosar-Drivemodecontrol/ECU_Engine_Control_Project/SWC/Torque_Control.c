#include "Rte_TorqueControl.h" // Bao gồm interface của RTE cho Torque Control
#include "Torque_Control.h"
#include "DriveMode_Control.h"
#include <stdio.h> // Thư viện cho printf
#include <math.h>
// Hàm khởi tạo hệ thống điều khiển mô-men xoắn
static void TorqueLimit(float *desired_torque)
{
    if (*desired_torque > DRIVER_MAX_TORQUE)
        *desired_torque = DRIVER_MAX_TORQUE;
    if (*desired_torque < 0)
        *desired_torque = DRIVER_MIN_TORQUE;
}
void TorqueControl_Init(void)
{
    // Khởi tạo các cảm biến bàn đạp ga, tốc độ và tải trọng
    Std_ReturnType status;

    printf("Khởi tạo hệ thống Torque Control...\n");

    // Khởi tạo cảm biến bàn đạp ga
    status = Rte_Call_RpThrottleSensor_Init();
    if (status == E_OK)
    {
        printf("Cảm biến bàn đạp ga đã khởi tạo thành công.\n");
    }
    else
    {
        printf("Lỗi khi khởi tạo cảm biến bàn đạp ga.\n");
        return;
    }

    // Khởi tạo cảm biến tốc độ
    status = Rte_Call_RpSpeedSensor_Init();
    if (status == E_OK)
    {
        printf("Cảm biến tốc độ đã khởi tạo thành công.\n");
    }
    else
    {
        printf("Lỗi khi khởi tạo cảm biến tốc độ.\n");
        return;
    }

    // Khởi tạo cảm biến tải trọng
    status = Rte_Call_RpLoadSensor_Init();
    if (status == E_OK)
    {
        printf("Cảm biến tải trọng đã khởi tạo thành công.\n");
    }
    else
    {
        printf("Lỗi khi khởi tạo cảm biến tải trọng.\n");
        return;
    }

    // Khởi tạo cảm biến mô-men xoắn thực tế
    status = Rte_Call_RpTorqueSensor_Init();
    if (status == E_OK)
    {
        printf("Cảm biến mô-men xoắn thực tế đã khởi tạo thành công.\n");
    }
    else
    {
        printf("Lỗi khi khởi tạo cảm biến mô-men xoắn.\n");
        return;
    }

    // Khởi tạo bộ điều khiển mô-men xoắn (có thể là PWM hoặc module điều khiển động cơ)
    status = Rte_Call_PpMotorDriver_Init();
    if (status == E_OK)
    {
        printf("Bộ điều khiển mô-men xoắn đã khởi tạo thành công.\n");
    }
    else
    {
        printf("Lỗi khi khởi tạo bộ điều khiển mô-men xoắn.\n");
        return;
    }
    printf("Hệ thống Torque Control đã sẵn sàng.\n");
}

// Hàm cập nhật hệ thống điều khiển mô-men xoắn
void TorqueControl_Update()
{
    float throttle_input = 0.0f;
    float current_speed = 0.0f;
    float load_weight = 0.0f;
    float actual_torque = 0.0f;
    float desired_torque = 0.0f;
    // Đọc dữ liệu từ cảm biến bàn đạp ga
    if (Rte_Read_RpThrottleSensor_ThrottlePosition(&throttle_input) == E_OK)
    {
        printf("Giá trị bàn đạp ga: %.2f%%\n", throttle_input*100); //scale from 0 - 1
    }
    else
    {
        printf("Lỗi khi đọc cảm biến bàn đạp ga!\n");
    }

    // Đọc dữ liệu từ cảm biến tốc độ
    if (Rte_Read_RpSpeedSensor_Speed(&current_speed) == E_OK)
    {
        printf("Tốc độ xe hiện tại: %.2f km/h\n", current_speed);
    }
    else
    {
        printf("Lỗi khi đọc cảm biến tốc độ!\n");
    }

    // Đọc dữ liệu từ cảm biến tải trọng
    if (Rte_Read_RpLoadSensor_LoadWeight(&load_weight) == E_OK)
    {
        printf("Tải trọng hiện tại: %.2f kg\n", load_weight);
    }
    else
    {
        printf("Lỗi khi đọc cảm biến tải trọng!\n");
    }

    // Tính toán mô-men xoắn ban đầu theo chế độ lái -> hiệu chỉnh các hệ số phản hồi bàn đạp gas,tải trọng,tốc độ
    desired_torque = (f_pedal(throttle_input) * f_load(load_weight) * f_speed(current_speed)) * DRIVER_MAX_TORQUE;

    //giới hạn mo-men xoắn trong mức cho phép
    TorqueLimit(&desired_torque);
    
    printf("mo-men xoắn điều chỉnh theo chế độ lái: %.2f Nm\n", desired_torque);

  
    // Ghi mô-men xoắn yêu cầu tới bộ điều khiển động cơ
    if (Rte_Write_PpMotorDriver_SetTorque(desired_torque) == E_OK)
    {
        printf("Đã gửi mô-men xoắn yêu cầu tới động cơ.\n");
    }
    else
    {
        printf("Lỗi khi gửi mô-men xoắn tới động cơ!\n");
    }

    // Đọc mô-men xoắn thực tế để so sánh với mô-men xoắn yêu cầu
    if (Rte_Read_RpTorqueSensor_ActualTorque(&actual_torque) == E_OK)
    {
        printf("Mô-men xoắn thực tế: %.2f Nm\n", actual_torque);
    }
    else
    {
        printf("Lỗi khi đọc mô-men xoắn thực tế!\n");
    }
    // So sánh và điều chỉnh nếu có sự sai lệch giữa mô-men xoắn thực tế và yêu cầu

    if (actual_torque < desired_torque)
    {
        printf("Tăng mo-men xoắn để đạt mức yêu cầu");
        //actual_torque += 10;
    }
    else if (actual_torque > desired_torque)
    {
        printf("giảm mo-men xoắn để đạt mức yêu cầu");
        //actual_torque -= 10;
    }
    else if (fabs(actual_torque - desired_torque) <= 5.0f)
    {
        printf("mô-men xoắn đạt mức yêu cầu.\n");
    }
}
