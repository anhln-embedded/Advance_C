# 1. Từ khóa extern 

## 1.1 Định nghĩa
được sử dụng để thông báo cho compiler biết 1 biến được gọi và sử dụng trong file hiện tại đã được khai báo ở file khác và không cần phải định nghĩa lại
## 1.2 Bản chất
Từ khòa extern cho phép 1 tài nguyên chung được chia sẻ và sử dụng trong nhiều file của chương trình

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
## 1.4 Gọi 1 hàm trong file khác
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
+ Ta có thể sử dụng biến static để thực hiện cập nhật giá trị của 1 dữ liệu nào đó mỗi khi gọi hàm (vùng nhớ không bị giải phóng khi ra khỏi phạm vi định nghĩa)
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
sử dụng khi ta muốn lưu trữ 1 biến nào đó trong thanh ghi của CPU thay vì trên RAM, mục đích là để tăng tốc độ tính toán xử lý. 
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
## 4.1 Định nghĩa
được sử dụng trên những biến thay đổi ngoài ý muốn của chương trình . Mục đích là để tránh việc compiler hiểu nhầm những biến này không Được cập nhật trong khoảng thời gian nhất định và thực hiện xóa nó đi để tối ưu hóa chương trình chẳng hạn như trong trong các trường hợp xử lý sau đây

+ __Phần cứng__: thanh ghi của thiết bị ngoại vi

+ __Ngắt__: bién được cập nhật khi có tín hiệu tác động đến từ trong/ngoài vi điều khiển

+ __Đa luồng:__ biến được truy cập hoặc thay đổi bời 1 luòng khác
## 4.2 Bản chất
Từ khóa volatile đảm bảo rằng mỗi lần truy cập, giá trị mới nhất của biến được lấy trực tiếp từ RAM, thay vì dùng giá trị lưu trên thahh ghi
## 4.3 Tối ưu hóa chương trình là gì ? cách ngăn chặn ?
### a) Định Nghĩa
Đó là cơ chế giảm tải hoạt động cho chương trình khi nó giả định 1 biến sẽ không thay đổi giá trị trừ khi nó được sửa đổi bởi logic trong chương trình chính. Nếu compiler thấy biến không thay đổi trong logic của chương trình, nó có thể
Bỏ qua việc đọc giá trị biến từ bộ nhớ chính. 
### b) Tác động của volatile
Khi từ khóa này được khai báo , nó sẽ báo cho compiler biết rằng giá trị cũa biến có thể thay đổi bất kỳ luc nào và yêu cầu
+ __không tối ưu hóa:__ Bắt buốc đọc lại giá trị biến từ bộ nhớ chính

+ __Luôn đọc giá trị trực tiếp từ bộ nhớ chính:__ compiler phải đọc giá trị mới nhất từ bộ nhớ thay vì dùng giá trị đã lưu trong thanh ghi

## 4.3 Ưng dụng cụ thể

Giả sử ta có 1 hệ thống nhúng điều khiển bởi 1 nút nhấn được cấu hình ngắt ngoài. Mỗi khi nhấn nút, thì sẽ có tín hiệu ngắt phát biến bởi vi điều khiển, và 1 biến trạng thái sẽ được dùng để lưu sự kiện ngắt này. Trong chương trình chính sẽ xử lý những công việc dựa trên giá trĩ của biến này.

### a) Định nghĩa và khai báo biến cần thiết

```bash
#include <stdio.h>
#include <stdbool.h>

// Biến cờ được cập nhật bởi ngắt
volatile bool button_pressed = false; // Khai báo volatile vì biến này thay đổi ngoài vòng lặp chính
```

### b) Định nghĩa 1 hàm ngắt giả lập 

```bash
void button_interrupt_handler() {
    button_pressed = true; // thay đổi giá trị khi có tín hiệu ngắt
}
```

### c) Chương trình chính

```bash
int main() {
    while (1) {
        // Kiểm tra trạng thái nut nhấn
        if (button_pressed) {
            // Reset cờ
            button_pressed = false;
            
            // Xử lý sự kiện nhấn nút
            printf("Button was pressed!\n");
        }
        for (volatile int i = 0; i < 100000; i++); // Chờ giả lập
    }
    return 0;
}
```
__LƯU Ýl__ lý do phải thêm volatile khi khai báo biến i trong vòng lặp for là vì 

+ Nếu không có volatile: compiler sẽ nhận ra rằng vòng for chỉ chạy 1 số lần nhất định và không làm gì bên trong vòng lặp, do đó nó có thể loại bỏ for
+ Nếu có volatile: compiler sẽ bị buộc phải luôn luông thực hiện thực thi for. Volatile sẽ yêu cầu compiler đọc.ghi giá trị của i từ RAM trong mỗi lần lặp

# 5. So sánh các từ khóa

<p align = "center">
<img src = "https://github.com/user-attachments/assets/e86cb852-f651-4850-ad37-20508a36e83d" width = "1200" height = "230">








