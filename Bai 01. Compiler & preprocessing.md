# 1. INCLUDE
đây là chỉ thị dùng để khai báo 1 file nguồn đã được viết sẵn, ta s4 khai báo chỉ thị này cùng với tên của file mà ta cần thêm vào chương trình chính.
+ __#include" "__ : khi file nguồn của chúng ta đặt trong " ", thì chạy chương trình, hệ thống sẽ tìm trong folder của project hiện tại có file đó không và thay thế vào chương trình

+ __#include <>__ : trong trường hợp này thì hệ thống sẽ tìm trong thư mục cài đặt gốc ở bất kỳ đâu trong máy tính để lấy ra file đó

# 2. Quá trình Compiler
Để 1 chương trình được viết bằng các ngôn ngữ bậc cao như C/C++ chạy được thì sẽ phải trải qua các bước sau. 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/e561b014-00d4-49fb-a92c-39fc23e49412" width = "500" height = "350">

### Bước 1: Tiền xử lý (Preprocessing)
Ở giai đoạn này file main.c sẽ được dịch sang file main.i bằng câu lệnh sau

```bash
 gcc -E main.c -o main.i
```
Muc tiêu của bước này sẽ là xuất ra file main.i 
+ tìm các file định nghĩa trong chỉ thì #include<> và thay thế bằng nội dung bên trong
+ thay thế các macro định nghĩa thông qua chỉ thị #define bằng nội dung mà nó định nghĩa 
+ xóa bỏ các comment trong file main.c 
### Bước 2: biên dịch (compiler) 
Lúc này từ file main.s sẽ được biên dịch sang file main.s bằng câu lệnh sau
```bash
 gcc -S main.i -o main.s
```
Mục tiêu của bước này sẽ xuất ra file main.s
+ chứa các dòng code đã được dịch từ ngôn ngữ cấp cao sang hợp ngữ để máy tính có thể hiểu và thực thi ở các bước sau
### Bước 3: dịch sang mã máy (assembler)
+ Từ file main.s sẽ được dịch sang fle main.o bằng câu lệnh sau
```bash
 gcc -c main.s -o main.o
```
Mục tiêu của bước này là xuất ra file main.o

+ chứa các đoạn code đã được mã hóa dưới dạng binary hoặc hex, để máy tính có thể xử lý 
### Bước 4: liên kết (linker)
+ Sau đó ta sẽ liên kết  các file main.o lại thành 1 file duy nhất, hay còn gọi là file exe thông qua câu lệnh sau
```bash
 gcc main.o -o main
 ```
### Bước 5: chạy chương trình
Cuối cùng ta sẽ thực hiện chạy chương trình với câu lệnh sau

```bash
./main
 ```


