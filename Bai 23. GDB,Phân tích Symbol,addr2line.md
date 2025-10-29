
# 1.GDB

## 1.1 Giới thiệu GDB: định nghĩa & mục đích
GDB (GNU Debugger) là một trình gỡ lỗi dòng lệnh, cho phép điều khiển luồng thực thi chương trình trong runtime, cho phép:
+ Dừng chương trình tại bất kỳ dòng nào
+ Quan sát giá trị biến, thanh ghi, call stack
+ Tìm lỗi crash, lỗi logic, lỗi pointer
+ Kiểm tra từng bước chạy (step-by-step)

## 1.2 Trình tự thao tác trong GDB

`gdb ./bug_demo.exe`	    Mở chương trình trong GDB

`start`	                    Bắt đầu chạy chương trình dừng tại main()

`break <func> hoặc break <line>`	Đặt điểm dừng

`next	`              Thực thi từng dòng (không vào hàm con)

`step`	              Bước vào trong hàm con

`print var`	          In giá trị biến

`backtrace`	          Hiện stack gọi khi crash

`run	`                  Chạy lại từ đầu

`quit`	              Thoát GDB    

## 1.3 Các lỗi phổ biến

### 1.3.1 Phân loại theo các bước xữ lý 
Các lỗi trong lập trình thường được chia thành nhiều loại và được xử lý dựa trên các bước của quá trình biên dịch 

__Preprocessing__
+ Lỗi thiếu `#include` báo lỗi thiếu định nghĩa hàm/kiểu, macro
+ lỗi khai báo nhiều lần khi thiếu `#ifndef / #pragma once`
+ Lỗi side-effect macro 

__Compilation__
+ `Syntax error` : sai/thiếu cú pháp như thiếu ';' hoặc đóng/mở ngoặc '{}' không hợp lý
+ `Semantic error` : gán sai kiểu dữ liệu 
+ `Format Specific error` : sai định dạng 
   
__Linking__
+ `redinition` : lặp định nghĩa, do include `.c` trực tiếp, thay vì `.h`
+ Khai báo biến extern chia sẻ nhiều file không hợp lệ

__Runtime__
+ `Segmentaion fault` : còn gọi là `core dump` do truy cập vùng nhớ không hợp lệ thường liên quan tới thao tác con trỏ
    => Truy cẫp Null pointer
    => dangling pointer (dùng con trỏ khi đã free)
    => truy cập giá trị ngoài phạm vi mảng
    => memory leak (rò rỉ heap do không free sau sử dụng)
+ `Logic error` : gán toán tử không hợp lệ
+ `Lỗi chi 0`
+ `threading error`: race condition, deadlock, thiếu cơ chế đồng bộ tài nguyên chung

**Ví dụ code tổng hợp lỗi**

### 1.3.2 Compiler flags để phát hiện lỗi

**Mục đích** : Ta có thể sử dụng các cờ warning để giúp phát hiện lỗi càng sớm càng tốt tại compile-time. Giúp hạn chế undefined behaviour. 

+ `"-Wall"`               : bật tất cả cảnh báo quan trọng
+ `"-Wextra"`             : Cảnh báo bổ sung như (bỏ sót biến , so sánh sai,...)
+ `"-Werro"r`             : chuyển cảnh báo thành lỗi
+ `"-Wpedantic"`          : nếu vi phạm chuẩn C ISO
+ `"-std=c11"`            : dùng chuẩn C hiện đại (C11 hoặc 17)
+ `"-02"` hoặc `"-0g"`    : tối ưu hóa
+ `"-g"`                  : tạo thông tin debug (nếu dùng gdb)
+ `"-fsanitize=undefined"`: dò __undefined behaviour__ tại runtime
+ `"-fsanitize=address"`  : dò lỗi __truy cập memory__ , __buffer overflow__ , __use-after-free__
+  `"D_FORTIFY_SOURCE=2"` : kiểm tra nâng cao cho các hàm C standard

+ **Ví dụ lỗi**

| Lỗi/Nguy cơ                                                     | Có cờ warning          | Không cờ warning |
| --------------------------------------------------------------- | ---------------------- | ---------------- |
| **Biến khai báo nhưng không dùng**                              | `-Wall`                | ❌ Không cảnh báo |
| **Hàm không trả giá trị dù có `int` return type**               | `-Wall`                | ❌ Không cảnh báo |
| **Gọi hàm `printf` sai định dạng (format string)**              | `-Wformat`             | ❌ Không cảnh báo |
| **So sánh giữa signed và unsigned**                             | `-Wextra`              | ❌ Không cảnh báo |
| **Gán kiểu không tương thích ngầm (implicit cast)**             | `-Wall`/`-Wconversion` | ❌ Không cảnh báo |
| **Thừa tham số trong lời gọi hàm**                              | `-Wall`                | ❌ Không cảnh báo |
| **Thiếu prototype hàm**                                         | `-Wmissing-prototypes` | ❌ Không cảnh báo |
| **Lỗi chính tả tên biến (do unused)**                           | `-Wall`                | ❌ Không cảnh báo |
| **Không dùng giá trị trả về của hàm quan trọng (e.g. `scanf`)** | `-Wunused-result`      | ❌ Không cảnh báo |

