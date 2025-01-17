#include "..//inc//os.hpp"
/* void RemoveECU(const string& ECU_name,Engine& Subject){
    string ecu_list[3] = {"cooling system","warning system","fuel injection system"};
    uint8_t ecu_index = 0;
    for(auto ecu : ecu_list){
        if(ECU_name == ecu)
            Subject.removeObserver()
    }
} */
int main()
{
    
    Engine EngineManager;

    CoolingSystem ECUcooling;
    WarningSystem ECUwarning;
    EngineControlUnit ECUfuelInjecttion;

    //subscribe to client for receiving notification 
    EngineManager.addObserver(&ECUcooling);
    EngineManager.addObserver(&ECUwarning);
    EngineManager.addObserver(&ECUfuelInjecttion);

    simulation(EngineManager,250,100);

    
   return 0;

}