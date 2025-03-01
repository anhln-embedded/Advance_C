#include "KeyboardHandler.hpp"
#include <iostream>
#include <thread>
// #include <termios.h>
#include <unistd.h>
#include <conio.h> // Thay thế cho <termios.h> trong môi trường Windows
#include <algorithm>
// Constructor
KeyboardHandler::KeyboardHandler(DatabaseHandler &db) : dbHandler(db), isRunning(false)
{
    keyMapping = {
        {72, SystemAttribute::UP},
        {80, SystemAttribute::DOWN},
        {77, SystemAttribute::RIGHT},
        {118, SystemAttribute::V}, 
        {98, SystemAttribute::B},   
        {32, SystemAttribute::SPACE},
        {13, SystemAttribute::ENTER}, // '\n' cho phím Enter trên macOS
        {110, SystemAttribute::N},    
        {109, SystemAttribute::M}};   
    // đặt trạng thái ban đầu của phím cuối cùng được nhấn
    lastPressedKey = -1;
}

// Destructor
KeyboardHandler::~KeyboardHandler()
{
    stop();
}

// Bắt đầu lắng nghe bàn phím
void KeyboardHandler::start()
{
    isRunning = true;
    /*
        Khi tạo một luồng với hàm thành viên,
        cú pháp bao gồm
        + con trỏ đến hàm
        + con trỏ đến đối tượng sở hữu nó.
     */
    std::thread(&KeyboardHandler::keyboardListener, this).detach();
}

// Dừng lắng nghe bàn phím
void KeyboardHandler::stop()
{
    isRunning = false;
}

// Hàm lắng nghe bàn phím

void KeyboardHandler::keyboardListener()
{
    //test only 
    /* auto getkeyName = [](int ch)
    {
        string name;
        if (ch == 72)
            name = "Up";
        else if (ch == 80)
            name = "Down";
        else if (ch == 77)
            name = "Right";
        else if (ch == 118)
            name = "v";
        else if (ch == 98)
            name = "b";
        else if (ch == 32)
            name = "space";
        else if (ch == 13)
            name = "enter";
        else if (ch == 110)
            name = "n";
        else if (ch == 109)
            name = "m";
        return name;
    }; */
    while (isRunning)
    { 
        // kiểm tra nếu có phím nào đó được nhấn
        if (_kbhit())
        {
            int ch = _getch(); // Đọc phím từ bàn phím
            // Kiểm tra phím đặc biệt (mũi tên)
            if (ch == 0 || ch == 224)
            {
                ch = _getch(); // Đọc thêm một ký tự để xác định phím mũi tên
            }
            // kiểm tra phím đã nhấn có trong bản đồ lưu trữ các phím ban đầu
            if (keyMapping.find(ch) != keyMapping.end())
            {
                // kiểm tra phím đã nhấn có được cập nhật chưa -> tránh in ra thông báo liên tục nếu đang giữ phím và thêm lại cùng 1 phím vào danh sách lưu trữ nhiều lần
                if (ch != lastPressedKey)
                {
                    activeKeys.insert(ch); // Thêm phím đang nhấn vào danh sách -> dùng để xác nhận phím đang nhấn sau này
                    lastPressedKey = ch;   // Lưu lại phím đã nhấn
                    dbHandler.setData(keyMapping[ch], 1);
                    //cout << "đã nhấn phím " << getkeyName(ch) << endl;
                }
            }
            else
                //cout << "Phím không có sẵn" << endl;

            // kiểm tra phím có đang giữ hay không
            if (lastPressedKey != -1)
            {
                //cout << "đang giữ phím " << getkeyName(lastPressedKey) << endl;
                std::this_thread::sleep_for(std::chrono::milliseconds(150)); //cập nhật với chu kỳ 200 ms nếu đang giữ phím
            }
        }

        // Nếu không có phím nào mới được nhấn (thà phím) -> reset trạng thái và xóa phím đã nhấn
        else
        {
            // kiểm tra có phím đã nhấn nào lưu trữ trong danh sách không
            if (!activeKeys.empty())
            {
                //xử lý tránh trường hợp dội phím
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
                if(!_kbhit()){
                    activeKeys.erase(find(activeKeys.begin(), activeKeys.end(), lastPressedKey), activeKeys.end());
                    dbHandler.setData(keyMapping[lastPressedKey], 0); // cập nhật xóa trạng thái phím trên server
                    //cout << "đã xóa phím " << getkeyName(lastPressedKey) << " ra khỏi danh sách đang nhấn" << endl;
                    lastPressedKey = -1; // xóa phím đã nhấn trước dó
                }
            }
            //cout << "chưa có phím được nhấn" << endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100)); //cập nhật với chu kỳ 100 ms để chờ người dùng nhấn phím
        }
    }
}