## 1.4 Cơ chế triển khai GDB

### 1.4.1 Dùng GDB với CL (Command Line)

+ **Vai trò**
    + Nắm rõ được bản chất của gdb, chứ không chỉ nhấn __Run and Debug__
    + Quen với sử dụng GDB ngoài IDE __(làm nhúng trên linux)__
    + Gặp lỗi phức tạp, không chạy được trên GUI, phải dùng CL
+ **Các lệnh**

__tạo file thực thi để dùng với gdb__

```c
gcc -g source.c -o output_file
```
    + -g: thêm thông tin debug để dùng với gdb.
    + -o: chỉ định tên file đầu ra (output).

__KHỞI ĐỘNG GDB__

| Lệnh                        | Chức năng                                                        |
| --------------------------- | ---------------------------------------------------------------- |
| `gdb ./program`             | Mở GDB với chương trình được biên dịch có debug symbols (`-g`).  |
| `gdb -tui ./program`        | Mở GDB với chế độ giao diện hiển thị source code trong terminal. |
| `gdb -ex "cmd1" -ex "cmd2"` | Chạy các lệnh tự động khi vào GDB.                               |

__XEM THÔNG TIN PROGRAM__

| Lệnh             | Chức năng                                |
| ---------------- | ---------------------------------------- |
| `list` hoặc `l`  | Hiển thị source code (mặc định 10 dòng). |
| `list main`      | Hiển thị code tại hàm `main`.            |
| `list 20`        | Hiển thị 10 dòng quanh dòng 20.          |
| `info functions` | Hiển thị danh sách hàm.                  |
| `info variables` | Liệt kê biến toàn cục.                   |
| `info source`    | Xem tên file đang debug.                 |
| `info files`     | Thông tin file nhị phân đã nạp.          |

__ĐẶT BREAKPOINT__

| Lệnh                          | Chức năng                                          |
| ----------------------------- | -------------------------------------------------- |
| `break main` hoặc `b main`    | Đặt breakpoint tại đầu hàm `main`.                 |
| `break 42` hoặc `b 42`        | Break tại dòng số 42 trong file hiện tại.          |
| `break file.c:20`             | Break tại dòng 20 của file `file.c`.               |
| `info breakpoints` hoặc `i b` | Danh sách breakpoint đang có.                      |
| `delete [n]`                  | Xóa breakpoint `n` hoặc tất cả nếu không chỉ định. |
| `disable n` / `enable n`      | Vô hiệu / kích hoạt breakpoint `n`.                |
| `clear`                       | Xóa breakpoint tại dòng hiện tại.                  |

__CHẠY VÀ ĐIỀU KHIỂN LUỒNG PROGRAM__

| Lệnh                | Chức năng                                  |
| ------------------- | ------------------------------------------ |
| `run` hoặc `r`      | Bắt đầu chạy chương trình.                 |
| `run arg1 arg2`     | Chạy chương trình với đối số.              |
| `continue` hoặc `c` | Tiếp tục chạy sau khi dừng tại breakpoint. |
| `step` hoặc `s`     | Bước vào từng dòng, **vào trong hàm gọi**. |
| `next` hoặc `n`     | Bước qua từng dòng, **bỏ qua thân hàm**.   |
| `finish`            | Chạy đến khi thoát khỏi hàm hiện tại.      |
| `until n`           | Chạy đến dòng `n`.                         |
| `kill`              | Kết thúc tiến trình hiện tại.              |
| `quit` hoặc `q`     | Thoát GDB.                                 |

__QUAN SÁT VÀ THAY ĐỔI BIẾN__

| Lệnh                 | Chức năng                                   |
| -------------------- | ------------------------------------------- |
| `print x` hoặc `p x` | In giá trị biến `x`.                        |
| `print *ptr`         | In nội dung con trỏ.                        |
| `set var x = 42`     | Gán lại giá trị cho biến `x`.               |
| `display x`          | Tự động in biến `x` mỗi lần dừng.           |
| `watch   x`          | Tự động hiển thị`x` nếu giá trị tha đổi.    |
| `undisplay n`        | Bỏ hiển thị tự động biến `n`.               |
| `info locals`        | Xem toàn bộ biến cục bộ trong hàm hiện tại. |
| `info args`          | Xem các tham số truyền vào hàm hiện tại.    |

__THAO TÁC TRÊN STACK__

| Lệnh                  | Chức năng                             |
| --------------------- | ------------------------------------- |
| `backtrace` hoặc `bt` | Hiển thị call stack hiện tại.         |
| `frame n`             | Di chuyển tới frame `n`.              |
| `info frame`          | Thông tin chi tiết về frame hiện tại. |
| `up` / `down`         | Di chuyển giữa các frame trong stack. |

__KIỂM TRA MEMORY VÀ ADDRESS__

