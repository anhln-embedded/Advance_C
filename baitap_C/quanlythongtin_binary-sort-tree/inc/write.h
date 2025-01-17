#ifndef _WRITE_H
#define _WRITE_H
#include "list.h"
#include <stdio.h>
#include <stdbool.h>
#include <malloc.h>
#define FAIL_CREATED_FILE 0
#define SUCCESS_CREATED_FILE 1
Info *readCSV(char *path);
bool writeCSV(char* path);
void log_status(const char* str);
#endif