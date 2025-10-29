# 1. STACK (Ngăn Xếp)
## 1.1. Định nghĩa
+ Cấu trúc dữ liệu quản lý bởi người dùng
+ Lưu trữ dữ liệu tạm thời, hay các hàm gọi lồng nhau 
+ Quyền truy cập: đọc/ghi 
+ Cấp phát và giải phóng vùng nhớ theo cơ chế LIFO

**Lưu ý**: 1 ngăn xếp có thể được cài đặt bằng cách lưu dữ liệu trong bất kỳ vùng nhớ nào   `.data`,`.bss`,`.heap`,`.stack` segment
## 1.2. Đặc điểm 
### a) Cách thao tác 
<p align = "center">
<img src="https://github.com/user-attachments/assets/450259e6-d00c-422b-9f9e-bbde2566f956" alt="image" width="650" height="350">

Việc quản lý stack sẽ phụ thuộc vào 3 cơ chế sau

__push__ : đẩy 1 thành phần vào đỉnh stack

__pop__: xóa 1 thành phần ở đỉnh stack

__top__: lấy 1 thành phần ở đỉnh stack

__empty & full STACK__

+ Được sử dụng để xác định kích thước hiện tại của stack 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/34601b9a-79e2-408f-b93b-df4f3a39de71" width = "500" height = "250" >

### b) Dữ liệu lưu trên ngăn xếp phổ biến trên heap so với stack

**Hạn chế cũa Stack so với Heap**
+ Kích thước nhỏ
+ Dữ liệu khai báo là tĩnh - cố định khi chạy runtime
+ Thời gian tồn tại ngắn, cục bộ trong phạm vi cấp phát
=> Dùng Stack khi biến nhỏ,tạm thời,không yêu cầu tồn tại lâu, và yêu cầu cấp tốc độ cấp phát nhanh

**Ưu điểm của heap**
+ Kích thước lớn
+ dữ liệu khai báo tại run-time và điều chỉnh được
+ Thời gian tồn tại dài, phụ thuộc user quản lý
=> Dùng stack khi quản lý dữ liệu lâu dài, truyền qua nhiều hàm

**Ví dụ cơ bản**

```c
char* createName() {
    char name[100]; // biến trên stack → sẽ invalid sau return!
    strcpy(name, "Duy");
    return name;    // ⚠️ lỗi – trả về con trỏ tới vùng nhớ đã bị hủy
}

// Giải pháp đúng:
char* createName() {
    char* name = malloc(100); // cấp phát trên heap
    strcpy(name, "Duy");
    return name;              // an toàn
}
```


**So sánh ví dụ thực tế**

| Tình huống                      | Dùng Stack hay Heap? | Lý do                                      |
| ------------------------------- | -------------------- | ------------------------------------------ |
| Gọi hàm tính toán đơn giản      | Stack                | Biến cục bộ, nhỏ                           |
| Cấp phát mảng ảnh 1920x1080     | Heap                 | Stack không đủ lớn                         |
| Trả về chuỗi từ hàm             | Heap                 | Stack không tồn tại sau khi hàm kết thúc   |
| Buffer nhận UART                | Heap hoặc Static     | Heap nếu cần linh hoạt; static nếu cố định |
| Temporary struct xử lý ngắn hạn | Stack                | Nhanh và gọn                               |


## 1.3 Triển khai Thuật toán Ngăn Xếp 

### a) Sử dụng với đệ quy 

Hàm sau đây sẽ dùng để tính giai thừa của 1 số với công thức                    
!n = n(n-1)(n-2)...
```bash
int giaithua(int n){
    if(n == 1){
        return 1;
    }
    else return n * giaithua(n - 1); 
}
int main() {
    int n = 6;
    printf("!%d = %d",n,giaithua(n)); // giaithua được push vào stack
    return 0;
}
```
+ hàm giaithua sẽ được liên tục được push vào stack cho đến khi n = 1, lúc này giaithua sẽ được pop khỏi stack.
```bash
PUSH process  
giaithua(6) // 0x01 
giaithua(5) // 0x02 
giaithua(4) // 0x03 
giaithua(3) // 0x04  
giaithua(2) // 0x05 
giaithua(1) // 0x06
POP process
giaithua(2) -> return 2 * giaithua(1) //0x06 
giaithua(3) -> return 3 * giaithua(2) //0x05
giaithua(4) -> return 4 * giaithua(3) //0x04
giaithua(5) -> return 5 * giaithua(4) //0x03
giaithua(6) -> return 6 * giaithua(5) //0x02
main() -> return giaithua(6) // 0x01
```
+ Như vậy kết quả sẽ là: 6 * 5 * 4 * 3 * 2 * 1 = 720

