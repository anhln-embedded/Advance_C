#ifndef  __OS_H
#define  __OS_H
#include <iostream>
#include <ctime>
#include <time.h>
#include <stdint.h>
#include"ecu.hpp"
void delay_ms(size_t ms);
void simulation(Engine& subject,size_t time_ms,uint8_t limit);
#endif