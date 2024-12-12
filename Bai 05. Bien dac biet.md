
# 1. Từ khóa extern 

được sử dụng để thông báo cho compiler biết 1 biến được gọi và sử dụng trong file hiện tại đã được khai báo ở file khác và không cần phải định nghĩa lại
+ file lib.c
```bash
 int a = 34;
```
+ file main.c
```bash
  Extern int a; 
  int main(){
    printf("%d",a);
    return 0;
  }
```
## 1.1 Mục đích 
sử dụng extern khi chúng ta chỉ muốn sử dụng 1 số biến nhất định ở trong 1 file khác mà không cần đến toàn bộ nội dung, tránh việc include toàn bộ file đó vào file main hiện tại có thể làm lãng phí tài nguyên và chậm quá trình biên dịch
## 1.2 Gọi 1 hàm trong file khác
Đối với việc gọi 1 hàm nào đó, từ 1 file khác thì ta không cần sử dụng từ khóa static mà sử dụng trực tiếp trong file main hiện tại
+ file output.c
```bash
 #include<stdio.h>
 int sensor = 34;
 void printdata(int sensor){
      printf("%d".sensor);
 }
```
+ file main.c
```bash
 #include<stdio.h>
 void printdata(int); // khai báo function prototype 
 extern int sensor;   // gọi biến từ file khác 
 int main(){
    printdata(sensor); //sử dụng hàm
    return 0;
 }
```
# 2. Từ khóa static 
## 2.1 biến static được khai báo local
1 biến sẽ được cấp phát vùng nhớ tồn tại xuyên suốt thời gian chạy chương trình và có phạm vi sử dụng bên trong 1 hàm
+ Ta có thể sử dụng biến static để thực hiện cập nhật giá trị của 1 dữ liệu nào đó mỗi khi gọi hàm 
```bash
#include<stdio.h>
void update(int count){
    static int data = 25; 
    printf("lan %d = %d\n",count,data++);
}
```
+ trong hàm update ta tạo ra 1 biến static với giá trị ban đầu là 25 và in ra giá trị của nó đồng thời tăng lên 1 đơn vị. với tham số count sẽ đếm số lần hàm được gọi thông qua đối số truyền vào trong hàm main
```bash
int main(){
    for(int i = 0 ; i < 5 ; i++){
         update(i + 1);
    }
    return 0;
}
```
+ Ở trong hàm main ta dùng 1 vòng lặp for để chạy chương trình với số làn nhất định, và truyền vào đối số i + 1 cho biến số lần in ra hiện tại của hàm update. Thực hiện chạy chương trình ta có kết quả sau
```bash
lan 1 = 25
lan 2 = 26
lan 3 = 27
lan 4 = 28
lan 5 = 29
```
## 2.2 biến hoặc hàm static được khai báo global
điều này cho biết biến hoặc hàm đó chỉ có thể gọi và sử dụng trong file hiện tại mà không thể gọi thông qua các file khác nhằm giới hạn quyền truy cập và đảm bảo biến hoặc hàm đó không thể thay đổi ngoài phạm vi cho phép 
. Ví dụ ta viết 1 chương trình tính toán 2 phân số như sau
+ file lib.h
```bash
typedef struct{
    int mauso;
    int tuso;
}phanso;
static phanso nhan2ps(phanso ps_a,phanso ps_b);
void print(phanso ps_a,phanso ps_b);
```
trong file trên ta tạo ra 1 struct để định nghĩa các thành phần của phân số và khai báo các function prototype
+ file calculation.c 
```bash
#include"lib.h"
#include<stdio.h>
static phanso nhan2ps(phanso ps_a,phanso ps_b){
    phanso sum;
    sum.mauso = ps_a.mauso * ps_b.mauso;
    sum.tuso = ps_a.tuso * ps_b.tuso;
    return sum;
}

void print(phanso ps_a,phanso ps_b){
    phanso ketqua = tinhtoan(ps_a,ps_b);
    printf("%d/%d * %d/%d = %d/%d",
                            ps_a.mauso,ps_a.tuso,
                            ps_b.mauso,ps_b.tuso,
                            ketqua.mauso,ketqua.tuso);
}
```
trong file trên ta định nghĩa 2 hàm, với 1 hàm dùng để tính toán và 1 hàm để hiển thị kết quả sẽ được gọi trong chương trình chính cùng với các đối số truyèn vào.
+ file main.c
```bash
#include"lib.h"
int main(){
    phanso psa = {23,21};
    phanso psb = {35,27};
    print(psa,psb);
    return 0;
}
```
trong hàm trên ta đã khai báo 2 phân số và truyền vào hàm print để in ra kết quả nhưng không thể gọi tới hàm nhan2ps để xem được cụ thể bên trong
# 3. Từ khóa register
sử dụng khi ta muốn lưu trữ 1 biến nào đó trong thanh ghi thay vì trên RAM, mục đích là để tăng tốc độ tính toán xử lý. 
```bash
#include<stdio.h>
#include<time.h>
int main(){
    //gán thời gian bắt đầu
    clock_t start = clock();

    //khai báo biến để kiểm tra
    register int data = 0;

    //thực hiện công việc nào đó
    for( ;data < 5000000;data++);

    //gán thời gian kết thúc
    clock_t end = clock();
    
    //in ra thời gian xử lý 
    double time_differece = ((double)(end - start)/CLOCKS_PER_SEC);
    printf("time : %f",time_differece);

    return 0;
}
```
hàm trên sẽ đo thời gian thực thi của vòng lặp đối với biến i khi khai báo là register. Nếu ta không khai báo biến i là register thì khi in ra kết quả sẽ có sự chênh lệch thời gian. Trong trường hợp khai báo là register thì khi ra kết quả thời gian sẽ nhỏ hơn khi không khai báo là register
# 4. Từ khóa volatile 
được sử dụng trên những biến thay đổi ngẫu nhiên bởi mà không chịu sự chia phối bơi chương trình chính. Mục đích là để tránh việc compiler hiểu nhầm biến này không được sử dụng và xóa nó đi để tối ưu hóa chương trình. 





