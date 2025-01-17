#ifndef _READ_H
#define _READ_H
#include "list.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <malloc.h>
//trả về thông tin sau khi đọc từ file csv
Info *readCSV(char *path);

//in ra thông tin
void print_info(Info* info); 

//giải phóng vùng nhớ heap lưu trữ thông tin
void free_info(Info* info);
#endif