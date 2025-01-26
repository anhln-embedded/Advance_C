#include "..//inc//os.hpp"
int main()
{
    Engine EngineManager;

    CoolingSystem cooling;
    WarningSystem warning;
    EngineControlUnit ECU;
    TransmissionControlUnit transmission;
    FuelInjectionSystem Injection(&ECU);

    // subscribe to client for receiving notification
    EngineManager.addObserver(&cooling);
    EngineManager.addObserver(&warning);
    EngineManager.addObserver(&ECU);
    EngineManager.addObserver(&transmission);
    EngineManager.addObserver(&Injection);

    simulation(EngineManager, 250, 100);

    return 0;
}