# 1. Khái niệm
+ Class là kiểu dữ liệu tự định nghĩa bỡi người dùng để quản lý và mô phỏng các đặc điểm của 1 đối tượng cụ thể nào đó chứa các biến và hàm bên trong. Có thể nói nó là 1 phiên bản nâng cấp của struct và union.
# 2. Đặc điểm
+ Trong class các biến và hàm được định nghĩa là

__property(thuộc tính) và method(phương thức)__

+ Class được quản lý dựa trên 3 phạm vi là 

__Public, private, protected__

+ Khi khai báo 1 class các thành phần của nó sẽ luôn mặc định là private (không thể truy cập từ bên ngoài class thông qua object)

# 3. Các Thao tác với class
Khi khai báo 1 class ta cần chú ý
__+ Khai báo private:__ đối với các properties khi ta muốn đảm bảo an toàn dữ liệu  
__+ Khai báo public:__ đối với các method, được gọi và sử dũng bên ngoài class
## 3.1 Tạo 1 object class và truy cập vào các properties và method
+ Ta sẽ tạo 1 class dùng để định nghĩa 1 Person, cũng như khai báo và in ra thông tin của người đó như sau

```bash
#include <iostream>  //thư viên C++
using namespace std; // cú pháp cho phép những hàm tiêu chuẩn như cout, cin 
class Person{
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
    Person person1;
    person1.setName("Pham Cao duy");
    person1.setAge(17);
    //in ra thong tin
    cout << "name: " << person1.getName << endl;
    cout << "age: " << person1.getAge << endl;
    return 0;
}
```
## 3.3 Constructor và DeConstructor 
### a) Construct (hàm tạo)
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
### b) DeConstructor (hàm hủy)
+ Được sử dụng để hủy 1 constructor. Destructor có cùng tên với constructor và được thêm vào dấu ~ phía trước. Khi khai báo destructor trong class, khi chương trình kết thức chúng sẽ được gọi tự động và giải phóng các constructor theo cơ chế LIFO

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
## 3.4 method và property static 
các method trong class khi được khai báo là static
+ có thể truy cập trực tiếp thông qua tên class
+ được cấp phát vùng nhớ khi ta gọi nó thông qua tên class ở ngoài class (lúc này ta mới sử dụng được property này)
+ chỉ được truy cập thông qua static method
    
```bash
class Person{
  private:
    string name;
    int age;
    static int total;
  public:
    Person(string _name , int _age){
        name = _name;
        age = _age;
        total += 1; //đếm só lượng object
    }
    static void print_total(){
        cout << "total of objects: << total << endl;
    }
};
int Person :: total = 0//cấp phát địa chỉ lưu ở data segment
int main(){
    Person person1("Duy Pham",30);
    Person person2("Hoang Le",38);
    Person person3("Tuan Dinh",22);
    Person :: print_total();
}
```
+ Kết quả in ra ta được __total of objects: 3__

## 3.5 Con trỏ this và toán tữ phạm vi ::
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
## 3.6 Function Overloading và OverOperator (xử lý ở quá trình compile time)
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
Đây là định nghĩa liên quan đến nạp chồng toán tử, được sử dụng khi ta muốn định nghĩa lại những phép toán logic thành các kiểu tiêu chuẩn hơn để thực hiện quá trình tính toán, so sánh giữa các kiểu dữ liệu không phải nguyên thủy ví dụ như nhân 2 phân số
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

## 3.7 Pass by value(tham trị) và Pass by reference(tham chiếu)

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
+ Đối với hàm calculate khi ta truyền trực tiếp giá trị cùa biến write (pass by value) thì để cập nhật giá trị thay đổi trong hàm này ta cần phải sử dụng từ khóa return và sửa đổi kiểu trả về của hàm. Viêc pass by value cũng gây phát sinh vùng nhớ, lãng phí tài nguyên trên RAM

+ ở hàm write_and_read, 2 đối số truyền vào hàm chính là địa chỉ của chúng để xử lý, vì vậy không gây phát sinh thêm bất kỳ vùng nhớ nào

+ biến compare_value được truyền vào theo kiểu là 1 tham chiếu const cho biết nó chỉ được dùng để đọc ra chứ không cho phép thay đổi giá trị

+ biến write_value được truyền vào như là 1 tham chiếu để cập nhật giá trị dựa trên giá trị của compare_value
# 4. Các thao tác với OOP trong class
## 4.1 Inheritance (Tính kế thừa)
+ Đây là khả năng tái xử dụng lại các method và properties từ class gốc từ các class con kề thừa từ nó, giúp ta tối ưu và rót gọn chương trình
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
    hocsinh hs1("Trinh Le Hoang",22,"12A1");
    sinhvien sv1("Pham Cao Duy",29,"Mechatronics Engineer");

    hs1.printInfo();
    sv1.printInfo();
}
```
+ class hocsinh và sinhvien sẽ kế thừa các thông tin cơ bãn từ class person và bổ sung thêm các thuộc tính đặc trưng 
+ 2 thuộc tính ten,tuoi ở class person được để ở quyền truy cập protected cho phép nó có thể sử dụng ở class kết thừa
+ hàm printInfo ở class person sẽ được ghi đè nội dung ở class kế thừa

## 4.2 Encapsulation (tính đóng gói)
+ Đây là khả năng giới hạn việc truy cập vào các thuộc tính được định nghĩa trong class bằng việc cài đặt chế độ private cho chúng, nhằm đảm bảo an toàn về những dữ liệu mà ta không muốn bị thay đổi trực tiếp ngoài phạm vi class

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
    sinhvien(string name, float dtoan, float dvan)
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
+ Ta định nghĩa 1 class sinhvien chứa các method để tính điểm trung bình và xếp hạng dựa vào các giá trị sẽ được truyền vào khi tạo ra 1 object class
+ 2 giá trị stb, rank không thể trực tiếp thay đổi vì chúng cần dựa vào các giá trị dtoan,dvan để tính toán xử lý thông qua cac method mà ta gọi ra.
## 4.3 polymorphism(tính đa hình)
+ Là khả năng truy cập vào cùng 1 method nhưng sẽ chứa các cách triển khai khác nhau tùy vào từng object mà ta định nghĩa

### a) Virtual function (Hàm ảo)
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
### b) Pure virtual function (hàm ảo thuần túy)
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
## 4.4 Abstract (Tính trừu tượng) 
+ Đây là khả năng ẩn đi những phần triển khai cụ thể của chương trình, chỉ cung cấp các interface để tương tác với các user.
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
+ Trong lớp Car ta sẽ được cung cấp 1 số interface với tính năng cụ thể để người dùng có thể tương tác nhưng phần triển khai cụ thể của nó sẽ được ẩn đi và chỉ được xử lý ở các lớp con bên dưới. 

    







