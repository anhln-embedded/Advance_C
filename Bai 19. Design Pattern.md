# 1. Tổng quan về design pattern

<p align = "center">
<img src = "https://github.com/user-attachments/assets/fd8cca7d-8702-462f-ad2d-032ba02f07f5" width = "500" height = "250">

## 1.1 Định nghĩa
Đây là giải pháp cung cấp các những code mẫu mang tính tổng quát để giải quyết các vấn đề phổ biến trong lập trình. Các code này là 1 dạng công thức giúp xử lý các tình huống thường gặp trong quá trình thiết kế phần mêm như:

__+ Code lặp lại:__ 

=> khó bảo trì: do phải sửa code ở nhiều chỗ trong chương trình (thiếu sự đồng bộ)

__+ Khó mở rộng mã nguồn:__

=> Không tái sử dụng lại code được do phải cập nhật mõi khi cần thêm tính năng mới

__+ Các module bị phụ thuộc lẫn nhau:__

=> Dễ gây lỗi dây chuyền khi sửa 1 module nào đó 
=> Khó thay thế hoặc nâng cấp tính năng

__+ Khó kiểm thử:__

=> Tốn thời gian sủa lỗi do các module phụ thuộc lẫn nhau mà cấu trúc code lại phức tạp

__+ Không tái sử dụng lại mã nguồn:__

=> Tăng khối lượng mã nguồn không cần thiết do Lặp lại mã giống nhau ở các module có cùng logic xử lý 

# 2. Các loại design pattern
## 2.1 Creational pattern (quản lý việc khởi tạo đối tượng)

<p align = "center">
<img src = "https://github.com/user-attachments/assets/c85222a3-628b-4d5e-905d-b3ad9c6342fa" width = "500" height = "300">

### a) Singleton

__Định nghĩa:__ Đảm bảo 1 lớp chỉ có thể tạo ra 1 đối tượng duy nhất, có nghĩa là địa chỉ sẽ được khởi tạo 1 lần duy nhất. Khi khởi tạo các đối tượng mới thì nò sẽ trả về địa chỉ của đối tượng tạo ra đầu tiên 

__Ứng dụng:__ Khi ta cần cài đặt cho 2 MCU sử dụng chung 1 cấu hình ngoại vi, tránh phải lặp lại việc tạo cấu hình riêng gây lãng phí vùng nhớ không cần thiết

<p align = "center">
<img src = "https://github.com/user-attachments/assets/bcdea374-37fa-4963-8d2c-9d99c14b1c47" width = "500" height = "300">

__=> Ví dụ:__ Quản lý tài nguyên phần cứng như UART,Timer, vốn chỉ có 1 phiên bản trong hệ thống

__Các thành phần chính__

+ __Private constructor:__ hàm khởi tạo đối tương duy nhất và không thể khởi tạo trực tiếp bên ngoài lớp, đảm bảo không có vùng nhớ dư thừa được cấp phát

+ __Static Instance:__ Xác định đối tượng duy nhất của lớp, không thể có nhiều hơn 1 đối tượng

+ __static method:__ phương thức để truy cập đến đối tương duy nhất đó ở bất kỳ đâu trong chương trình

__Triển khai cụ thể__

Ta có ví dụ sau đây dùng để cấu hình chung 1 bộ thông số của ngoại vi uart cho nhiều port GPIO như sau

```bash
class GPIO
{
private:
    GPIO()
    {
        uartInit(); // Khởi tạo thông số ngay khi 1 đối tượng được tạo ra
    }
    void uartInit()
    {
        cout << "UART is initialized" << endl;
        /*
            details implementation
        */
    }
    static GPIO *instance; // biến static trỏ đến object duy nhất
public:
    static GPIO *getInstance()
    { // method để khởi tạo object
        if (instance == nullptr)
        {
            instance = new GPIO(); // khởi tạo constructor và gọi hàm cấu hình uartInit
            //instance->uartinit();  // nếu hàm uartInit được định nghĩa bên ngoài constructor
        }
        return instance;
    }
};
GPIO *GPIO::instance = nullptr; // cấp phát địa chỉ cho static property
int main()
{
    GPIO::getInstance(); // gọi hàm trả về địa chỉ của obkect đã tạo

    GPIO::getInstance();//trả về địa chỉ của object được khởi tạo ở lần đầu gọi
    return 0;
}
```

