# 1. Macro function

+ Là macro hoạt động như 1 hàm, được đình nghĩa bằng #define
+ Nó sẽ thay thế nội dung mà nó định nghĩa tại thời điểm biên dịch
+ các dòng của hàm được định nghĩa bên trong macro sẽ kết thúc bằng dấu \

## Ví dụ cách định nghĩa và gọi hàm thông qua macro
```bash
#include <stdio.h>
#define CREATE_FUNC(name, arg) \
    void name()                \
    {                          \
        printf(arg);           \
    }

CREATE_FUNC(test1, "Duy Pham");
CREATE_FUNC(test2, "Hoang Le");
CREATE_FUNC(test3, "Nhat Le");
/*
được thay thế bằng các dòng dưới đây tại thời điểm biên dịch
void test1() { printf("Duy Pham"); };
void test2() { printf("Hoang Le"); };
void test3() { printf("Nhat Le"); };
*/
int main()
{ 
    test1();
    test2();
    test3(); 
    return 0;
}
```
## 1.1.Macro nối chuỗi 
Macro này sử dụng toán tử ##, cho phép ghép các phần tử lại với nhau

__Lưu ý:__ giá trị khi truyền vào macro là các ký tự không nằm trong dấu nháy kép ""
__Khai báo__
```bash

#define CONCATE(name1, name2) \
    char *sensor_##name2;      \
    int data_##name1          \
```
__Sử dụng__

```bash
#include <stdio.h>
int main(){
    CONCATE(65,Temp); // thay thế bằng     char *sensor_Temp; int data_65;
    return 0;
}
```
## 1.2. Macro chuẩn hóa chuỗi từ text
Macro này sử dụng toàn tử #, cho phép ta chuẩn hóa 1 dãy các ký tự truyền vào thành chuỗi 

__Khai báo__

```bash
#define STRING_CONVERT(str) printf(#str)
```
__Sử dụng__

```bash
#include <stdio.h>
int main(){
    STRING_CONVERT(Pham Cao Duy); // kết quả in ra chuỗi Pham Cao Duy
    return 0;
}
```
## 1.3 Macro variadic 
+ Macro cho phép ta định nghĩa đối số truyền vào với số lượng không cố định, có nghĩa là bao nhiêu cũng được.
+ Nó được định nghĩa bằng cách sử dụng dấu chấm __...__ để cho thể hiện các tham số sẽ nhận vào 

__Ví dụ:__ tạo ra macro để định nghĩa 1 hàm tính tổng các đối số truyền vào với số lượng tùy ý

```bash

#define SUM(...)                  \
    int arr[] = {__VA_ARGS__, 0}; \
    int i = 0;                    \
    int tong = 0;                 \
    while (arr[i] != 0)           \
    {                             \
        tong += arr[i++];         \
    }                             \
    printf("tong:%d\n", tong);
int main()
{ 
    SUM(22, 35, 25);
    return 0;
}
```

# 2. Thư viện STDARD
Đây là thư viện cung cấp các macro để thao tác và xử lý danh sách chứa các biến đối số 
## 2.1 Các macro phổ biến sử dụng trong STDARG

__+ va_list:__ Định nghĩa 1 biến để lưu trữ danh sách các đối số ở dạng chuỗi

__+ va_start:__ Xác định điểm bắt đầu của biến lưu danh sách để xử lý

__+ va_arg:__ lấy ra đối số hiện tại mỗi lần gọi 

__+ va_copy:__ trỏ vào địa chỉ của các đối số trong biến danh sách

__+ va_end:__ giải phóng biến lưu danh sách 
## 2.2 Cách sử dụng để thao tác với 1 danh sách các đối số

### a) Khi biết trước kích thước

```bash
#include <stdio.h>
#include <stdarg.h>

//tham số thứ 2 là danh sách các đối số truyền vào
int sum(int count,...){
    va_list list;  //biến lưu danh sách đối số kiểu char*
    va_start(list,count); //xác định điểm bắt đầu của danh sách cũng chính là đối số đầu tiên 
    int sum = 0;
    while(count > 0){
        sum += va_arg(list,int); //lấy ra từng đối số và tính toán
        count--;
    }
    va_end(list); //release memory
    return sum;
}
int main(){
    int count = 5;
    int total = sum(count,12,13,15,11,15);
    printf("total: %d",total);
    return 0;
}
```
    
