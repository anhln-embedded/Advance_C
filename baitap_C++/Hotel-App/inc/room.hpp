#ifndef __ROOM_HPP
#define __ROOM_HPP
#include "Std_Types.hpp"

//enum mô tả định dạng cho trạng thái của danh sách các phòng được khởi tạo ban đầu khi chạy chương trình
typedef enum{
    Unavailable, //chưa được thêm bởi quản lý
    Available    //đã được thêm bởi quản lý
}default_room_status;

//enum mô tả định dạng cho trạng thái của danh sách các phòng đã thêm bởi quản lý
typedef enum
{
    Empty,      //còn trống
    Reserved    //đã đặtđặt
}available_roomstatus;

typedef int room_number; 
typedef map<room_number,available_roomstatus> room_available_dtype; //định nghĩa kiểu dữ liệu cho phòng được thêm
typedef map<room_number,default_room_status> room_default_dtype;    //định nghĩa kiểu dữ liệu cho phòng được khởi tạo ban đầu


class Room
{
private:
    room_available_dtype room_available;
    room_default_dtype room_default;
public:
    //hàm tạo để thêm phòng bởi manager
    Room(const room_available_dtype& room_available) : room_available(room_available){}
    //trả về danh sách phòng đã thêm 
    room_available_dtype getRoomAvailable() const {return room_available;} 
    //thay đổi trạng thái phòng được gọi bởi employee khi đặt hoặc trả phòng cho khách 
    void CheckInRoom(const int& number){room_available[number] = Reserved;}
    void CheckOutRoom(const int& number){room_available[number] = Empty;}
    
};
#endif