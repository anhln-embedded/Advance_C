/********************************************************
 *******************
 * @file ManageUser.h
 * @brief Khai báo cấu trúc lưu dữ cách thức tìm kiếm thông tin của 1 User
 * @details File này cung cấp định nghĩa cấu trúc cây nhị phân,Header này chỉ nên được include bởi
 *          module Service
 * @version 1.0
 * @date 2025-16-8
 * @author Pham Cao Duy
 *********************************************************
 ******************/
#ifndef CENTERPOINT_H
#define CENTERPOINT_H
/*
 * Định nghĩa cấu trúc CenterPoint để xây dựng cây nhị phân quản lý các node của linked list
 * left : nhánh con bên trái node gốc  
 * right: nhánh con bên phải node gốc
 * user : node gốc chứa thông tin user
 */
#include "UserNode.h"
typedef struct CenterPoint{
    struct CenterPoint* left;
    struct CenterPoint* right;
    UserNode* root;
}CenterPoint;
#endif