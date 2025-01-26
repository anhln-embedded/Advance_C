#ifndef UI_HPP
#define UI_HPP
#include "Std_Types.hpp"
class UI {
public:
    // Phương thức hiển thị và lấy dữ liệu đầu vào
    static int getUserChoice(const string& prompt);        // Lấy lựa chọn từ người dùng
    static float getUserChoiceFloat(const string& prompt);   
    static void showMessage(const string& message);        // Hiển thị thông báo
    static string getInputString(const string& prompt);    // Lấy chuỗi nhập từ người dùng
};

#endif // UI_HPP
