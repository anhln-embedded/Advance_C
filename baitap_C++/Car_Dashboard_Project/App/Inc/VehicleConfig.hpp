/* 
    + cung cấp các class và kiểu dữ liệu sử dụng cho toàn bộ hệ thống
    + cung cấp các thông số thuộc tính cho loại xe cụ thể  
    + cung cấp các hàm tính toán các thông số ảnh hưởng đến trạng thái hoạt động của các thành phần trong xe
*/
#ifndef VEHICLE_CONFIG
#define VEHICLE_CONFIG
#include <iostream>
#include <cstdint>
#include <map>
#include <string>
#include <mutex>
#include <atomic>
#include <thread>
#include <vector>
#include <future>
#include <chrono>
#include <ctime>
#include <algorithm>
#include <iomanip>
#include <unordered_map>
#include <cmath>

using namespace std;

//hàm chuyển đổi chuỗi thành boolean sử dụng ở nhiều file 
bool strToBool(const string& str);

//lớp xây dưng công thức tính toán các thông số đặc biệt ảnh hưởng đến việc điều khiển xe 
class VehicleCalculation {
    private:
    /*sử dụng constexpr 
        + tối ưu hóa hiệu suất 
        + đảm bảo các giá trị không bị thay đổi trong suốt thời gian chương trình chạy.
    */
    //các hệ số để tính toán lực ma sát lăn, lực cản gió, và hiệu suất
        static constexpr int gear_ratio = 9;                  //ty so truyen cua hop so xe dien           
        static constexpr float pi = 3.14;                     //hang so pi
        static constexpr float GR = 9.1;                      //ti so truyen cuoi cung 
        static constexpr float gravity = 9.81;                //gia toc trong truong m/s^2
        static constexpr float Cr = 0.011;                    //He so ma sat lan
        static constexpr float Cd = 0.23;                     //He so can khi dong
        static constexpr float Us = 0.013;                      //hệ số ma sát tĩnh tối thiểu lớn hơn hệ số cho ma sát lắn 
        static constexpr float Uk = 0.7;                      //hệ số ma sát động luôn nhỏ hơn us
        static constexpr float airdensity =  1.225;           //mat do khong khi kg/m^3
        static constexpr float efficiency_drivetrain =  0.95; //hieu suat truyen dong
        static constexpr float efficiency_engine =  0.9;      //hieu suat dong co dien
        static constexpr float Area = 2.22;                   //dien tich mat can truoc m^2
    //các hệ số để tính toán ảnh hưởng đến nhiệt độ pin
        static constexpr float Talpha = 0.01; //he so the hien muc do nhiet sinh ra do cong suat dong co (độ C / Kw)
        static constexpr float Tbeta = 0.15;   //he so the hien muc do lam mat anh huong den nhiet pin (độ c / Kw)
        static constexpr const int C_coolingBase = 1000; // hieu qua lam mat co ban (w)
        static constexpr const int k_cooling = 30;      // he so tang cuong lam mat (w/do c)
    //hệ số để tính tiêu hao do điều hòa
        static constexpr int deltaT_ac  = 20; //chênh lệch nhiệt độ lớn nhất mà điều hòa xử lý ổn định nhất
    
    
    //ma sát tĩnh tối thiểu
    static float getMinStaticFriction(const int& weight){
        float F_static_friction = Us * weight * gravity;  
        return F_static_friction;
    }
    
    //ma sát lăn
    static float getRollingFriction(const int& weight){
        float F_rolling =  Cr * weight * gravity;  
        return  F_rolling;  
    }
    
    //lực cản gió
    static float getAirDragForce(const float& speed_ms){
        return 0.5 * Cd * airdensity * Area * (speed_ms*speed_ms);      
    }
    
    //lực hãm từ hệ thống phanh
    static float getBrakeForce(const int& brakeLevel,const int& weight,const float& speed_ms){
        float F_maxBrake = 0.0f;    //lực hãm tối đa
        //chỉ khi xe di chuyển lực phanh với được sinh ra
        if(speed_ms > 0) F_maxBrake = weight * gravity * Uk; 
        else F_maxBrake = 0.0f;
        //cout << "F_BrakeMax: " << F_Static_friction << endl;
        return (brakeLevel/100.0f)*F_maxBrake;
    }
    public:
    //lực kéo từ động cơ
    static float getTractionForce(const int& wheel_radius,const int& current_Torque){
        float radius_m = wheel_radius/100.0f; //đổi ra mét
        float F_Traction = (float)(current_Torque * gear_ratio) / radius_m; //lực kéo tối đa 
        //cout << "F_tractionMax: " << F_Traction << endl;
        return F_Traction;
    }
        
