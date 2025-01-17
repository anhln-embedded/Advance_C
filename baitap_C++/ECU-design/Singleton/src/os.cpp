#include"..//inc//os.hpp"
static void delay_ms(uint32_t ms){
     // Storing start time
    clock_t start_time = clock();

    // looping till required time is not achieved
    clock_t desired_time = start_time + ms;
    while (clock() < desired_time);
}
void simulation(EngineControlUnit *ECU, uint32_t sample_period, uint32_t simlulation_time)
{
    cout << "CAR STARTS MOVING" << endl;
    while (simlulation_time--)
    {   cout<<"-------------"<<endl;
        ECU->readsensor_ECU();
        ECU->display_ECU();
        cout<<"-------------"<<endl;
        delay_ms(sample_period);
    }
    ECU->DataRecord_ECU();
    cout << "CAR HAS STOPPED" << endl;
}
