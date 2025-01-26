#ifndef __MANAGER_HPP
#define __MANAGER_HPP
#include "file-handle.hpp"
#include "Menu.hpp"
#include <cstdlib>

//lớp xây dựng các hàm để tương tác giữa quản lý và các chức năng hệ thống
class Manager
{
public:
    Manager();
    void ShowManagerMenu();
private:
    //đối tượng quản lý các method giúp hỗ trợ xây dựng các tính năng
    EmployeeManager employeeManage;
    RoomManager roomManage;
    ServiceManager serviceManage;
    File_Handle file_manager;

    void manageEmployee();
    void addEmployee();      // Thêm nhân viên
    void editEmployee();     // Sửa thông tin nhân viên
    void deleteEmployee();   // Xóa nhân viên
    void listEmployees();    // Liệt kê nhân viên
    void setWorkShift();  // set ca lam
    void TableSchedule();    // hien thi thoi gian lam viec


    void manageRoom();
    //tính năng quản lý phòng
    void AddRoom();
    void DeleteRoom();
    void ShowListRoom();

    void manageService();
    //tính năng quản lý dịch vụ
    void AddService();
    void DeleteService();
    void ShowListService();

    //tính năng ghi/đọc thông tin trên máy tính
    void SaveDataCSV();


};
#endif