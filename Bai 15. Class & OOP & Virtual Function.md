# 1. Tổng quan về Class
## 1.1 Khái niệm

Class là kiểu dữ liệu tự định nghĩa bỡi người dùng để quản lý và mô phỏng các đặc điểm của 1 đối tượng cụ thể nào đó chứa các biến và hàm bên trong. Có thể nói nó là 1 phiên bản nâng cấp của struct và union.

<p align = "center">
<img src ="https://github.com/user-attachments/assets/bbb0c5c5-5b7e-4088-aa44-7cca28804df8"width = "650" height = "300">

## 1.2 Đặc điểm
Trong class các biến và hàm được định nghĩa là

__a) property(thuộc tính) và method(phương thức)__

+ Class được quản lý dựa trên 3 phạm vi là 

__b) Public, private, protected__

+ Khi khai báo 1 class các thành phần của nó sẽ luôn mặc định là private (không thể truy cập từ bên ngoài class thông qua object)

## 1.3 Các Thao tác với class
Khi khai báo 1 class ta cần chú ý

__+ Khai báo private:__ đối với các properties khi ta muốn đảm bảo an toàn dữ liệu  

__+ Khai báo public:__ đối với các method, được gọi và sử dũng bên ngoài class

__+ Khai báo protected :__ Đối với các thành viên mà ta muốn nó được phép truy cập thông qua các lớp con kế thừa từ lớp gốc

### a) Sử dụng properties và method
```bash
#include <iostream>  //thư viên C++
using namespace std; // cú pháp cho phép những hàm tiêu chuẩn như cout, cin 
class Person{
  //giới hạn quyền truy cập bên ngoài class
  private:
    string name;
    int age;
  public:
    void setName(string _name){
        name = _name;
    }
    void setAge(int _age){
        age = _age;
    }
    string getName(){
        return name;
    }
    int getAge(){
        return age;
    }
};
int main(){
    Person person1; //tạo ra 1 object từ class 
    //truy cập gián tiếp các property trong qua method 
    person1.setName("Pham Cao duy");
    person1.setAge(17);
    //in ra thong tin
    cout << "name: " << person1.getName << endl;
    cout << "age: " << person1.getAge << endl;
    return 0;
}
```
### b) Constructor và Destructor 

__Construct (hàm tạo)__

+ Được sử dụng để khởi tạo tự động các thuộc tính cũng như phương thức, Constructor sẽ được khởi tạo có cùng tên với class,và chứa các tham số mà ta muốn khởi tạo ban đầu.
    
```bash
class Person{
  private:
    string name;
    int age;
  public:
  /*hàm tạo chứa tham số*/
    Person(string _name , int _age){
        name = _name;
        age = _age;
    }
  /*hàm tạo mặc định*/
    /*hàm tạo mặc định*/
    Person(){
        name = 0;
        age = 0;
    }
    void printInfo(){
        cout << "name: " << name << endl;
        cout << "age: " << age << endl;
    }
};
int main(){
    Person person1("Pham Cao Duy",2424);
    person1.printInfo();
}
```
__Destructor (hàm hủy)__

+ Được sử dụng để hủy 1 constructor, hay nói cách khác là giải phóng các properties
+ Destructor có cùng tên với constructor và được thêm vào dấu ~ phía trước
+ Khi chương trình kết thức chúng sẽ được gọi tự động và giải phóng các constructor theo cơ chế LIFO

```bash
class Person{
  private:
    string name;
    int age;
  public:
    Person(string _name , int _age){
        name = _name;
        age = _age;
    }
    ~Person(){
          cout << "constructor:  " << name << " has been released" << endl;
    }
};
int main(){
    Person person1("Pham Cao Duy ",24);
    Person person2("Dinh Anh Tuan ",29);
    Person person3("Trinh Le Hoang ",29);
}
```
+ Kết quả khi chạy chương trình trên ta được
    
```bash
constructor: Trinh Le Hoang has been released
constructor: Dinh Anh Tuan has been released
constructor: Pham Cao Duy has been released
```
### c) method và property static 

__Đặc điểm__

+ các method và property được sử dụng bằng cách gọi trực tiếp thông qua tên class kết hợp với toán tử phạm vi ::
+ Static property chỉ được cấp phát địa chỉ để sử dụng khi ta gán giá trị bên ngoài class __(lúc này ta mới sử dụng được property này)__
+ Chỉ có các static method mới được phép truy cập đến static property

__Ví dụ:__ Ta sẽ dùng static property để lưu giá trị đếm, và truy cập nó thông qua static method. 