### b) Factory pattern

__Đặt vấn đề:__ Giả sử ta có nhiều loại cảm biến với cách khởi tạo và đọc dữ liệu khác nhau. Như vậy làm thế nào mà chúng ta có thể triển khai 1 lớp định nghĩa tổng quát để sử dụng chung cho tất cả các loại mà không cần quan tâm chi tiết mỗi loại hoạt động như thế nào

<p align = "center">
<img src = "https://github.com/user-attachments/assets/4c961370-bde5-489f-8d5d-48e932daf15b" width ="500" height = "300">

__Định nghĩa:__

Cung cấp 1 cơ chế cho phép ta định nghĩa 1 đối tượng thông qua 1 lớp trừu tượng mà không cần chỉ rõ lớp của đối tượng đó

__Các thành phần__

__+ Product:__ Lớp cơ sở hoặc interface mà lớp con sẽ kế thừa

__+ Concrete product:__ Các lớp con cụ thể được tạo ra từ factory

__+ Factory:__ lớp trung gian để tạo ra các đối tượng

__Lợi ích:__

__+ Trừu tượng:__ Giúp ẩn đi những phần chi tiết của đối tượng, cung cấp 1 lớp trung gian để tạo ra đối tượng mà không cần hiểu rõ cấu trúc của từng loại 

__+ Mở rộng:__ Dễ dàng tích hợp thêm nhiều đối tượng mới mà không ảnh hưởng đến mã nguồn 

__+ Linh hoạt:__ Khi cần thêm đối tượng mới chỉ cần cập nhật factory mà không phải thay đổi mã nguồn

__+ Giảm sự phụ thuộc:__ Factory giúp mã nguồn giảm sự phụ thuộc vào các lớp cụ thể, mà chỉ cần thao tác thông qua lớp trung gian. Tăng tính tái sử dụng mã nguồn cho các dự án khác nhau

__Triển khai cụ thể:__ Ta có ví dụ sau đây để khởi tạo cảm biến thông qua 1 lớp trung gian mà không cần quan tâm đến lớp cụ thể 

+ Tạo lớp cơ sở và định nghĩa 1 method ảo để đọc dữ liệu của các cảm biến, method này sẽ được triển khai cụ thể ở các lớp con kế thừa

```bash
// Abstract class
class Sensor{
    public:
        virtual void readData() = 0;
        ~virtual Sensor(){
            cout << "Destructor for Sensor is called" << endl;
        }
};
```
__Giải thích cụ thể:__

__+ readData()__ : được khai báo là 1 hàm ảo cho phép nó được ghi đè cách triển khai tùy vào các lớp con định nghĩa các loại cảm biến khác nhau

__+ ~Sensor()__ : Hàm hủy ảo của lớp trừu tượng, ở các lớp con cũng cần phải có hàm hủy riêng để thu hồi hoàn toàn bộ.

__=> Lý do khai báo hàm hủy là virtual__:cho phép ta xóa các đối tượng của lớp kế thừa thông qua con trỏ của lớp cơ sở

+ Tạo các lớp con để xử lý dữ liệu cho từng loại cảm biến
```bash

// Temperature class
class TemperatureSensor : public Sensor{
    public:
        void readData() override {
            cout<<"reading temp data: "<<endl;
        }
        ~TemperatureSensor(){
            cout << "destructor for temp sensor is called" << endl;
        }
};

// Humidity class
class HumiditySensor : public Sensor{
    public:
        void readData() override {
            cout<<"reading humidity data: "<<endl;
        }
       ~HumiditySensor(){
            cout << "destructor for humi sensor is called" << endl;
        }
};
```
+ Định nghĩa lớp trung gian để khởi tạo gián tiếp đối tượng

