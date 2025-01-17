#include "..//inc//ecu.hpp"
#define MAX_TEMP     100
#define MAX_SPEED    6000
#define MAX_SAFE_TEMP 90


/* SUBJECT */
void Engine::addObserver(Observer* new_ecu){
    list_ecu.push_back(new_ecu);
}
void Engine::removeObserver(Observer* delete_ecu){
    vector<Observer*>::iterator it;
    for(it = list_ecu.begin() ; it != list_ecu.end() ; it++){
        if(*it == delete_ecu){
            list_ecu.erase(it);
            break;
        }
    }
}
void Engine::notifyObservers(){
    getState();
    for(auto observer : list_ecu)
        observer->update(update_speed,update_temp);
}
void Engine::setEngineState(){
    srand(time(0));
    update_speed = rand() % (MAX_SPEED + 200);
    update_temp = rand() % (MAX_TEMP + 200);
    notifyObservers();
}
void Engine::getState(){
    cout << "current speed: " << update_speed << " km/h\t";
    cout << "current temp: " << update_temp << " degree celsius" << endl;
}

/* CONCREATE OBSERVER */

void CoolingSystem::update(int speed,float temp){
    if(temp > MAX_SAFE_TEMP){
        cout << "Fan ON -> cool down engine, current temp: " << temp <<" degree celcius" << endl;
    }
    else cout << "Fan OFF" << endl;
}
void WarningSystem::update(int speed,float temp){
    if(temp > MAX_TEMP){
        cout << "WARNING -> temperature exceeds 100 degree celsius" << endl;
    }

    else if(speed > MAX_SPEED){
        cout << "speed exceeds 6000 RPM" << endl;
    }
    else{
        cout << "temperature and speed are normal " << endl;
    }
}
void EngineControlUnit::update(int speed,float temp){
    if(speed > MAX_TEMP){
        cout << "lower fuel" << endl;
    }
    else{
        cout << "increase fuel" << endl;
    }
}
void FuelInjectionSystem :: update(int speed , float temp){
    float k_speed = (float)(1 - (float)((speed / 6000)));
    float k_temp =  (float)(1 - (float)((temp / 100)));
    float fuel_level = 100 * k_speed * k_temp;
    
    if(fuel_level > 100.0f)        fuel_level = 100.0f;
    else if(fuel_level < 0)        fuel_level = 0;

    if(speed < MAX_SPEED){
        cout << "increasing fuel amount: " << fuel_level << "%" << endl;
    }
    else
        cout << "decreasing fuel amount: " << fuel_level << "%" << endl;
}

