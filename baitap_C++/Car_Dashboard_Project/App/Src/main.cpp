#include "DatabaseHandler.hpp"
#include "KeyboardHandler.hpp"
#include "DashboardController.hpp"
#include "DisplayManager.hpp"
#include "SpeedCalculator.hpp"
#include "DriveModeManager.hpp"
#include "BatteryManager.hpp"
#include "SafetyManager.hpp"
using namespace std::chrono;

mutex key;

//định nghĩa các tài nguyên truy cập bởi các luồng
atomic<int> ac_temp(0),current_odometer(0),wind_level(0),remaining_range(0),current_speed(0),battery_level(0),current_battery_temp(0);
atomic<bool> Isbraking,IsAcclerating,acSignal,IsEcoModeChanged(false);
string drivemode,turnSignal;


/**
 * @brief  hàm khởi tạo trạng thái ban đầu cho xe
 * @details các thông số hệ thống của xe lưu trữ trong database sẽ được đặt về 
 *          giá trị mặc định khi xe chưa khởi động
 * @param[in] dataInit tham chiếu đển module DatabaseHandler để ghi dữ liệu vào server 
 * @note cần được gọi trước khi chương trình chạy các luồng 
 */
void Vehicle_BaseInit(DatabaseHandler& dataInit){
    dataInit.setMultipleData( 
        {
            {SystemAttribute::VEHICLE_SPEED,0},
            {SystemAttribute::DRIVE_MODE, DriveMode::ECO},
            {SystemAttribute::WIND_LEVEL,0},
            {SystemAttribute::BATTERY_LEVEL,100},
            {SystemAttribute::AC_STATUS,DeviceState::OFF},
            {SystemAttribute::AC_CONTROL,0},
            {SystemAttribute::BATTERY_TEMP,0},
            {SystemAttribute::BRAKE,PedalState::RELEASED},
            {SystemAttribute::ACCELERATOR,PedalState::RELEASED},
            {SystemAttribute::GEAR_SHIFT,GearShift::P},
            {SystemAttribute::ODOMETER,0}
        }
    );
    cout << "Khởi tạo thành công trạng thái mặc định của xe" << endl;
    cout << "-----------------BẮT ĐẦU MÔ PHỎNG-------------------" << endl;

}

/**
 * @brief   hàm cập nhật dữ liệu được gọi liên tục khi chạy chương trình 
 * @details được gọi trong luồng đọc dữ liệu để cập nhật data
 *          từ server  và thông báo tới các module khác 
 * @param[in] dbHandler  tham chiếu đển module DatabaseHandler để truy xuất dữ liệu trên server
 * @param[in] dbcontroller tham chiếu đến module DashboardController để lưu trữ dữ liệu đọc từ server
 * @note cần được gọi trong luồng chạy đồng bộ với luồng chính
 */
