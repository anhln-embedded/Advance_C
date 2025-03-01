#include "VehicleConfig.hpp"

//cấp phát địa chỉ và gán thông số cài đặt ban đầu cho biến toàn cục lưu trữ thuộc tính của xe
Vehicle_Brand ElectricVehicle_Init::brand = Vehicle_Brand::NOT_SET;

Vehicle_Version ElectricVehicle_Init::version = Vehicle_Version::NOT_SET;

Vehicle_BaseParam ElectricVehicle_Init::initParam = {
        {vehicle_Attribute::BATTERY_CAPACITY,0},
        {vehicle_Attribute::BATTERY_VOLTAGE,0},
        {vehicle_Attribute::MAX_TORQUE,0},
        {vehicle_Attribute::MAX_AC_POWER,0},
        {vehicle_Attribute::MAX_ENGINE_POWER,0},
        {vehicle_Attribute::MAX_SPEED_SPORT,0},
        {vehicle_Attribute::MAX_SPEED_ECO,0},
        {vehicle_Attribute::MAX_RPM,0},
        {vehicle_Attribute::WEIGHT,0},
        {vehicle_Attribute::AC_TEMP_MAX,0},
        {vehicle_Attribute::AC_TEMP_MIN,0},
        {vehicle_Attribute::WIND_LEVEL_MAX,0},
        {vehicle_Attribute::ENGINE_TOTAL,0} 
}; 

//định nghĩa bản đồ lưu trữ thông số chi tiết cho mỗi phiên bản của xe tesla model 3
Vehicle_BaseParam TeslaModel3_Standard  = {
    {vehicle_Attribute::BATTERY_CAPACITY,54},
    {vehicle_Attribute::BATTERY_VOLTAGE,350},
    {vehicle_Attribute::MAX_RANGE,409},
    {vehicle_Attribute::MAX_TORQUE,300},
    {vehicle_Attribute::MAX_AC_POWER,2500},
    {vehicle_Attribute::MAX_ENGINE_POWER,211},
    {vehicle_Attribute::MAX_SPEED_SPORT,225},
    {vehicle_Attribute::MAX_SPEED_ECO,160},
    {vehicle_Attribute::MAX_RPM,16000},
    {vehicle_Attribute::WEIGHT,1612},
    {vehicle_Attribute::WHEEL_RADIUS,34},
    {vehicle_Attribute::AC_TEMP_MAX,28},
    {vehicle_Attribute::AC_TEMP_MIN,15},
    {vehicle_Attribute::WIND_LEVEL_MAX,5},
    {vehicle_Attribute::ENGINE_TOTAL,1}
    };
    
Vehicle_BaseParam TeslaModel3_LongRange  = {
    {vehicle_Attribute::BATTERY_CAPACITY,75},
    {vehicle_Attribute::BATTERY_VOLTAGE,350},
    {vehicle_Attribute::MAX_RANGE,560},
    {vehicle_Attribute::MAX_TORQUE,440},
    {vehicle_Attribute::MAX_AC_POWER,3000},
    {vehicle_Attribute::MAX_ENGINE_POWER,324},
    {vehicle_Attribute::MAX_SPEED_SPORT,233},
    {vehicle_Attribute::MAX_SPEED_ECO,190},
    {vehicle_Attribute::MAX_RPM,17000},
    {vehicle_Attribute::WEIGHT,1847},
    {vehicle_Attribute::WHEEL_RADIUS,35},
    {vehicle_Attribute::AC_TEMP_MAX,28},
    {vehicle_Attribute::AC_TEMP_MIN,15},
    {vehicle_Attribute::WIND_LEVEL_MAX,5},
    {vehicle_Attribute::ENGINE_TOTAL,2},
    };
    
Vehicle_BaseParam TeslaModel3_Performance  = {
    {vehicle_Attribute::BATTERY_CAPACITY,75},
    {vehicle_Attribute::BATTERY_VOLTAGE,350},
    {vehicle_Attribute::MAX_RANGE,530},
    {vehicle_Attribute::MAX_TORQUE,650},
    {vehicle_Attribute::MAX_AC_POWER,3500},
    {vehicle_Attribute::MAX_ENGINE_POWER,393},
    {vehicle_Attribute::MAX_SPEED_SPORT,261},
    {vehicle_Attribute::MAX_SPEED_ECO,210},
    {vehicle_Attribute::MAX_RPM,18000},
    {vehicle_Attribute::WEIGHT,1847},
    {vehicle_Attribute::WHEEL_RADIUS,36},
    {vehicle_Attribute::AC_TEMP_MAX,28},
    {vehicle_Attribute::AC_TEMP_MIN,15},
    {vehicle_Attribute::WIND_LEVEL_MAX,5},
    {vehicle_Attribute::ENGINE_TOTAL,2} 
    };
    
ElectricVehicle_Init::ElectricVehicle_Init(Vehicle_Version version,Vehicle_Brand brand){
    if(brand == Vehicle_Brand::TESLA){
        string version_name;
        this->brand = Vehicle_Brand::TESLA;
        //khởi tạo thông số tương ứng cho từng phiên bản
        if(version == Vehicle_Version::STANDARD){
            initParam = TeslaModel3_Standard;
            this->version = Vehicle_Version::STANDARD;
            version_name = "STANDARD";

        }
        else if(version == Vehicle_Version::LONG_RANGE){
            initParam = TeslaModel3_LongRange;
            this->version = Vehicle_Version::LONG_RANGE;
            version_name = "LONG_RANGE";
        }
        else{
            initParam = TeslaModel3_Performance;
            this->version = Vehicle_Version::PERFORMANCE;
            version_name = "PERFORMANCE";
        }
        cout << "Thông số cho dòng xe Tesla model 3 (" + version_name + ") đã được cập nhật\n";
    }
    else cout << "chưa có thông tin";
    /* 
        xử lý cho các dòng xe khác 
    */
}

//hàm chuyển đổi chuỗi thành boolean
bool strToBool(const std::string& str) {
    return (str == "1");
}