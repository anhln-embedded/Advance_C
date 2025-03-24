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

//phương thức chuyển đổi chuỗi thành boolean sử dụng ở nhiều file 
bool strToBool(const string& str);

/**
 * @brief lớp để quản lý việc tính toán các thuộc tính của xe
 * @details Cung cấp các API để trừu tượng việc tính toán các yếu tố vận hành cũa xe
 *          như lực tác động,mo-men xoắn,tốc độ góc,vòng tua,gia tốc và năng lượng tiêu hao
 *          do động cơ,diều hòa,mức gió, nhiệt độ pin
 */
class VehicleCalculation {
    private:
    /**
     * @brief Định nghĩa các hệ số để tính toán các lực cản lăn,cản gió,lực kéo,lực hãm,tốc độ góc,
    */
        static constexpr int gear_ratio = 9;                  //tỷ số truyền của hộp số xe điện    
        static constexpr float pi = 3.14;                     //hằng số pi
        static constexpr float GR = 9.1;                      //Tỷ số truyền cuối cùng
        static constexpr float gravity = 9.81;                //gia tốc trọng trường m/s^2
        static constexpr float Cr = 0.011;                    //Hệ số ma sát lăn
        static constexpr float Cd = 0.23;                     //Hệ số cản khí động
        static constexpr float Us = 0.013;                    //hệ số ma sát tĩnh tối thiểu lớn hơn hệ số cho ma sát lắn 
        static constexpr float Uk = 0.7;                      //hệ số ma sát động 
        static constexpr float airdensity =  1.225;           //mật độ không khí kg/m^3
        static constexpr float efficiency_drivetrain =  0.95; //hiệu suất truyền động
        static constexpr float efficiency_engine =  0.9;      //hiệu suất động cơ điện
        static constexpr float Area = 2.22;                   //diện tích mặt cản trước m^2
    /**
    * @brief Định nghĩa các hệ số để tính toán nhiệt độ pin
    */
        static constexpr float Talpha = 0.01;                 //hệ số thể hiện mức nhiệt độ sinh ra do công suất động cơ (độ C / Kw)
        static constexpr float Tbeta = 0.15;                  //hệ số thể hiện mức độ làm mát ảnh hưởng đến nhiệt độ pin (độ c / Kw)
        static constexpr const int C_coolingBase = 1000;      //hiệu quả làm mát cơ bản (w)
        static constexpr const int k_cooling = 30;            //hệ số tăng cường làm mát (w/do c)
    //hệ số để tính tiêu hao do điều hòa
        static constexpr int deltaT_ac  = 20;                 //chênh lệch nhiệt độ lớn nhất mà điều hòa xử lý ổn định nhất

        /**
         * @brief phương thức tính toán ma sát tĩnh tối thiểu
         * @details tính toán ma sát tĩnh để kiểm tra liệu có thắng được lực kéo 
         *          ban đầu sinh ra khi đạp gas không để xe có thể lăn bánh
         * @param[in] weight  trọng lượng và tải trọng của xe, dựa trên @Vehicle_BaseParam
         * @return float : giá trị ma sát tĩnh tính bằng Newton
         * @note cần được gọi trong phương thức getAcceleration để so sánh với F_traction
         */
        static float getMinStaticFriction(const int& weight){
            float F_static_friction = Us * weight * gravity;  
            return F_static_friction;
        }
        
        /**
         * @brief phương thức tính toán ma sát lăn
         * @details tính toán ma sát lăn để đánh giá hợp lực tác động lên xe
         *          khi bắt đầu di chuyển
         * @param[in] weight  trọng lượng và tải trọng của xe, dựa trên @Vehicle_BaseParam 
         * @return float : giá trị ma sát lăn tính bằng Newton
         * @note cần được gọi trong phương thức getAcceleration ở điều kiện F_traction > F_static_friction
         */
        static float getRollingFriction(const int& weight){
            float F_rolling =  Cr * weight * gravity;  
            return  F_rolling;  
        }
        