void Read_Data(DatabaseHandler &dbHandler,DashboardController& dbcontroler)
{
    unordered_map<string,string> data_update; //bản đồ để lưu trữ dữ liệu cập nhật theo từng cặp key - value 
    while (1)
    {
        {
            //mở khóa mutex để truy cập tài nguyên chung
            lock_guard<mutex> lock(key); 
            
            data_update["VEHICLE_SPEED"] = dbHandler.getDataString(SystemAttribute::VEHICLE_SPEED);
            data_update["ROUTE_PLANNER"] =  dbHandler.getDataString(SystemAttribute::ROUTE_PLANNER);
            data_update["BATTERY_LEVEL"] = dbHandler.getDataString(SystemAttribute::BATTERY_LEVEL);
            data_update["WIND_LEVEL"] = dbHandler.getDataString(SystemAttribute::WIND_LEVEL);
            data_update["DRIVE_MODE"] = dbHandler.getDataString(SystemAttribute::DRIVE_MODE);
            data_update["AC_CONTROL"] = dbHandler.getDataString(SystemAttribute::AC_CONTROL);
            data_update["AC_STATUS"]  = dbHandler.getDataString(SystemAttribute::AC_STATUS);
            data_update["BRAKE"] = dbHandler.getDataString(SystemAttribute::BRAKE);
            data_update["ACCELERATOR"]  = dbHandler.getDataString(SystemAttribute::ACCELERATOR);
            data_update["TURN_SIGNAL"] = dbHandler.getDataString(SystemAttribute::TURN_SIGNAL);

            dbcontroler.updateData(data_update);     //cập nhật dữ liệu đọc từ server  -> thông báo đến displayManager

            //tài nguyên sử dụng bởi luồng xử lý yêu cầu từ bàn phím 
            ac_temp = stoi(data_update["AC_CONTROL"]);                  //nhiệt độ điều hòa
            wind_level =  stoi(data_update["WIND_LEVEL"]);              //mức gió
            Isbraking =  strToBool(data_update["BRAKE"]);               //trạng thái phanh
            IsAcclerating = strToBool(data_update["ACCELERATOR"]);      //trạng thái gas
            acSignal = strToBool(data_update["AC_STATUS"]);             //trạng thái điều hòa bật/tắt
            turnSignal =  data_update["TURN_SIGNAL"];                   //tín hiệu rẽ trái/phải
            drivemode =  data_update["DRIVE_MODE"];                     //chế độ lái 

            //tài nguyên xử lý bởi luồng chính để cập nhật thay đổi 1 số thuộc tính của xe 
            current_odometer = stoi(dbHandler.getDataString(SystemAttribute::ODOMETER));
            current_battery_temp = stoi(dbHandler.getDataString(SystemAttribute::BATTERY_TEMP));
            current_speed = stoi(data_update["VEHICLE_SPEED"]);
            battery_level = stoi(data_update["BATTERY_LEVEL"]);
            remaining_range = stoi(data_update["ROUTE_PLANNER"]);
        }
        this_thread::sleep_for(chrono::milliseconds(200)); //delay để giảm tải
    }
}

/**
 * @brief   hàm xử lý yêu cầu từ bàn phím
 * @details được gọi trong lường xử lý yêu cầu từ bàn phím để cập nhật và điều chỉnh 
 *          1 số trạng thái của xe như điều hòa,mức gió,tín hiệu xi nhan 
 * @param[in] dbHandler         tham chiếu đển module DatabaseHandler để ghi dữ liệu vào server 
 * @param[in] safetyHandler     tham chiếu đến module SafetyManager để liên tục kiểm tra các yếu tố an toàn 
 * @param[in] drivemodeManager  tham chiếu đến module DriveModeManager để cập nhật chế độ lái
 * @note cần được gọi trong luồng chạy đồng bộ với luồng chính 
 */
