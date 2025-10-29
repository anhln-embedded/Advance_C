#include "../inc/service-manager.hpp"
vector<string> service_description = {"khong su dung dich vu","tap gym mien phi","to chuc sinh nhat","cho thue xe","cham soc thu cung","dat do an","spa va massage"};
vector<Service> list_service;
bool ServiceManager::IsServiceExist(const service_option& option){
    for(auto& service : list_service){
        for(auto& service_ : service.getService()){
            if(service_.first == option)
                return SERVICE_EXIST;
        }
    }
    return SERVICE_NOT_EXIST;
}
bool ServiceManager::AddService(const int& service_number,const int& price){
    service_option option = static_cast<service_option>(service_number);
    if(IsServiceExist(option) == SERVICE_NOT_EXIST){
        list_service.emplace_back(option,price);
        return SUCCESS;
    }
    return FAIL;
}
bool ServiceManager::deleteService(const int& service_number){
    service_option option = static_cast<service_option>(service_number);
    for(auto& service : list_service){
        for(auto& service_ : service.getService()){
            if(service_.first == option){
                service.deleteService(option);
                return SUCCESS;
            }
        }
    }
    return FAIL;
}
bool ServiceManager::ShowListService(){
    if(list_service.empty()){    
        return FAIL;
    }
    cout << left << setw(20) << "ten dich vu" << setw(20) << "gia dich vu" << endl;
    // Dòng kẻ ngang
    cout << setfill('-') << setw(50) << "-" << endl;

    // Reset fill về mặc định (space)
    cout << setfill(' ');

    for(const auto& service : list_service){
        for(const auto& service_ : service.getService())
            cout << left << setw(20) << service_description[service_.first] << setw(2) << to_string(service_.second) << " $"  << endl;
    }
    return SUCCESS;
}