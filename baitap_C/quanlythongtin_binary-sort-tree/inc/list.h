#ifndef _LIST_H
#define _LIST_H
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
typedef struct 
{
    char* name;
    char* address;
    char* phone;
    uint8_t age;
}Info;
typedef struct New_user{
    struct New_user* next_user; //next address of node
    Info info;                  //data of node
}User_node;
typedef struct CenterPoint{
    struct CenterPoint* left;
    struct CenterPoint* right;
    User_node* user;
}CenterPoint;

void Create_UserList(Info *info, User_node **list_user_sortName, User_node **list_user_sortPhone);
void print_user(User_node *head);
void free_list_user(User_node* head);


extern int stringCompare(const char *str1, const char *str2);
#endif