```bash
// Factory class (Creator)
class SensorFactory{
    public:
        static Sensor* createSensor(const char* sensorType){
            if(sensorType == "temp"){
                return new TemperatureSensor();     // trả về đối tượng TemperatureSensor
            }
            else if (sensorType == "humi"){
                return new HumiditySensor();        // trả về đối tượng PressureSensor
            }
            else{
                return nullptr;                     // trả về con trỏ null
            }
        }
};
```

__Giải thích cụ thể__

__+ createSensor(const char* sensorType)__ hàm này được dụng để khởi tạo các object và truy cập trực tiếp thông qua class Factory, trả về con trỏ đến các đối tượng được khởi tạo thông qua lớp cơ sở Sensor

+ khởi tạo và đọc giá trị cảm biến

```bash
int main(int argc, char const *argv[])
{
    Sensor* sensor = SensorFactory::createSensor("temp");
    sensor->readData();

    //giải phóng vùng nhớ sau sử dụng -> lúc này destructor mới được gọi 
    delete sensor;
    return 0;
}

```
    
## 2.2 Structural patterns

### a) Decorator 

## 2.3 Behavioral pattern (quản lý hành vi và tương tác giữa các thành module trong hệ thống)

<p align = "center">
<img src = "https://github.com/user-attachments/assets/feea3ffc-22c4-41a0-b4d9-9a435c9bc2f4" width = "500" height = "280">

### a) MVP 

__Định nghĩa:__ 

+ tách chương trình thành các phần độc lập để quản lý cách mà các thành phần hệ thống tương tác trao đổi dữ liệu với nhau bên trong hệ thống giúp dễ dàng bảo trì và phát hiện sửa lỗi
+ Phổ biến trong lập trình giao diện người dùng __UI__ 

__Các thành phần chính:__

+__Model__: Chứa các logic liên quan đến xử lý cơ sở dữ liệu của hệ thống 

=> ví dụ: hệ thống quản lý sinh viên với database: tên,tuổi,id,ngành học

+__View__: Chứa các API  để tương tác với người dùng 

__=> ví dụ:__ APi hiển thị, nhận tương tác thông qua nút nhấn , bản phím

+__Presenter__: Trung gian giữa model và view, cho phép tách biệt xử lý giữa 2 phần đó. Nhằm đảm bảo khả năng tái sử dụng, tăng tính bảo trì code 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/9c2315be-97ed-401b-8f96-55c92fcff3fd" width = "500" height = "350">

__Triển khai cụ thể:__ 

Hệ thống điều hòa điều khiển bởi người dùng 

__Khởi tạo dữ liệu cho hệ thống__

__+ database:__ nhiệt độ, trạng thái

__+ Phương thức thao tác__: cài đặt , đọc về dữ liệu trong database


```bash

class ClimateControlModel{
    private:
        int temperature;    // Nhiệt độ hiện tại trong xe
        bool isAirOn;       // Trạng thái của điều hòa (bật/tắt)

    public:
        ClimateControlModel(int temp = 24, bool air = true): temperature(temp), isAirOn(air){}

        int getTemperature() const{
            return temperature;
        }

        bool getAirStatus() const{
            return isAirOn;
        }

        void setTemperature(int newTemperature){
            temperature = newTemperature;
        }

        void setAirStatus(bool status){
            isAirOn = status;
        }
};
```

__Hiển thị và tương tác với người dùng__

__+ Phương thức thao tác:__ Hiển thị lựa chọn, cài đặt nhiệt độ, cài đặt trạng thái 

