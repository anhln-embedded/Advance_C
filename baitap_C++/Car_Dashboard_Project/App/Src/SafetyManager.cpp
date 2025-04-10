#include "SafetyManager.hpp"
#include <iostream>
#define MAX_PEDAL   100
#define MIN_PEDAL   0
SafetyManager::SafetyManager(){
    gasIntensity = 0,brakeIntensity = 0;
    cout << "Khởi tạo thành công hệ thống quản lý an toàn" << endl;
}
bool SafetyManager::checkBrakeAndAccelerator(bool isAccelerating, bool isBraking){
    //kiểm tra phanh và gas có đang nhấn cùng lúc không
    if(isAccelerating && isBraking){
        applyBrake();
        return true; //trả về trạng thái cho biết gas và phanh đang nhấn
    }
    return false;
}
void SafetyManager::applyBrake(){
  brakeIntensity = min(brakeIntensity + 2,MAX_PEDAL);
  gasIntensity = MIN_PEDAL;
}
void SafetyManager::releaseBrake(){
    brakeIntensity = max(MIN_PEDAL,brakeIntensity - 2);
}
void SafetyManager::applyGas(){
    gasIntensity = min(gasIntensity + 1,MAX_PEDAL);
    brakeIntensity = MIN_PEDAL;
}
void SafetyManager::releaseGas(){
    gasIntensity = max(MIN_PEDAL,gasIntensity - 2);

}

