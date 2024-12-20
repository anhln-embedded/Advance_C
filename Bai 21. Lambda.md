# 1. Tổng quan về Lambda 

## 1.1 Định nghĩa 
Đây là 1 hàm ẩn danh được định nghĩa cục bộ bên trong 1 hàm khác mà không cần phải định nghĩa trước trong 1 lớp hoặc file khác

## 1.2 Đặc điểm

### a) Ưu điểm 
__+ Tối ưu hóa mã nguồn:__ 

=> Được dùng trong 1 phạm vi nhỏ, không cần khai báo trước

=> Sử dụng đối với các hàm chạy 1 lần trong chương trình, giúp tránh lãng phí memory nếu viết 1 hàm toàn cục để xử lý riêng 

=> Thích hợp với các hàm logic đơn giản 

### b) Ứng dụng

+ Dùng trong việc gọi hàm callback khi xử lý ngắt

+ Xử lý sự kiện trong các hệ thống đièu khiển 
## 1.3 Cách sử dụng 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/0ec06ab0-c9d0-4e5a-bc44-fef9fa52274f" width = "550" height = "250">

### a) capture []

Xác định cách mà lambda truy cập các biến bên ngoài

__[]:__ Không sử dụng biến bên ngoài

__[&]:__ Tham chiếu đến tất cả biến bên ngoài có thể truy cập

__[=]:__ copy tất cả các biến bên ngoài có thể truy cập

__[&a,b]:__ tham chiếu đến biến a, copy biến a (tham trị)

__[&,b]:__ tham chiếu tất cả các biến bên, copy biến b 

### b) parameter ()

Chứa Tham số truyền vào như hàm thông thường
### c) funtion definition {}

Chứa nội dung của hàm

# 2. Các ví dụ 

## 2.1 Ví dụ cơ bản 

### a) Sử dụng với ()

```bash
#include <iostream>
using namespace std;
int main(){
    auto sum = [](int a,int b){return a + b;};
    cout << "sum: " << sum(3,5) << endl;
}
```
### b) Sử dụng với []  
```bash
#include <iostream>
using namespace std;
int main(){
    int a = 21, b = 31;
    //example 1
    auto sum1 = [a,&b](){ 
        b += a;
        return b;
    };
    cout << "sum1 = " << sum1() << endl;
    //example 2
    auto lambda = [=]() 
    {       
            int c = a + b;
            cout << "c = " << c << endl; };
    lambda(); 
}
```
    
## 2.2 Ví dụ nâng cao

### a) Xử lý ngắt trạng thái led
```bash
#include <iostream>
#include <functional>
#include <vector>
#include <algorithm>
using namespace std;
// Hàm nhận callback
void handleInterrupt(const function<void()> &callback)
{
    cout << "Interrupt occurred!" << endl;
    callback();
}
int main(){
    int ledState = 1;
    handleInterrupt([&ledState](){
    ledState = !ledState; // Đổi trạng thái LED
       cout << "LED State: " << ledState <<endl; 
    });
}
```
### b) Xử lý dữ liệu cảm biến 

```bash
#include <iostream>
#include <functional>
#include <vector>
#include <algorithm>
int main(){
  // Lọc dữ liệu cảm biến lớn hơn 15
    auto count = count_if(sensorData.begin(), sensorData.end(), [](int val)
                          { return val > 5; });

    cout << "Number of values > 15: " << count << endl;
}
```
    
