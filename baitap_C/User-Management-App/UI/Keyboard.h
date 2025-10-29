/********************************************************
 *******************
 * @file Keyboard.h
 * @brief Khai báo các hàm để nhập dữ liệu từ bàn phím
 * @details File này cung cấp giao diện cho việc nhập giá trị số và chuỗi ký tự
 * @version 1.0
 * @date 2025-16-8
 * @author Pham Cao Duy
 *********************************************************
 ******************/
#ifndef KEYBOARD_h
#define KEYBOARD_H
#include "StdTypes.h"
/**
 * @brief       Đọc chuỗi ký tự nhập từ bàn phím
 * @param str   chuỗi ký tự do người dùng nhập
 * @retval      chuỗi mà người dùng nhập
 */
char* UI_InputString();
/**
 * @brief       Đọc giá trị số nguyên nhập từ bàn phím
 * @retval  giá trị só nguyên mà người dùng nhậps
 */
int UI_InputChoice();
/**
 * @brief       Hiển thị thông tin dựa trên chuỗi truyền vào
 * @param str   chuỗi ký tự do người dùng nhập
 * @retval      none
 */
void UI_ShowMessage(const char* msg);

#endif