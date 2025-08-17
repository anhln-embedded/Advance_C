#ifndef _READ_H
#define _READ_H
#include "stdTypes.h"
#include "list.h"       

//trả về thông tin sau khi đọc từ file csv
Info *readfile(char *path);

//in ra thông tin
void print_UserInfo(Info* info); 

//giải phóng vùng nhớ heap lưu trữ thông tin
void free_UserInfo(Info* phead);

extern uint8_t total_user; 
#endif