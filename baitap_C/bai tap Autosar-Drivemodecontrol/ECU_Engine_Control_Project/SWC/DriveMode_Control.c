#include "DriveMode_Control.h"
#include "Rte_TorqueControl.h"
#include <math.h>
#include <stdio.h>
/*
    ECo:
    + mo-men xoắn ít nhạy hơn đối với các mức độ đap gas
    + mo-men xoắn tăng khi tốc độ thấp và giảm dần khi tốc độ tăng
    + mo-men xoắn tăng ít giữa các mức tải trọng
    NORMAL:
    + mo-men xoắn cân bằng giữa ECO và SPORT
    SPORT:
    + mo-men xoắn nhạy hơn với các mức độ đạp ga
    + mo-men xoắn tăng mạnh nhất khi tốc độ thấp và giảm giảm dần khi tốc độ tăng
    = mo-men xoắn tăng mạnh khi tải trọng lớn dần
 */
DriveMode mode = ECO;
void DriveMode_Init()
{
    printf("Khởi tạo hệ thống Drive Mode Control...\n");
    printf("ĐÃ CHỌN CHẾ ĐỘ ");
    switch (mode)
    {
    case ECO:
        printf("ECO\n");
        mode = ECO;
        break;
    case NORMAL:
        printf("NORMAL\n");
        mode = NORMAL;
        break;
    case SPORT:
        printf("SPORT\n");
        mode = SPORT;
        break;
    default:
        break;
    }
}
void DriveMode_Update()
{
    char command;
    scanf("%c", &command);
    printf("\nCHẾ ĐỘ LÁI ĐÃ CHUYỂN SANG ");
    switch (command)
    {
    case 'e':
        printf("ECO\n");
        mode = ECO;
        break;
    case 'n':
        printf("NORMAL\n");
        mode = NORMAL;
        break;
    case 's':
        printf("SPORT\n");
        mode = SPORT;
        break;
    default:
        break;
    }
}
float f_pedal(float pedal_position)
{
    switch (mode)
    {
    case ECO:
        //printf("pedal factor is adjusting based on ECO MODE...\n");
        return pow(pedal_position, 2);
        break;
    case NORMAL:
        //printf("pedal factor is adjusting based on NORMAL MODE...\n");
        return pedal_position; // Đảm bảo cảm giác lái không bị chậm trễ mà vẫn tiết kiệm năng lượng.
        break;
    case SPORT:
        //printf("pedal factor is adjusting based on SPORT MODE...\n");
        return sqrt(pedal_position) + (1 - sqrt(pedal_position)) * pedal_position; // Làm giảm mô-men xoắn ít hơn để duy trì khả năng tăng tốc ngay cả ở tốc độ cao.
        break;
    default:
        return 0;
        break;
    }
}
float f_load(float weight_load)
{
    return 1 + weight_load / VEHICLE_LOAD;
}
float f_speed(float current_speed)
{
    return (1 - current_speed / MAX_SPEED);
}