| Lệnh                | Chức năng                                                              |
| ------------------- | ---------------------------------------------------------------------- |
| `x/nfu address`     | Xem nội dung bộ nhớ ở địa chỉ (`n`: số lượng, `f`: format, `u`: unit). |
| Ví dụ: `x/4xb &var` | Xem 4 byte dạng hex tại địa chỉ `var`.                                 |
| `x/s ptr`           | Xem chuỗi ký tự tại địa chỉ `ptr`.                                     |
| `x/i $pc`           | Xem lệnh máy tại địa chỉ chương trình hiện tại.                        |

+ **Ứng dụng trong Embedded bắt buộc dùng CL(không có sẵn GUI)**
    + Debug qua UART/JTAG không chính hãng (OpenOCD)	
    + Debug chip lạ (RISC-V, ESP32, RP2040…)
    + Debug từ xa (SSH vào thiết bị nhúng Linux)
    + Làm việc với CI/CD hoặc script tự độn
    + Debug core thứ 2 của chip (dual-core MCU)

### 1.4.2 Dùng GDB với GUI

+ **Chạy GDB trên giao diện Vscode**

Vscode hỗ trợ tự động cấu hình thông qua giao diện cung cấp sẵn, và khi nhấn __Run and Debug__, sẽ:
    + tự sinh `launch.json`tạm thời trong bộ nhớ (khi chọn đúng môi trường -  C/C++ (GDB/LLDB))
    + Dùng .exe gần nhất 
    + dùng cấu hình debugging mặc định

+ **Chạy GDB từ cấu hình thủ công**

__Trường hợp sủ dụng__

| Tình huống                              | Cần `launch.json`                         |
| --------------------------------------- | ----------------------------------------- |
| Truyền đối số (`argv`)                  | ✅ Có                                      |
| Thay đổi thư mục làm việc (`cwd`)       | ✅ Có                                      |
| Chạy task build trước khi debug         | ✅ Có                                      |
| Debug bằng giao diện VSCode             | ✅ Nên dùng                                |
| Debug trên nhiều chương trình khác nhau | ✅ Cần cấu hình riêng cho mỗi chương trình |

__Cấu hình launch.json__

Để cấu hình launch.json thủ công để chạy GDB trong VS Code, bạn cần tạo hoặc chỉnh sửa file .vscode/launch.json với thông tin chính xác về:
+ Đường dẫn GDB (miDebuggerPath)
+ Tên file thực thi bạn build ra (program)
+ Thư mục làm việc (cwd)

+ **Step by step**
    ```c
    1. Mở Command Palette (Ctrl+Shift+P)
    2. Gõ Debug: Open launch.json → Chọn C++ (GDB/LLDB) hoặc C/C++: gcc.exe
    3. Chọn template hoặc tạo trống
    4. Nhấn Run and Debug (icon tam giác bên trái sidebar)
    5. Chọn cấu hình "Debug with GDB"
    6. Nhấn ► hoặc F5 để bắt đầu
    ``` 

`.vscode/launch.json`
```c
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug with GDB",
            "type": "cppdbg",
            "request": "launch",
            "program": "${fileDirname}\\test0.exe",
            "args": [],
            "stopAtEntry": true,
            "cwd": "${fileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "miDebuggerPath": "C:\\MinGW\\msys64\\mingw64\\bin\\gdb.exe",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```
| Trường             | Ý nghĩa                                               |
| ------------------ | ----------------------------------------------------- |
| `"program"`        | Đường dẫn tới file `.exe` được build từ C file        |
| `"cwd"`            | Thư mục hiện tại để chạy lệnh (chứa source và binary) |
| `"miDebuggerPath"` | GDB bạn muốn sử dụng                                  |
| `"MIMode": "gdb"`  | Bắt buộc nếu dùng GDB                                 |
| `"stopAtEntry"`    | Tạm dừng ở entry point (`main()`)                     |
| `"args"`           | Tham số dòng lệnh nếu có                              |

+ **Ưu điểm**
    + __Kiểm soát và chọn 1 số thông tin cần thiết:__ binary , arguments,working directory, gdb path, env, symbol
    + __debug project lớn:__ makefile, cmake , cross-compile , embedded
    + __chạy trên mô trường embedded:__ openOCD , gdbserver


__Ví dụ: Chạy chương trình với tham số dòng lệnh__

**Thế nào là tham số dòng lệnh**

Tham số cho phép chương trình nhận đầu vào ngay lúc chạy, mà không cần phải dùng scanf. Giúp ta kiểm tra và chạy chương trình linh hoạt, dễ test,và chuyên nghiệp hơn
    + `Khai báo`
    ```c
    int main(int argc, char *argv[]) 
    ```
    + `Cú pháp` 
    ```c
    ./run.exe input.txt 123 hello
    ```
__Mô tả__

+ argc = 4 → số lượng chuỗi (bao gồm tên chương trình)
+ argv là mảng các chuỗi:
+ argv[0] = "./run.exe" (tên chương trình)
+ argv[1] = "input.txt"
+ argv[2] = "123"
+ argv[3] = "hello"

__So sánh với scanf()__