        /**
         * @brief phương thức tính toán lực cản gió
         * @details tính toán dựa trên tốc độ của xe để đánh giá hợp lực tác động lên xe
         *          khi bắt đầu di chuyển
         * @param[in] speed_ms tốc độ của xe tính bằng đơn vị m/s  
         * @return float : giá trị lực cản gió tính bằng Newton
         * @note cần được gọi trong phương thức getAcceleration ở điều kiện F_traction > F_static_friction
         */
        static float getAirDragForce(const float& speed_ms){
            return 0.5 * Cd * airdensity * Area * (speed_ms*speed_ms);      
        }
        
        /**
         * @brief phương thức tính toán lực hãm phanh 
         * @details tính toán dựa trên mức phanh,trọng lượng xe,tốc độ
         * @param[in] brakeLevel % mức phanh sinh ra khi đạp phanh 
         * @param[in] weight  trọng lượng của xe bao gồm khối lượng không tải và tải trọng kg
         * @param[in] speed_ms tốc độ xee m/s
         * @return float : giá trị lực phanh tính bằng Newton
         * @note cần được gọi trong phương thức getAcceleration ở điều kiện F_traction > F_static_friction
         */
        static float getBrakeForce(const int& brakeLevel,const int& weight,const float& speed_ms){
        float F_maxBrake = 0.0f;    //lực hãm tối đa
        //chỉ khi xe di chuyển lực phanh với được sinh ra
        if(speed_ms > 0) F_maxBrake = weight * gravity * Uk; 
        else F_maxBrake = 0.0f;
        //cout << "F_BrakeMax: " << F_Static_friction << endl;
        return (brakeLevel/100.0f)*F_maxBrake;
    }
    public:
        /**
         * @brief phương thức tính toán lực kéo sinh ra khi đạp gas
         * @details tính toán dựa trên mo-men xoán,bán kính bánh xe
         * @param[in] wheel_radius bán kinh của bánh xe, dựa trên @Vehicle_BaseParam
         * @param[in] weight  trọng lượng và tải trọng của xe
         * @param[in] speed_ms tốc độ trước đó của xe m/s
         * @return float : giá trị lực kéo tính bằng Newton
         * @note cần được gọi trước khi tính toán gia tốc ỏ phương thức getAcceleration
         */
        static float getTractionForce(const int& wheel_radius,const int& current_Torque){
            float radius_m = wheel_radius/100.0f; //đổi ra mét
            float F_Traction = (float)(current_Torque * gear_ratio) / radius_m; //lực kéo tối đa 
            //cout << "F_tractionMax: " << F_Traction << endl;
            return F_Traction;
        }
            
