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
    cout << "XE BÁT ĐẦU DI CHUYỂN" << endl;
    while(simlulation_time--)
    {   cout<<"-------------"<<endl;
        ECU->ECU_Read();
        ECU->brakeControlInteraction();
        ECU->setFuelInjectionRate();
        cout<<"-------------"<<endl;
        delay_ms(sample_period);
    }
    ECU->ECU_SaveData();
    cout << "XE ĐÃ DỪNG" << endl;
}