```bash
class Person{
  private:
    string name;
    int age;
    static int total; //chỉ có thể truy cập thông qua static method
  public:
    Person(string _name , int _age){
        name = _name;
        age = _age;
        total += 1; //đếm só lượng object mỗi lần khởi tạo 
    }
    static void print_total(){
        cout << "total of objects: << total << endl;
    }
};
int Person :: total = 0 //cấp phát địa chỉ và khởi tạo giá trị lưu ở data segment
int main(){
    Person person1("Duy Pham",30);
    Person person2("Hoang Le",38);
    Person person3("Tuan Dinh",22);
    Person :: print_total();
}
```
+ Kết quả in ra ta được __total of objects: 3__

__Ừng dụng thực tế:__

+ Khi ta cần chia sẻ cấu hình cài đặt giống nhau giữa các ngoại vi trong 1 hệ thống nhúng. Ví dụ như cài đặt thông số baudrate giống nhau cho nhiều bộ UART

```bash
#include <iostream>

class UART {
private:
    static int baudRate; // Shared property for baud rate
    int instanceId;      // Each UART has a unique ID

public:
    UART(int id) : instanceId(id) {}

    // Static method to set baud rate
    static void setBaudRate(int rate) {
        baudRate = rate;
    }

    // Static method to get baud rate
    static int getBaudRate() {
        return baudRate;
    }

    // Non-static method to display UART details
    void displayDetails() {
        std::cout << "UART Instance ID: " << instanceId
                  << ", Baud Rate: " << baudRate << std::endl;
    }
};

// Define static member outside the class
int UART::baudRate = 9600; // Default baud rate

int main() {
    UART uart1(1); // UART instance 1
    UART uart2(2); // UART instance 2

    // Set shared baud rate using static method
    UART::setBaudRate(115200);

    // Each instance will use the same baud rate
    uart1.displayDetails();
    uart2.displayDetails();

    // Retrieve shared baud rate
    std::cout << "Shared Baud Rate: " << UART::getBaudRate() << std::endl;

    return 0;
}
```
__Giải thích chương trình__

+ __baudRate__:được sử dụng để lưu giá trị cài đặt chung. Thay đổi giá trị này sẽ tự động cập nhật cho tất cả bộ UART
+ __instanceId__: được dùng để phân biệt giữa 2 bộ UART với nhau. Mỗi bộ UART sẽ có 1 ID riêng
+ __getBaudRate__: được sử dụng để đọc ra giá trị baud thông qua tên class mà không cần phải sử dụng object cụ thể

__Lợi ích sử dụng static member__

__+ Chia sẻ Tài nguyên chung__ : đối với đặc trưng của 1 hệ thống nhúng với tài nguyên giới hạn, thì sử dụng static member sẽ tối ưu và tránh lãnh phí memory không cần thiết

__+ Truy cập global:__ Cho phép ta truy cập static member trực tiép thông qua tên class 

### d) Con trỏ this và toán tữ phạm vi ::
Con trỏ this và toán tử phạm vi :: đều được sử dụng để truy cập đến 1 đối tương được khai báo cục bộ 

Đối với Con trỏ this sẽ có các đặc điểm sau:
+ Được tạo ra tự động khi ta định nghĩa 1 class
+ Trỏ đến đối tượng hiện tại khi ta tạo ra
+ Dùng để phân biệt giữa tham số truyền vào và thuộc tính của class
+ là 1 constant pointer (không thể thay đổi địa chỉ mà nó trỏ đến nhưng vẫn thay đổi được giá trị)

```bash
class Person{
  private:
    string name;
    int age;
    static int total;
  public:
    Person(string name , int age){
        this->name = name;
        this->age = age;
        total += 1; //đếm só lượng object
    }
    void PrintAddress(){
        cout << "Address of this: << this << endl;
    }
    static void print_total(){
        cout << "total of objects: << Person :: total << endl;
    }
    
};
int Person :: total = 0//cấp phát địa chỉ lưu ở data segment
int main(){
  Person person1("Duy Pham",19);

  //kết quả khi in ra 2 dòng bên dưới là giống nhau do tính chất cùa con trỏ this là trỏ đến đối tượng hiện tại
  cout << "address of person1: " << &person1 << endl;
  person1.PrintAddress();
}
```

### e) Pass by value(tham trị) và Pass by reference(tham chiếu)

<p align = "center">
<img src = "https://github.com/user-attachments/assets/3b918061-fa8f-4214-827e-37f74821e47b" width = "500" height = "150">

