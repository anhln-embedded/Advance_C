#ifndef TASK_H_
#define TASK_H_

#include "EcuState_SWC.h"
#include "Diagnostic_SWC.h"
#include "Actuator_SWC.h"
#include "EngineControl_SWC.h"
#include "sensor_SWC.h"
#include "Os_Cfg.h"

void* Task_Keyboard(void* arg);
void* Task_Sensor(void* arg);
void* Task_EngineControl(void* arg);
void* Task_Actuator(void* arg);
void* Task_Diagnostic(void* arg);
void* ISR_CAN_RX(void* arg);

#endif