```bash
class ClimateControlView{
    public:
        void displayCurrentSettings(int temperature, bool isAirOn){
            cout << "---- Thông tin điều hòa xe hơi ----" << endl;
            cout << "Nhiệt độ hiện tại: " << temperature << "°C" << endl;
            cout << "Trạng thái điều hòa: " << (isAirOn ? "Bật" : "Tắt") << endl;
        }

        int getUserTemperatureInput() {
            int temp;
            cout << "Nhập nhiệt độ mong muốn: ";
            cin >> temp;
            return temp;
        }

        bool getUserAirStatusInput() {
            int choice;
            cout << "Bật/Tắt điều hòa (1: Bật, 0: Tắt): ";
            cin >> choice;
            return (choice == 1);
        }
};
```

__Khởi tạo lớp thao tác trung gian__

```bash
class ClimateControlPresenter{
    private:
        ClimateControlModel& model;
        ClimateControlView&  view;

    public:
    //hàm khởi tạo tham chiếu đến database và interface để điều khiển logic chương trình một cách an toàn 
        ClimateControlPresenter(ClimateControlModel& m, ClimateControlView& v): model(m), view(v){}

        void showCurrentSettings(){
            view.displayCurrentSettings(model.getTemperature(), model.getAirStatus());
        }

        void updateTemperature(){
            int newTemperature = view.getUserTemperatureInput();
            model.setTemperature(newTemperature);
        }

        void updateAirStatus(){
            bool newAirStatus = view.getUserAirStatusInput();
            model.setAirStatus(newAirStatus);
        }
};
```

 __Luồng hoạt động của chương trình chính__

```bash
int main()
{
    ClimateControlModel model; //khởi tạo database và  các  dữ liệu ban đầu 
    ClimateControlView view;   //Khởi tạo interface tương tác với user
    ClimateControlPresenter presenter(model, view); //khởi tạo lớp trung gian giao tiếp giữa interface và database 

    int choice;
    do{
        cout << "\n1. Hiển thị thông tin điều hòa" << endl;
        cout << "2. Điều chỉnh nhiệt độ" << endl;
        cout << "3. Bật/Tắt điều hòa" << endl;
        cout << "4. Thoát" << endl;
        cout << "Nhập lựa chọn: ";
        cin >> choice;

        switch (choice){
            case 1:
                presenter.showCurrentSettings();
                break;

            case 2:
                presenter.updateTemperature();
                
                break;

            case 3:
                presenter.updateAirStatus();
                break;

            case 4:
                cout << "Thoát chương trình." << endl;
                break;

            default:
                cout << "Lựa chọn không hợp lệ!" << endl;
        }

    } while (choice != 4);

    return 0;
}
```

### b) Oberserver  
__Định nghĩa:__

Là 1 cớ chế giám sát mô tả 1 mối quan hẹ phụ thuộc __1 to many__ , có nghĩa là khi 1 đối tượng __(subject)__ thay đổi trạng thái thì các đối tượng khác __(observer)__ phụ thuộc vào nó cũng sẽ được thông báo và cập nhật

<p align = "center">
<img src = "https://github.com/user-attachments/assets/93726554-1e6f-48e8-8958-bc8cf0e95432" width ="450" height = "250">

__Ứng dụng:__ 

Khi ta mướn đọc dữ liệu từ 1 cảm biến, thì đồng thời các ngoại vi khác như LCD sẽ được tự động hiển thị dữ liệu và đèn hoặc động cơ sẽ được bật/kích hoạt

__Các thành phần__

__+ Subject:__ 

=> Đối tượng chính thông báo cho các observer về sự thay đổi trạng thái

=> Cung cấp các cơ chế thêm/xóa/thông báo cho observer

__+ Concrete subject:__ 

=> Các lớp con triển khai cụ thể của subject

=> Chứa các logic quản lý danh sách các observer và trạng thái của object

__+ Oberserver:__ 

=> Là lớp cơ sở, chứa các định nghĩa về phương thức update() mà các lớp con phải triển khai  

=> Thực hiện hành động khi nhận được thông báo từ subject

__+ Concrete Oberserver:__

