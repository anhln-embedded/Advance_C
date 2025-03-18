#include "DashboardController.hpp"

#define EXIST 1
#define NOT_EXIST 0

DashboardController::DashboardController(){
    cout << "Khởi tạo thành công giao diện điều khiển" << endl;
}
void DashboardController::registerObserver(Observer* new_obs){
    //lambda kiểm tra observer đã đăng ký chưa
    auto IsObserverExist = [this,new_obs](vector<Observer*> observers){
        bool result = find(observers.begin(),observers.end(),new_obs) != observers.end();
        return result ? EXIST : NOT_EXIST;};
    if(IsObserverExist(observers) == NOT_EXIST){
        observers.push_back(new_obs);
    }
    else cout << "Observer đã tồn tại\n";
}
void DashboardController::removeObserver(Observer* del_obs){
    observers.erase(find(observers.begin(),observers.end(),del_obs),observers.end());
}
void DashboardController::updateData(const unordered_map<string,string>& newData){
    
    //trich xuat value tuong ung voi key -> luu tru vao trong cac thuoc tinh
    for(const auto& [key,value] : newData){
        if(key == "VEHICLE_SPEED")              speed = stoi(value);
        else if(key == "DRIVE_MODE")            driveMode = value;
        else if(key == "BATTERY_LEVEL")         batteryLevel = stoi(value);
        else if(key == "ROUTE_PLANNER")         remainingRange = stoi(value); 
        else if(key == "WIND_LEVEL")            windlevel = stoi(value);
        else if(key == "AC_CONTROL")            climateTemp = stoi(value);
        else if(key == "AC_STATUS")             AC_status = strToBool(value);
        else if(key == "ACCELERATOR")           IsAccelerating = strToBool(value);
        else if(key == "BRAKE")                 IsBraking = strToBool(value);
        else if(key == "TURN_SIGNAL")           turnSignal = value;
    }
    //thong bao data cap nhat den cac cam bien
    notifyObservers();
}
void DashboardController::notifyObservers() const{
    for(auto obs : observers){
        obs->update(speed,remainingRange,batteryLevel,climateTemp,windlevel,turnSignal,driveMode,IsBraking,IsAccelerating,AC_status);
    }
}