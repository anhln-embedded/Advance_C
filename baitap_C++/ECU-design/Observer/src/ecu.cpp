#include "..//inc//ecu.hpp"

#define MAX_TEMP                120
#define MAX_RPM                 6000
#define WARNING_TEMP            90
#define WARNING_RPM             6000
#define MAX_PEDAL_APPLY         100
#define OPTIMAL_TEMP            85    // nhiệt độ lý tưởng
#define BASE_FUEL               10

Engine::Engine(){
    throttle_input = 0.0f;
    rpm = 0;
    temperature = OPTIMAL_TEMP;   
    cout << "ECU Đã được khởi tạo với các thông số mặc định" << endl;
}
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
        observer->update(rpm,temperature,throttle_input);
}
void Engine::generateRandomData(){
    this->rpm =  rand() % (MAX_RPM + 1);
    this->temperature = 40 + rand() % 81;
    this->throttle_input = rand() % (MAX_PEDAL_APPLY + 1);
}
void Engine::setEngineState(){
    generateRandomData();
    notifyObservers();
}
void Engine::getState(){
    cout << "tốc độ: " << rpm << " rpm\tnhiệt độ: " << temperature << " Độ C" << endl;
}
                                    /* CONCREATE OBSERVER */

void CoolingSystem::update(const int&,const float& temperature,const float&) {
    if(temperature > WARNING_TEMP){
        cout << "hệ thống làm mát đã bật" << endl;
    }
    else cout << "hệ thông làm mát đã tắt" << endl;
}
void WarningSystem::update(const int& rpm,const float& temperature,const float&){
    if(temperature > WARNING_TEMP){
        cout << "CẢNH BÁO NHIỆT ĐỘ VƯỢT MỨC AN TOÀN" << endl;
    }

    else if(rpm > WARNING_RPM){
        cout << "CẢNH BÁO TỐC ĐỘ QUÁ LỚN" << endl;
    }
}
void EngineControlUnit::update(const int& rpm,const float& temperature,const float& throttle_input) {
    float fuel_rate_adjusted = calculateFuelInjectionRate(rpm,temperature,throttle_input);
    float Power = calculateEnergyOutput(rpm,temperature);
    float efficiency = calculateEfficiency(Power,fuel_rate_adjusted);

    //cout << "throttle_input: " << throttle_input << " %" << endl;
    cout << "Mức nhiên liệu hiệu chỉnh: " << fuel_rate_adjusted << " %" << endl;
    cout << "hiệu suất: " << efficiency << " %" << endl; 

}
void FuelInjectionSystem::update(const int&,const float&,const float&){
    float read_fuel = ECUbase->getFuelRate();
    cout << "phun nhiên liệu với";
    if(read_fuel < 30)  cout << " công suất nhỏ";
    else if(read_fuel >= 30 && read_fuel < 60) cout << " công suất trung bình";
    else cout << " công suất lớn";
    cout << " ở mức nhiên liệu " << read_fuel << " %" << endl;
}
void TransmissionControlUnit::update(const int& rpm,const float& ,const float&){
    Gear gear = getGearForRpm(rpm);
    cout << "Điều chỉnh hộp số tự động -> Gear:";
    switch (gear)
    {
    case Gear::NEUTRAL:
      cout << " Neutral";
        break;
    case Gear::FIRST:
      cout << " First";
        break;
    case Gear::SECOND:
      cout << " Second";
        break;
    case Gear::THIRD:
      cout << " Third";
        break;
    case Gear::FOURTH:
      cout << " Fourth";
        break;
    case Gear::FIFTH:
      cout << " Fifth";
        break;
    case Gear::SIXTH:
      cout << " Sixth";
        break;
    }
    cout << endl;
}