+ Ta có ví dụ sau mô tả cách sử dụng của truyền tham trị và tham chiếu 
```bash
/*PASS BY REFERENCE*/
void write_and_read(int &write_value, int const &compare_value)
{
    if (compare_value > 23)
    {
        write_value += 12;
    }
    else
        write_value -= 12;
}
/* PASS BY VALUE */
int calculate(int write_value)
{
    return write_value += 12;
}
int Person ::total = 0;
int main()
{
    int write = 12;
    int compare_value = 20;
    int result = calculate(write);
    write_and_read(write,compare_value);
    cout << "write: " << write << endl;
    return 0;
}
```
__Giải thích chương trình__

+ __Hàm calculate__ khi ta truyền trực tiếp giá trị cùa biến write (pass by value) thì để cập nhật giá trị thay đổi trong hàm này ta cần phải sử dụng từ khóa return và sửa đổi kiểu trả về của hàm. Viêc pass by value cũng gây phát sinh vùng nhớ, lãng phí tài nguyên trên RAM

+ __Hàm write_and_read__ ta sử dụng tham chiếu để truy cập trực tiếp đến địa chỉ các đối số để xử lý, vì vậy không gây phát sinh thêm bất kỳ vùng nhớ nào. Mọi thay đổi bên trong hàm cục bộ đều được cập nhật ở bên ngoài 

+ __biến compare_value__ được truyền vào theo kiểu là 1 tham chiếu const cho biết nó chỉ được dùng để đọc ra chứ không cho phép thay đổi giá trị

+ __biến write_value__ được truyền vào như là 1 tham chiếu để cập nhật giá trị dựa trên giá trị của compare_value
# 2. Các thao tác với OOP trong class
## 2.1 Inheritance (Tính kế thừa)

__Định nghĩa__

+ Đây là khả năng tái xử dụng lại các method và properties từ class gốc từ các class con kề thừa từ nó, giúp ta tối ưu và rót gọn chương trình

__Lợi ích:__

+ Cho phép ta tái sử dụng mã nguồn, giúp giảm thời gian và công sức viết lại code
+ Dễ dàng mở rộng các tính năng mới bằng cách kế thừa dựa trên lớp gốc
+ Cung cấp 1 tính nhất quán khi các lớp con phải tuân theo cấu trúc và hành vi của lớp gốc
<p align = "center">
<img src ="https://github.com/user-attachments/assets/9409ad5c-7d3a-49a0-87df-fc4c71e8ff27"width = "600" height = "250">

__Ví dụ:__ 

```bash
class person
{
protected:
    int tuoi;
    string ten;
public:
    person(string ten, int tuoi)
    {
        this->ten = ten;
        this->tuoi = tuoi;
    }
    void printInfo()
    {
        cout << "ten: " << ten << endl;
        cout << "tuoi: " << tuoi << endl;
    }
};
class hocsinh : public person
{
private:
    string lop;
public:
    hocsinh(string ten, int tuoi, string lop) : person(ten, tuoi)
    {
        this->lop = lop;
    }
    void printInfo()
    {
        cout << "ten: " << ten << endl;
        cout << "tuoi: " << tuoi << endl;
        cout << "lop: " << lop << endl;
    }
};
class sinhvien : public person
{
private:
    string major;
public:
    sinhvien(string ten, int tuoi, string major) : person(ten, tuoi)
    {
        this->major = major;
    }
    void printInfo()
    {
        cout << "ten: " << ten << endl;
        cout << "tuoi: " << tuoi << endl;
        cout << "nganh hoc: " << major << endl;
    }
};
int main()
{
    hocsinh hs1("Trinh Le Hoang",26,"12A1");
    sinhvien sv1("Pham Cao Duy",17,"Mechatronics Engineer");

    hs1.printInfo();
    sv1.printInfo();
}
```
__Giải thích chương trình__

+ class hocsinh và sinhvien sẽ kế thừa các thông tin cơ bãn từ class person và bổ sung thêm các thuộc tính đặc trưng 
+ 2 thuộc tính ten,tuoi ở class person được để ở quyền truy cập protected cho phép nó có thể sử dụng ở class kết thừa
+ hàm printInfo ở class person sẽ được ghi đè nội dung ở class kế thừa

## 2.2 Encapsulation (tính đóng gói)

__Định nghĩa:__

