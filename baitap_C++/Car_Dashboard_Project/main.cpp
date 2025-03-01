#include <iostream>
#include <cstdint>
#include <chrono>
#include <thread>
#include <math.h>
using namespace std;
using namespace std::chrono;
int main(){
    int preSpeed = 212; //km/h
    float speed_ms = preSpeed/3.6f;
    int speed = round(speed_ms);
    cout << speed;
    return 0;
    while (1) {
        static steady_clock::time_point lastUpdate = steady_clock::now();
        auto now = steady_clock::now();
        duration<double> elapsed = now - lastUpdate;  // Chênh lệch thời gian

        double deltaT = elapsed.count();  // Thời gian trôi qua tính bằng giây

        if (deltaT >= 1.0) {  // Kiểm tra thời gian >= 1 giây
            cout << "1s..." << endl;
            lastUpdate = now;  // Cập nhật lại mốc thời gian
        }

        //this_thread::sleep_for(milliseconds(10)); // Nghỉ 10ms để tránh chạy quá nhanh
    }
    return 0;
}