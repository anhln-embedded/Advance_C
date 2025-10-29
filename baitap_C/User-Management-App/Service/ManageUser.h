/**
 * @file ManageUser.h
 * @brief Khai báo các hàm để quản lý việc tổ chức thông tin user thành danh sách sắp xếp theo tiêu chí tìm kiếm 
 * @details File này cung cấp giao diện cho việc tạo ra danh sách liên kết chứa khối thông tin của từng user 
 *          Header này chỉ nên được include bởi module App
 * @version 1.0
 * @date 2025-16-8
 * @author Pham Cao Duy
**/
#ifndef MANAGEUSER_H
#define MANAGEUSER_H
#include "UserNode.h"
/**
 * @brief   Hàm in ra thông tin của toàn bộ user 
 *          lưu trữ trên danh sách sắp xếp theo tên hoặc sdt
 * @param[in] type    biến enum cho biết định dạng cũa danh 
 *                    sách lưu trữ theo tên hoặc sdt sẽ in ra
 *                    tự động kiểm tra để xác định định dạng tìm kiếm
 * @retval  E_OK    Hàm xử lý thành công
 * @retval  NOT_OK  Hàm xử lý thất bại
 */
Status Print_ListUser(SortType type);
/**
 * @brief   Hàm xây dựng danh sách liên kết sắp xếp theo tên và sdt
 * @retval  E_OK    Hàm xử lý thành công
 * @retval  NOT_OK  Hàm xử lý thất bại
 */
Status Build_ListUser();
/**
 * @brief   Hàm xóa bỏ danh sách liên kết sắp xếp theo tên và sdt
 * @retval  E_OK    Hàm xử lý thành công
 * @retval  NOT_OK  Hàm xử lý thất bại
 */
Status Remove_ListUser();
#endif