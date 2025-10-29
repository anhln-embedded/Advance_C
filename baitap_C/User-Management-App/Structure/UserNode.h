/********************************************************
 *******************
 * @file ManageUser.h
 * @brief Khai báo cấu trúc lưu trữ các node chứa dữ liệu  User
 * @details File này cung cấp định nghĩa cấu trúc linked list chứ các node UserData,
 *          Header này chỉ nên được include bởi module Service
 * @version 1.0
 * @date 2025-16-8
 * @author Pham Cao Duy
 *********************************************************
 ******************/
#ifndef USERNODE_H
#define USERNODE_H
#include "UserData.h"

/**
 * @brief Trạng thái xác định kiểu lựa chọn sắp xếp theo tên hoặc sdt 
 * 
 * Enum này dùng để quản lý việc lựa chọn 
 * Phạm vi sử dụng: Module AddNode.c và BuildTree.c
 */
typedef enum{
     /** 
     * @brief giá trị đại diện cho sắp xếp theo tên
     */
    SORT_NAME,
     /** 
     * @brief giá trị đại diện cho sắp xếp theo sdt
     */
    SORT_PHONE
}SortType;

/*
 * Định nghĩa cấu trúc UserNode lưu trữ các node của linked list
 * + user : thông tin của node 
 * + next_user : đối tượng UserNode kế tiếp
 */
typedef struct UserNode{
    struct UserNode* next; 
    UserData value;                  
}UserNode;
#endif