+ Đây là khả năng đóng gói những dữ liệu quan trọng ảnh hường bao gồm cả thuộc tính và phương thức trong 1 class, là những thành phần sẽ thay đổi dựa trên tương tác giữa người dùng và hệ thông
+ Được thiết lập thông qua các từ khóa public,private,protected
+ Cung cấp các API trung gian để thao tác như getter hay setter

__Lợi ích:__

+ Giúp bảo vệ được dữ liệu, nhằm ngăn chặn việc truy cập trực tiếp bên ngoài. Qua đó giảm được nguy cơ lỗi và các vấn để bảo mật


__Ví du:__

<p align = "center">
<img src ="https://github.com/user-attachments/assets/8121ac09-0410-4f7b-86b9-f98e37c88732"width = "600" height = "250">

```bash
class sinhvien
{
private:
//không thể truy cập thay đổi giá trị ngoài class
    string rank;
    float dtb;
public:
    float dtoan;
    float dvan;
    string name;
    sinhvien(string name , float dtoan, float dvan)
    {
        this->name = name;
        this->dtoan = dtoan;
        this->dvan = dvan;
    }
    float tinh_dtb()
    {
        dtb = (dtoan + dvan) / 2;
        return dtb;
    }
    string xep_hang()
    {
        if (dtb >= 8)
            rank = "gioi";
        else if (dtb > 6.5)
            rank = "kha";
        else if (dtb >= 5 && dtb < 6.5)
            rank = "trung binh";
        else
            rank = "yeu";
        return rank;
    }
};
int main()
{
    sinhvien sv1("Pham Cao Duy",8.2,8.4);
    cout << "diem trung binh: " << sv1.tinh_dtb() << endl;
    cout << "xep hang: " << sv1.xep_hang();
}
```
__Giải thích chương trình__

+ Ta định nghĩa 1 class sinhvien chứa các method để tính điểm trung bình và xếp hạng dựa vào các giá trị sẽ được truyền vào khi tạo ra 1 object class
+ 2 giá trị stb, rank không thể trực tiếp thay đổi vì chúng cần dựa vào các giá trị dtoan,dvan để tính toán xử lý thông qua cac method mà ta gọi ra.
## 2.3 Abstract (Tính trừu tượng) 

__Định nghĩa:__

+ Đây là khả năng cho phép ẩn đi những phần phức tạp và cách triển khai chi tiết của 1 đối tượng thông qua việc cung cấp các API để thao tác với chúng
+ Nó chỉ tập trung vào việc ứng dụng những gì cho sẵn và sử dụng, thay vì hiểu rõ bản chất quy trình
+ Nó có thể được sử dụng thông qua các __abstract class__ cùng với __pure virtual function__ 

 __Lợi ích:__

 + Giảm đi sự phức tạp thông qua việc cung cấp các interface cần thiết và ẩn đi những phần cụ thể
 + Dễ dàng sử dụng và thân thiện vói người dùng, vì không cần biết phải hiểu rõ cách thức hoạt động bên trong đối tượng

<p align = "center">
<img src ="https://github.com/user-attachments/assets/477e32ab-173c-493a-b8ff-44402aaebcdf"width = "600" height = "250">

```bash
class Car{
    virtual void Airbar_Control() = 0;
    virtual void Torque_Control() = 0;
    virtual void Throttle_Control() = 0;
};
class Airbar : public Car{
    void void Airbar_Control(){
        /*detail implementation*/
    }
};
class Torque : public Car{
     void Torque_Control(){
        /*detail implementation*/
     }
}
class Throttle : public Car{
     void Throttle_Control(){
        /*detail implementation*/
     }
}
```
__Giải thích chương trình__

+ Trong lớp Car ta sẽ được cung cấp 1 số interface với tính năng cụ thể để người dùng có thể tương tác nhưng phần triển khai cụ thể của nó sẽ được ẩn đi và chỉ được xử lý ở các lớp con bên dưới. 

## 2.4 polymorphism(tính đa hình) 
__Định nghĩa:__ 
+ Là khả năng cho phép các phương thức có các cách triển khai khác nhau tùy thuộc vào từng đối tượng của nhiều lớp con kế thừa từ lớp gốc

__Lợi ích:__

+ Cung cấp 1 cơ chế linh hoạt để xử lý các đối tượng mà không cần biết rõ lớp của chúng
+ Tăng khả năng mở rộng nhiều chức năng mà không làm thay đổi lớp hiện có
   
<p align = "center">
<img src ="https://github.com/user-attachments/assets/bc5431ca-6b88-46e0-8389-a071b855c951"width = "600" height = "250">

