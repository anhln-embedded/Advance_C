#include"..//inc//os.hpp"
void delay_ms(size_t ms){
     // Storing start time
    clock_t start_time = clock();

    // looping till required time is not achieved
    clock_t desired_time = start_time + ms;
    while (clock() < desired_time);
}
void simulation(Engine& subject,size_t sample_period,uint8_t sample_time){
    cout << "Begin communication between OBSERVER and SUBJECT" << endl;
   
    while(sample_time-- > 0){
        cout << "-----------" << endl;
        subject.setEngineState();
        cout << "-----------" << endl;
        delay_ms(sample_period);
    }
    cout << "Communication has ended" << endl;
}
