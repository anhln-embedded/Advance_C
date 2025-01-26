#ifndef PID_H
#define PID_H
typedef struct
{
    double kp, ki, kd;
    float error, error_pre1, error_pre2;
    float output, last_output;
} PID_Config;
#define T 1 // sample time 1s
void PID_Init(PID_Config *param, double Kp, double Ki, double Kd);
float PID_Calculation(PID_Config param, float setpoint_value, float current_value);
#endif