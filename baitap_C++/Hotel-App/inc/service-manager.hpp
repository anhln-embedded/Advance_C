#ifndef __SERVICEMANAGER_HPP
#define __SERVICEMANAGER_HPP
#include "service.hpp"
#include "UI.hpp"
#include <iomanip>
#define SERVICE_EXIST     0
#define SERVICE_NOT_EXIST 1

class ServiceManager{
    private:
        bool IsServiceExist(const service_option& name_service);
    public:
        bool AddService(const int& service_number,const int& price);
        bool deleteService(const int& name_service);
        bool ShowListService();
};
extern vector<Service> list_service;   //danh sách dịch vụ quản lý bởi manager
extern vector<string> service_description; //danh sách mô tả dịch vụ
#endif