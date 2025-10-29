#ifndef __EMPLOYEE_HPP
#define __EMPLOYEE_HPP
#include "file-handle.hpp"
#include "Menu.hpp"
#include <cstdlib>

//lớp xây dựng các hàm tương tác giữa nhân viên và các chức năng hệ thống
class Employee
{
public: 
    Employee();
    void ShowEmployeeMenu(const string& user_name);
private:
    File_Handle file_Employee;
    GuessEmployee guessEmp;
    void ReviewWorkshift(const string& user_name);
    void EditInfoEmployee(const string& user_name);
    void BookRoom();
    void UnbookRoom();
    void ShowRoom();
    void SaveGuessInfo();

    string ReturnPosition(const string& user_name);

};
#endif