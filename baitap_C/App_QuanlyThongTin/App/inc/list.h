#ifndef _LIST_H
#define _LIST_H
#include "stdTypes.h"

typedef struct 
{
    char* name;
    char* address;
    char* phone;
    uint8_t age;
}Info;
typedef struct User_node{
    struct User_node* next_user; 
    Info info;                  
}User_node;
typedef struct CenterPoint{
    struct CenterPoint* left;
    struct CenterPoint* right;
    User_node* user;
}CenterPoint;

void Create_UserList(Info *info, User_node **list_user_sortName, User_node **list_user_sortPhone);
void print_UserList(User_node *head);
void free_UserList(User_node** head);
int stringCompare(const char *str1, const char *str2);

extern uint8_t total_user; 
#endif