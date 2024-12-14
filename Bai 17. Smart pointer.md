# 1. Tổng quan về smart pointer
Trước khi tìm hiểu về smart pointer ta cần hiểu thế nào là 1 con trỏ thô, và chúng có liên hệ gì với nhau.
## 1.1. Con trỏ thô (raw pointer)
### a) Khái niệm
Đây là 1 con trỏ cơ bản được khai báo chỉ đơn giản thông qua toán tử * mà không được quản lý bởi bất kỳ 1 đối tượng hay lớp nào. Nó cung cấp 1 số chức năng như
+ Quản lý địa chỉ của vùng nhớ mà nó trỏ đến
+ Thao tác với vùng nhớ tại địa chỉ đó

__Tuy nhiên nó không cung cấp bất cứ chức năng nào để kiểm soát vùng nhớ mà nó trỏ đến. Vì vậy ta có thể mắc phải các lỗi như__

+ Truy xuất giá trị không hợp lệ do vùng nhớ mà nó trỏ đến đã bị thu hồi

```bash
int* ptr = new int(12);
delete ptr;
cout << "value: " << *ptr // error -> dereference undefined memory
```
+ vùng nhớ bị rò rỉ khi ta quên giải phóng

```bash
int* ptr = new int(12);
//memory leak issue 
```
+ Không có cơ chế kiểm tra phạm vi của vùng nhớ mà nó quản lý

```bash
int* ptr = new int[6]; //allocate heap with 5 element
arr[10] = 20 // truy cập vào vùng nhớ chưa được cấp phát -> lỗi undefined behaviour
delete[] arr;
```

__=> Chính vì vậy ta sẽ cần 1 cách hiệu quả hơn để giải quyết những vấn đề trên 1 cách tự động. Smart pointer sẽ cung cấp những tính năng cho phép ta làm được điều đó__ 

## 1.2. Thế nào là smart pointer 
### a) Khái niệm
Đây là 1 class template cung cấp những method cho phép ta quản lý vùng nhớ với lợi ích như tự động giải phóng vùng nhớ để tránh các lỗi phổ biến khi sử dụng với raw pointer như

+ memory leak (rò rỉ bộ nhớ)
+ dangling pointer (con trỏ lơ lửng -> không trỏ đến vùng nhớ xác định)


### b) Đặc điểm
Smart pointer là 1 class template chứa
+ con trỏ thô (raw pointer) để quản lý đối tương được cấp phát vùng nhớ khi ta tạo ra 1 object
+ Các method để tự động thao tác với vùng nhớ mà ta khởi tạo

# 2. Cách loại smart pointer
Có 3 loại smart pointer như sau và ta có thể truy cập chúng thông qua thư viện
__#include<memory>__

## 2.1 Unique pointer

### a) Đặc điểm
+ Dùng để quản lý duy nhất 1 đối tượng
+ Không cho phép đối tượng đó bị sao chép hoặc trỏ đến bởi raw pointer của các object khác 
+ Các method bên trong vẫn có thể được truy cập bởi các con trỏ khai báo ngoài phạm vi
+ Có thể chuyển giao quyền sở hữu sang 1 object khác 

### b) Sử dụng 

+ Cách khai báo object và thao tác với vùng nhớ được cấp phát

__Đầu tiên ta tạo ra 1 class như sau__
```bash
class Sensor
{
private:
    float value1;
    float value2;
public:
    /*cach 2*/
    Sensor(float init1 = 23.21,float init2 = 12.21){
        value1 = init1;
        value2 = init2;
    }
    ~Sensor(){
        cout <<"call destructor" << endl;
    }
    float getValue1()
    {
        return value1;
    }
    float getValue2()
    {
        return value2;
    }
    void setValue1(float value1){
        this->value1 = value1;
    }
    void display()
    {
        cout << "sensor1 value: " << getValue1() << endl;
        cout << "sensor2 value: " << getValue2() << endl;
    }
};
```

__trong hàm main ta khai báo 1 object và khởi tạo vùng nhớ cho nó với kiểu dữ liệu chính là class mà ta đã định nghĩa trước đó__

