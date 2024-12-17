# 1. template
## 1.1 Định Nghĩa 
+ cho phép viết 1 hàm và lớp tổng quát với nhiều kiểu dữ liệu khác nhau mà không phải viết lại code cho mỗi kiểu
+ ứng dụng trong thiết kế thư viện 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/cbc0785d-0a7a-42d1-92cf-1400e9a2431c" width = "450" height = "250">

+ Có 2 loại template: 

__function template:__ tạo ra các hàm tổng quát

__class template:__ tạo ra các lớp tổng quát

+__Cách template hoạt động:__ Khi 1 template được sử dụng với 1 kiểu dữ liệu mà ta truyền vào thì compiler sẽ tự động tạo ra 1 phiên bản của template với kiểu dữ liệu đó
## 1.2 Sử dụng template  với hàm
+ ví dụ ta có 1 hàm tính tổng 2 số nguyên như sau 
```bash
int sum(int a,int b){
    return a + b;
}
int main(){
    cout << "Sum: " << sum(23.45,21.1) << endl;  //float + float
    cout << "Sum: " << sum(25,211.13) << endl;  //int + float
    cout << "Sum: " << sum(25,12) << endl; //int + int
    return 0;
}
```
+ Trong hàm main ta sẽ thử truyền vào các đối có kiểu dữ liệu khác tuy nhiên kết quả khi trả về sẽ dựa trên kiểu dữ liệu ban đầu mà ta định nghĩa. Vì vậy khi chạy chương trình trên ta được kết quả sau 
    
```bash
Sum: 44
Sum: 236
Sum: 37
```
+ Chính vì vậy ở đây ta sẽ sử dụng 1 template để định nghĩa ra các kiểu dữ liệu tổng quát mà khi ta truyền đói số vào sẽ được tự động ép lại theo đúng kiểu mà ta mong muốn 
    
```bash
template <typename Type1 , typename Type2>
auto sum(Type1 a, Type2 b){
    return a + b;
}
```
+ Từ khóa auto được sử dụng để tự động ép lại kiểu trả về phù hợp, Chạy lại chương trình trước đó với hàm sum được truyền vào 2 kiểu dữ liệu tổng quát, ta được kết quả:
```bash
Sum: 44.55
Sum: 236.13
Sum: 37
```
## 1.3 Sử dụng template với class
+ Ta có thể tạo ra 1 class để quản lý data đọc về từ các cảm biến khác nhau, bằng cách định nghĩa 1 template để định nghĩa các kiểu dữ liệu tổng quát, ta sẽ không cần phải biết trước kiểu trả về đọc từ các cảm biến
+ Đầu tiên ta định nghĩa 1 class như sau
    
```bash
template <typename type1, typename type2>
class Sensor
{
private:
    type1 value1;
    type2 value2;
public:
    /*cach 1*/
    Sensor(type1 init1, type2 init2)
    {
        value1 = init1;
        value2 = init2;
    }
    /*cach 2*/
    // Sensor(type1 init1,type2 init2) : value1(init1) , value2(init2{}
    type1 getValue1()
    {
        return value1;
    }
    type2 getValue2()
    {
        return value2;
    }
    void display()
    {
        cout << "sensor1 value: " << getValue1() << endl;
        cout << "sensor2 value: " << getValue2() << endl;
    }
};
```
+ Trong hàm main khi tạo ra 1 object, ta sẽ cần phải truyền vào kiểu dữ liệu cụ thể để khởi tạo giá trị cho các thuộc tính bên trong class tùy vào từng loại cảm biến

```bash
int main()
{
    Sensor<double,double> tempSensor(65.12,40.45); //temp and humi 
    tempSensor.display();

    Sensor<int, int> lightSensor(510, 390); // upper and lower range
    lightSensor.display();

    Sensor<string, float> StateSensor("ON", 3.14);
    StateSensor.display();
```

+ Kết quả in ra ta được
```bash
sensor1 value: 65.12
sensor2 value: 40.45
sensor1 value: 510
sensor2 value: 390
sensor1 value: ON
sensor2 value: 3.14
```
    

## 1.4  Định nghĩa 1 class array để thao tác với nhiều kiểu dữ liệu
+ Ta sẽ tạo 1 template với
__+ Arrtype:__ kiểu dữ liệu của phần tử 