### 1.3.2 Các bước triển khai Ngăn xếp

**+ Định nghĩa cấu trúc Ngăn xếp**
```bash
typedef struct Stack {
    int* items; // mảng giả lập stack để lưu trữ dữ liệu
    int size; // kích thước của stack
    int top; //chỉ số để truy cập vào phần tử trong stack
} Stack;
```
**+ Khởi tạo ngăn xếp**
```bash
void initialize(Stack *stack, int size) {
  stack->items = (int*) malloc(sizeof(int) * size);// cấp phát ngăn xếp trên heap
  stack->size = size;                              // kích thuóc ngăn xếp
  stack->top = -1;                                 // cài đặt ngăn xếp rỗng ban đầu
}
```
**+ kiểm tra trạng thái ngăn xếp**

```bash
bool is_empty(Stack stack) {
    return (stack.top == -1) ? true : false;
}
bool is_full( Stack stack) {
    return (stack.top == stack.size - 1) ? true : false;
}
```

**+ Các thao tác với ngăn xếp**

```bash
#define STACK_EMPTY -1

void push(Stack *stack, int value) {
    if (is_full(*stack) == false) {
//gán giá trị trước khi dịch đến địa chỉ tiếp theo vì mặc định ban đầu stack có chỉ số là -1
        stack->items[++stack->top] = value; 
    } else {
        printf("Stack overflow\n"); //nếu stack đầy thì in ra thông báo
    }
}

int pop(Stack *stack){
    if (is_empty(*stack) == false) {
        return stack->items[stack->top--]; //trả về giá trị hiện tại ở đỉnh stack trước khi xóa nó 
    }
    else{
        printf("Stack underflow\n"); //néu stack rỗng mà ta vẫn thực hiện xóa stack thì in ra thông báo
        return STACK_EMPTY;
    }
}

int top(Stack stack) {
    if (is_empty(stack) == false) {
        return stack.items[stack.top]; //trả về giá trị ở đỉnh stack nếu stack không rỗng
    } else {
        printf("Stack is empty\n"); //nếu stack rỗng mà ta vẫn truy cập để đọc giá trị thì in ra thông báo
        return STACK_EMPTY;
    }
}
```

+ Ta sẽ kết hợp các hàm đã tạo ở trên để thao tác với stack 
```bash
int main()
{
    Stack stack1;
    int8_t size = 5;           //kích thước của stack
    initialize(&stack1, size); //khởi tạo giá trị ban đầu cho stack

    //in và Lưu giá trị vào stack 
    for (int8_t i = 0; i < size; i++)
    {
        push(&stack1, i + 2);
        printf("element: %d -> add:%p\n", stack1.items[i], &stack1.items[i]);
    }

    //xảy ra lỗi stack overflow nếu cố gắng push thêm data vượt quá size đã khởi tạo ban đầu
    push(&stack1,1111);
    
    //In và lấy từng phần tử ra khỏi stack    
    for (int8_t i = size - 1 ; i >= -1; i--)
    {
        printf("top element: %d -> add:%p\n", pop(&stack1), &stack1.items[i]);
    }

    return 0;
}
```  

### 1.4 Stack Segment vs Stack (Ngăn xếp)

**a) So sánh**

