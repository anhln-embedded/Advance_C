#ifndef EMPLOYEEMANAGER_HPP
#define EMPLOYEEMANAGER_HPP

#include "Employee-info.hpp"
#include "Account.hpp"
#include "UI.hpp"
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <cstdlib> // Cần cho hàm rand và srand
#include <ctime>   // Cần cho hàm time nếu muốn tạo seed ngẫu nhiên
using namespace std;
class EmployeeManager {
private:
    int employeeCounter_ = 0;  // Biến đếm số lượng nhân viên để tạo ID tự động

    // Tạo ID tự động cho nhân viên mới
    string generateEmployeeId(const string& position);
    
    // Tìm nhân viên theo tên và sdt
    Employee_Info* findEmployeeById(const string& id);
    static Employee_Info* findEmployeeByPhone(const string& user_name);

    // cài đặt ca làm từ chuỗi nhập từ bàn phím -> hàm hỗ trợ cho setWorkShift
    bool setWorkshiftfromString(Employee_Info& employee,const string& workshift);
public:
    // thêm nhân viên mới với ID tự động
    bool addEmployee(vector<Account>& accountList,const string& name,const string& phoneNumber,const string& position);

    // Sửa thông tin nhân viên dựa theo ID
    void editEmployeeById(const string& id, const string& newName,string& newPosition);
    
    // Xóa nhân viên dựa trên ID
    void deleteEmployeeById(const string& id);
    
    // Set ca làm việc cho nhân viên
    void setWorkShift(const string& id, const string& shift);
    
    // Xem danh sách thông tin của tất cả nhân viên
    void listEmployees() const;
    void ShowWorkshiftTable() const;

    // 2 method sau được sử dụng trong employee.cpp
    static bool editEmployeePassword(vector<Account>& accountList,const string& user_name,const string& old_pass,const string& new_pass);
    static void ShowWorkshiftTablebyPhone(const string& user_name);
};
extern vector<Employee_Info> list_employee;


#endif // EMPLOYEEMANAGER_HPP
