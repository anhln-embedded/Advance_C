/********************************************************
 *******************
 * @file Menu.h
 * @brief Khai báo các macro variadic để tạo menu tự động
 * @details File này cung cấp giao diện cho việc xây dụng menu nhanh chóng và hiệu quả
 * @scope   Public API – Có thể include từ các module khác.
 * @version 1.0
 * @date 2025-16-8
 * @author Pham Cao Duy
 *********************************************************
 ******************/
#ifndef MENU_H
#define MENU_H
#include <stdio.h>

//macro thay thế cho hàm in chuỗi chứa tiêu đề và đề mục
#define PRINT_MENU_ITEM(number, item) printf("%d. %s\n", number, item)

//macro variadic tự động in ra các chuỗi mà người dùng nhập vào
#define PRINT_MENU(...)                             \
    do {                                            \
        const char* items[] = {__VA_ARGS__};        \
        int n = sizeof(items) / sizeof(items[0]);   \
        for (int i = 0; i < n; i++) {               \
            PRINT_MENU_ITEM(i + 1, items[i]);       \
        }                                           \
    } while (0)
//macro thay thế cho các case tùy chọn hàm xử lý, được gọi trong macro HANDLE_OPTION
#define CASE_OPTION(number, function) case number: function(); break;

//macro variadic tự động xử lý danh sách các macro CASE_OPTION 
#define HANDLE_OPTION(option, ...)              \
    switch (option) {                           \
        __VA_ARGS__                             \
        default: printf("Invalid option!\n");   \
    }
#endif