| Tiêu chí             | Ngăn xếp (Stack Data Structure)                                                 | Stack trong Memory Layout (OS cấp phát)                                      |
|----------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| **Bản chất**          | Là một cấu trúc dữ liệu tuyến tính (LIFO).                                      | Là một vùng nhớ trong RAM do hệ điều hành cấp phát cho mỗi thread/process.   |
| **Quản lý bộ nhớ**    | Do lập trình viên tự quản lý (cấp phát tĩnh, động, hoặc biến toàn cục).        | Được quản lý tự động bởi OS hoặc trình biên dịch.                            |
| **Cách hoạt động**    | Dựa trên thao tác `push()` và `pop()`.                                          | Khi một hàm được gọi, một *stack frame* được tạo; kết thúc thì bị xóa.       |
| **Kích thước**        | Linh hoạt, tùy thuộc vào cách cài đặt và vị trí lưu trữ (heap, static, v.v.).  | Giới hạn (thường vài KB - vài MB), có thể gây lỗi stack overflow.           |
| **Lưu trữ**           | Bất kỳ loại dữ liệu nào theo nhu cầu thuật toán.                                | Tham số hàm, biến cục bộ, địa chỉ trả về, frame pointer,...                  |
| **Mục đích**          | Quản lý dữ liệu LIFO, hỗ trợ thuật toán như duyệt cây, hậu tố, đệ quy, undo,... | Quản lý lời gọi hàm, lưu trạng thái hàm đang chạy trong chương trình.        |
| **Tồn tại bao lâu?**  | Tùy ý – tồn tại miễn là chương trình còn sử dụng nó.                            | Tự động tạo khi vào hàm và xóa khi ra khỏi hàm (runtime).                    |
| **Tốc độ truy cập**   | Nhanh (nếu cài bằng mảng/tĩnh); chậm hơn nếu trên heap.                         | Rất nhanh, do tối ưu cho lời gọi hàm.                                        |
| **Vị trí lưu trữ**    | Có thể nằm ở `.bss`, `.data`, `heap`, hoặc `stack`.                             | Nằm ở vùng stack segment riêng biệt trong bộ nhớ tiến trình.                 |
| **Lỗi thường gặp**    | Tràn stack logic (push nhiều hơn pop, lỗi thuật toán).                         | Stack overflow do gọi hàm sâu/biến cục bộ lớn quá.                           |

**b) Tóm tát**
+ Stack (Data Structure) là thuật toán liên quan đến cách tổ chức dữ liệu 1 cách linh hoạt, cho phép triển khai ở bất kỳ đâu trong RAM
=> Do người lập trình quản lý 
+ Stack (Memory layout) là segment trên RAM được Os quản lý, để lưu call stack (chứa các stack frame khi 1 hảm được gọi)
=> Được tự động cấp phát khi chạy
# 2. QUEUE

<p align = "center">
<img src = "https://github.com/user-attachments/assets/cf831539-70c2-4bdc-8e43-e7ec84ac99ae" width = "400" height = "300">

Đây là 1 kiểu cấu trúc dữ liệu tuân theo theo cơ chế __FIFO__, có nghĩa là phần tử nào vào hàng đợi trước sẽ được lấy ra đầu tiên

__Các phần tử được thêm lần lượt__ 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/b3b41d9d-0ff5-4e60-880f-f7d2196e4d15" width = "400" height = "150">


__Lấy ra theo thứ tự cái nào vào trước__ 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/0ffca03c-95c0-424a-8827-3cda964f8d61" width = "400" height = "150">

## 2.1 Đặc điểm của QUEUE

### a) Các thao tác 
<p align = "center">
<img src = "https://github.com/user-attachments/assets/b0885609-b47a-4c21-84ca-136bd4eed15f" width = "500" height = "250">

__enqueue__ : thêm 1 phần tử vào cuối hàng đợi

__dequeue__ : lấy 1 phần tử ở đầu hàng đợi

__front__ : chỉ số truy cập giá trị ở đàu hàng đợi (tăng khi dequeue)

__rear__ : chỉ số truy cập giá trị ở cuối hàng đợi (tăng khi enqueue)

__Empty queue__ : khi front = rear = -1

__full queue__ : khi rear = size - 1 hoặc front > rear

### b) Ưu điểm
+ Thích hợp cho quản lý các tác vụ hoặc dữ liệu xử lý theo thứ tự thời gian
+ Truyền nhận dữ liệu của các ngoại vi như UART,SPI

### c) Ứng dụng 

__Quản lý dữ liệu giao tiếp giữa cảm biến và MCU__
<p align = "center">
<img src = "https://github.com/user-attachments/assets/7f2ff887-5c22-4919-b223-0e0f9651024a" width = "600" height = "400">
__

## 2.2 Các loại queue

### a) linear queue
+ Trong hàng đợi linear, khi ta dequeue trong trường hợp full queue __(size = rear - 1)__ , thì lúc này ta sẽ không thể enqueue phần tử mới được dù cho có vùng nhớ trống ở đầu vừa được dequeue Cơ ché này được giải thích như sau.
+ Khi chưa có giá tri, lúc này hàng đợi rỗng và giá trị của front và rear mặc định là -1

<p align = "center">
<img src = "https://github.com/user-attachments/assets/62f24d68-44eb-4064-b9cf-501c8867f1af" widht = "250" height = "100">


+ enqueue lần đầu, lúc này chỉ số front = rear = -1

+ enqueue sau lần đầu,front giữ nguyên, trong khi rear tăng để trỏ tới phần tử cuối queue

+ khi queue đầy, tiến hành dequeue thì lúc này do rear = size - 1 ,không cho phép ta enqueue nữa, mặc dù vùng nhớ vùng nhớ ở đầu queue đang trống, gây lãng phí vùng nhớ

