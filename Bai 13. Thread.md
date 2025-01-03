# 1. Tổng quan về Đa luồng 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/22120bf9-ce18-4bfb-b219-d6dc239bee1a" width = "500" height = "300">

Thông thường đa số các chương trình khi chạy sẽ theo dạng tuần tự từ trên xuống, có nghĩa là các tác vụ hiện tại phải hoàn thành xong mới đến những cái tiếp theo. Trong những chương trình nhỏ thì điều này có vẻ không chịu ảnh hưởng gì nhiều tuy nhiên đối với những chương trình lớn chạy theo thời gian thực với những yêu cầu khắt khe và chính xác về thời gian để xử lý dữ liệu chính xác thì cách lập trình tuần tự không còn hiệu quả nữa

=> Chính vì vậy đa luồng được sinh ra để giải quyết vấn để trên
## 1.1 Khái niệm

<p align = "center">
<img src = "https://github.com/user-attachments/assets/09832edf-c7a3-4dd1-a895-1edee33e34db" width = "500" height = "200">

+ Luồng được hiểu là 1 đơn vị thực thi nhỏ nhất của 1 tiến trình. Mỗi tiến trình chứa nhiều thread và cho phép chúng chạy song song.
+ Các task sẽ chia sẻ chung 1 tài nguyên chương trình, nhưng có stack và bộ đếm riêng
+ Về bản chất đa luồng vẫn là tuần tự nhưng nó phân chia thời gian thực hiện giữa các tác vụ.

__Ưu điểm của đa luồng__

+ Xử lý đa nhiệm
+ tăng tốc độ xử lý và tối ưu hóa chương trình
+ Thích hợp với các hệ thống real-time như embedded system 

# 2. Thư viện pthread trong C
Trong c có hỗ trợ lập trình qua thư viện __#include<pthreah.h> cung cấp các APIs để thực hiện các chức năng như

## 2.1  Synchronization 
+ Cho phép các thread chia sẻ tài nguyên chung và xử lý 1 cách an toàn

## 2.2 Thread control
+ Cho phép tạo, quản lý và phối hợp với các thread khác

## 2.3 Các API cơ bản 

### a) Tạo 1 luồng 
```bash
int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine)(void *), void *arg);
```

__+ thread:__ con trỏ lưu Id của thread vừa tạo

__+ attr:__ thuộc tính của thread, mặc định là null

__+ start_rountine:__ con trỏ hàm để lưu địa chỉ của tác vụ cần thực thi

__+ arg:__ đối số truyền vào start_routine

### b) Chờ 1 thread kết thúc
```bash
int pthread_join(pthread_t thread, void **retval);
```

__+ thread:__ ID của luồng cần chở

__+ retval:__ con trỏ đến giá trị trả về từ luồng. mặc định là null

### c) Các API để đồng bộ hóa mutex 
Đây là 1 cơ chế cho phép các hàm chia sẻ tài nguyên chung để xử lý dữ liệu trong đa luồng. Tuy nhiên nó đảm bảo rằng ở mỗi thời điểm chỉ có 1 luồng duy nhất được cho phép truy cập vào tài nguyên để tránh xung đột và đảm bảo an toàn cho tài nguyên chia sẻ đó. Quy trình hoạt động mutex như sau

__+ Khởi tạo mutex:__
```bash
int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
```
__mutex:__ con trỏ đến mutex vừa được khởi tạo

__attr:__ thuộc tính của mutex(mặc định là null)

__+ Khóa mutex:__ 

=> Nếu mutex chưa khóa, luồng hiện tại sẽ khóa mutex và thực hiện công việc của nó

=> Những luồng khác sẽ chờ đến khi mutex được mở khóa mới cho phép sử dụng tài nguyên

```bash
int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
```

Hàm trên sẽ chở đến khi mutex sẵn sàng để khóa

__+ Mở khóa mutex:__

=> Sau khi hoàn thành xong công việc, lường hiện tại mở khóa muxtex cho phép các luồng khác truy cập vào tài nguyên

```bash
int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
```

Hàm trên sẽ mở khóa mutex để các luồng khác truy cập tài nguyên

__+ Hủy mutex:__
```bash
int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
```
Hàm trên sẽ hủy mutex khi không sử dụng nữa
## 2.2 Các ví dụ sử dụng đa luống

### a) 2 luồng chạy song song và sử dụng stack riêng để xử lý giá trị

```bash
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <unistd.h>

void *task1(void* data)
{
    static int i = 0;
    while(1)
    {
        printf("count task1: %d\n", i++);
        sleep(1);
    }
}

void *task2(void* data)
{
    static int i = 0;
    while(1)
    {
        printf("count task2: %d\n", i++);
        sleep(3);
    }
}

int main(int argc, char const *argv[])
{   
    //tạo ra 2 luồng
    pthread_t t1; // luồng 1
    pthread_t t2; // luồng 2
    
    //Khởi tạo 
    pthread_create(&t1, NULL, task1,NULL);
    pthread_create(&t2, NULL, task2,NULL;

    //lần lượt chờ đến khi luồng này thực hiện xong thì đến luồng tiếp theo
    pthread_join(t1, NULL);
    pthread_join(t2,NULL);
    return 0;
}

```
### b) 2 luổng chạy song và chia sẻ tài nguyên chung để xử lý giá trị

```bash
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <unistd.h>

//tạo khóa mutex
pthread_mutex_t lock;

//khởi tạo tài nguyên chung
int count = 0;
void* display(void* a)
{
    static int i = 0;
    while(i++ < 20)
    {
        pthread_mutex_lock(&lock);
        printf("%s:%d\n", (char*)a,count++);
        pthread_mutex_unlock(&lock);
        sleep(1);
    }
}

int main(int argc, char const *argv[]){
    const char *str = "duy pham";
    const char *ptr = "Hello world";

    //khởi tạo mutex
    pthread_mutex_init(&lock,NULL);

    pthread_t t1; // luồng 1
    pthread_t t2; // luồng 2

    pthread_create(&t1, NULL, display, (void*)str);
    pthread_create(&t2, NULL, display,(void*)ptr);

    pthread_join(t1, NULL);
    pthread_join(t2,NULL);

    printf("final count: %d",count);
    pthread_mutex_destroy(&lock);
}
```
