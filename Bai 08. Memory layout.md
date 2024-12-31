# Memory layout
là phân vùng bố trí vùng nhớ của dữ liệu 1 chương trình được lưu trữ trên RAM khi ta tải chương trình lên. Nó sẽ chia làm 5 phần.

<p align = "center">
<img src = "https://github.com/user-attachments/assets/71fc9574-93e0-4cf0-a661-1d776b60a516" width = "500" height = "400">

## 1. Code segment
 Đây là phần vùng chỉ dọc mà không thể ghi dữ liệu, dùng để lưu:
 + các biến khai báo const
 + các chuỗi ký tự
 + mã lệnh thực thi của chương trình

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
## 2. DATA 
dùng để đọc/ghi data, lưu trữ các biến: 
+ khai báo (static/global) khác 0
+ vùng nhớ được thu hồi khi chương trình kết thúc
```bash
int a = 23;        // lưu ở data segment
static int b = 21; // lưu ở data segment
  int main(){
     static int c = 12; // lưu ở data segment
     return 0;
  }
```
### Lưu ý với struct
Khi ta khởi tạo 1 struct với các biến thành viên, khi chạy chương trình thì những biến này vẫn chưa được cấp phát vùng nhớ cho đến khi ta tạo ra biến struct 
```bash
typedef struct{
  int a;  
  int b;
}data;
static data dt = {23,12}; // 2 member a và b của struct data lúc này mới được cấp phát vùng nhớ ở data segment
```
## 3. BSS 
Vùng nhớ dùng để đọc/ghi data,lưu các biến
+ khai báo static/global được khởi tạo bằng 0, hoặc chưa gán giá trị (mặc định là 0)
+ vùng nhớ được thu hồi khi chương trình kết thúc
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
## 4. STACK
+ Vùng nhớ được cấp phát tại thời điểm biên dịch và được giải phóng khi ra khỏi phạm vi được cấp phát

__phân vùng dùng để lưu trữ:__

+ các biến khai báo cục bộ (local)
+ tham số hàm 
+ địa chỉ trả về của hàm 
+ Vùng nhớ được thu hồi khi hàm kết thúc theo cơ chế LIFO
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
### So sánh 1 biến const khi khai báo local vs global

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
## 5. HEAP
+ Vùng nhớ cấp phát tại thời điểm run-time 
+ Kích thước thay đổi được trong khi chương trình chạy 
+ được quản lý bởi người dùng thông qua các từ khóa malloc, calloc,realloc, free (sử dụng thư viện stdlib.h)
+ vùng nhớ được giải phóng bằng cách sử dụng từ khóa free

