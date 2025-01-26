#ifndef MENUITEM_HPP
#define MENUITEM_HPP
#include "Std_Types.hpp"
#include <functional>

class MenuItem {
private:
    int choice_;
    std::string description_; //mô tả đề mục
    std::function<void()> action_; //lưu trữ hàm thực thi 
public:
    MenuItem(int choice, const std::string& description, std::function<void()> action)
        : choice_(choice), description_(description), action_(action) {}
    //method used in Menu.hpp
    int getChoice() const { return choice_; }
    std::string getDescription() const { return description_; }
    void executeAction() const { action_(); }
};

#endif // MENUITEM_HPP
