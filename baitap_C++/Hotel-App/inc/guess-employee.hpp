#ifndef __GUESSEMPLOYEE_HPP
#define __GUESSEMPLOYEE_HPP
#include "guess.hpp"
#include "room-manager.hpp"
#include "service-manager.hpp"
#include "UI.hpp"
#include <ctime>
class GuessEmployee
{
private:
    Guess *findRoombyPhone(const string &phone);
    feedback_dtype GenerateRandomFeedback();
    string GenerateRandomService();
    void EraseGuessInfo(const int& room);
public:
    void ServiceFeedbackInfo(const Guess &guess);
    Guess *GuessInfo(const string &phone);
    bool BookRoom(const int &number, const string &name, const string &phone, const string &checkin);
    void UnbookRoom(Guess& guess,string& checkout);
    bool ShowListGuess();
    bool ShowListRoomAvailable();
    bool IsRoomAvailable(int room_number);
};
extern vector<Guess> list_guess; // danh sách thông tin khách (toàn cục)
#endif