/********************************************************
 *******************
 * @file ManageUser.h
 * @brief Khai báo các thư viện, kiểu dữ liệu chia sẻ chung cho toàn bộ hệ thống,
 *        Header này có thể được include bởi tất cả module 
 * @version 1.0
 * @date 2025-16-8
 * @author Pham Cao Duy
 *********************************************************
 ******************/
#ifndef STDTYPES_H
#define STDTYPES_H

#include<stdint.h>
#include<stdlib.h>
#include<stdio.h>
#include<string.h>

/**
 * @brief Trạng thái của hệ thống.
 * 
 * Enum này dùng để quản lý kết quả xử lý của các hàm trong hệ thồng
 * Phạm vi sử dụng: toàn bộ module
 */
typedef enum{
    
    /** 
     * @brief hàm xử lý thành công
     */
    E_OK,
    
    /** 
     * @brief hàm xử lý thất bại
     */
    NOT_OK
}Status;


#endif