void Handle_Input(DatabaseHandler &dbHandler,SafetyManager& safetyHandler, DriveModeManager& drivemodeHandler){
     //các giá trị ngưỡng để giới hạn thông số cài đặt
    const int ac_min = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::AC_TEMP_MIN);
    const int ac_max = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::AC_TEMP_MAX);
    const int maxwindlevel = ElectricVehicle_Init::getDesignValue(vehicle_Attribute::WIND_LEVEL_MAX);
    while(1){
        static KeyState isKeyPressed = KeyState::RELEASED; // Biến để theo dõi bàn phím có nhấn hay không
        static PedalState lastGasStatus(PedalState::RELEASED),lastBrakeStatus(PedalState::RELEASED); //biến để cập nhật phím đã nhấn
        // thực hiện mở khóa mutex để ghi dữ liệu
        { 
            lock_guard<mutex> lock(key);
            //tăng nhiệt độ điều hòa
            if (dbHandler.getDataString(SystemAttribute::UP) == "1")
            {
                if(acSignal)
                { 
                    if(ac_temp < ac_max)   ac_temp++;
                    else                   ac_temp = ac_max;
                }
                dbHandler.setData(SystemAttribute::AC_CONTROL,ac_temp.load());
                isKeyPressed = KeyState::PRESSED;

            }
            //giảm nhiệt độ điều hòa
            else if (dbHandler.getDataString(SystemAttribute::DOWN) == "1")
            {
                if(acSignal){
                    if(ac_temp > ac_min)   ac_temp--;
                    else                    ac_temp = ac_min;
                }
                dbHandler.setData(SystemAttribute::AC_CONTROL,ac_temp.load());
                isKeyPressed = KeyState::PRESSED;
            }
            //tăng mức gió
            else if(dbHandler.getDataString(SystemAttribute::RIGHT) == "1"){
                if(acSignal){
                    if(wind_level < maxwindlevel) wind_level++;
                    else wind_level = 0;
                }
                dbHandler.setData(SystemAttribute::WIND_LEVEL,wind_level.load());
                isKeyPressed = KeyState::PRESSED;
            }
            //Bật/tắt điều hòa
            else if (dbHandler.getDataString(SystemAttribute::N) == "1")
            {
                if(acSignal)  {
                    dbHandler.setData(SystemAttribute::AC_STATUS,DeviceState::OFF);
                    dbHandler.setData(SystemAttribute::AC_CONTROL,0);   //khi tắt điều hòa nhiệt độ tự động trở về 0
                }
                else{
                    dbHandler.setData(SystemAttribute::AC_STATUS,DeviceState::ON);
                    dbHandler.setData(SystemAttribute::AC_CONTROL,22); //khi bật điều hòa nhiệt độ tự cài đặt nhiệt độ mặc dịnh là 22
                }
                isKeyPressed = KeyState::PRESSED;
            }
            //thay đổi chế độ lái
            else if(dbHandler.getDataString(SystemAttribute::M) == "1"){
                //kiểm tra chế độ trước đó và cập nhật đảo trạng thái
                if(drivemode == "ECO"){
                    //IsSportModeChanged = true;
                    dbHandler.setData(SystemAttribute::DRIVE_MODE,DriveMode::SPORT); 
                    drivemodeHandler.setDriveMode(DriveModeManager::Mode::SPORT);
                }
                else{ 
                    IsEcoModeChanged = true;    //biến trạng thái dùng để giới hạn lại tốc độ nếu chuyển sang chế độ ECO
                    dbHandler.setData(SystemAttribute::DRIVE_MODE,DriveMode::ECO);   
                    drivemodeHandler.setDriveMode(DriveModeManager::Mode::ECO);       
                }
                outputPower = drivemodeHandler.getPowerOutput(); //lấy giới hạn công suất và hiển thị trên terminal
                isKeyPressed = KeyState::PRESSED;
            }
            //bật/tắt rẽ trái
            else if(dbHandler.getDataString(SystemAttribute::V) == "1"){
                if(turnSignal == "0")   dbHandler.setData(SystemAttribute::TURN_SIGNAL,TurnSignalState::LEFT);
                else if(turnSignal == "1")  dbHandler.setData(SystemAttribute::TURN_SIGNAL,TurnSignalState::OFF);
                isKeyPressed = KeyState::PRESSED;
            }
            //bật/tắt rẽ phải
            else if(dbHandler.getDataString(SystemAttribute::B) == "1"){
                if(turnSignal == "0")        dbHandler.setData(SystemAttribute::TURN_SIGNAL,TurnSignalState::RIGHT);
                else if(turnSignal == "2")   dbHandler.setData(SystemAttribute::TURN_SIGNAL,TurnSignalState::OFF);
                isKeyPressed = KeyState::PRESSED;
            }
            //điều khiển chân gas
            else if(dbHandler.getDataString(SystemAttribute::SPACE) == "1"){
                dbHandler.setData(SystemAttribute::ACCELERATOR,PedalState::PRESSED);
                lastGasStatus = PedalState::PRESSED;
                isKeyPressed = KeyState::PRESSED;

            }
            else if(dbHandler.getDataString(SystemAttribute::SPACE) == "0" && lastGasStatus == PedalState::PRESSED){
                dbHandler.setData(SystemAttribute::ACCELERATOR,PedalState::RELEASED);
                lastGasStatus = PedalState::RELEASED; //cập nhật lại trạng thái sau khi nhả phím
            }
            //điều khiển chân phanh
            else if(dbHandler.getDataString(SystemAttribute::ENTER) == "1"){
                //brakeIntensity++;
                dbHandler.setData(SystemAttribute::BRAKE,PedalState::PRESSED);
                //safetyHandler.applyBrake();
                lastBrakeStatus = PedalState::PRESSED;
                isKeyPressed = KeyState::PRESSED;
            }
            else if(dbHandler.getDataString(SystemAttribute::ENTER) == "0" && lastBrakeStatus == PedalState::PRESSED){
                dbHandler.setData(SystemAttribute::BRAKE,PedalState::RELEASED);
                lastBrakeStatus = PedalState::RELEASED;
            }
            //chỉ xử lý reset lại trạng thái nếu phát hiện đã nhấn phím
            if(isKeyPressed == KeyState::PRESSED){
                isKeyPressed = KeyState::RELEASED;
                this_thread::sleep_for(chrono::milliseconds(150)); //delay 1 khoảng trước khi tiếp tục đọc phím mới
            }
        }     
        //kiểm tra an toàn và trả về trạng thái của xe -> hiển thị thông báo trên displayManager nếu có hành động nguy hiểm
        IsSafetyAction = safetyHandler.checkBrakeAndAccelerator(IsAcclerating,Isbraking);
        //lấy dữ liệu mức gas và phanh để hiển thị ở displayManager
        brakeLevel_display = safetyHandler.getBrakeLevel();
        gasLevel_display = safetyHandler.getGasLevel();
        this_thread::sleep_for(chrono::milliseconds(50));
    }
}

