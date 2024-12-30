# 1. Từ khóa goto
## 1.1 Định nghĩa 
goto có thể dùng để nhảy đến 1 label (nhãn) mà ta định nghĩa tại vị trí mà ta muốn điều hướng luồng chạy của chương trình.
## 1.2 Cách sử dụng
### a) Ứng dụng để làm điều kiện dừng
+ Ta có thể dùng goto như 1 cách để dừng việc xử lý 1 công việc nào đó như chương trình dưới đây
```bash
#include <stdio.h>
int main(){
    int cnt = 0;
    while(1){
        if(cnt > 5){
            goto stop; // nhảy đến vị trí label mà ta khai báo
        }
    printf("%d\n",cnt);
    cnt++;
    }
    stop: // khai báo label tại trị trí mà ta muốn nhảy đến
    return 0;
}
```
### b) Ứng dụng Thoát khỏi nhiều vòng lặp
+ Ta có 1 chương trình với 1 vòng for để kiểm tra 1 giá trị nào đó và ta muốn dừng vòng lặp tại 1 giá trị nào đó, thì ta có thể dùng break như sau
```bash
for(int i = 0 ; i < 5 ; i++){
    if(i == 3) break;
}
```
+ Tuy nhiên nếu có nhiều vòng for lồng vào nhau như sau thì việc sử dụng for sẽ chỉ thoát khỏi vòng lặp hiện tại 
```bash
  for(int i = 0 ; i < 10 ; i++){
        for(int j = 0 ; j < 10 ; j++){
            for(int k = 0 ; k < 10 ; k++){
                if(i == 3 && j == 5 && k == 7){
                    break;
                }
            }
            //chương trình sẽ nhảy đến vị trí này khi break được gọi
        }
    }
```
+ Chính vì vậy ta có thể sử dụng goto thay cho break ở đây để thoát khỏi toàn bộ vòng lặp
### c) Xử lý lỗi đơn giản
+ Giả sử ta sẽ thiết lập các trường hợp kiểm tra lỗi và sẽ thực thi hành động cụ thễ nếu phát hiện lỗi bằng cách sử dụng goto để nhảy đến vị trí xử lý lỗi
```bash
void process() {
    if (!initialize()) {
        goto error; // Nhảy đến xử lý lỗi nếu khởi tạo thất bại
    }
    if (!process_data()) {
        goto error; // Nhảy đến xử lý lỗi nếu xử lý dữ liệu thất bại
    }
    cleanup();
    return;

error:
    cleanup_error();
}
```

# 2. Thư viện setjmp.h
## 2.1 Định nghĩa
Đây là thư viện cung cấp các hàm như setjmp và longjmp để thực hiện nhảy giữa các hàm với mục đích là thiết kế những mã lỗi hay các thông báo mà ta muốn hiển thị tùy thuộc vào các điều kiện xử lý của chương trình

## 2.2 Đặc điểm
### a) Ưu điểm
__Lưu trữ trạng thái toàn cục:__ Cho phép nhảy qua nhiều hàm, không chỉ gới hạn trong phạm định nghĩa như goto

__Linh hoạt trong xử lý lỗi:__ Tiện lợi hơn so với goto khi xử lý các ngoại lệ và khôi phục trạng thái khi gặp lỗi

### b) Nhược điểm

__Khó bảo trì:__ Nếu quá lạm dụng có thể dẫn đến rối về cách xử lý 

__Không có cơ chế bảo vệ tài nguyên:__ bỏ qua các bước như hủy bộ nhớ hoặc giải phóng tài nguyên dẫn đến rò rỉ bộ nhớ
__

## 2.3 Cách sử dụng

+ __setjmp__ : dùng để lưu trạng thái của vị trí hiện tại(giá trị, con trỏ stack)
+ __longjmp__: dùng để nhảy ngược trở lại vị trí đã lưu bởi setjmp, 

__Ví dụ:__

```bash  
jmp_buf state_pointer;
```
+ Ta gọi hàm setjmp và truyền vào biến này và gán nó cho 1 biến với kiểu dữ liệu bất kỳ 
```bash
int state = setjmp(state_pointer);
```
+ Ta gọi hàm longjmp ở vị trí nào đó trong chương trình mà ta muốn nhảy ngược trỏ lại vị trí ta gọi hàm setjmp.
```bash
  longjmp(jmp_buf,value of state);
``` 
+ Ta sẽ viết 1 hàm để kiểm tra 1 số nguyên có phải là chẵn hay không và in ra thông báo tương ứng tương ứng
```bash    
#define ODD  2
#define EVEN 1
bool IsEven(int a){
    int result = ((a % 2) == 0 ? true : false); // nếu chia hết cho 2 thì  trả về true
    return result;
}
int main(){
    jmp_buf jump_position; //lưu vị trí sẽ nhảy tới sau này
    int a = 18;
    int state = setjmp(jump_position); // biến chứa trạng thái sẽ nhảy tới và có giá trị mặc định là 0 khi khai báo 
    int thongbao; // giá trị này sẽ được gán cho biến state sau này để thực thi các diều kiện tương ứng 
    if(state == 0){  
        bool result = IsEven(a);
        if(result) thongbao = EVEN; 
        else    thongbao = ODD;
    longjmp(jump_position,thongbao); // nhảy trở lại vị trí mà ta gọi jmp_buf 
    }
    else if(state == EVEN){
        printf("%d la so chan",a);
    }
    else if(state == ODD){
        printf("%d khong phai la so chan",a);
    }
    return 0;
}
```

# 3. So sánh goto và setjmp

<p align = "center">
<img src = "https://github.com/user-attachments/assets/dcb978ce-20d6-4eb1-ab71-eb97c49451e9" width = "1200" height = "230">
    
## 3.1 Khi nào nên sử dụng goto hay setjmp

### a) Dùng goto khi
+ Xử lý lỗi đơn giản, hoặc thoát ra khỏi nhiều vòng lặp
### b) Sử dụng setjmp khi
+ Xử lý lỗi phức tạp, cần nhảy giữa các hàm
+ Yêu cầu khôi phục trạng thái chương trình khi có lỗi



