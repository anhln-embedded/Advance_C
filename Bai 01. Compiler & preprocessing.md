# 1. INCLUDE
đây là chỉ thị dùng để khai báo 1 file nguồn đã được viết sẵn, ta s4 khai báo chỉ thị này cùng với tên của file mà ta cần thêm vào chương trình chính.
+ __#include" "__ : khi file nguồn của chúng ta đặt trong " ", thì chạy chương trình, hệ thống sẽ tìm trong folder của project hiện tại có file đó không và thay thế vào chương trình

+ __#include <>__ : trong trường hợp này thì hệ thống sẽ tìm trong thư mục cài đặt gốc ở bất kỳ đâu trong máy tính để lấy ra file đó

# 2. Quá trình Compiler
Để 1 chương trình được viết bằng các ngôn ngữ bậc cao như C/C++ chạy được thì sẽ phải trải qua các bước sau. 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/e561b014-00d4-49fb-a92c-39fc23e49412" width = "500" height = "350">

### Bước 1: Tiền xử lý (Preprocessing)

```bash
 gcc -E main.c -o main.i
```
__Xứ lý thư viện và header__

+ thay thế thư viện #include <> và file header #include"" bằng nội dung bên trong chúng

__Thay thế macro__

+ Thay thế tất cả chỉ thị #define bắng nội dung nó định nghĩa

__Xử lý điều kiện tiền xử lý__

+ Các chỉ thị như #if, #ifdef, #ifndef, #else, #endif sẽ được dùng để quyết định đoạn mã nào sẽ được giữ lại hay loại bỏ

__Xử lý comment__

+ xóa bỏ các dòng chú thích trong //comment hoặc /* comment */

__VÍ DỤ__
<p align = "center">
<img src = "https://github.com/user-attachments/assets/1a9263d1-8745-48cf-bbe0-1a4250d13a7f" width = "500" , height = "350">


### Bước 2: biên dịch (compiler) 

```bash
 gcc -S main.i -o main.s
```

+ dịch mã nguồn C sang hợp ngữ (assembly để máy tính có thể hiểu và thực thi ở các bước sau

__VÍ DỤ__

<p align = "center">
<img src ="https://github.com/user-attachments/assets/ff5cfa2b-1660-465d-884c-25a8aba30c5a" width = "550" , height = "350">

### Bước 3: Hợp dịch (assembler)

```bash
 gcc -c main.s -o main.o
```
+ dịch sang mã máy (machine code) dưới dạng binary

### Bước 4: liên kết (linker)

```bash
 gcc main.o main1.0 main2.o -o program
 ```
+ Li6n kết các file .o lại thành 1 tệp thực thi (.exe)

### Bước 5: chạy chương trình
Cuối cùng ta sẽ thực hiện chạy chương trình với câu lệnh sau

```bash
 ./program
 ```
__TÓM TÁT QUY TRÌNH__
<p align = "center">
<img src = "https://github.com/user-attachments/assets/f620fed6-d60c-4345-b740-2bc7c97d9abd"width = "600" , height = "300"> 



