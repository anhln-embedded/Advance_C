#ifndef ACCOUNT_HPP
#define ACCOUNT_HPP

#include "Std_Types.hpp"
class Account {
private:
    string username;  // Tên tài khoản
    string password;  // Mật khẩu
public:
    // Constructor mặc định và constructor có tham số
    Account(); //khởi tạo tài khoản cho manager
    Account(const string& username, const string& password);

    // Getter và Setter cho các thuộc tính
    string getUsername() const;
    string getPassword() const;

    void setPassword(const string& password);
    static bool VerifyManagerAccount(const string& password);
    // Kiểm tra nếu tài khoản đã tồn tại trong danh sách
    static bool accountExists(const vector<Account>& accountList, const string& username);

    // Phương thức static để đăng ký và đăng nhập
    static void registerAccount(vector<Account>& accountList, const string& username, const string& password);
    static bool login(const vector<Account>& accountList, const string& username, const string& password);

    static void showListAccount(); //only for test purpse
};

extern vector<Account> accountList; //biến toàn cục lưu trữ danh sách tài khoản nhân viên và quản lý sử dụng ở nhiều file

#define SUCCESS 1
#define FAIL   0
#endif // ACCOUNT_HPP
