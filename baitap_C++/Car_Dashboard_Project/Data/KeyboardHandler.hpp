#ifndef KEYBOARD_HANDLER_HPP
#define KEYBOARD_HANDLER_HPP

#include "DatabaseHandler.hpp"
#include <unordered_map>
#include <unordered_set>
#include <thread>
#include <atomic>
#include <iostream>

class KeyboardHandler {
private:
    DatabaseHandler& dbHandler; // Tham chiếu đến đối tượng DatabaseHandler để ghi dữ liệu
    std::unordered_map<int, SystemAttribute> keyMapping; // Bản đồ ánh xạ các phím với các thuộc tính trong Database

    // Trạng thái chạy của vòng lặp bàn phím
    std::atomic<bool> isRunning;

    // Hàm kiểm tra trạng thái bàn phím và ghi dữ liệu
    void keyboardListener();

    int lastPressedKey; // Lưu trữ phím đang được nhấn
    std::unordered_set<int> activeKeys; //Lưu trữ danh sách các phím đang được nhấn giữ

public:
    // Constructor
    KeyboardHandler(DatabaseHandler& db);
    
    // Destructor để dừng listener khi đối tượng bị hủy
    ~KeyboardHandler();

    // Hàm khởi chạy listener để ghi nhận sự kiện bàn phím
    void start();

    // Hàm dừng listener
    void stop();
};

#endif // KEYBOARD_HANDLER_HPP