/**
 * @brief   hàm điều phối các chức năng của hệ thống  
 * @details được gọi trong lường chính để xử lý các công việc như
 *      - hiển thị dữ liệu lên terminal
 *      - tính toán và cập nhật mức pin, quãng đượng còn lại, và tốc độ lên server
 *      - đồng bộ hóa các thành phần với chế độ lái
 * @param[in] dbUpdate          tham chiếu đển module DatabaseHandler để ghi dữ liệu vào server 
 * @param[in] displayUpdate     tham chiếu đến module DisplayManager để cập nhật dữ liệu lên terminal 
 * @param[in] speedUpdate       tham chiếu đến module SpeedCalculator để tính toán tốc độ hiện tại
 * @param[in] batteryUpdate     tham chiếu đến module BatteryManager để tính toán quãng đường và mức pin còn lại
 * @param[in] drivemodeUpdate   tham chiếu đến module DriveModeManager để lấy ra chế độ lái hỗ trợ cho việc đồng bộ với các tính năng khác
 * @note được gọi trực tiếp trong hàm main sau khi đã khởi tạo các luồng khác
 */
void update_Data(DatabaseHandler& dbUpdate ,DisplayManager& displayUpdate,SpeedCalculator& speedUpdate,BatteryManager& batteryUpdate,DriveModeManager& drivemodeUpdate)
{
    int update_speed;
    outputPower = drivemodeUpdate.getPowerOutput(); //lấy giá trị công suất ban đầu
    while(1)
    {   
        //mở khóa mutex để truy cập vào tài nguyên chung để thực hiện điều chỉnh trạng thái hệ thống
        {
            lock_guard<mutex> lock(key);
        //hiển thị dữ liệu lên terminal
            displayUpdate.updateDisplay();
        //cạp nhật mức pin, quãng đượng còn lại, và tốc độ
            batteryUpdate.updateBatteryLevel(ac_temp.load(),wind_level.load());
        //dự đoán quãng đường còn lại, đã đi, mức pin, nhiệt độ pin
            int update_battery_level =  static_cast<int>(batteryUpdate.getBatteryLevel());
            int update_remaining_range =  static_cast<int>(batteryUpdate.calculateRemainingRange());
            update_odometer = speedUpdate.getTotalDistanceTraveling();   //hiển thị bời displayManager ở dạng float
            update_battery_temp =  batteryUpdate.calculateBatteryTemp(); //hiển thị bời displayManager ở dạng float
        //đồng bộ hóa các thành phần với chế độ lái
            //nếu phát hiện chuyển sang chế độ ECO, điều chỉnh lại giới hạn tốc độ nếu cần 
            if(IsEcoModeChanged){
                if(update_speed > speedUpdate.getMaxSpeed("ECO")){
                    update_speed = drivemodeUpdate.limitSpeedForEcoMode(current_speed);
                    cout <<  "đang giảm tốc để phù phù hợp với chế độ lái" << endl;
                }
                else  IsEcoModeChanged = false; //reset lại trạng thái sau khi đã cập nhật lại tốc độ
               
            }
            //bắt đầu tính toán tốc độ theo chế độ lái hiện tại 
            else{
                update_speed = speedUpdate.calculateSpeed(IsAcclerating,Isbraking);
            }
            
        //cập nhật trạng thái hệ thống mỗi khi có sự chênh lệch nhất định giữa các giá trị -> tránh quá tải cho cpu nếu cập nhật liên tục
            if(abs(update_odometer - current_odometer) >= 1){                   
                int update_distance = static_cast<int>(update_odometer);
                dbUpdate.setData(SystemAttribute::ODOMETER,update_distance);
            }
            else if(abs(update_battery_level - battery_level) >= 1){
                dbUpdate.setData(SystemAttribute::BATTERY_LEVEL,update_battery_level);
            }
            else if(abs(update_speed - current_speed) >= 1){
                dbUpdate.setData(SystemAttribute::VEHICLE_SPEED,update_speed);
                if(update_speed == 0)    dbUpdate.setData(SystemAttribute::GEAR_SHIFT,GearShift::P);
                else                     dbUpdate.setData(SystemAttribute::GEAR_SHIFT,GearShift::D);
            }
            else if(abs(update_remaining_range - remaining_range) >= 1){
                dbUpdate.setData(SystemAttribute::ROUTE_PLANNER,update_remaining_range);
            }
            else if(abs(update_battery_temp - current_battery_temp) >= 1){
                int update_temp = static_cast<int>(update_battery_temp);
                dbUpdate.setData(SystemAttribute::BATTERY_TEMP,update_temp);   
            }
        }
        this_thread::sleep_for(chrono::milliseconds(150)); //cập nhật terminal với chu kỳ 250 ms
    }
}