| So sánh           | Nhập từ `scanf()`             | Tham số dòng lệnh (`argv`)       |
| ----------------- | ----------------------------- | -------------------------------- |
| Cách dùng         | Người dùng gõ trong lúc chạy  | Gõ ngay khi **gọi chương trình** |
| Mục đích          | Tương tác thời gian thực      | Tự động hóa, test nhanh          |
| Ví dụ dùng        | Giao diện người dùng đơn giản | Tools, compiler, script...       |
| Độ tiện khi debug | Mất công nhập lại nhiều lần   | Gán sẵn 1 lần qua `launch.json`  |


`main.c`
    ```c
    #include <stdio.h>
    int main(int argc, char *argv[]) {
        printf("Working directory debug test\n");

        printf("Number of arguments: %d\n", argc);

        //in ra tất cả các tham số đã nhập
        for (int i = 0; i < argc; i++) {
            printf("argv[%d]: %s\n", i, argv[i]);
        }

        FILE *fp = fopen(argv[1], "r");
        if (!fp) {
            perror("Failed to open input.txt");
            return 1;
        }

        char line[100];
        while(fgets(line, sizeof(line), fp) != NULL){
            printf("Read from file: %s", line);
        }
        fclose(fp);

        return 0;
    }
    return 0;
    ```
