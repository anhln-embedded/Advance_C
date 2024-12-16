# 1. Tổng quan về design pattern

<p align = "center">
<img src = "https://github.com/user-attachments/assets/29354d09-8d43-4a5e-828f-08ef40e4b1d6"width = "550" height = "400">

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

### a) Single pattern

__Mục đích:__ Đảm bảo 1 lớp chỉ có thể tạo ra 1 đối tượng duy nhất 

__Ứng dụng:__ Khi ta cần cài đặt cho 2 MCU sử dụng chung 1 cấu hình ngoại vi, tránh phải lặp lại việc tạo cấu hình riêng gây lãng phí vùng nhớ không cần thiết

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
## 2.2 Structural patterns (quản lý tương tác giữa các thành phần hệ thống)
### a) MVP pattern

__Mục đích:__ tách chương trình thành các phần độc lập để dễ dàng quản lý, bảo trì và phát hiện sửa lỗi

__Các thành phần chính:__

+__Model__: Chứa các logic liên quan đến xử lý cơ sở dữ liệu của hệ thống 

=> ví dụ: hệ thống quản lý sinh viên với database: tên,tuổi,id,ngành học

+__View__: Chứa các API  để tương tác với người dùng 

=> ví dụ: APi hiển thị, nhận tương tác thông qua nút nhấn,bản phím

+__Presenter__: Trung gian giữa model và view, cho phép tách biệt xử lý giữa 2 phần đó. Nhằm đảm bảo khả năng tái sử dụng, tăng tính bảo trì code 

```bash

```
    