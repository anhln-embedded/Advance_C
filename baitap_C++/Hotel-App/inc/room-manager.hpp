#ifndef __ROOMMANAGER_HPP
#define __ROOMMANAGER_HPP
#include "room.hpp"
#include "guess-employee.hpp"
#include "UI.hpp"
#include <vector>
#define SUCCESS 1
#define FAIL    0
#define EXIST       0
#define NOT_EXIST   1

class RoomManager{
    private:
        Guess* findguessbyRoom(const int& room);
        void Activate_Deactivate(const int& room,bool Action);
        bool EraseAvailableRoom(const int& room);
    public:
        RoomManager();  //khởi tạo các phòng của khách sạn ở trạng thái unavailble
        static bool IsRoomAvailableExist(const int& room_number);
        bool IsRoomDefaultExist(const int& room_number);
        bool AddRoom(const int& number);
        void deleteRoom(const int& number);
        bool RoomInfo(const int& room);
        void ShowListRoomDefault();
};
extern vector<Room> list_room_available; //danh sách các phòng đã thêm bởi manager
#endif