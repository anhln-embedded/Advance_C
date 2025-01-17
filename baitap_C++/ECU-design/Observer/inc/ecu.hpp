#include<iostream>
#include<cstdlib> // Cần cho hàm rand và srand
#include<ctime>   // Cần cho hàm time nếu muốn tạo seed ngẫu nhiên
#include<vector>
#include<stdint.h>
using namespace std;
class Observer{
    public:
        virtual void update(int speed,float temperature) = 0;
        virtual ~Observer(){
            cout << "destructor for Observer is called" << endl;
        }
};
class Engine{
    private:
        int update_speed;
        float update_temp;
        vector<Observer*> list_ecu;
    public:
        void addObserver(Observer*);
        void removeObserver(Observer*);
        void notifyObservers();
        void setEngineState();
        void getState();
};
class CoolingSystem : public Observer{
    public:
        void update(int speed,float temperature) override;
};
class WarningSystem : public Observer{
    public:
        void update(int speed,float temperature) override;
};
class EngineControlUnit : public Observer{
    public:
        void update(int speed,float temperature) override;
};
class FuelInjectionSystem : public Observer{
    public: 
         void update(int speed,float temperature) override;
};