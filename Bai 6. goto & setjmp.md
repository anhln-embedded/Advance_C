# 1. Từ khóa goto
goto có thể dùng để nhảy đến 1 vi trí bất kỳ trong chương trình phụ thuộc vào label (nhãn) mà ta định nghĩa, giúp ta có thể điều khiển được luồng chạy của chương trình
## 1.1 Trường hợp 1: điều kiện dừng 
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
## 1.2 Trường hợp 2: Thoát khỏi nhiều vòng lặp
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
# 2. Thư viện setjmp.h
Đây là thư viện cung cấp các hàm như setjmp và longjmp để thiết kế những mã lỗi hay các thông báo mà ta muốn hiển thị tùy thuộc vào các điều kiện xử lý của chương trình
+ trong thư viện setjmp.h ta tìm đến phần định nghĩa sau 
```bash   
// Define the buffer type for holding the state information
#ifndef _JMP_BUF_DEFINED
    #define _JMP_BUF_DEFINED
    typedef _JBTYPE jmp_buf[_JBLEN];
#endif
```
+ Đầu tiên ta sẽ khai báo 1 biến kiểu jmp_buf để lưu trạng thái hiện tại của môi Trường
```bash  
jmp_buf state_pointer;
```
+ Ta gọi hàm setjmp và truyền vào biến này và gán nó cho 1 biến với kiểu dữ liệu bất kỳ 
```bash
int state = setjump(state_pointer);
```
+ Ta gọi hàm longjmp ở vị trí nào đó trong chương trình mà ta muốn nhảy ngược trỏ lại vị trí định nghĩa state_pointer với 2 đối số cần truyền vào như sau
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
