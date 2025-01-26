#ifndef __FILE_HANDLE_HPP
#define __FILE_HANDLE_HPP
#include <stdio.h>
#include <string.h>
#include <cstdlib>
#include "Account.hpp"
#include "guess-employee.hpp"
#include "employee-manager.hpp"
#include "room-manager.hpp"
#include "service-manager.hpp"

#define GUESS_CSV_PATH ".//database//guess.csv"
#define ROOM_CSV_PATH ".//database//room.csv"
#define SERVICE_CSV_PATH ".//database//service.csv"
#define EMPLOYEE_CSV_PATH ".//database//employee.csv"


#define FILE_EMPTY 2
#define FILE_NOT_EMPTY 3


//enum lưu trữ định dạng loại dữ liệu sẽ lưu trữ
typedef enum
{
    GUESS_CSV,
    ROOM_CSV,
    SERVICE_CSV,
    EMMPLOYEE_CSV
}Storage_dtype;
class File_Handle
{
public:
    bool SaveData(const char *path, Storage_dtype type);
    int LogData(const char *path, Storage_dtype type);
    static bool Erase_CSV(); //only for test purpose
private:
    void SaveGuessInfo(FILE *);
    void SaveRoomInfo(FILE *);
    void SaveServiceInfo(FILE *);
    void SaveEmployeeInfo(FILE *);

    void LogGuessInfo(char *line);
    void LogRoomInfo(char *line);
    void LogServiceInfo(char *line);
    void LogEmployeeInfo(char *line);
};
#endif