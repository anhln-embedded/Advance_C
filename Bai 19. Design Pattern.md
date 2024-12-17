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

### a) Single pattern

__Mục đích:__ Đảm bảo 1 lớp chỉ có thể tạo ra 1 đối tượng duy nhất 

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
        uartInit(); // cach 1
    }
    void uartInit()
    {
        cout << "UART is initialized" << endl;
    }
    static GPIO *instance; // trỏ đến object duy nhất
public:
    void uartinit()
    {
    }
    static GPIO *getInstance()
    { // method để khởi tạo object
        if (instance == nullptr)
        {
            instance = new GPIO(); // tạo ra 1 object duy nhất
            //instance->uartinit();  // cach 2
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
## 2.2 Structural patterns
## 2.3 Behavioral pattern (quản lý hành vi và tương tác giữa các thành module trong hệ thống)

<p align = "center">
<img src = "https://github.com/user-attachments/assets/feea3ffc-22c4-41a0-b4d9-9a435c9bc2f4" width = "500" height = "280">

### a) MVP pattern

__Mục đích:__ tách chương trình thành các phần độc lập để dễ dàng quản lý, bảo trì và phát hiện sửa lỗi

__Các thành phần chính:__

+__Model__: Chứa các logic liên quan đến xử lý cơ sở dữ liệu của hệ thống 

=> ví dụ: hệ thống quản lý sinh viên với database: tên,tuổi,id,ngành học

+__View__: Chứa các API  để tương tác với người dùng 

__=> ví dụ:__ APi hiển thị, nhận tương tác thông qua nút nhấn , bản phím

+__Presenter__: Trung gian giữa model và view, cho phép tách biệt xử lý giữa 2 phần đó. Nhằm đảm bảo khả năng tái sử dụng, tăng tính bảo trì code 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/9c2315be-97ed-401b-8f96-55c92fcff3fd" width = "500" height = "350">

__Ví dụ:__ Hệ thống điều hòa điều khiển bởi người dùng 

### a) Khởi tạo dữ liệu cho hệ thống

__database:__ nhiệt độ, trạng thái

__Phương thức thao tác__: cài đặt , đọc về dữ liệu trong database


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

### b) Hiển thị và tương tác với người dùng

__Phương thức thao tác:__ Hiển thị lựa chọn, cài đặt nhiệt độ, cài đặt trạng thái 

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

### c) Khởi tạo lớp thao tác trung gian

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

### d) Luồng hoạt động của chương trính chính


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

