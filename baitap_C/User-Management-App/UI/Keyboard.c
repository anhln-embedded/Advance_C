#include "Keyboard.h"
#include <stdio.h>
#include <string.h>
#include <ctype.h>
char str[30];   //mảng chứa ký tự cho người dùng nhập
char* UI_InputString(){
    printf("Vui lòng nhập tên/sdt:");
    fgets(str,sizeof(str),stdin);           //đọc chuỗi từ bán phím bao gồm khoảng trắng
    str[strcspn(str,"\n")] = '\0';          //xóa ký tự xuống dòng trước khi nhập chuỗi/giá trị mới 
    system("cls");                          //xóa màn hình
    return str;
}
int UI_InputChoice(){
    int choice = 0;
    printf("Vui lòng nhập giá trị:");
    scanf("%d",&choice);
    while (getchar() != '\n');              //xóa ký tự xuống dòng do nhấp enter 
    system("cls");                          //xóa màn hình
    return choice;
}
void UI_ShowMessage(const char* msg){
    printf("%s\n",msg);
}