__+ size:__ số lượng phần tử (mặc định là int)

+ Tiếp theo ta tạo ra 1 class với 1 hảm dùng để khởi tạo các phần tử của mảng, và 1 hàm để trả về các phần tử bên trong nó 
```bash
template <typename Arrtype, int size>
class Array
{
private:
    Arrtype arr[size];
public:
    void set(int index, Arrtype value)
    {
        if (index >= 0 && index < size)
            arr[index] = value;
    }
    Arrtype getElement(int index)
    {
        return arr[index];
    }
};
```
+ Trong hàm main ta thực hiện khởi tạo và in ra các phần tử
+ Đầu tiên ta tạo ra 1 object bằng cách khai báo tên class và truyền vào kiểu dữ liệu của phần tử và kích thước của mảng __(đã được xác định kiểu khi tạo template)__

```bash
int main(){
    Array<int,5> arr;
    for(int i = 0 ; i < 5 ; i++)
        arr.set(i,i + 2);
    for(int i = 0 ; i < 5 ;i++)
       cout << arr.getElement(i) << " "; 
    return 0;
}
```
+ Kết quả in ra ta được

```bash
2 3 4 5 6
```
## 1.5 Sử dụng template với variadic
+ Ta có thể tạo ra 1 hàm tính tổng với số lượng tham số không xác định với nhiều kiểu dữ liệu 
```bash
template<typename type>
//hàm đệ quy 1 giá trị
type sum(type value){
    return value;
}
//hàm đệ quy 2 giá trị trở lên
template<typename type,typename...Args>
auto sum(type first,Args... args){
    return first + sum(args...);
}
int main(){
    cout << "sum of int: " << sum(1,2,3,4,5) << endl;
    cout << "sum of float: " << sum(12.3,2.12,3.3,4.5,5.9) << endl;
    cout << "sum of int and float: " << sum(1,2,3,4.7,5.5) << endl;
    return 0;
}
```
+ Kết quả in ra ta được

```bash
sum of int: 15
sum of float: 28.12
sum of int and float: 16.2
```

# 2. NAMESPACE
+ Cho phép nhóm các đối tượng (biến/hàm/class cùng tên) thành các không gian riêng biệt để tránh xung đột tên (khi ta muốn khai báo các đối tượng trùng tên)
+ Từ khóa __using__ cho phép truy cập trực tiếp các thành viên của namespace mà không cần sử dụng toán tử phạm vi ::

<p align = "center">
<img src = "https://github.com/user-attachments/assets/fbfc4535-3203-4035-881f-9f044d80c650" width = "500" height = "280">

## 2.1 Khai báo và sử dụng namespace
### a) Sử dụng các biến và hàm thông qua namespace
```bash
#include <iostream>     
using namespace std; // cho phép ta truy cập vào các hàm tiêu chuẩn của C++ như cout cin 

namespace A{
  string name = "Pham Cao Duy";
    void display()
    {
        cout << "name: " << name;
    }
    namespace B 
    {
        string name = "Pham Bang Bang";
        void display()
        {
            cout << "name: " << name;
        }
    }
}
namespace C
{
    string name = "Trinh Le Hoang";
    void display()
    {
        cout << "name: " << name;
    }
}
using namespace A :: B; // access directly to namespace B via A
int main(){
    cout << "name: " << name << endl;    // name from namespace B
    cout << "name: " << A::name << endl;
    cout << "name: " << C::name << endl;
    return 0;
}
```
### b) Sử dụng struct thông qua namespace
    
```bash
namespace user
{
    class Point
    {
    private:
        int x;
        int y;

    public:
        Point() = default;
        void display()
        {
            cout << "x = " << x << endl;
            cout << "y = " << y << endl;
        }
        void setpoint(int x, int y)
        {
            this->x = x;
            this->y = y;
        }
        int get_pointX()
        {
            return this->x;
        }
        int get_pointY()
        {
            return this->y;
        }
    };
    Point point1;
}
using namepsace user;
int main(){
    point1.display();
    point1.setpoint(12, 22);
    cout << "x: " << point1.get_pointX() << endl
         << "y: " << point1.get_pointY() << endl;
    return 0;
}
```


    

    