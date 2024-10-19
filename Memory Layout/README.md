# Memory layout
là phân vùng bố trí vùng nhớ của dữ liệu 1 chương trình được lưu trữ trên RAM khi ta tải chương trình lên. Nó sẽ chia làm 5 phần.
![image](https://github.com/user-attachments/assets/349ecec2-7d50-4433-9a1c-4ffa38bc36c0)
## Code segment
Đây là phần dùng để lưu trữ mã lệnh thực thi của chương trình cũng như các biến được khai báo với từ khóa const hay các chuỗi được trỏ tói bởi con trỏ.
+ Phân vùng này chí có chức năng là read-only, và không cho phép thay đổi nội dung bên trong
```bash
 const int a = 23;
 int main(){
  a = 14; // wrong -> read-only
  return 0;
 }
```
ví dụ trên là 1 minh họa của 1 biến được khai báo const, khi ta thực hiện thay đổi giá trị thì compiler sẽ báo lỗi ngay lập tức
```bash
 char* str = "Hello world";
 int main(){
  str[3] = 'y'; // wrong
  return 0;
 }
```
Tương tự đối với trường hợp thay đổi nội dung của 1 chuỗi mà được trỏ tới bởi 1 con trỏ là không thể được
## BSS 
Đây là nơi cấp phát vùng nhờ cho các biến mà chưa được khởi tạo giá trị , hoặc khởi tạo bằng 0 khi:
+ khai báo global
+ khai báo static (global + local)
=> BSS có thể đọc/ghi data (vùng nhớ chỉchỉ giải phóng khi chương trình kết thúc)
Ta có ví dụ sau minh họa cho việc sử dụng BSS
```bash
 int a;        // global -> uninitialized  
 static int b; // static global -> uninitialized
 int c = 0;    // global -> intialized 0
 int main(){
  static int e; //local static -> uninitialized
    printf("a:%d\n",a);
    printf("b:%d\n",b);
    printf("c:%d\n",c);
    printf("c:%d\n",c);
  return 0;
 }
```
Tất cả 4 biến trên khi in ra đều sẽ có giá trị bằng 0
## DATA 
Vùng nhớ này cũng tương tự như BSS, nhưng nó dùng để lưu những biến được khởi tạo khác 0
=> DATA có thể đọc/ghi data (vùng nhớ chỉ giải phóng khi chương trình kết thúc)
```bash
int a = 23;        // lưu ở data segment
static int b = 21; // lưu ở data segment
  int main(){
     static int c = 12; // lưu ở data segment
     return 0;
  }
```
## STACK
Đây là phân vùng dùng để lưu trữ: 
+ các biến khai báo cục bộ (local)
+ tham số hàm 
+ địa chỉ trả về của hàm 
Khi 1 hàm được gọi thì toàn bộ thông tin của hàm đó bao gồm các giá trị trên sẽ được push lên stack và cấp phát cho 1 vùng nhớ để lưu trữ và sẽ được giải phóng khi hàm thực thi xong. 
=> STACK có thể đọc/ghi data (tồn tại từ lúc cấp phát đến khi thoát khỏi hàm)
+ Ví dụ dưới đây sẽ mô tả cách mà stack được gọi:
```bash
  void swap(int a,int b){
    int temp = a;
    a = b;
    b = temp; 
  }
  int main(){
     int a = 23,b = 78;
     swap(a,b);
  }
```
+ Khi ta truyền giá trị a,b vào trong hàm swap, thực chất ta chỉ đang truyền bản copy của chúng
+ Khi hàm swap được gọi, địa chỉ của nó sẽ được đẩy lên stack, và các giá trị copy của tham số truyền vào cũng như các biến cục bộ bên trong swap sẽ được cấp phát vùng nhớ riêng biệt
+ Chính vì vậy quá trình tính toán xử lý bên trong swap sẽ không ảnh hưởng đến giá trị bên ngoài phạm vi của nó

### Stack trỏ đến code segment
Khi ta khai báo như sau 
```bash
  int main(){
  char* str = "hello world"; // stack trỏ đến code segment
  char pstr[] = "hello world"; //cấp phát toàn bộ trên stack
  str[0] = 'g'; //wrong -> can't modify read-only memory
    return 0;
  }
```
+ con trỏ str sẽ được lưu trên stack
+ chuỗi "hello world" mà str trỏ đến sẽ được lưu ở code segment
## So sánh 1 biến const khi khai báo local vs global
khi ta khai báo 1 biến const ở phạm vi local, nó sẽ được lưu trên stack và không thể thay đổi được giá trị. Tuy nhiên dùng 1 con trỏ để truy cập vào địa chỉ của nó thì vẫn thay đổi được

```bash
 const int b = 12;
 int main(){
 const int a = 23;
 a = 34; //wrong -> can't modify value
 int* p = &a;
 *p = 16; //true
 p = &b;
 *p = 15; //wrong -> can't modify value
 }
```
+ Việc chỉnh sửa giá trị của 1 biến const cục bộ thông qua con trỏ sẽ khiến compiler đưa ra cảnh báo nhưng vẫn thực hiện được
+ Đối với biến const toàn cục, thì ta không thể thay đổi giá trị của nó như làm với biến local. 
# HEAP
Vùng nhớ được quản lý bởi người dùng thông qua 1 con trỏ. Không chịu sử quản lý bởi chương trình. Được cấp phát và giải phóng thông qua các từ khóa malloc, calloc, recalloc, free 
+ các từ khóa trên được sử dụng thông qua thư viện #inlude <stdlib.h>
## Dynamic memory allocation
Đây là kỹ thuật dùng để cấp phát vùng nhớ trên heap, mục địch là thay đổi kích thước của vùng nhớ trong lúc chương trình đang chạy, giúp tối ưu được kích thước cần dùng mà không bị cấp phát dư như sử dụng stack 
+ Ví dụ ta có chương trình sau để cấp phát vùng nhớ heap ở thời điểm chương trình đang chạy.
```bash
 #include <stdio.h>
 #include <stdlib.h>

int main(){
  int size;
  printf("nhap so phan tu:");
  scanf("%d",&size);
  //khai báo 1 con trỏ để quản lý vùng nhớ heap được cấp phát 
  int* ptr = (int*)malloc(size * sizeof(int));

  //kiểm tra vùng nhớ được cấp phát thành công hay chưa
  if(ptr == NULL){
    printf("cap phat vung nho that bai");
    return 0;
  }

  //gán giá trị cho mỗi phần tử của vùng nhớ
  for(int i = 0 ; i < size ; i++){
    printf("input %d:",i);
    scanf("%d",&ptr[i]);
  }
  printf("\n");

  //in ra giá trị vừa nhập
  for(int i = 0 ; i < size ; i++){
    printf("output %d:%d\n",i,ptr[i]);
  }
  
  //giải phóng vùng nhớ sau khi sử dụng để tránh lỗi memory leak
  free(ptr);
  return 0;
 }
```
+ Khi ta chạy chương trình trên, sẽ yêu cầu ta nhập vào số lượng phần tử ví dụ size = 5, thì sau đó hàm sau đây sẽ cấp phát cho ta 1 vùng nhớ trên heap với tổng cộng là size * (kiểu dữ liệu của size) = 20 byte
```bash
  int* ptr = (int*)malloc(size * sizeof(int));
```
+ Sau đó ta phải kiểm tra liệu địa chỉ trỏ tới vùng nhớ hiện tại có hợp lệ hay không để tránh việc cấp phát vùng nhớ thất bại
```bash
 if(ptr == NULL){
    printf("cap phat vung nho that bai");
    return 0;
  }
```
+ Tiếp theo ta sử dụng chỉ số để truy xuất vào giá trị của các phần tử được cấp phát trên heap để gán giá trị
```bash
  for(int i = 0 ; i < size ; i++){
    printf("input %d:",i);
    scanf("%d",&ptr[i]);
  }
```
+ Cuối cùng ta sẽ in ra giá trị, và thu hồi vùng nhớ sau khi đã sử dụng xong bằng từ khóa free
```bash
  for(int i = 0 ; i < size ; i++){
    printf("output %d:%d\n",i,ptr[i]);
  }
  
  //giải phóng vùng nhớ sau khi sử dụng để tránh lỗi memory leak
  free(ptr);
```


    
    



    
