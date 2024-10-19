# Memory layout
là phân vùng bố trí vùng nhớ của dữ liệu 1 chương trình được lưu trữ trên RAM khi ta tải chương trình lên. Nó sẽ chia làm 5 phần.
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
    