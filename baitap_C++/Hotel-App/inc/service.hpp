#ifndef __SERVICE_HPP
#define __SERVICE_HPP
#include <iostream>
#include <map>
using namespace std;
typedef enum{
    NONE_SERVICE,GYM,BIRTHDAY_PARTY,CAR_RENT,PET_CARE,FOOD_ORDER,SPA_MASSAGE,TOTAL_SERVICE
}service_option;

typedef map<service_option,int> service_dtype; // enum : service option , float : price
class Service{
    private:
        service_dtype service;
    public:
        Service(const service_option& option,const int& price){
            service[option] = price;
        }
        service_dtype getService() const {return service;}
        void deleteService(const service_option& option){
            if(service.find(option) != service.end()){
                service.erase(option);
            }
        }
};
#endif