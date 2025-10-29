/********************************************************
 *******************
 * @file UserApp.h
 * @brief Khai báo các hàm để xây dựng menu chức năng tương tác với người dùng
 * @details File này cung cấp giao diện cho việc xây dựng các tính năng chính của hệ thống,
 *          Header này chỉ nên được include bởi module hiện tại
 * @version 1.0
 * @date 2025-16-8
 * @author Pham Cao Duy
 *********************************************************
 ******************/
#ifndef USERAPP_H
#define USERAPP_H
#include "Menu.h"
#include "Keyboard.h"
#include "ManageDB.h"
#include "ManageUser.h"
#include "SearchUser.h"

typedef enum SystemEvent{
    INIT_SUCCES,
    INIT_FAIL,
    STOP,
    SEARCH_USER,
    LIST_USER,
}SystemEvent;
/**
 * @brief   Khởi tạo hệ thống.
 * 
 * @details Hàm thực hiện:
 *          - Kiểm tra trạng thái xử lý việc đọc file CSV.
 *          - Tạo danh sách liên kết (linked list).
 *          - Xây dựng cây nhị phân (binary tree).
 *          Sau đó trả về trạng thái khởi tạo.
 *
 * @param[in]  filename  Đường dẫn đến file CSV chứa dữ liệu người dùng.
 *
 * @return  SystemEvent
 *          - INIT_SUCCESS : Khởi tạo thành công.
 *          - INIT_FAIL    : Khởi tạo thất bại.
 */
SystemEvent ExecuteInitProgram(const char* filename);
/**
 * @brief   Hiển thị menu chính
 * 
 * @details Hàm thực hiện:
 *          - Hiển thị các lựa chọn
 *          - xử lý điều hướng luổng thực thi đến các menu con thông qua kết quả trả về
 * @retval STOP           : điều hướng đến trạng thái xử lý dừng chương trình
 * @retval SEARCH_USER    : điều hướng đến xử lý tìm kiếm user
 * @retval LIST_USER      : điều hướng đến xử lý in ra danh sách user 
 */
SystemEvent ShowMainMenu();
/**
 * @brief  Hiển thị giao diện xử lý kết thúc chương trình
 * @details Hàm thực hiện gọi ra các giao diện trừu tượng quá trình
 *            - xóa cây nhị phân tìm kiếm user theo tên và sdt
 *            - xóa danh sách liên kết sắp xếp theo tên và sdt
 *            - xóa dữ liệu user đã lưu trên bộ nhớ
 * @return void
 */
void ExecuteEndProgram();
/**
 * @brief  Hiển thị giao diện các tùy chọn hiển thị thông tin user
 * @details Hàm thực hiện gọi ra các giao diện trừu tượng quá trình
 *            - hiển thị danh sách thông tin user theo tên
 *            - hiển thị danh sách thông tin user theo sdt
 * @return void
 */
void ShowMenuListUser();
/**
 * @brief  Hiển thị giao diện các tùy chọn tìm kiếm thông tin user
 * @details Hàm thực hiện gọi ra các giao diện trừu tượng quá trình
 *            - hiển thị thông tin user tìm kiếm theo tên
 *            - hiển thị thông tin user tìm kiếm theo sdt
 * @return void
 */
void ExecuteSearchUser();

#endif