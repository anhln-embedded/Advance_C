#ifndef __ROOM_HPP
#define __ROOM_HPP
#include <iostream>
#include <map>
using namespace std;

typedef enum{
    Unavailable,
    Available
}default_room_status;

typedef enum
{
    Empty,
    Reserved
}available_roomstatus;

typedef int room_number;
typedef map<room_number,available_roomstatus> room_available_dtype;
typedef map<room_number,default_room_status> room_default_dtype;


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