Triển khai các tham số dòng lệnh nhập vào theo cơ chế `key: value ` giúp cho ta làm rõ được loại tham số kèm với dữ liệu cụ thể của chúng. Dựa vào đó ta không cần quan tâm đến thứ tự nhập mà chỉ cần quan tâm loại dữ liệu mà ta muốn nhập thông qua `key:` của chúng và theo sau là dữ liệu cụ thể `value`

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[])
{
    char* file_name;
    int num = 0;
    char* message;

    for (int i = 0; i < argc; i++)
    {
        if (strcmp(argv[i], "file:") == 0)
        {
            file_name = argv[++i];
        }
        else if (strcmp(argv[i], "num:") == 0)
        {
            num = atoi(argv[++i]);
        }
        else if (strcmp(argv[i], "msg:") == 0)
        {
            message = argv[++i];
        }
        else
        {
            printf("Unknown argument: %s\n", argv[i]);
        }
    }

    printf("filename: %s\n", file_name);
    printf("num: %d\n", num);
    printf("message: %s\n", message);

    FILE *fp = fopen(file_name, "r");
    if (!fp)
    {
        perror("Failed to open input.txt");
        return 1;
    }

    char line[100];
    while (fgets(line, sizeof(line), fp) != NULL)
    {
        printf("Read from file: %s", line);
    }
    fclose(fp);
}
```






### 1.4.3 So sánh chạy GDB với GUI và CL 

| Tiêu chí                      | Dùng **GUI Debugger**                   | Dùng **GDB CLI**                          |
| ----------------------------- | --------------------------------------- | ----------------------------------------- |
| ✅ Debug đơn giản, trực quan   | ✔ Rất phù hợp                           | ✘ Không cần thiết                         |
| ✅ Debug hệ thống phức tạp     | ✔ (nếu cần theo dõi nhiều biến, stack…) | ✔ Khi script hóa/automation               |
| ✅ Môi trường embedded         | ✔ Nếu hỗ trợ OpenOCD, J-Link...         | ✔ Khi cần debug từ log/crash              |
| ✅ Truy vết hậu crash log      | ✘ Không hữu ích                         | ✔ Bắt buộc (với `core dump`, `addr2line`) |
| ✅ SSH vào remote device       | ✘ Khó/không hỗ trợ                      | ✔ Chuẩn nhất                              |
| ✅ Tự động hóa hoặc CI/CD      | ✘ Không phù hợp                         | ✔ Dễ tích hợp                             |
| ✅ Khi bạn cần học và hiểu sâu | ✘ Ẩn logic nội bộ                       | ✔ Tăng kỹ năng GDB thực thụ               |

+ **Tóm lại**
    + Dùng GUI khi cần trực quan, học tập, hoặc debug code đơn giản
    + Dùng CLI (GDB) khi cần linh hoạt, phân tích chuyên sâu, làm việc với hệ thống không có GUI, hoặc tự động hóa.


# 2. addr2line 
Công cụ để ảnh xạ địa chỉ ảo từ static memory thành dòng code tương ứng trong mã nguồn dựa trên symbol table, được tạo ra khi biên dich với `-g`. Cu thể hơn là nó dựa vào thông tin debug nằm trong các section đặc biệt như .debug_line, .debug_info, .debug_abbrev (DWARF)

# 2.1 Tổng quan về addr2line
+ **Cú pháp**
-f để hiển thị tên hàm
```c
addr2line -e my_binary -f 0x080484a2
out:
main
main.c:42
```
+ **Trường hợp dủng**

| Tình huống                | Lý do dùng                                      |
| ------------------------- | ----------------------------------------------- |
| Crash log chỉ có địa chỉ  | Bạn muốn dịch địa chỉ sang dòng mã              |
| Debug không dùng GDB      | Bạn có địa chỉ nhưng không có session đang chạy |
| Embedded debug / firmware | Gỡ lỗi offline từ dump địa chỉ                  |

## 2.2 Ảnh hưởng của ASLR đến địa chỉ thực load trên RAM khi chạy runtime

### 2.2.1 ASLR là gì
+ cơ chế bảo mật của hệ điều hành, làm cho mỗi lần chương trình chạy thì địa chỉ bộ nhớ bị xáo trộn.
+ Nó giúp chống tấn công kiểu buffer overflow.
+ Nhưng khi bạn đang debug hoặc dùng addr2line, gdb, symbol table..., thì địa chỉ thay đổi khiến bạn không tra được đúng dòng code.DLL sẽ được random hóa mỗi lần chạy

=> Tắt ASLR = địa chỉ không đổi = dễ debug
### 2.2.2 So sánh giữa ASLR tắt/mở

**BÌNH THƯỜNG (ASLR OFF)**

| Tên phân vùng | Địa chỉ compile (symbol table) | Địa chỉ runtime (gdb) | Ghi chú |
| ------------- | ------------------------------ | --------------------- | ------- |
| `.text`       | 0x00401000                     | 0x00401000            | Khớp    |
| `.data`       | 0x00403000                     | 0x00403000            | Khớp    |
| `.bss`        | 0x00404000                     | 0x00404000            | Khớp    |

**Khi ASLR ON (EXE có DYNAMIC_BASE)**

| Tên phân vùng | Địa chỉ compile (symbol table) | Địa chỉ runtime (gdb) | Ghi chú            |
| ------------- | ------------------------------ | --------------------- | ------------------ |
| `.text`       | 0x00401000                     | ⚠ 0x76892000 + offset | **Bị dịch chuyển** |
| `.data`       | 0x00403000                     | ⚠ 0x76894000 + offset | Dịch luôn          |

## 2.3 Cách thao tác với ASLR 

+ Kiểm tra ASLR có được bật 

```c
objdump -x file.exe | findstr "DYNAMIC"
```
=> TNếu không thấy dòng nào chứa "DYNAMIC", tức là file run.exe đã không còn hỗ trợ ASLR

### 2.3.1 Sử dụng cờ biên dịch để tắt ASLR

```c
gcc -g run.c -o run.exe "-Wl,--disable-dynamicbase"
```

### 2.3.2 Dùng editbin để chỉnh sửa

công cụ của Microsoft Visual Studio (có trong Developer Command Prompt hoặc x64 Native Tools)

**Cách 1 : sửa thủ công**
+ Mở công cụ trên thông qua start menu, thêm path đến thư mục chứa .exe
``tắt ASLRD`` : editbin /DYNAMICBASE:NO run.exe
``Mở ASLR``   : editbin /DYNAMICBASE run.exe
**Cách 2: sửa tự động qua task.json**
+ truyền flag `/DYNAMICBASE:NO` để cấu hình tool tắt tự động ASLR
```c
{
    "tasks": [
        {
            "label": "Remove-ASLR",
            "type": "shell",
            "command": "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Tools\\MSVC\\14.39.33519\\bin\\Hostx64\\x64\\editbin.exe",
            "args": [
                "/DYNAMICBASE:NO",
                "${fileDirname}/run.exe",
            ],
            "dependsOn": "Build-C-program",
            "problemMatcher": [],
            "group": "build"
        },
    ],
    "version": "2.0.0"
}
```

| Trường             | Ý nghĩa cụ thể                                                                                       |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| `"label"`          | Tên task bạn sẽ dùng để gọi (hiển thị trong UI hoặc dùng `dependsOn`)                                |
| `"type": "shell"`  | VS Code sẽ **thực thi lệnh bằng shell** (cmd/bash/powershell) chứ không thông qua task type đặc biệt |
| `"command"`        | Đường dẫn tới **lệnh sẽ chạy** — ở đây là `editbin.exe`                                              |
| `"args"`           | Danh sách tham số truyền vào command (`/DYNAMICBASE:NO`, và đường dẫn đến file `.exe`)               |
| `"dependsOn"`      | Task này **phụ thuộc** vào task `"Build-C-program"` (tức là sẽ chạy sau nó)                          |
| `"problemMatcher"` | Không dùng parser nào để detect lỗi compile (vì `editbin` không sinh lỗi kiểu compile)               |
| `"group": "build"` | Gán task này vào nhóm `"build"` — nghĩa là `Ctrl+Shift+B` có thể gọi nó                              |

 

## 2.3.3 ý nghĩa của ASLR

| Vấn đề                      | Nguyên nhân                      | Cách xử lý                                          |
| --------------------------- | -------------------------------- | --------------------------------------------------- |
| Địa chỉ runtime lệch nhiều  | ASLR làm random hóa địa chỉ load | Tắt ASLR khi compile hoặc khi debug                 |
| Symbol table không khớp GDB | Symbol là địa chỉ tĩnh (file)    | So sánh offset tương đối hoặc dùng GDB debug symbol |


## 2.4 Ví dụ trace dòng code bằng addr2line
+ khi một chương trình C crash trên Windows, bạn thường không thấy bất kỳ địa chỉ nào in ra trong console — khác với Linux (vốn thường có core dump kèm địa chỉ lỗi). Điều này làm debug rất khó khăn nếu:
    + Bạn không có debugger attach trực tiếp (như GDB/WinDbg).
    + Bạn muốn bắt lỗi ở runtime để trace ngược thủ công (ví dụ: dùng addr2line để map địa chỉ về source code).

**Trường hợp thực tế không dùng GDB**

| Tình huống thực tế                                               | Lý do không dùng GDB       |
| ---------------------------------------------------------------- | -------------------------- |
| Hệ thống embedded không có cổng debug (SWD/JTAG)                 | Không có debugger          |
| Chạy trên thiết bị IoT xa                                        | Không attach debugger được |
| Lỗi xảy ra ngẫu nhiên trong runtime, không dễ tái hiện khi debug | Cần log lỗi                |
| Dùng FreeRTOS hoặc Bare Metal không hỗ trợ remote GDB            | GDB không kết nối được     |


**Cơ chế bắt lỗi và in chính xác địa chỉ lỗi**

__Dùng SetUnhandledExceptionFilter– Windows-only__

```c
#include <windows.h>
#include <stdio.h>

