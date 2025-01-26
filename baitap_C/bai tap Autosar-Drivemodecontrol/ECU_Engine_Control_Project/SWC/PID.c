#include "PID.h"
#include "DriveMode_Control.h"
#include <math.h>
void PID_Init(PID_Config *PID, double Kp, double Ki, double Kd)
{
    PID->kp = Kp;
    PID->ki = Ki;
    PID->kp = Kp;
    PID->error = 0, PID->error_pre1 = 0, PID->error_pre2 = 0;
    PID->output = 0, PID->last_output = 0;
}
float PID_Calculation(PID_Config PID, float setpoint, float current_value)
{

    float P_part = 0;
    float I_part = 0;
    float D_part = 0;
    // establish formula for PID PIDeter
    PID.error = setpoint - current_value;
    P_part = PID.kp * (PID.error - PID.error_pre1);
    I_part = 0.5 * PID.ki * T * (PID.error + PID.error_pre1);
    D_part = PID.kd * (PID.error - 2 * PID.error_pre1 + PID.error_pre2) / T;
    PID.output = PID.last_output + P_part + I_part + D_part;
    // store data
    PID.last_output = PID.output;
    PID.error_pre1 = PID.error;
    PID.error_pre2 = PID.error_pre1;
    // process raw output data and export final output control value
    return PID.output;
}