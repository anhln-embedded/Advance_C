#include"..//inc//ecu.hpp"
#define MAX_RPM         6000
#define WARNING_TEMP    100
EngineControlUnit*  EngineControlUnit :: Instance = NULL;

                                        /* PUBLIC INTERFACE */
void EngineControlUnit::display_ECU(){
    cout <<"current speed: " << getEngineSpeed() << "km/h\tcurrent temp: " << getEngineTemperature() << " degree celsius" << endl;
}
void EngineControlUnit::diagnostics_ECU(){
    cout << "======DIAGNOSTIC ECU======"<< endl;
    if(dataRead(PATH) == FAIL){
        cout << "fail to read datalog history" << endl;
        return;
    }
}
void EngineControlUnit::DataRecord_ECU(){
    if((dataRecord(PATH,speed_history,temp_history)) == FAIL){
        cout << "fail to save data" << endl;
        return;
    }
}
void EngineControlUnit::readsensor_ECU(){
    srand(time(0));      
    float temp = rand() % 150;
    int speed = rand() % 6100; 
    setEngineTemperature(temp);
    setEngineSpeed(speed);
    setFuelInjectionRate();
    brakeControlInteraction();
    if(isOverheadting())
        cout << "WARNING => Engine is overhead -> exceeds 100 degree celsius" << endl;
    
}

                                                /* PRIVATE INTERFACE */
void EngineControlUnit::setEngineSpeed(int speed){
    update_speed = speed;
    speed_history.push_back(speed);
    if(speed > MAX_RPM){
        cout << "warning -> speed must be lower than 6000 RPM" << endl;
    }
}
int EngineControlUnit::getEngineSpeed(){
    return update_speed;
}
void EngineControlUnit::setEngineTemperature(float temp){
    update_temp = temp;
    temp_history.push_back(temp);
    if(temp > 120 || temp < -20){
        cout << "warning -> temperature must be within -20 to 120 degree celsius" << endl;
    }
}
float EngineControlUnit::getEngineTemperature(){
    return update_temp;
}
bool EngineControlUnit::isOverheadting(){
    if(update_temp > WARNING_TEMP)
        return true;
    return false;
} 

void EngineControlUnit::setFuelInjectionRate(){
    int current_speed = getEngineSpeed();
    //speed factor reflects the increase fuel level amount as the car speeds up
    float k_speed = (float)(1 - (float)((this->update_speed / 6000)));
    float k_temp =  (float)(1 - (float)((this->update_temp / 100)));
    float fuel_level = 100 * k_speed * k_temp;
    
    if(fuel_level > 100.0f)        fuel_level = 100.0f;
    else if(fuel_level < 0)        fuel_level = 0;

    if(current_speed < MAX_RPM){
        cout << "increasing fuel amount: " << fuel_level << "%" << endl;
    }
    else
        cout << "decreasing fuel amount: " << fuel_level << "%" << endl;
}
void EngineControlUnit::brakeControlInteraction(){
    double brake_level = (double)(100 -  (double)((this->update_speed / 6000))*100);
    if(brake_level > 100.0f) brake_level = 100.0f;
    else if(brake_level < 0)   brake_level = 0;
    cout << "Brake level at: " << brake_level <<"%" << endl; 
}  