+ Các loại đa hình trong OOP 

<p align = "center">
<img src ="https://github.com/user-attachments/assets/28bbca14-8944-4eb0-85bd-ef10a2c5ef55"width = "400" height = "200">

### a) Function Overloading 
Đây là định nghĩa liên quan đến nạp chồng hàm, Được sử dụng khi ta muốn định nghĩa nhiều hàm cùng tên có cách xử lý giống nhau nhưng khác nhau về:
+ Số lương tham số 
+ Kiểu dữ liệu trả về
+ Kiểu dữ liệu tham số
```bash
class tinh_toan{
    public:
    /*Overloading method*/
        int tong(int a , int b){ 
            return a + b;
        }
        double tong(double a , double b){
            return a + b;
        }
        int tong(double a,double b,double c, double d){
            return (int)a + b + c+ d;
        }
};
int main(){
    tinh_toan tinh;
    cout << "tong 2 so integer: << tinh.tong(12,14) << endl;
    cout << "tong 2 so double: << tinh.tong(12.12,14.42) << endl;
    cout << "tong 4 so double: << tinh.tong(9.23,14.12,17.21,89.23) << endl; 
    return 0;
}
```
### b) Operator Overloading

__Định nghĩa:__ Cơ chế cho phép ta định nghĩa lại các toán tử cơ bản như +,-,*,/ thành các kiểu đặc biệt để thao tác được trên các kiểu dữ liệu không phải nguyên thủy ví dụ như struct hay class
__Ứng dụng:__ Khi ta cần trực quan và đơn giản hóa trong việc đọc hiểu code ví dụ thay vì viết v3 = v1.add(V2) ta có thể viết v3 = v1 + v2, thông quan việc định nghĩa lại toán tử + để trình biên dịch có thể hiểu được  

__Cú pháp:__ 
```bash
<return type> operator symbol (param){
    //logic toán 
}
```
__operator:__ từ khóa để nạp chồng toán tử

__symbol:__ toán tử muốn nạp chồng, phải là nằm trong phạm vi các toán tử nguyên thủy như +,-*,/

__Ví dụ:__ Nạp chồng toán tử + để cộng 2 phân số 

```bash
class Phanso{
    private:
        int mauso;
        int tuso;
    public:
    //khởi tạo giá trị mặc định ban đầu 
        Phanso(int mauso = 0,int tuso = 0){
            this->mauso = mauso;
            this->tuso = tuso;
        }
        Phanso operator + (Phanso other){
            Phanso ketqua;
            ketqua.mauso = this->mauso * other.tuso + this->tuso * other.mauso;
            ketqua.tuso = this->tuso * other.tuso;   
            return ketqua;
        }  
        void display(Phanso a, Phanso b,Phanso ketqua){
            cout << a.mauso << "/" << a.tuso << " + " << b.mauso << "/" << b.tuso << " = " << ketqua.mauso << "/" << ketqua.tuso << endl;
        }
};

int Person :: total = 0;
int main(){
   Phanso ps1(12,42);
   Phanso ps2(14,11);
   Phanso ps3 = ps1 + ps2;
   ps3.display(ps1,ps2,ps3);
   return 0;   
}
```

### c) Virtual function (Hàm ảo)
+ khi 1 hàm được định nghĩa là virtual nó có thể được ghi đè (override) trong class con, để cung cấp cách triển khai cụ thể
+ Khi gọi 1 hàm ảo thông qua 1 con trỏ/tham chiếu đến các lớp con. Hàm ảo tương ứng sẽ được gọi ra dựa trên object mà nó trỏ tới, chứ không dựa vào kiểu dữ liệu mà nó được định nghĩa
+ Nếu lớp con không cung cấp cách triển khai cụ thể thì nội dung trong hàm ảo được định nghĩa ở class gốc sẽ được dùng nếu ta gọi
```bash
class Instrument
{
public:
    virtual void makesound(){
        cout << "make sound " << endl;
    }
};
class Piano : public Instrument
{
    void makesound()
    {
        cout << "playing the piano" << endl;
    }
};
class guitar : public Instrument
{
    void makesound()
    {
        cout << "playing the guitar" << endl;
    }
};
class Ukelele : public Instrument
{
    void makesound()
    {
        cout << "playing the Ukelele" << endl;
    }
};
int main(){
    Instrument* p[3];
    //trỏ đến các lớp con
    p[0] = new Piano(); 
    p[1] = new Guitar(); 
    p[2] = new Ukelele(); 
    for(int i = 0 ; i < 3 ;i++){
        p[i]->makesound(); //in ra hàm ảo tương ứng với từng lớp con
    }
}
```
### d) Pure virtual function (hàm ảo thuần túy)
+ Lúc này hàm ảo mà ta định nghĩa sẽ được gán giá trị bằng 0, và bắt buộc lớp con kế thừa phải cung cấp cách triển khai cụ thể 
+ Khi 1 class chứa ít nhất 1 pure virtual function nó sẽ trở thành abstract class, nghĩa là ta sẽ không thể tạo ra 1 object từ class này
```bash
class Instrument
{
public:
    virtual void makesound() = 0; 
};
int main(){
    Instrument myInstrument; //wrong 
    return 0;
}
```
## 2.5 Ví dụ kết hợp 4 tính chất OOP