+ Khi dequeue hết tất cả phần tử , lúc này front > rear, tiến hành cập nhật front = rear = -1 để reset queue mới cho phép enqueue phần tử mới

<p align = "center">
<img src = "https://github.com/user-attachments/assets/df3db37c-321d-4489-b4ef-cde304b6d6e7" widht = "450" height = "250">



### b) Circular queue

+ Cho phép tiếp tục enqueue khi rear = size - 1 và front != 0. Bằng cách quay vòng về đầu queue để thêm phần tử ở các vị trí trống thông qua cập nhật rear = 0

## 2.3 Mô phỏng cấp phát cơ chế queue

**+ Cấu trúc lưu trữ thuộc tính của queue**

```bash
typedef struct Queue
{
    int *queue_item; //mảng để lưu các thành phần 
    int size;        //kích thước mảng queue
    int front;       //chỉ số truy cập vào phần tử đầu hàng đợi
    int rear;        //chỉ số truy cập vào phần tử cuối hàng đợi
}Queue;
```

**+ Khởi tạo queue**

```bash
Queue* initialize(int size)
{
    Queue *queue = (Queue *)malloc(size * sizeof(Queue));   // cấp phát vùng nhớ cho queue
    queue->queue_item = (int *)malloc(size * sizeof(int)); // cấp phát vùng nhớ cho mảng chứa các phần tử sẽ đẩy vào queue
    queue->size = size; 
    queue->front = queue->rear = -1; //giá trị mặc định khi queue rỗng
    return queue;   // trả về địa chỉ của vùng nhớ vừa được khởi tạo
}
```  
**+ Kiểm tra queue empty**

```bash
bool IsQueue_Empty(Queue queue)
{
    return ((queue.front == -1) ? true : false); 
}
```  
### a) Triển khai Linear queue

**+ Kiểm tra queue full**
```  
bool IsQueue_Full(Queue queue)
{
    //return ((queue.rear == queue.size - 1) ? true : false); 
}
```  

**+ Quá trình enqueue**
+ Queue full ? 
    => true => queue empty ? 
                => true => cập nhật front = rear = 0
                => false => rear++
            => thêm phần tử mới vào vị trí rear mới cập nhật
    => false => dừng xử lý
 ```bash
void enqueue(Queue *queue, int value)
{
    if (!IsQueue_Full(*queue))
    {
        if (IsQueue_Empty(*queue))
        {
            queue->front = queue->rear = 0;
        }
        else
        {
            queue->rear++;
        }
        queue->queue_item[queue->rear] = value;
        printf("enqueue %d -> %p\n", queue->queue_item[queue->rear], &queue->queue_item[queue->rear]);
    }
    else
        printf("queue overflow, can't add more item\n");
}
```  

**+ Quá trình dequeue**
```bash

void dequeue(Queue *queue)
{
    if (!IsQueue_Empty(*queue))
    {
        printf("dequeue %d -> %p\n", queue->queue_item[queue->front], &queue->queue_item[queue->front]);
        if (queue->front == queue->rear && queue->rear = queue->size - 1)
        {
            queue->front = queue->rear = -1;
        }
        else{
            queue->front++;
        }

    }
    else printf("queue underflow\n");
}
```  
+ Ta sẽ thực hiện việc enqueue và dequeue trong hàm main như sau 


```bash

int main(){
    int size = 5;
    Queue* queue = initialize(size);
    for(int i = 0 ; i < size ; i++){
        enqueue(queue,i + 1);
    }
    enqueue(queue,23); // báo lỗi do lúc này queue đã đầy
    printf("\n");
    for(int i = queue->front ; i <= queue->rear ; i++){
        dequeue(queue);
    }
    dequeue(queue); //báo lỗi do lúc này queue đã rỗng
    return 0;
}
```  
+ kết quả in ra ta thấy các phần tử được enqueue và dequeue hoàn toàn theo cơ chế __FIFO__  

```bash
enqueue 1 -> 00000217ACBFE910      
enqueue 2 -> 00000217ACBFE914      
enqueue 3 -> 00000217ACBFE918      
enqueue 4 -> 00000217ACBFE91C      
enqueue 5 -> 00000217ACBFE920      
queue overflow, can't add more item

dequeue 1 -> 00000217ACBFE910      
dequeue 2 -> 00000217ACBFE914      
dequeue 3 -> 00000217ACBFE918      
dequeue 4 -> 00000217ACBFE91C      
dequeue 5 -> 00000217ACBFE920      
queue underflow
```  

