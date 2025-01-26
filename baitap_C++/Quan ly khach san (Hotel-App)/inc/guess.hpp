#ifndef __GUESS_HPP
#define __GUESS_HPP
#include "Std_Types.hpp"
using namespace std;

//enum lưu trữ các định dạng phản hồi của khách
typedef enum{
    NONE_FEEDBACK,
    NEGATIVE,
    POSITIVE,
    TOTAL_FEEDBACK
}feedback_selection;
typedef map<feedback_selection,string> feedback_dtype; //định nghĩa kiểu dữ liệu để lưu trữ phản hồi của khách
class Guess{
    private:
        int room;
        string name;
        string phone;
        string checkin;
        string checkout;
        feedback_dtype guess_feedback;
        string guess_service;
    public:
        //ham tao khoi tao du lieu cho khach dat phong
        Guess(const int& room,const string& name,const string& phone ,const string& checkin) : 
        room(room),name(name),phone(phone),checkin(checkin){
            guess_feedback[NONE_FEEDBACK] = "chua co danh gia";
            checkout = "khong co thong tin";
        } 
        void setCheckOut(string& guess_checkout) {checkout = guess_checkout;}
        void setService(string name_service){guess_service = name_service;}
        void setFeedback(feedback_dtype feedback){guess_feedback = feedback;}
        feedback_dtype getFeedback() const {return guess_feedback;}
        string getService() const {return guess_service;}
        string getName() const{return name;}
        string getPhone() const{return phone;}
        string getCheckin() const {return checkin;}
        string getCheckout() const {return checkout;}
        int getRoom() const {return room;}
};
#endif