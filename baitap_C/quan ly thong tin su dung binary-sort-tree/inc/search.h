#ifndef _SEARCH_H
#define _SEARCH_H
#include"list.h"
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include<malloc.h>
//xây dựng cây nhị phân
CenterPoint *buildTree(User_node *head, int start, int end);

//trả về node giữa của cây nhị phân
CenterPoint *centerPoint(User_node *head);

//so sánh từng ký tự của 2 chuỗi và trả về kết quả 
/* 
     > 0 :nếu str1 > str2
     < 0: nếu str1 < str2
 */
int stringCompare(const char *str1, const char *str2);

//tìm thông tin dựa trên cây nhị phân
CenterPoint *Search_Info(CenterPoint **root, const char *search);

//hàm tìm thông tin theo tên / sdt
void print_Search_byPhone(CenterPoint *root);
void print_Search_byName(CenterPoint *root, User_node *list_user);

//giải phóng vùng nhớ lưu trữ cây nhị phân
void freeBST(CenterPoint* user);
#endif