### b) Circular queue 

+ Ta biết rằng 1 linear queue sẽ chỉ được enqueue sau khi queue đã đày bằng cách dequeue toàn bộ phần tử bên trong nó. vậy nên ta sẽ không thể enqueue phần tử mới khi bắt đầu dequeue. Chính vì vậy ta sẽ sử dụng co chế __circular queue__ để giải quyết được vấn đề này 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/1aace635-b65c-482f-88e9-5560ee928196" width = "300" height = "250">

+ Hình trên mô tả 1 queue được dequeue 3 phần tử và chỉ số front lúc này bằng 3 đang trỏ tới phần tử thứ 4. Trong khi đó chỉ số rear = size - 1. Lúc này cơ chế circular sẽ cho phép rear trỏ đến đầu hàng đợi để enqueue tiếp 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/c9fc6a35-624b-4b51-b4e1-d2dfd1fccb16" width = "300" height = "150">

+ Lúc này ta sẽ có thể tiếp tục enqueue cho đến khi các ô trống được lắp đầy

<p align = "center">
<img src = "https://github.com/user-attachments/assets/2b1ec340-0185-4801-bac5-3f8d008e58d8" width = "300" height = "150">

Vì vậy ta kết luận được. điều kiện để 1 circular queue full là:

__trường hợp rear = size - 1__ : thì front = 0

__trường hợp rear khác size - 1__: thì rear = front - 1

+ Ta sẽ có hàm sau với công thức tổng quát trả về 1 full queue như sau 


```bash
bool IsQueue_Full(Queue queue)
{
    return (queue.rear + 1) % queue.size == queue.front; 
}
```
__Phân tích biểu thức:__

+ rear + 1 : đảm bảo giá trị rear nằm trong khoảng cho phép không vượt quá size
+ (rear + 1 ) % size : tính vị trí tiếp theo của queue và so sánh với chỉ số của front nếu bằng nhau thì kết luận hàng đợi đầy

+ Lúc này trong hàm enqueue ta cũng sửa lại điều kiện cập nhật chỉ số  rear như sau, toàn bộ những phần còn lại thì giữ nguyên như linear queue

```bash
void enqueue(Queue *queue, int value)
{...
        else
        {
           queue->rear = (queue->rear + 1) % queue->size; 
        }
 ...
}
```
+ Ta cũng làm tương tự vói hàm dequeue, để cập nhật chỉ số front

```bash
void dequeue(Queue *queue)
{
    ...
        else{
            queue->front = (queue->front + 1) % queue->size;
        }
    ...
}
```

+ Ta viết hàm dùng để enqueue 1 mảng các phần tử 
```bash
void implement_enqeue(Queue *queue, int *ptr)
{
    printf("***enqueue process***\n");
    for (int8_t i = 0; i < queue->size; i++)
    {
        enqueue(queue, ptr[i]);
    }
}
+ Ta sẽ có 1 hàm để hiện thị các phần tử trước và sau khi sử dụng circular queue
```
``` bash
void display(Queue* queue){
printf("\nelements in queue\n");
   //khi chỉ số rear chưa trỏ về đầu hàng đợi để enqueue 
    if (queue->rear > queue->front) 
    {
        for (int8_t i = queue->front; i <= queue->rear; i++)
        {
            printf("queue %d\n", queue->queue_item[i]);
        }
    }
//khi cơ chế circular queue được kích hoạt -> rear trỏ về đầu hàng đợi
    else if (queue->rear < queue->front)
    {
        for (int8_t i = 0; i < queue->size; i++)
        {
            printf("queue %d\n", queue->queue_item[i]);
        }
    }
}
```

+ Trong chương trình chính ta sẽ test như sau
```bash
int main(){
    int arr[] = {1, 2, 3, 4, 5};
    int size = sizeof(arr) / sizeof(arr[0]);
    Queue *queue = initialize(size);
    implement_enqeue_dequeue(queue, arr);
    printf("***dequeue 2 element***\n");
    printf("dequeue: %d\n", dequeue(queue));
    printf("dequeue: %d\n", dequeue(queue));
    display(queue);
    printf("\nenqueue more\n");
    enqueue(queue, 6);
    enqueue(queue, 7);
    display(queue);
    return 0;
}
```

# 3 So sánh stack và queue

<p align = "center">
<img src = "https://github.com/user-attachments/assets/d64c2f7c-3557-4701-850c-7302fbf944c9" wisth = "600" height = "400">


    