```bash
#include <iostream>
#include <memory>
using namespace std;
int main()
    unique_ptr<Sensor> uptr = make_unique<Sensor>(10); 

    //truy cập và đọc giá trị
    uptr->display(); // cach 2 : (*uptr).display(); 

    // get data -> trả về raw nhưng vẫn còn quyền sở hữu
    cout << "get data" << endl;
    Sensor *rawptr = uptr.get();
    rawptr->setValue1(100.21);
    rawptr->display();

    //giải phóng raw pointer và object
    cout << "release" << endl;
    Sensor *rawptr = uptr.release();
    rawptr->setValue1(89.23);
    rawptr->display(); 
    delete rawptr; //tự giải phóng do unique_ptr đã được thu hồi 

    //thu hồi object và cho phép quản lý đối tượng mới
    cout << "reset" << endl;
    uptr.reset(new Sensor(20));
    uptr->display();

    //chuyển quyền sở hữu
    cout << "move" << endl;
    unique_ptr<Sensor> uptr2 = move(uptr); 
    uptr2->display();
```
+ Kết quả chạy chương trình

```bash
sensor1 value: 10
sensor2 value: 12.21
get data
sensor1 value: 100.21
sensor2 value: 12.21
release
sensor1 value: 89.23
sensor2 value: 12.21
call destructor
reset
sensor1 value: 20
sensor2 value: 12.21
move
sensor1 value: 20
sensor2 value: 12.21
call destructor
```
## 2.2 Share pointer
### a) Đặc điểm
+ Cho phép nhiều con trỏ thô của smart pointer cùng quản lý 1 tài nguyên cấp phát
+ Có tích hợp method để đếm số lượng con trỏ thô đang trỏ đến đối đối tượng
+ Được giải phóng tự động khi không còn con trỏ thô nào quản lý
### b) Sử dụng

+ Ta sẽ khai báo và thao tác với share pointer như sau

```bash
int main(){
    shared_ptr<int> sptr1 = make_shared<int>(20);
    shared_ptr<int> sptr2 = sptr1; 
    shared_ptr<int> sptr3 = sptr2;

    //hàm cục bộ
    {
        shared_ptr<int> sptr4 = sptr1;
        cout << "count:" << sptr1.use_count() << endl; // đếm số lượng raw pointer
    }
    cout << "count:" << sptr1.use_count() << endl;
    int *raw = sptr1.get();
    cout << "raw: " << *raw << endl;
    shared_ptr<int> a = make_shared<int>(40);
    shared_ptr<int> b = make_shared<int>(50);
    
    //hoán đổi giá trị object
    a.swap(b);
    cout << "a: " << *a << endl
         << "b: " << *b << endl;

    //chuyển quyền sở hữu
    a = move(b);
    cout << "a: " << *a << endl
         << "b: " << *b << endl;
}
```
+ Kết quả chạy chương trình

```bash
count:4
count:3
raw: 20
a: 50  
b: 40  
```
## 2.3 Weak pointer
### a) Đặc điểm
+ Được sử dụng để giám sát và theo dõi các share pointer
+ Không thực hiện đếm raw pointer
+ Sử dụng kết hợp với share pointer để tránh tham chiếu vòng

### b) Sử dụng

# 3. Ứng dụng của smart pointer trong embedded system

__+ Quản lý bộ nhớ heap__ : việc sử dụng heap memory thích cho hệ thống nhúng vì yêu cầu hạn chế về tài nguyên. Do đó việc sử dụng smart pointer có thể tối ưu hóa việc quản lý bộ nhớ

__+ Quản lý tài nguyên chung__: Khi ta cần chia sẻ vùng nhớ giữa các thành phần như 1 buffer chứa dữ liệu cảm biến

__+ Tránh rò rỉ vùng nhớ__: việc quản lý vùng nhớ bằng smart pointer là tự động vì vậy sẽ giảm thiểu được lỗi liên quan đến bộ nhớ so với việc dùng raw pointer