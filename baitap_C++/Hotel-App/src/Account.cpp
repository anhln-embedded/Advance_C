#include "../inc/Account.hpp"

// Định nghĩa biến accountList toàn cục
vector<Account> accountList;  // Chỉ định biến toàn cục ở đây

// Constructor mặc định
Account::Account(){
    accountList.emplace_back("admin","234598");
}

// Constructor có tham số
Account::Account(const string& username, const string& password)
    : username(username), password(password) {}

// Getter cho từng thuộc tính
string Account::getUsername() const {
    return username;
}

string Account::getPassword() const {
    return password;
}

// Setter cho từng thuộc tính

void Account::setPassword(const string& password) {
    this->password = password;
}

// Kiểm tra nếu tài khoản đã tồn tại trong danh sách

bool Account::accountExists(const vector<Account>& accountList, const string& username) {
        for (const auto& account : accountList) {
            if (account.getUsername() == username) {
                return true;
            }
        }
        return false;
    }

// Đăng ký tài khoản mới
void Account::registerAccount(vector<Account>& accountList, const string& username, const string& password) {
    Account newAccount(username, password);
    accountList.push_back(newAccount);
}

// Đăng nhập
bool Account::login(const vector<Account>& accountList, const string& username, const string& password) {
    for (const auto& acc : accountList) {
        if (acc.getUsername() == username && acc.getPassword() == password) {
            return true; // Đăng nhập thành công
        }
    }
    return false; // Đăng nhập thất bại
}
bool Account::VerifyManagerAccount(const string& password){
    auto manager_pass = accountList.begin();
    if((*manager_pass).getPassword() == password)
        return SUCCESS;
    else return FAIL;
}

void Account::showListAccount(){
    for(auto& acc : accountList)
        cout << "user_name: " << acc.getUsername() << "\tpassword: " << acc.getPassword() << endl;
}