### b) Khi sử dụng giá trị để xác định điểm dừng của danh sách

```bash
#include <stdio.h>
#include <stdarg.h>

#define tong(...) sum(__VA_ARGS__,0)  
int sum2(int begin,...){
    va_list list;
    va_start(list,begin); 

    int result = begin; 

    int value = 0;
    while((value = va_arg(list,int)) != 0){ // nếu bằng 0 thì kết thúc xử lý
        result += value;
    }

    va_end(list);
    return result;

}
int main(){
    int total = tong(12,13,15,16);
    printf("total: %d",total);
    return 0;
}
```
    
### c) Khi sử dụng con trỏ để xác định điểm dừng của danh sách

```bash
#include <stdio.h>
#include <stdarg.h>
#define tong1(...) sum3(__VA_ARGS__,'\n') 

int sum3(int begin,...){
    va_list list; //save input arguments
    va_list check; //con trỏ để kiểm tra các biến danh sách
    
    va_start(list,begin); 
    
    /** 
     * @param: first : pointer used to loop through every argument in list
     *         second: list contains input arguments 
    
     */
    va_copy(check,list); 

    int result = count; //save the first element to result

    int value = 0;
    while(va_arg(check,char*) != (char*)'\n'){ //nếu gặp ký tự kết thúc chuỗi thì dừng xử lý -> vì biến danh sách thuộc kiểu char* 
        result += va_arg(list,int);
    }

    va_end(list);
    return result;

}
int main(){
    int total = tong(12,0,11,0,15);
    printf("total: %d",total);
    return 0;
}
```

### d) Được định nghĩa trong 1 struct

```bash
typedef struct Data
{
    float data;
    char *name;
} sensor_info;

void display(int count, ...)
{

    va_list data_list;
    va_list check;

    va_start(data_list, count);

    while (count > 0)
    {
        sensor_info tmp = va_arg(data_list, sensor_info);
        printf("sensor: %s\t", tmp.name);
        printf("data: %.2f\n", tmp.data);
        count--;
    }
    va_end(data_list);
}
int main()
{
    sensor_info humi = {.name = "Humidity",.data = 23.45 };
    sensor_info temper = {.name = "temperature",.data = 67.45 };
    sensor_info speed = {.name = "Speed",.data = 102.21};
    display(3,humi,temper,speed);
    return 0;
}
```
# 3. Thư viện ASSERT
Đây là thư viện cung cấp các hàm giúp ta thiết kế các mã lỗi để giúp cho quá trình debug và sửa lỗi nhanh chóng hiệu quả. Với các tính năng như
+ Nó cho ta biết Đó là loại lỗi gì ? nằm ở đâu trong chương trình ?
+ Dừng hẳn chương trình nếu phát hiện lỗi

## 3.1 Cách sử dụng

### a) Kiểm tra giá trị có hợp lệ 

__Sử dụng trưc tiếp hàm assert__

```bash
#include<assert.h>
#include<stdio.h>

double divide(int mau,int tu){
    assert(mau != 0 && "mau phai khac 0"); //nội dung bên trong sẽ được in ra nếu giá trị không hợp lệ
    return (double)mau/tu;
}
int main(){
    double result = divide(0,21); 
    printf("%.2f",result);
}
```

__Sử dụng hàm assert thông qua macro__

```bash
#include<assert.h>
#include<stdio.h>

#define LOG(condition,cmd) assert(condition && #cmd) // ký tự # cho phép chuẩn hóa lên chuỗi

double divide(int mau,int tu){
    LOG(mau=0,mau phai khac 0);
    return (double)mau/tu;
}
int main(){
    double result = divide(0,21); 
    printf("%.2f",result);
}
```

### b) Kiểm tra giá trị có nằm trong khoảng cho phép

```bash
#include<assert.h>
#include<stdio.h>

#define LOG_IN_RANGE(val,min,max) assert((val) >= (min) && (val) <= (max))

void check_inRange(int val){
    LOG_IN_RANGE(val,1,10);
    printf("%d in range",val);

}
int main(){
        check_inRange(154);
}
```





