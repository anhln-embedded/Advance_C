# 1. Tổng quan về Inline Function

<p align = "center">
<img src = "https://github.com/user-attachments/assets/e82287dc-52d1-4d8e-9918-f89e1f96f8e0" width = "550" height = "300">

## 1.1 Định Nghĩa 
Từ khóa inline được dùng để thông báo đển compiler biết được là nội dung bên trong hàm sẽ được thay thế trực tiếp thay vì xử lý như cách thông thường mỗi khi 1 hàm được gọi đó là địa chỉ của nó sẽ phải được lưu vào trong main stack pointer trước sau đó mói nhảy đến nội dung trong hàm để thực 
## 1.2 Đặc điểm
### a) Ưu và Nhươc điểm
+ Thích hợp cho những hàm được gọi nhiều lần
+ Tối ưu hóa những hàm có logic đơn giản (tính toán, các method getter/setter trong class)
+ Không thích hợp cho những hàm xử lý phức tạp (chứa vòng lặp,điều kiện)
+ Không hỗ trợ xử lý đệ quy
+ Dễ dàng bảo trì mã nguồn

### b) So sánh với macro

<p align = "center">
<img src = "https://github.com/user-attachments/assets/64c33371-690a-4984-9bed-468a8c3b3236" width = "400" height = "200">

__+ Kiểm tra kiểu dữ liệu:__ inline function kiểm tra tham số tại thời điểm biên dịch, còn macro thì không`

__+ Inline function không gây lỗi biên dịch khó hiểu:__ Macro có thể gây ra lỗi khó debug

__+ Inline function hỗ trợ debug tốt hơn:__ được hiển thị trong stack trace,còn macro thì không 

```bash
// Macro
#define SQUARE(x) ((x) * (x))

//inline
inline int square(int x) { return x * x; }

int main(){

    int result = SQUARE(1 + 2); // Lỗi: ((1 + 2) * (1 + 2)) = 1 + 4 + 4 = 9

    int result = square(1 + 2); // Kết quả chính xác: 9

}
```
# 2. Các ví dụ 

Ứng dụng của inline function thường sử dụng cho các hàm nhỏ để truy cập thanh ghi hoặc thực hiện các phép tính cơ bản giúp tối ưu chương trình 

## 2.1 Thực hiện tính toán cơ bản 
```bash
#include <iostream>
#include <cstdint>
using namespace std;
inline int multiply(int a, int b)
{
    return a * b;
}
int main(){
     int result = multiply(4, 5);
     cout << "Result: " << result << endl; // Output: Result: 20
}
```

## 2.2 Sử dụng với method getter/setter trong class

```bash
#include <iostream>
#include <cstdint>
using namespace std;
class Point
{
private:
    int x, y;

public:
    inline void setX(int xVal) { x = xVal; }
    inline int getX() const { return x; }
    inline void setY(int yVal) { y = yVal; }
    inline int getY() const { return y; }
};
int main(){
    Point p;
    p.setX(10);
    p.setY(20);
    cout << "Point: (" << p.getX() << ", " << p.getY() << ")" << endl;
}
```

## 2.3 Truy cập và thao tác trên thanh ghi

```bash
#include <iostream>
#include <cstdint>
using namespace std;
inline void setRegister(volatile uint32_t *reg, uint32_t value)
{
    *reg = value;
}
inline void toggleLED(volatile uint32_t *port, uint32_t pin)
{
    *port ^= (1 << pin); // Đảo trạng thái pin
}
int main(){
    volatile uint32_t PORTA = 0;
    setRegister(&PORTA, 0xFF); // Ghi giá trị 0xFF vào thanh ghi PORTA

    volatile uint32_t GPIO_PORT = 0;
    toggleLED(&GPIO_PORT, 5); // Toggle LED trên pin 5
    return 0;
}
```

