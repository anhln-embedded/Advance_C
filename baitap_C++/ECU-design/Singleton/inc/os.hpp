#ifndef  __OS_H
#define  __OS_H
#include <iostream>
#include <ctime>
#include <time.h>
#include <stdint.h>
#include "ecu.hpp"
void simulation(EngineControlUnit *ECU, uint32_t ms, uint32_t limit);
#endif