    //gia tốc 
    static float getAcceleration(const float& speed_ms,const float& F_traction,const int& weight,const int& brakeLevel){
        float a = 0.0f;
        //float F_Static_Friction = getMaxStaticFriction(weight);
        float F_static_friction = getMinStaticFriction(weight);
        //cout << F_static_friction;
        //trường hợp xe đứng yên -> kiểm tra lực kéo cung cấp cho xe 
        if(speed_ms <= 0.0f){
            //nếu lực kéo < ma sát tĩnh cưc đại -> xe chưa thẻ chuyển động
            if(F_traction < F_static_friction){
                a = 0.0f;
            }
            else{
                float F_rolling = getRollingFriction(weight);
                float F_AirDrag = getAirDragForce(speed_ms);
                float F_brake = getBrakeForce(brakeLevel,weight,speed_ms);
                float F_total = F_traction - (F_brake + F_AirDrag + F_rolling);
                a = F_total / weight;
            }
        }
        //khi xe bắt đầu chuyển động -> chỉ cần duy trì lực kéo để vượt qua lực cản lăn
        else{
            float F_rolling = getRollingFriction(weight);
            float F_AirDrag = getAirDragForce(speed_ms);
            float F_brake = getBrakeForce(brakeLevel,weight,speed_ms);
            float F_total = F_traction - (F_brake + F_AirDrag + F_rolling);
            a = F_total / weight;
        }
        return a;
    }
        
    //momen xoan hien tai
    static  float getTorque(const int& rpm,const int& maxRpm,const int& gasLevel,const int& MaxTorque){
        int rpm_threshold = 6000;//giá trị ngưỡng rpm mà mo-men xoắn duy trì ở mức cực đại
        float torque = 0.0f;
        //xe điện có xu hướng tăng mo-men xoắn nhanh và đạt cực đại khi xe tăng tốc ở vòng tua thấp 
        if (rpm < rpm_threshold) {
            torque = MaxTorque;  // Giữ mô-men xoắn tối đa ở RPM thấp
        } 
        //khi vòng tua vượt ngưỡng nhất định, mo-men xoắn giảm dần để tăng công suất và duy trì tốc độ của xe
        else {
            torque = MaxTorque * (1.0f - ((float)(rpm - rpm_threshold) / (float)(maxRpm - rpm_threshold)));
        }
        return torque * ((float)gasLevel / 100.0f); //mức mo-men xoắn thực tế theo cường độ gas
    }
    
    //số vòng quay động cơ
    static int getRpm(const float& speed_ms,const int& wheel_radius,const int& maxRpm){
        float wheel_d = (wheel_radius*2)/100.0f;  //đường kính (m)
        int rpm =  static_cast<int>((speed_ms*GR*60.0f )/(pi*wheel_d));//số vòng quay hiện tại
        if(rpm > maxRpm) rpm = maxRpm;
        else if(rpm < 0) rpm = 0;
        return rpm;
    }
    
    //toc do goc cua dong co ras/s
    static float getAngularSpeed(const int& rpm){
        return (2.0f * pi * rpm) / 60.0f;
    }

    //công suất tiêu thụ do điều hòa -> đơn vị Watt
    static int getPowerAC(const int& env_temp,const int& desired_temp,const int& maxAcpower){
        int P_ac = 0;
        if(desired_temp == 0) P_ac = 0;
        else{
            int kac = maxAcpower / deltaT_ac;   //hệ số ảnh hưởng đến mức tiêu hao do điều hòa
            P_ac = kac * abs(env_temp - desired_temp);
        }
        return P_ac;
    }

    //công suất tiêu thụ do mức gió -> đơn vị Watt
    static int getPowerWind(const int& windlevel){
        if(windlevel == 0) return 0;
        else if(windlevel == 1) return 300; 
        else if(windlevel == 2) return 600;
        else if(windlevel == 3) return 900;
        else if(windlevel == 4) return 1200;
        else return 1500;
    }

    //công suất tiêu thụ của động cơ -> đơn vị Watt
    static double getPowerEngine(const float& Torque,const float& AngularSpeed){
        return (Torque * AngularSpeed)/efficiency_drivetrain;
    }