=> Lớp con kế thừa từ Observer, triễn khai cụ thể các phương thức update()

=> Nhận thông báo từ subject và xử lý

__Mối quan hệ giữa Observer và Subject__

<p align = "center">
<img src = "https://github.com/user-attachments/assets/14510c02-9eee-4eb8-a1fd-58e7df7ee778" width ="400" height = "200">

__Subject:__ 

+ giữ danh sách chứa các observer
+ dễ dàng thay đổi observer mà không phải thay đổi subject

__Observer:__ 

+ đăng ký và nhận thông báo từ subject khi có sự thay đổi từ subject
+ Có thể thêm/xóa trên danh sách mà subject quản lý 
+ Có thể ngừng nhận thông báo bằng cách hủy đăng ký , giúp kiểm soát tốt tài nguyên và sự kiện hệ thống

__Triển khai cụ thể__ : Ta có ví dụ sau đây để mô tả cách đọc dữ liệu từ cảm biến và thực hiện các hành động cụ thể

<p align = "center">
<img src = "https://github.com/user-attachments/assets/ff0ebcd1-be51-4c23-88e0-777c7a6b15ab" width = "500" height = "250">

+ Định nghĩa 1 subject để giữ trạng thái và thông báo đến các observer

```bash
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
// Subject (SensorManager) holds the state and notifies observers
class SensorManager {
    float temperature;
    float humidity;
    float light;
    std::vector<Observer*> observers; //khởi tạo danh sách chứa các observer để quản lý 
public:
    //method thêm observer
    void registerObserver(Observer* observer) {
        observers.push_back(observer);
    }
    //method xóa observer
    void removeObserver(Observer* observer) {
        observers.erase(std::remove(observers.begin(), observers.end(), observer), observers.end());
    }
    //method thông báo 
    void notifyObservers() {
        //thông báo đến từng concrete observer 
        for (auto observer : observers) {
            observer->update(temperature, humidity, light); //mỗi obserer nhận thông báo và thực hiện hành động cụ thể
        }
    }
    //method cập nhật trạng thái 
    void setMeasurements(float temp, float hum, float lightLvl) {
        temperature = temp;
        humidity = hum;
        light = lightLvl;
        notifyObservers();
    }
};
```

+ Định nghĩa 1 Observer để nhận thông báo từ observer thông qua method update(), sẽ được triển khai cụ thể tùy vào các concrete observer

```bash
// Interface for observers (display, logger, etc.)
class Observer {
public:
    //Định nghĩa method để nhận thông báo từ observer
    virtual void update(float temperature, float humidity, float light) = 0;
};
```
+ Định nghĩa 2 concrete observer để hiển thị và ghi dữ liệu ghi nhận được thông báo từ observer

```bash
// Display component (an observer)
class Display : public Observer {
public:
    void update(float temperature, float humidity, float light) override {
        std::cout << "Display: Temperature: " << temperature
                  << ", Humidity: " << humidity
                  << ", Light: " << light << std::endl;
    }
};

// Logger component (an observer)
class Logger : public Observer {
public:
    void update(float temperature, float humidity, float light) override {
        std::cout << "Logging data... Temp: " << temperature
                  << ", Humidity: " << humidity
                  << ", Light: " << light << std::endl;
    }
};
```
+ Giao tiếp giữa Subject và Observer
    
```bash

int main() {
    SensorManager sensorManager; //Khởi tạo subject và cập nhật trạng thái

    //Khởi tạo concrete observer 
    Display display;
    Logger logger;

    //đăng ký vào subject để nhận thông báo
    sensorManager.registerObserver(&display);
    sensorManager.registerObserver(&logger);

    //thực hiện hành động sau khi nhận thông báo
    sensorManager.setMeasurements(25.0, 60.0, 700.0); // Simulate sensor data update
    sensorManager.setMeasurements(26.0, 65.0, 800.0); // Another sensor update

    return 0;
}

``` 