LONG WINAPI MyExceptionHandler(EXCEPTION_POINTERS *ExceptionInfo) {
    printf("[CRASH] Exception address: %p\n", ExceptionInfo->ExceptionRecord->ExceptionAddress);
    return EXCEPTION_EXECUTE_HANDLER;
}

void cause_crash() {
    int *ptr = NULL;
    *ptr = 42;  // Crash here
}

int main() {
    SetUnhandledExceptionFilter(MyExceptionHandler);
    cause_crash();
    return 0;
}
```

__Output__
```c
[CRASH] Exception address: 0x00401234
```

__trace địa chỉ lỗi__
```c
addr2line -e your_program.exe 0x00401234
```

| **STT** | **Ứng dụng**                                                                | **Mô tả chi tiết**                                                                                                                              | **Liên hệ thực tiễn trong Embedded**                                                                            |
| ------: | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
|       1 | **Phân tích lỗi qua địa chỉ (address-based debugging)**                     | Chuyển đổi địa chỉ bộ nhớ từ thông báo lỗi (như crash, assert, stack trace) sang tên hàm và dòng lệnh tương ứng trong mã nguồn.                 | Giúp xác định dòng gây crash khi thiết bị nhúng reset, ví dụ: HardFault trên STM32 trả về địa chỉ PC.           |
|       2 | **Hỗ trợ phân tích Core Dump / Stack Trace**                                | Khi hệ thống dump địa chỉ lệnh trong ngăn xếp (stack), `addr2line` giúp tra cứu để biết dòng nào trong code đã được gọi.                        | Dễ dàng xác định call chain trước khi hệ thống gặp lỗi, đặc biệt khi không có debugger trực tiếp.               |
|       3 | **Gỡ lỗi trong môi trường không có Debugger**                               | Trong hệ thống nhúng không thể dùng GDB trực tiếp, địa chỉ lỗi có thể được log ra UART. `addr2line` dùng để tra ngược địa chỉ về source.        | Rất phổ biến trong các thiết bị không có kết nối SWD/JTAG hoặc debugger không sẵn có.                           |
|       4 | **Tối ưu hóa mã bằng phân tích hiệu suất (profiling)**                      | Dùng kèm công cụ profiler như `gprof`, khi biết địa chỉ của các hàm gọi nhiều, `addr2line` giúp xác định tên và vị trí chính xác.               | Gợi ý các điểm nghẽn hiệu năng trong hệ thống nhúng, giúp tối ưu sử dụng CPU hoặc năng lượng.                   |
|       5 | **Kết hợp với công cụ phân tích log tự động**                               | Sử dụng trong script hoặc pipeline CI/CD để tự động phân tích log lỗi bằng cách ánh xạ địa chỉ về mã nguồn.                                     | Hữu ích trong quá trình kiểm thử (testing), đặc biệt khi có nhiều thiết bị nhúng chạy song song (mass testing). |
|       6 | **Giải mã lỗi không rõ nguyên nhân trong firmware release (release build)** | Khi firmware ở chế độ release không có debug symbol, vẫn có thể build bản có symbol riêng để dùng `addr2line` phân tích nếu biết địa chỉ lỗi.   | Giúp khắc phục lỗi khách hàng báo mà không cần gắn debugger vào thiết bị của họ.                                |
|       7 | **Xác định vùng bộ nhớ sinh lỗi liên quan đến linker script**               | `addr2line` giúp xác định lỗi liên quan đến pointer, stack/heap, nhờ ánh xạ địa chỉ tới code cụ thể - dễ dò sai sót trong linker hoặc overflow. | Phân tích các lỗi kiểu như stack overflow, memory corruption, thường gặp khi RAM giới hạn.                      |

# 3. Symbol Table và Memory Map

+ **Bối cảnh**
Qua 2 nội dung trên ta đã biết được cách sử dụng `gdb` để gỡ lỗi chương trình qua việc quan sát hành vi của câu lệnh và thông tin trạng thái tại thời điểm đó kết hợp với `addr2line` để trích xuất vị trí của lệnh gây lỗi từ địa chỉ gây lỗi. Nhưng nếu ta muốn biết rõ hơn về 
   + địa chỉ đó đén từ đâu ?
   + biến/hàm được lưu ở nơi nào ?
**file thực thi (PE) giúp chương trình hiểu được**
    + nó cần nạp cái gì
    + nạp code/data vào đúng vị trí trên RAM
    + Thiết lập entry point (điểm bắt đầu chương trình)
    + Hỗ trợ linking tới DLL, import/export symbol
**Mục đích của DLL**
    + "Thư viện động (DLL/.so) giúp liên kết các hàm được định nghĩa bên ngoài chương trình, thường là thuộc về thư viện hệ thống, trong quá trình chạy (runtime) chứ không cần phải nhúng toàn bộ mã đó ngay từ khi biên dịch (compile time).

## 3.1 Symbol Table
### 3.1.1 Symbol là gì
Symbol đại diện cho tên của 1 thực thể trong chương trình (hàm,biến,hằng số), được compiler ánh xạ vào các địa chỉ cụ thể trong tệp nhỉ phân hoặc bộ nhớ
+ **Phân tích symbol là gì**
Quá trình truy xuất và giải mã bảng symbol trong 1 tệp thực thi để biết tên, kiểu, địa chỉ, và phạm vi của các thực thể trong chương trình
+ **Vai trò** : Symbol table chính là thông tin cần thiết để ta có thể debug, cho phép ta
   + biết được địa chỉ của các hàm/biến khi sử dụng `gdb`  với `info functions` và `info variables`
   + thông tin của Symbol table với `nm -n <tên_file.exe> bao gồm dịa chỉ,tên biến/hàm,phân vùng. Dùng `addr2line` để trả về dòng lệnh tương ứng 
   + Vùng địa chỉ của các phân vùng trước khi được đưa lên RAM khi chạy __Run_time__ với `objdump -h <tên_file.exe>`
   + Phân tích lỗi build, linking, overflow vùng nhớ
