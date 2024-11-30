# 1. template

## 1.1 Định Nghĩa 

+ cho phép viết 1 hàm tổng quát với nhiều tham số truyền vào với các kiểu dữ liệu khác nhau,
+ Cho phép định nghĩa 1 class với kiểu thuộc tính khai báo chưa xác định kiểu dũ liệu
+ ứng dụng trong thiết kế thư viện 
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
    

    


    

    