float EngineControlUnit::calculateFuelInjectionRate(const int& rpm ,const float& temperature,const float& throttle_input){
    float k_rpm = 0.0f , k_temp = 0.0f;
    //lambda để cài đặt các hệ số tốc độ và nhiệt độ ảnh hưởng tới điều chỉnh mức nhiên liệu
    auto AdjustFactor = [=](float& k_rpm,float& k_temp){
           //điều chỉnh hệ số nhiên liệu dựa trên tốc độ
        if(rpm >= 1500 && rpm <= 3000){
            k_rpm = 1.5f;  //tăng nhẹ đối với tốc độ vừa phải
        }
        else if(rpm <= 5000){
            k_rpm = 2.0f; //tăng mạnh đối với tốc độ cao
        }
        else if(rpm > 5000){
            k_rpm = 2.5f;
        }
        //điều chỉnh hệ số nhiên liệu dựa trên nhiệt độ
        if(temperature < OPTIMAL_TEMP){
            k_temp = 1.2f; //tăng mức nhiên liệu khi nhiệt độ dưới mức lý tưởng
        }
        else if(temperature > WARNING_TEMP){
            k_temp = 0.8f; //giảm mức nhiên liệu khi nhiệt độ quá cao
        }
    };
    
    AdjustFactor(k_rpm,k_temp);
    
    float fuel_rate = throttle_input + k_rpm * (rpm /MAX_RPM) + k_temp * (temperature / MAX_TEMP);
    
    if(fuel_rate < BASE_FUEL) fuel_rate = BASE_FUEL;
    setFuelRate(fuel_rate);
    return fuel_rate;
}
float EngineControlUnit::calculateEnergyOutput(const int& rpm,const float& temperature){
    //tính toán mo-men xoắn ở các giá trị rpm khác nhau
    auto torque = [](const int& rpm){
        #define MAX_TORQUE 300
        if (rpm <= 3000) { // Dưới 50% maxRPM, mô-men xoắn tăng dần
            return MAX_TORQUE * (0.5 + 0.5 * (rpm / 3000.0));
        } else { // Sau 50% maxRPM, mô-men xoắn giảm dần
            return MAX_TORQUE * (1.0 - 0.5 * ((rpm - 3000.0) / (6000 - 3000.0)));
        }
    };
    //tính toán tổng thất năng lượng ở các mức tốc độ và nhiệt độ
    auto loss_energy = [](const int& rpm,const float& temperature,const float& raw_energy){
        //he so ton that do ma sat
        float friction_loss_factor = 0.1f + (rpm/MAX_RPM) * 0.05f;
        //he so ton that nhiet
        float thermal_loss_factor = 0.3f + (temperature / 120.0f) * 0.2f;
        //he so ton that bom
        float pumping_loss_factor = 0.05f + ((MAX_RPM - rpm) / MAX_RPM) * 0.05f;
        //ton that nang luong
        float sum_factor = friction_loss_factor + thermal_loss_factor + pumping_loss_factor;

        //giới hạn giá trị hệ số tổng tiêu hao năng lượng
        if(sum_factor > 1.0f) sum_factor = 1.0f;
        return sum_factor*raw_energy;
    };
    
    //Công suất đầu ra chưa tính hao phí 
    float raw_energy = (torque(rpm) * rpm)/ 5252; 
    float loss = loss_energy(rpm,temperature,raw_energy);
        
    
    //giới hạn giá trị năng lượng tiêu hao trong mức an toàn
    if(raw_energy < loss) raw_energy = loss;

    return raw_energy - loss;  // Công suất đầu ra thực tế sau khi loại bỏ hao phí
}
float EngineControlUnit::calculateEfficiency(const float& Power,const float& input_energy){
    if(input_energy == 0) return 0;
    return (Power / input_energy) * 100; //Hiệu suất % 
}

Gear TransmissionControlUnit::getGearForRpm(const int& rpm)
{
    //bản đồ ánh xạ giá trị tốc độ tương ứng với các số tương ứng
    const map<int, Gear> speedToGear = {
        {0, Gear::NEUTRAL},
        {1000, Gear::FIRST},
        {2000, Gear::SECOND},
        {3000, Gear::THIRD},
        {4000, Gear::FOURTH},
        {5000, Gear::FIFTH},
        {6000, Gear::SIXTH} // Giá trị lớn nhất
    };
    //tìm kiếm và trả về giá trị enum biểu diển cho tốc độ
    for(const auto& it : speedToGear){
        if(rpm <= it.first){
            return it.second;
        }
    }
    return Gear::SIXTH;
}


