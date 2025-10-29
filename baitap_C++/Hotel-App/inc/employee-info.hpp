#ifndef EMPLOYEE_HPP
#define EMPLOYEE_HPP

#include "Std_Types.hpp"
using namespace std;
//kiểu enum lưu trữ các định dạng ca làm
typedef enum
{
    none,
    morning,   // Sáng
    afternoon, // Chiều
    evening    // Tối
}session;

//kiểu enum lưu trữ các định dạng ngày trong tuần
typedef enum 
{
    Mon, // Thứ 2
    Tue, // Thứ 3
    Wed, // Thứ 4
    Thu, // Thứ 5
    Fri, // Thứ 6
    totalday
}dayinWeek;
typedef map<dayinWeek,vector<session>> workshift_dtype;


class Employee_Info{
private:
    string id_;  // ID tự động
    string name_;
    string phoneNumber_;
    string position_;
    string workShift_;
    workshift_dtype schedule;  
public:
    Employee_Info(const string& id, const string& name, const string& phoneNumber, const string& position)
        : id_(id), name_(name), phoneNumber_(phoneNumber), position_(position){
            workShift_ = "chưa được set";
            // Khởi tạo lịch làm việc với các ngày và giá trị mặc định
            for (int day = Mon; day < totalday; ++day)
            {
                schedule[static_cast<dayinWeek>(day)] = {}; //thời khóa biểu chứa danh sách các ngày và rỗng ca làm
            }
        }
    // Getters và setters
    string getId() const { return id_; }
    string getName() const { return name_; }
    string getPhoneNumber() const { return phoneNumber_; }
    string getPosition() const { return position_; }
    workshift_dtype getSchedule() const { return schedule; }
    string getWorkshift() const {return workShift_;}

    void setName(const string& name) { name_ = name; }
    void setPosition(const string& position) { position_ = position; }
    void setWorkShift(const string& workshift) {workShift_ = workshift;} 
    void setSchedule(const dayinWeek& day,const session& sess) 
    { schedule[day].push_back(sess); }
};


#endif // EMPLOYEE_HPP