### a) Tạo ra 1 lớp chung để cung cấp những thuộc tính và phương thức chung cho các loại xe

__+ Tính Đóng gói:__ chứa các thuộc tính và đặc điểm của xe cần được bảo mật và không cho phép truy cậo trực tiếp

__+ Tính Trừu tượng:__ Chứa các hành động mà xe sẽ thực hiện (phương thức). Mỗi loại xe sẽ có cung cấp cách vận hành khác nhau

__Triển khai cụ thể__ 

```bash
#include <iostream>
using namespace std;
class Car
{
private:
    /*ENCAPSULATION  */
    string brand;
    string model;
    int speed;

public:
    /* ABSTRACT */
    virtual void startEngine()
    {
        cout << "base startEngine" << endl;
    }
    virtual void stopEngine()
    {
        cout << "base stopEngine" << endl;
    }

    virtual ~Car() {} // Destructor ảo
    // Constructor
    Car(string b, string m, int s) : brand(b), model(m), speed(s) {}

    // Getter và Setter
    string getBrand() { return brand; }
    void setBrand(string b) { brand = b; }

    string getModel() { return model; }
    void setModel(string m) { model = m; }

    int getSpeed() { return speed; }
    void setSpeed(int s)
    {
        if (s >= 0)
            speed = s;
    }

    // Hiển thị thông tin
     void displayInfo()
    {
        cout << "Brand: " << getBrand() << ", Model: " << getModel()  << ", Speed: " << getSpeed() << " km/h" << endl;
    }
};
```

__Sử dụng như sau__

```bash
int main() {
    Car basicCar("Toyota", "Corolla", 180);
    basicCar.displayInfo();
```
    

### b) Tạo ra các lớp con đại diện cho các loại xe khác nhau sử dụng những thuộc tính và phương thức chung cơ bản cúa 1 chiếc xe (lớp cơ bản)

__+ Tính Kế thừa:__ 2 lớp Gascar và EletricCar sẽ sử dụng lại những thành phần được cung cấp từ lớp Car đồng thời có những thuộc tính và phương thức riêng 


```bash
class ElectricCar : public Car {
private:
    int batteryCapacity; // Dung lượng pin

public:
    // Constructor
    ElectricCar(string b, string m, int s, int battery) : Car(b, m, s), batteryCapacity(battery) {}

    // Getter và Setter cho batteryCapacity
    int getBatteryCapacity() { return batteryCapacity; }
    void setBatteryCapacity(int battery) { batteryCapacity = battery; }

    // Ghi đè phương thức displayInfo để hiển thị thêm thông tin về pin
    void displayInfo() {
        Car::displayInfo();
        cout << "Battery Capacity: " << batteryCapacity << " kWh" << endl;
    }
};
class GasCar : public Car {
public:
    GasCar(string b, string m, int s) : Car(b, m, s) {}
    void startEngine() override {
        cout << "Gas engine started!" << endl;
    }

    void stopEngine() override {
        cout << "Gas engine stopped!" << endl;
    }
};
```


__Sử dụng như sau__

```bash
int main() {
    ElectricCar tesla("Tesla", "Model 3", 200, 75);
    tesla.displayInfo();

    GasCar toyota("Toyota","Model 2",180);
    toyota.displayInfo();
```
### c) Áp dụng tính đa hình để quản lý nhiều loại xe thông qua lớp cơ sở
```bash
int main(){
     Car* type[2];
    type[0] = new ElectricCar("Tesla", "Model S", 250, 100);
    type[1] = new GasCar("Toyota","model A",180);
    //tham chiếu đến từng object và gọi ra cách triển khai method tương ứng 
    for(auto& car : type)
        car->displayInfo();
}
```

    






