#ifndef DRIVEMODE_CONTROL_H
#define DRIVEMODE_CONTROL_H
typedef enum
{
    ECO,
    NORMAL,
    SPORT
} DriveMode;

// định nghĩa momen xoắn điều chỉnh tối đa cho từng chế độ

extern DriveMode mode;

void DriveMode_Init(void);
void DriveMode_Update(void);
float f_pedal(float pedal_position); //hàm tính toán hệ số hiệu chỉnh phản hồi của bàn đạp
float f_load(float weight_load); //hàm tính toán hệ số ảnh hưởng đến momen xoắn dựa trên tải trọng
float f_speed(float current_speed);//hàm tính toán hệ số ảnh hưởng đến momen xoắn dựa trên tốc độ 
#endif