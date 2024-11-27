# 1. Tổng quan về Pointer
## 1.1 Khái niệm
Con trỏ là 1 biến dùng để lưu trữ địa chỉ của 1 biến khác hoặc 1 đối tượng như hàm, mảng, struct

## 1.2 Cách dùng thông thường 
con trỏ p sẽ trỏ tới biến a ngay khi nó được khởi tạo
```bash
  int a = 34;
  int* p = &a;
```
giá trị của con trỏ p chính là địa chỉ của biến a, trong khi sử dụng toán tử truy xuất * sẽ in ra giá trị tại địa chỉ đó
```bash
  printf("address of a:%p\n",p);
  printf("value of a:%d",*p);
```
## 1.3 Kích thước:
phụ thuộc vào hệ điều hành. 8 byte(64bit) và 4 byte (32bit)
- kích thước của con trỏ p được in bằng cách sử dụng hàm sizeof()
- Con trỏ p được khai báo là NULL khi chưa được gán địa chỉ cụ thể, để không trỏ tới địa chỉ rác gây ra lỗi không xác định

```bash
  int* p = NULL;
  printf("size of a:%d\n",sizeof(p));
```
## 1.4 Kiểu dữ liệu của con trỏ: 
kiểu dữ liệu mà con trỏ được khai báo cho biết số byte mà nó truy xuất hay đọc ra trong 1 lần. Ta có ví dụ sau đây để minh họa về kiểu dữ liệu của 1 con trỏ 

```bash
#include<stdio.h>
#include<stdint.h>
void tach_byte(){
    uint16_t sum = 0xabcd;
    uint8_t* px = (uint8_t*)&sum; 
    uint8_t bit_low = *px;
    uint8_t bit_high = *(px + 1);
    printf("2 bit cao: 0x%x\n 2 bit thap: 0x%x",bit_high,bit_low);
}
int main(){
    tach_byte();
    return 0;
}
```
chương trình trên sử dụng con trỏ để tách 1 biến 2 byte và lưu vào 2 biến 1 byte với cách làm như sau
+ con trỏ px sẽ trỏ tới địa chỉ của sum, và truy xuất 1 lần 1 byte do nó được khai báo là uint8_t, và lưu giá trị mà nó truy xuất vào biến bit_low
```bash
  uint8_t* px = (uint8_t*)&sum; 
  uint8_t bit_low = *px;
```
+ con trỏ px sẽ di chuyển đến byte tiếp theo của sum, và lưu giá trị mà nó truy xuất vào bit_high
```bash
   uint8_t bit_high = *(px + 1);
```
kết quả
```bash
2 bit cao: 0xab 
2 bit thap: 0xcd
```
# 2. Ứng Dụng của con trỏ 
## 2.1 CON TRỎ VÀ MẢNG 
con trỏ có thể được dùng để thao tác với các phần tử trong mảng bằng cách trỏ đến địa chỉ của mảng hay nói cách khác là địa chỉ đầu tiên trong mảng đó. 
```bash
int arr[] = {2,4,6,8,10};
int* px = &arr; //hoặc arr
```
các phần tử trong mảng có thể được truy cập thông qua việc di chuyển địa chỉ của con trỏ px
```bash
for(int i = 0 ; i < 5 ; i++){
  printf("index %d: %d/n",i,*(px + i));
}
```
kết quả
```bash
 index 0: 2
 index 1: 4
 index 2: 6
 index 3: 8
 index 4: 10
```
__Ứng dụng:__ Khi ta cần truyền 1 mảng vào trong hàm để xử lý thì ta chỉ cần truyền địa chỉ của nó và dùng 1 con trỏ như là tham số của hàm, lúc này con trỏ sẽ trỏ tới địa chỉ của mảng ta muốn xử lý chứ không phải truyền toàn bộ mảng vào hàm làm tốn tài nguyên của chương trình 
## 2.2 CON TRỎ HẰNG (POINTER TO CONSTANT)
con trỏ tới vùng nhớ chỉ có chức năng read-only mà không thể thay đổi giá trị tại địa chỉ đó, tuy nhiên nó có thể trỏ tới địa chỉ khác
```bash
int a = 23, b = 78;
const int* p = &a;
printf("truoc *p: %d\n",*p);
//*p = 23; -> sai
p = &b;
printf("sau *p: %d\n",*p);
```
ket qua
```bash
truoc: 23
sau: 78
```
__Ứng dụng:__ ta có thể sử dụng con trỏ hằng để bảo vệ những dữ liệu quan trọng mà ta không muốn bị tác động  thay đổi trong quá trình thực thi chương trình 
## 2.3 HẰNG CON TRỎ (CONSTANT POINTER)
con trỏ có thể thay đổi giá trị của vùng nhớ mà nó trỏ đến nhưng không thể trỏ tới vùng nhớ khác
```bash
int a = 23, b = 78;
int* const p = &a;
printf("truoc *p: %d\n",*p);
//p = &b; -> sai
*p = 45;
printf("sau *p: %d\n",*p);
```
kết quả
```bash
truoc: 23
sau: 45
```
__Ứng dụng:__ Hằng con trỏ có thể được dùng để lưu trữ địa chỉ cúa 1 thanh ghi và chỉ thao tác với các giá trị trên thanh ghi đó, giúp tách biệt và xử lý chính xác trên thanh ghi mà ta mong muốn 
## 2.4 CON TRỎ VÔ ĐỊNH (VOID POINTER)
con trỏ có thể trỏ tới bất kỳ kiểu dữ liệu nào
+ con trỏ p dưới đây sau khi trỏ tới biến a sẽ được ép lại theo kiểu dữ liệu mà nó trỏ tới và dùng toán tử truy xuất * để lấy ra giá trị tại địa chỉ đó
```bash
int a = 43;
void* p = &a;
printf("%d",*((int*)p));
```
+ Con trỏ void cũng có thể dùng để trỏ tới 1 mảng lưu trữ nhiều giá trị đa dữ liệu
```bash
    double c = 765656.65653;
    float d = 23.54;
    int e = 21;
    char f = 'e';
    void* ph[] = {&c,&d,&e,&f};
    printf("c = %lf\n",*((double*)ph[0]));
    printf("d = %.2f\n",*((float*)ph[1]));
    printf("e = %d\n",*((int*)ph[2]));
    printf("f = %c\n",*((char*)ph[3])); 
```
kết quả
```bash
c = 765656.656530
d = 23.54
e = 21
f = e
```
__Ứng dụng:__ Con trỏ void có thể được dùng để truyền nhiều loại dữ liệu khác nhau mà không cần phải viết lại hàm cho mỗi loại riêng biệt, giúp tối ưu và rút gọn chương trình 
## 2. CON TRỎ HÀM (FUNCTION POINTER)
con trỏ lưu địa chỉ của 1 hàm, có cấu trúc khai báo như sau
```bash
cách khai báo: (*pointer_name)(input parameter)
```
+ Ta có thể gọi 1 hàm thông qua con trỏ như sau 
```bash
void print(){
  printf("hello world");
}
int main(){
  void (*ptr)();
  ptr = print; //gán địa chỉ hàm print cho con trỏ ptr
  ptr(); //gọi con trỏ ptr để thực hiện hàm print
}
```
+ Ta có thể gọi nhiều hàm thông qua việc trỏ tới từng hàm như sau
### CÁCH 1
```bash
//định nghĩa các hàm
void Tong(int a,int b){
    printf("%d + %d = %d\n",a,b,a + b);
}
void Hieu(int a,int b){
    printf("%d - %d = %d\n",a,b,a - b);
}
void Tich(int a,int b){
    printf("%d x %d = %d\n",a,b,a*b);

}
void Thuong(int a,int b){
    if(b != 0)
       printf("%d / %d = %.2f\n",a,b,(float)a/b);
    else printf("value of b is invalid\n");
}
```
+ trong hàm main ta khai báo 1 con trỏ kiểu void với 2 tham số tryền và lần lượt trỏ tới từng hàm và truyền vào các giá trị để thực thi như sau
  void (*operator)(int,int);