+ **Lưu ý**
__Symbol table chỉ ánh xạ:__
    + Tên function → địa chỉ bắt đầu của function đó
    + Tên biến toàn cục → địa chỉ trong section .data hoặc .bss
    + Nếu bật chế độ debug (-g), sẽ thêm thông tin tên file, dòng, cột (nhờ .debug_line, chứ không phải .symtab)

+ **Ví dụ** : tìm địa chỉ của 1 biến/hàm trong tệp thực thi sau khi biên dịch 
__Step by step__

+ Lệnh `nm -n <tên_file.exe> | grep <pattern>` để tìm kiếm dòng văn bản khớp với `pattern` 
+ Sử dụng `nm -n run.exe | grep trigger_fault` 
    + `nm -n run.exe` : in toàn bộ thông tin liên quan từ `symbol table` trong run.exe và sắp xếp theo địa chỉ
    + `grep trigger_fault` : chỉ in ra dòng có chứa từ "trigger_fault"
+ Sau khi lấy ra được địa chỉ từ bước trên sử dụng lệnh `addr2line -e <tên_file.exe> địa_chỉ_hex`để lấy ra dòng tương ứng trong mã nguồn
+ Ta cũng có thể tham chiếu ngược địa chỉ trả về để tìm trên symbol table, nơi lưu các hàm/biến đó

## 3.2 Memory map 
Sơ đồ phân bố bộ nhớ chương trình khi chạy. Cho ta biết được chương trình sử dụng bộ nhớ RAM như thế nào. Bao gồm  

| Segment | Mục đích                     |
| ------- | ---------------------------- |
| `.text` | Chứa mã máy (code/hàm)       |
| `.data` | Biến toàn cục đã khởi tạo    |
| `.bss`  | Biến toàn cục chưa khởi tạo  |
| `heap`  | malloc/cấp phát động         |
| `stack` | Lưu biến cục bộ, return addr |


### 3.2.1 Các lệnh thao tác trên RAM (khi debug trên gdb)
+ **Thao tác trên static memory**
    - `info files`             Các phân vùng thực tế trên RAM (.bss .data .text)
    - `info address <element>` địa chỉ của các `element` có thể làm hàm/biến trích xuất từ symbol table có được khi build với `-g`
    - `info symbol 0x401130`   địa chỉ nào thuộc hàm nào?
    - `info line`              địa chỉ của dòng hiện tại
    - `info functions`         liệt kê hàm
    - `info variables`         liệt kê biến toàn cục
    - `p &<tên_biến>`          địa chỉ của biến
- **Thao tác trên Stack**
    - `show architecture`      trả về kiến trúc xử lý (32-bit/64-bit)
    - `info register $<reg>`   địa chỉ của thanh ghi : rsp,rbp,...
    - `info locals`            liệt kê biến cục bộ
    - `x/[N][FU] <address>`    Hiển thị vùng nhớ từ địa chỉ cụ thể 
        + __N__: số lượng đơn vị muốn hiển thị (number of units)
        + __F__: format hiển thị (`x` = hex, `d` = decimal, `c` = char, v.v.)
        + __U__: kích thước đơn vị:
            + `b`: byte (1 byte)
            + `h`: halfword (2 bytes)
            + `w`: word (4 bytes)
            + `g`: giant word (8 bytes)
                
### 3.2.2 Ví dụ phân tích Symbol và memory map

