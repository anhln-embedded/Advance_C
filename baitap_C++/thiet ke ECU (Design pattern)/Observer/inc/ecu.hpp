#include<iostream>
#include<cstdlib> // Cần cho hàm rand và srand
#include<ctime>   // Cần cho hàm time nếu muốn tạo seed ngẫu nhiên
#include<vector>
#include<stdint.h>
#include <map>
using namespace std;
class Observer{
    public:
        virtual void update(const int& rpm,const float& temperature,const float& throttle_position) = 0;
        virtual ~Observer(){}
};
class Engine{
    private:
        int rpm;
        float temperature;
        float throttle_input;
        vector<Observer*> list_ecu;
        void generateRandomData();
    public:
        Engine();
        void addObserver(Observer*);
        void removeObserver(Observer*);
        void notifyObservers();
        void setEngineState();
        void getState();
};
class CoolingSystem : public Observer{
    public:
        void update(const int&,const float& temperature,const float&) override;
};
class WarningSystem : public Observer{
    public:
        void update(const int& rpm,const float& temperature,const float&) override;
};
class EngineControlUnit : public Observer{
    private:
        float fuel_energy_intput;
        void setFuelRate(const float& fuel_rate){fuel_energy_intput = fuel_rate;}
        float calculateFuelInjectionRate(const int& rpm ,const float& temperature,const float& throttle_position);                         //tính toán mức điều chỉnh nhiên liệu
        float calculateEnergyOutput(const int& rpm,const float& temperature);            
        float calculateEfficiency(const float& Power,const float& input_energy); //tính toán hiệu suất
        

    public:
        // gọi bởi lớp FuelInjectionSystem để thực hiện hành động tưong ứng
        float getFuelRate(){return fuel_energy_intput;} //đọc mức nhiên liệu cài đặt
        void update(const int& rpm,const float& temperature,const float& throttle_position) override;
};
class FuelInjectionSystem : public Observer{
    private:
        EngineControlUnit* ECUbase;
    public:
        //FuelInjectionSystem();
        FuelInjectionSystem(EngineControlUnit* ECU) : ECUbase(ECU){}
        void update(const int&,const float&,const float&) override;
};

//enum biểu diễn các trạng thái vào số của xe
enum class Gear
{
    NEUTRAL, // Xe ở trạng thái trung lập
    FIRST,   // Số 1
    SECOND,  // Số 2
    THIRD,   // Số 3
    FOURTH,  // Số 4
    FIFTH,   // Số 5
    SIXTH    // Số 6 (nếu có)
};
class TransmissionControlUnit : public Observer{
    private:
        //hàm để lấy hệ số truyền động dựa trên tốc độ
        Gear getGearForRpm(const int& rpm);
    public:
        void update(const int& rpm,const float& ,const float&) override;
};