        /**
         * @brief phương thức tính toán gia tốc xe
         * @details tính toán để đánh giá được sự thay đổi tốc độ xe theo thời gian
         * @param[in] speed_ms tốc độ xe tính bằng m/s
         * @param[in] F_traction lực keo
         * @param[in] weight  trọng lượng và tải trọng của xe
         * @param[in] speed_ms tốc độ trước đó của xe m/s
         * @return float : giá trị lực kéo tính bằng Newton
         * @note cần được gọi trước khi tính toán gia tốc gọi bởi phương thức getAcceleration
         */
        static float getAcceleration(const float& speed_ms,const float& F_traction,const int& weight,const int& brakeLevel){
            float a = 0.0f;
            float F_static_friction = getMinStaticFriction(weight);
            //cout << F_static_friction;
            //trường hợp xe đứng yên -> kiểm tra lực kéo cung cấp cho xe 
            if(speed_ms <= 0.0f){
                //nếu lực kéo < ma sát tĩnh tối thiểu -> xe chưa thẻ chuyển động
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
            
        /**
         * @brief phương thức tính toán mo-men xoắn hiện tại
         * @details tính toán để dùng xác định được mức tiêu thụ công suất của động cơ, cũng như 
         *          lực kéo hiện tại
         * @param[in] rpm       vòng tua hiện tại động cơ
         * @param[in] maxRpm    vòng tua cực đại của động cơ, dựa trên @Vehicle_BaseParam  
         * @param[in] gasLevel  % mức gas sinh ra khi đạp gas
         * @param[in] MaxTorque mo-men xoắn cực đại, dựa trên @Vehicle_BaseParam  
         * @return float : giá trị mo-men xoắn tính bằng N.m
         * @note cần được gọi trước khi tính toán 
         *       + tiêu hao do công suất động: Api getPowerEngine
         *       + lực kéo cấp cho xe : Api getTractionForce
         */
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
        
        /**
         * @brief phương thức tính toán số vòng quay hiện tại
         * @param[in] speed_ms      tốc độ xe tính bằng m/s
         * @param[in] wheel_radius  bàn kính xe, dựa trên @Vehicle_BaseParam
         * @param[in] maxRpm        vòng tua cực đại của động cơ, dựa trên @Vehicle_BaseParam  
         * @return float : số vòng tua
         */ 
        static int getRpm(const float& speed_ms,const int& wheel_radius,const int& maxRpm){
            float wheel_d = (wheel_radius*2)/100.0f;  //đường kính (m)
            int rpm =  static_cast<int>((speed_ms*GR*60.0f )/(pi*wheel_d));//số vòng quay hiện tại
            if(rpm > maxRpm) rpm = maxRpm;
            else if(rpm < 0) rpm = 0;
            return rpm;
        }
        
         /**
         * @brief phương thức tính toán tốc độ góc
         * @param[in] rpm      số vòng quay hiện tại
         * @return float : tốc độ góc tính bằng m/s^2
         */ 
        static float getAngularSpeed(const int& rpm){
            return (2.0f * pi * rpm) / 60.0f;
        }

        /**
         * @brief phương thức tính toán tiêu hao do công suất điều hòa
         * @param[in] env_temp      nhiệt độ môi trường tính bằng độ C
         * @param[in] desired_temp  nhiệt độ mong muốn tính bằng độ CC
         * @param[in] maxAcpower    công suất cực đại của điều hòa, dựa trên @Vehicle_BaseParam
         * @return int : công suất tiêu thụ hiện tại tính bằng Watt
         */ 
        static int getPowerAC(const int& env_temp,const int& desired_temp,const int& maxAcpower){
            int P_ac = 0;
            if(desired_temp == 0) P_ac = 0;
            else{
                int kac = maxAcpower / deltaT_ac;   //hệ số ảnh hưởng đến mức tiêu hao do điều hòa
                P_ac = kac * abs(env_temp - desired_temp);
            }
            return P_ac;
        }

        /**
         * @brief phương thức tính toán công suất tiêu thụ do mức gió -> đơn vị Watt
         * @param[in] windLevel:   mức gió hiện tại, với 6 mức từ 0 - 5
         * @return float : tiêu hao do mức gió tính bằng watt
         */ 
        static int getPowerWind(const int& windlevel){
            if(windlevel == 0) return 0;
            else if(windlevel == 1) return 300; 
            else if(windlevel == 2) return 600;
            else if(windlevel == 3) return 900;
            else if(windlevel == 4) return 1200;
            else if(windlevel == 5) return 1500;
            else 
                return 1500;
        }

        /**
         * @brief phương thức tính toán công suất tiêu thụ cùa động cơs
         * @param[in] Torque:    mo-men xoắn tính toán tính bằng N.m
         * @param[in] AngularSpeed  tốc độ góc tính bằng m/s^2
         * @return float : tiêu hao do động cơ tính bằng watt
         */ 
        static double getPowerEngine(const float& Torque,const float& AngularSpeed){
            return (Torque * AngularSpeed)/efficiency_drivetrain;
        }

         /**
         * @brief phương thức tính tóan nhiệt độ pin 
         * @param[in] previous_battery_temp nhiệt độ trước đó tính bằng độ C
         * @param[in] Environment_temp      nhiệt độ môi trường tính bằng độ C
         * @return float : nhiệt độ hiện tại tính bằng độ C
         */
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
/**
 * @brief kiểu enum xác định phiên bản xe
 * @details được sử dụng để cài đặt phiên bản xe muốn chọn để mô phỏng, và thông số kỹ thuật
 *          tương ứng sẽ được cập nhật tương ứng 
 */
enum class Vehicle_Version{
    STANDARD,
    LONG_RANGE,
    PERFORMANCE,
    NOT_SET
};

/**
 * @brief kiểu enum xác định dòng xe
 * @details được sử dụng để cài đặt dóng xe muốn chọn để mô phỏng,cần được xác định trước khi 
 *          cài đặt phiên bản xe xe
 */
enum class Vehicle_Brand{
    VINFAST,
    TESLA,
    TOTOTA,
    HYUNDAI,
    MERCEDES,
    NOT_SET
};

/**
 * @brief kiểu enum class để xây dựng các thuộc tính thông số kỹ thuật cơ bản của xe
 */
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

/**
 * @brief kiểu dữ liệu chung mô tả giá trị của các thuộc tính thông số xe
 */
typedef int16_t design_value;

/**
 * @brief bản đồ lưu trữ các thông số kỹ thuật với các cặp key - value 
 * @details được sử dụng để truy cập các giá trị phục vụ cho việc tính toán các 
 *          yếu tố thực tế ảnh hưởng đến quá trình vận hành xe
 */
typedef map<vehicle_Attribute,design_value> Vehicle_BaseParam;
//lớp khởi tạo và truy xuất thông số kỹ thuật của xe

/**
 * @brief lớp để quản lý các thông số kỹ thuật của xe
 * @details Cung cấp các API để khởi tạo và truy xuất các thông số chi tiết 
 */
class ElectricVehicle_Init{
private:
    static Vehicle_Brand brand;         //enum mô tả dòng xe
    static Vehicle_Version version;     //enum mô tả phiên bản của dòng xe
    static Vehicle_BaseParam initParam; //enum lưu trữ bản đồ thông số xe
public:
    //phương thức tạo để khởi tạo các thông số của nxs cho các dòng xe
     /**
     * @brief phương thức tạo tự động tải dữ liệu các thông số của dòng xe muốn khởi tạo
     * @param[in] version phiên bản của dòng xe
     * @param[in] brand   dòng xe  
     */
    ElectricVehicle_Init(Vehicle_Version version,Vehicle_Brand brand);
     /**
     * @brief phương thức hủy tự động gọi khi kết thúc chương trình để giải phóng vùng nhớ lưu trữ các thông số
     */
    ~ ElectricVehicle_Init(){}

    /**
     * @brief phương thức hiển thị thông số chi tiết của xe
     * @details được gọi để kiểm tra việc khởi tạo trong constructor có đúng với thông số chỉ định không 
     */
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
    /**
     * @brief Lấy ra thông số chi tiết của xe
     * @param vehicle_param biến enum xác định loại thông số kỹ thuật cần truy cập
     * @return int : giá trị của thông số 
     */    
    static int getDesignValue(vehicle_Attribute vehicle_param) {
        if(initParam.find(vehicle_param) != initParam.end()){
            return initParam[vehicle_param];
        }
        else return 0;
    } 
    /**
     * @brief truy cập thông số dòng xe đã khởi tạo
     * @return Vehicle_Brand : giá trị enum tương ứng với thuộc tính mô tả dòng xe
     */
    static Vehicle_Brand getBrand() {return brand;}
     /**
     * @brief truy cập thông số phiên bản xe đã khởi tạo
     * @return Vehicle_Version : giá trị enum tương ứng với thuộc tính mô tả phiên bản xe
     */
    static Vehicle_Version getVersion()  {return version;}
};

#endif