int main()
{
    //DatabaseHandler::WriteDataBase(); //dùng để ghi lại cấu trúc dữ liệu trong server  trong trường hợp file bị lỗi tự động xóa trắng
    DatabaseHandler dbHandler;                   //khoi tao co so du lieu
    KeyboardHandler keyboard(dbHandler);         //khoi tao giao dien ban phim tuong tac voi user
    
    ElectricVehicle_Init TeslaModel3(Vehicle_Version::PERFORMANCE,Vehicle_Brand::TESLA); //Khởi tạo thông số kỹ thuật cho xe 
    ElectricVehicle_Init::Display_VehicleInfo(); //hiển thị thông số của xe

    //khoi tao cac module
    DashboardController dashboard;
    DisplayManager displayControl(&dashboard);
    SafetyManager safetymanage;
    DriveModeManager drivemodemanage;  
    SpeedCalculator speedControl(&drivemodemanage,&safetymanage);//đồng bộ 2 module tính toán tốc độ và chế độ lái
    BatteryManager batterymanage(&speedControl);                 //đồng bộ 2 module quản lý pin,tính tốc độ 

    //Khởi tạo các thông số thuộc tính hệ thống ban đầu 
    Vehicle_BaseInit(dbHandler);
    
    this_thread::sleep_for(chrono::seconds(5)); // hiển thị thông số kỹ thuật
    
    //Khởi tạo luòng đọc dữ liệu
    thread Thread1(Read_Data,ref(dbHandler),ref(dashboard));                          
    //Khởi tạo luồng xử lý yêu cầu từ bàn phím
    thread Thread2(Handle_Input,ref(dbHandler),ref(safetymanage),ref(drivemodemanage));  

    //luồng đọc và lưu phím nhấn
    keyboard.start();  

    //luồng chính -> điều phối và xử lý các chức năng cụ thể
    update_Data(dbHandler,displayControl,speedControl,batterymanage,drivemodemanage); 

    //các luồng đồng bộ chạy song song với luồng chính
    Thread1.join();       
    Thread2.join(); 

    keyboard.stop();
   
    return 0;
}