Ví dụ ta có chương trình sau để cấp phát vùng nhớ heap ở thời điểm chương trình đang chạy.
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
Khi ta chạy chương trình trên, sẽ yêu cầu ta nhập vào số lượng phần tử ví dụ size = 5, thì sau đó hàm sau đây sẽ cấp phát cho ta 1 vùng nhớ trên heap với 
+ tổng cộng là size * (kiểu dữ liệu của size) = 20 byte
+  malloc(mặc định là void*) được ép lại thành kiểu (int*) để nó biết phải lấy ra 4 byte đối với mỗi ô địa chỉ được cấp phát vùng nhớ 
+ con trỏ ptr (được khởi tạo trên stack) được trỏ tới heap để quản lý vùng nhớ vừa được khởi tạo
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
### So sánh malloc, calloc, realloc
CÚ PHÁP KHAI BÁO
### malloc 
```bash
(void*)malloc(size_t size)
```
+ Chức năng để cấp phát vùng nhớ trên heap
+ size: kích thước hoặc số lượng phần tử 
+ hàm trên sẽ trả về 1 con trỏ tới vùng nhớ vừa cáp phát trên heap có kiểu void*
### calloc
```bash
(void*)malloc(size_t count,size_t size)
```
+ Chức năng để cấp phát vùng nhớ trên heap
+ count: kích thước hoặc số lượng phần tử 
+ size: kích thước của 1 phần tử
### realloc 
```bash
(void*)realloc(void* ptr,size_t size) 
```
+ Chức năng để điều chỉnh kích thước trên heap
+ ptr: Con trỏ  tới vùng nhớ đã cấp phát trước đó
+ size: kích thước của 1 phần tử
SỬ DỤNG
+ cả 2 hàm calloc và malloc đều có cách khởi tạo giá trị giống nhau
```bash
For(int i = 0 ; i < size ; i++){
    ptr[i] = i + 3; //truy cập các ô địa chỉ trên heap thông qua chỉ số i và ghi vào dữ liệu 
}
```
+ Hàm realloc sẽ được sử dụng để điều chỉnh kính thước của vùng nhớ đã được cấp phát trước đó, và sẽ quyết định giữ lại data của vùng nhớ cũ hay không tùy thuộc vào nhu cầu
+ Ví dụ ta có chương trình sau để tăng kích thước của vùng nhớ heap đã được cấp phát trước đó như sau.
```bash
//khai báo 1 con trỏ để quản lý vùng nhớ heap được cấp phát 
  int* ptr = (int*)calloc(size,sizeof(int));

  //kiểm tra vùng nhớ được cấp phát thành công hay chưa
  if(ptr == NULL){
    printf("cap phat vung nho that bai");
    return 0;
  }
  //gán giá trị cho mỗi phần tử của vùng nhớ
  for(int i = 0 ; i < size ; i++){
      ptr[i] = i + 3;
  }
  printf("\n");

  //in ra giá trị vừa nhập
  for(int i = 0 ; i < size ; i++){
    printf("output %d:%d\n",i,ptr[i]);
  }
  //khởi tạo 1 biến lưu kích thước mới
  int new_size = size + 3;
  
  printf("\n new heap\n");
  ptr = (int*)realloc(ptr,new_size * sizeof(int));

  //gán giá trị cho phần kích thước vừa được thêm vào
  for(int i = size ; i < new_size ; i++){
    ptr[i] = i + 3;
  }
   for(int i = 0 ; i < new_size ; i++){
    printf("output %d:%d\n",i,ptr[i]);
  }
  //giải phóng vùng nhớ sau khi sử dụng
  free(ptr);
  return 0;
```
+ Chạy chương trình trên ta được kết quả như sau
```bash
output 0:3
output 1:4
output 2:5
output 3:6
output 4:7

 new heap
output 0:3
output 1:4
output 2:5
output 3:6
output 4:7
output 5:8
output 6:9
output 7:10
```
### Phân biệt STACK và HEAP
![Capture](https://github.com/user-attachments/assets/b729ce20-051e-48f9-987c-e21d43eb7002)
### a) Khai báo các biến trên STACK để đọc dữ liệu thông qua cảm biến dht11 và đưa ra cảnh báo

```bash
typedef struct{
  float temp;
  float humi;
}dht11;
void read_dht11(dht11* mydht){
	float temp,humi; // khai báo 2 biến để lưu kết quả xủ lý
      /*
	 	 giả sử khung truyền data của dht11 được xử lý ở đây
	  */
	//lưu data đọc về vào struct
	mydht->temp = temp;
	mydht->humi = humi;
}
void control_Alarm(dht11* mydht){
//khai báo 2 biến local để đọc giá trị từ struct
    float read_temp = mydht->temp;
    float read_humi = mydht->humi;
    if(read_temp > 50 && read_humi < 60){
      // bật còi cảnh báo
    }
    else if(read_temp > 20 && read_temo <= 50){
      // do something
    }
}
int main(){
  dht11 mydht;
  read_dht11(&mydht);
  control_Alarm(&mydht);
  return 0;
}
```
### b) Sử dụng HEAP để đọc về 1 buffer trên server online nào đó và thực hiện hành đông cụ thể
Ta sẽ có 1 hàm để thực hiện việc đọc 1 buffer nào đó và trả về con trỏ tới vùng nhớ được cấp phát trên heap để lưu trữ chuỗi đọc về

```bash
char* get_data_online(char* online_buffer){
    uint8_t size = 0;
    char* ptr = online_buffer; //trỏ tới chuỗi cần đọc 
    for(int i = 0 ; ptr[i] != '\0'; i++){
        size += 1; //tính toán kích thước chuỗi
    }
	
	//cấp phát động trên heap
    char* read_buff = (char*)malloc((size + 1) * sizeof(char));

	//sao chép vào vùng nhớ heap
    for(int i = 0 ; i < size ; i++){
      read_buff[i] = ptr[i];
    }
    
	read_buff[size] = '\0'; 	//thêm ký tự kết thúc chuỗi
    return read_buff;
}
```
sau đó ta sẽ gọi hàm trên và lưu vào 1 chuỗi và thực hiện so sánh nếu giống như cmd thì sẽ thực hiện 1 công việc nào đó 
```bash
int main(){
  char* buff = "turn on led 1";
  int num = 231;
  char* read_buff = get_data_online(buff);
  if (strcmp(read_buff,"turn on led 1") == 0){
      //thực hiện bật led 
      printf("led 1 has been turned on\n"); // in ra thông báo
  }
  else printf("other commands\n");
  free(read_buff);
  return 0;
```




    
    



    