```c
#include <stdio.h>
#include <stdlib.h>

// Biến toàn cục đã khởi tạo → .data
int global_data = 123;

// Biến toàn cục chưa khởi tạo → .bss
int global_bss;

void trigger_fault() {
    int arr[3] = {1, 2, 3}; // stack
    arr[5] = 42;            // ❌ lỗi ghi vượt giới hạn
}

int main() {
    int *heap = malloc(sizeof(int) * 3); // heap
    *heap = 23;
    heap[0] = global_data;

    global_bss = 0;
    trigger_fault();
    free(heap);
    return 0;
}
```
__a. Compile với thông tin symbol__

```c
gcc -g memmap_demo.c -o memmap_demo.exe
```

+ Lý do compile với `-g` là để tạo ra thông tin cần thiết cho __gdb__ hiểu để cho phép ta kiểm soát và xem được trạng thái chương trình thông qua dữ liệu từ symbol table(bảng ánh xạ địa chỉ tương ứng với hàm/biến, dòng code)

__b. Phân tích Symbol Table__

```c
nm -n memmap_demo.exe
```


__c. __Phân tích Section header Table__

```c
objdump -h memmap_demo.exe
```

| Trường        | Ý nghĩa                              |
| ------------- | ------------------------------------ |
| **Idx**       | Số thứ tự section                    |
| **Name**      | Tên section (`.text`, `.data`, ...)  |
| **Size**      | Kích thước vùng                      |
| **VMA / LMA** | Địa chỉ ảo và vật lý khi nạp vào RAM |
| **File off**  | Offset trong file `.exe`             |
| **Algn**      | Alignment (căn lề) trong bộ nhớ      |

**Dữ liệu chương trình**
+ `.text` : mã máy đã được biên dịch, nạp vào RAM, để thực thi
+ `.data` : biến global đã khởi tạo
+ `.bss`  : biến global chưa khởi tạo
+ `.rdata`: hằng số
+ `.tls`  : dùng cho các biến thread
**Dữ liệu hệ thống**
+ `.idata` : lưu import table để liên kết DLL dùng cho sử dụng các thư viện bên ngoài
+ `.reloc` : dùng cho ASLR, cơ chế random hóa địa chỉ
+ `.rsrc`  : chứa dữ liệu tài nguyên liên quan đến UI (hiển thị hệ thống -> biểu tượng,menu,version info)
+ `.pdata` : chứa các function dùng cho exception handling (xác định vùng code tương ứng với exception) được gdb dùng để gỡ lỗi 
+ `.xdata` : Metadata của tửng function (giúp quay ngược stack khi exception xảy ra)
**Dữ liệu debug**
+ `.debug_info` : cấu trúc chương trình,biến,kiểu dữ liệu
+ `.debug_line` : mapping địa chỉ code với dòng trong file
+ `.debug_str`  : chuỗi ký tự trong debug
+ `.debug_bbrev`,`debug_arranges`,`debug_frame` : phân tích khổi chương trình, vùng stack

**Mối liên hệ giữa VMA,LMA, và file off **
+ `VMA` : Nơi CPU truy cập khi thực thi (địa chỉ ảo hiển thị gdb)
+ `LMA` : Nơi loader đặt section trong RAM (địa chỉ vật lý lưu trên phần cứng thông qua MMU)
+ `file off` : nơi Os sẽ bắt đầu load dữ liệu lên RAM 

__TÓM LẠI__
| Thuật ngữ | Viết tắt               | Vai trò                                                                  | Có thể thấy từ user-space?                   |
| --------- | ---------------------- | ------------------------------------------------------------------------ | -------------------------------------------- |
| **LMA**   | Load Memory Address    | Địa chỉ **RAM thật (vật lý)** nơi dữ liệu được nạp vào (hoặc ánh xạ tới) | ❌ **Không thể thấy** trực tiếp từ user-space |
| **VMA**   | Virtual Memory Address | Địa chỉ **ảo** mà chương trình (và GDB) dùng để truy cập                 | ✅ **Có thể thấy** trong GDB, objdump, etc.   |


+ **Khởi động gdb**
```c
gdb memmap_demo.exe
```


+ **debug từ dòng đầu**

```c
(gdb) start
```

__Phân tích VMA trên RAM__

```c
info files 
```

Dòng đầu tiên

```c
Entry point : 0x140001410
```
Đây là địa chỉ của hàm khởi tạo hệ thống thường là `_start_` hoặc `mainCRTStartup` chứ không phải main trực tiếp


+ **In địa chỉ các biến**

```c
(gdb) p &global_data
(gdb) p &global_bss
(gdb) p &local_var
(gdb) p heap_ptr
```

### 3.2.3 ý Nghĩa và vai trò của việc phân tích symbol và memory map

Khi thực hiện gỡ lỗi chương trình ta cần xác định được vấn đề mà ta cần xử lý dựa trên các lỗi như 
   + ghi đè biến
   + stack overflow
   + lỗi linker
Để giải quyết được các vấn đề trên ta cần nắm được các kiến thức về symbol table, memory map, để xác định được địa chỉ cấp phát và vị trí của hàm/biến/dòng lệnh trong chương trình











