    //nhiet do pin
    static float getBatteryTemp(const float& previous_battery_temp,const float& Environment_temp,double& enginePower){
        //hieu qua lam mat -> watt
        double CoolingEfficiency = C_coolingBase + k_cooling * (previous_battery_temp - Environment_temp);
        //đổi ra kW
        CoolingEfficiency /= 1000.0f;
        enginePower /= 1000.0f;
        //cout << "\n+ Cooling Efficiency: " << CoolingEfficiency << endl;
        float current_battery_temp = Environment_temp + Talpha * enginePower - Tbeta * CoolingEfficiency; 
        return current_battery_temp;
    } 
};
//kiểu enum xác định phiên bản xe
enum class Vehicle_Version{
    STANDARD,
    LONG_RANGE,
    PERFORMANCE,
    NOT_SET
};
//kiểu enum xác định dòng xe
enum class Vehicle_Brand{
    VINFAST,
    TESLA,
    TOTOTA,
    HYUNDAI,
    MERCEDES,
    NOT_SET
};
//kiểu enum xác định thông số xe -> sử dụng để tính toán toán, điều chỉnh tốc độ,chế độ lái,mức pin,quãng đường đi được, và nhiều yếu tố khác
enum class vehicle_Attribute {
    ENGINE_TOTAL,     //Số lượng động cơ
    BATTERY_CAPACITY, //Kwh -> dung luong pin
    BATTERY_VOLTAGE,  //V   -> dien ap pin
    MAX_RANGE,        //km  -> quang duong toi da di duoc neu day pin
    MAX_TORQUE,       //Nm  -. momen xoan
    MAX_ENGINE_POWER, //kW  -> cong suat toi da cua dong co
    MAX_AC_POWER,     //W   -> cong suat toi da cua dieu hoa   
    MAX_SPEED_SPORT,  //Km/h-> toc do toi da o che do sport
    MAX_SPEED_ECO,    //Km/h-> toc do toi da o che do sport
    MAX_RPM,          //rotation per minute -> so vong quay 
    WEIGHT,           //kg -> khoi luong khong tai cua xe
    WHEEL_RADIUS,     //cm -> ban kinh banh xe
    AC_TEMP_MAX,      //do c -> nhiet do toi da dieu ching duoc tren dieu hoa
    AC_TEMP_MIN,      //do c -> nhiet do nho nhat dieu chinh duoc tren dieu hoa
    WIND_LEVEL_MAX    //muc gio manh nhat tren dieu hoa
};
//định nghĩa kiểu tổng quát cho giá trị của thông số
typedef int16_t design_value;
//bản đồ lưu trữ giá trị cụ thể ứng với mỗi thông số 
typedef map<vehicle_Attribute,design_value> Vehicle_BaseParam;
//lớp khởi tạo và truy xuất thông số kỹ thuật của xe
class ElectricVehicle_Init{
private:
    //thuộc tính của dòng xe 
    static Vehicle_Brand brand; 
    static Vehicle_Version version;
    static Vehicle_BaseParam initParam; 
public:
    //constructor để khởi tạo các thông số của nxs cho các dòng xe
    ElectricVehicle_Init(Vehicle_Version version,Vehicle_Brand brand);
    ~ ElectricVehicle_Init(){}
    
    //hiển thị thông số chi tiết của xe
    static void Display_VehicleInfo(){
        cout <<"------------------------------------------------------------" << endl;
        cout << "+ dung lượng pin: " << getDesignValue(vehicle_Attribute::BATTERY_CAPACITY) << " kWh" << endl;
        cout << "+ điện áp pin: " << getDesignValue(vehicle_Attribute::BATTERY_VOLTAGE) << " V"<< endl;
        cout << "+ momen xoắn: " << getDesignValue(vehicle_Attribute::MAX_TORQUE) << " N.m" << endl;
        cout << "+ tốc độ tối đa ở chế độ Sport: " << getDesignValue(vehicle_Attribute::MAX_SPEED_SPORT) <<  " Km/h" << endl;
        cout << "+ tốc độ tối đa ở chế độ ECO: " << getDesignValue(vehicle_Attribute::MAX_SPEED_ECO) <<  " Km/h" << endl;
        cout << "+ công suất tối đa của động cơ: " << getDesignValue(vehicle_Attribute::MAX_ENGINE_POWER) << " kW" << endl;
        cout << "+ công suất tối đa của điều hòa: " << getDesignValue(vehicle_Attribute::MAX_AC_POWER) << " W" << endl;
        cout << "+ vòng tua tối đa: " << getDesignValue(vehicle_Attribute::MAX_RPM) << " RPM" << endl;
        cout << "+ Quãng đường tối đa (đầy pin): " << getDesignValue(vehicle_Attribute::MAX_RANGE) << " Km" << endl;
        cout << "+ Số lượng động cơ: " <<  getDesignValue(vehicle_Attribute::ENGINE_TOTAL) << endl;
        cout << "+ trọng lượng: " << getDesignValue(vehicle_Attribute::WEIGHT) << " Kg" << endl;
        cout << "+ bán kính bánh xe: "<< getDesignValue(vehicle_Attribute::WHEEL_RADIUS) << " cm" << endl;
        cout <<"------------------------------------------------------------" << endl;
    }
    //lấy ra giá trị của thông số mong muốn
    static int getDesignValue(vehicle_Attribute vehicle_param) {
        if(initParam.find(vehicle_param) != initParam.end()){
            return initParam[vehicle_param];
        }
        else return 0;
    } 
    static Vehicle_Brand getBrand() {return brand;}
    static Vehicle_Version getVersion()  {return version;}
};

#endif