```bash
int main(){
  void (*operator)(int,int);
  operator = Tong;
  operator(34,56);

  operator = Hieu;
  (*operator)(84,96);

  operator = Tich;
  operator(34,5);

  operator = Thuong;
  operator(34,12);
  return 0;
}
```
kết quả
```bash
34 + 56 = 90
84 - 96 = -12
34 x 5 = 170
34 / 12 = 2.83
```
### CÁCH 2
+ Ngoài ra ta cũng có thể sử dụng con trỏ hàm như là 1 đối số truyền vào, bằng cách sau
```bash
void Operator(void (*op)(int,int),int a,int b){
    op(a,b);
}
```
+ ta sẽ gọi hàm trên ở trong hàm main, và lân lượt truyèn địa chỉ các hàm vào, cùng với các giá trị để tính toán là a và bit_high
```bash
int main(){
  int a = 23 , b = 2;
  void (*operator)(int,int);
  Operator(Tong,a,b);
  Operator(Hieu,a,b);
  Operator(Tich,a,b);
  Operator(Thuong,a,b);
  return 0;
}
```
### CÁCH 3
+ Ta cũng có thể tạo ra 1 mảng con trỏ hàm để trỏ tới từng địa chỉ của các hàm và sử dụng chúng như sau
```bash
int main(){
 void (*opeArr[])(int,int) = {Tong,Hieu,Tich,Thuong};
    for(int n = 0 ; n < 4 ; n++){
        opeArr[n](a,b);
    }
return 0;
}
```
+ ta truy cập và gọi ra các hàm thông qua việc sử dụng chỉ số và tăng giá trị của nó mỗi khi di chuyển đến địa chỉ của hàm tiếp theo

__Ứng dụng:__ Ta có thể dùng con trỏ hàm ứng dụng trong việc chọn hàm mà ta muốn xử lý ở những thời điểm khác nhau trong chương trình thông qua 1 con trỏ duy nhất, giúp tăng tốc và tiết kiệm thời gian gọi mỗi hàm thông qua việc truy cập chúng bằng con trỏ
