# 1. STACK (Ngăn Xếp)
## 1.1. Định nghĩa
+ Cấu trúc dữ liệu quản lý bởi người dùng
+ Lưu trữ dữ liệu tạm thời, hay các hàm gọi lồng nhau 
+ Quyền truy cập: đọc/ghi 
+ Cấp phát và giải phóng vùng nhớ theo cơ chế LIFO
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

### b) Ưu điểm 
+ Dễ triển khai
+ Ứng dụng trong quản lý tài nguyên hoặc khi sử dụng với các hàm đệu quy
### c) Ứng dụng 

+ __Quán lý stack frame__: lưu trữ những giá trị cục bộ, địa chỉ trả về, tham số hàm khi 1 hàm được gọi
+ __Undo hoặc redo tác vụ__: thường thấy khi ta chuyển tiếp hoặc quay lại giữa các giao diện trang web trên máy tính (mõi khi ta click chọn vào 1 trang web thì địa chỉ của chúng sẽ được lưu trữ trên stack)


## 1.3 Mô phỏng stack 

### 1.3.1 Sử dụng với đệ quy 

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

### 1.3.2 Mô phỏng code cấp phát trên stack

+ đầu tiên ta sẽ tạo ra 1 struct để khai báo những thuộc tính của stack
```bash
typedef struct Stack {
    int* items; // mảng giả lập stack để lưu trữ dữ liệu
    int size; // kích thước của stack
    int top; //chỉ số để truy cập vào phần tử trong stack
} Stack;
```
+ Tiếp theo ta sẽ tạo ra 1 hàm để cài đặt giá trị ban đầu cho stack
```bash
void initialize(Stack *stack, int size) {
  stack->items = (int*) malloc(sizeof(int) * size);// cấp phát memory cho các phần tử
  stack->size = size; // kích thuóc của stack
  stack->top = -1; //cài đặt stack rỗng ban đầu
}
```
+ Ta tạo ra 2 hàm để kiểm tra tình trạng hiện tại của stack là rỗng hay đầy
```bash
bool is_empty(Stack stack) {
    return (stack.top == -1) ? true : false;
}
bool is_full( Stack stack) {
    return (stack.top == stack.size - 1) ? true : false;
}
```
+ Cuối cùng ta sẽ có 3 hàm để thao tác với stack 
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

Kết quả in ra màn hình
```bash
element: 2 -> add:000002E41321E9D0
element: 3 -> add:000002E41321E9D4
element: 4 -> add:000002E41321E9D8
element: 5 -> add:000002E41321E9DC
element: 6 -> add:000002E41321E9E0
Stack overflow
top element: 6 -> add:000002E41321E9E0
top element: 5 -> add:000002E41321E9DC
top element: 4 -> add:000002E41321E9D8
top element: 3 -> add:000002E41321E9D4
top element: 2 -> add:000002E41321E9D0
Stack underflow
top element: -1 -> add:000002E41321E9CC
```   
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

__Empty queue__ : 1 queue được xem là rỗng khi giá trị front và rear là -1 

__full queue__ : khi kích thước của queue size = rear - 1


### b) Ưu điểm
+ Thích hợp cho quản lý các tác vụ hoặc dữ liệu xử lý theo thứ tự thời gian
+ Truyền nhận dữ liệu của các ngoại vi như UART,SPI,

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


+ Tiếp theo ta sẽ tiến hành enqueue, lúc này chỉ số front và rear sẽ tăng lên 0 trước khi giá trị được enqueue vào

+ Tuy nhiên khi ta tiếp tục enqueue, thì front sẽ luôn chỉ tới giá trị ở đầu hàng đợi, trong khi rear sẽ tăng để trỏ tới các vùng nhớ tiếp theo về phía cuối hàng đợi.

+ Sau khi hàng đợi đầy, ta tiến hành dequeue thì lúc này do chỉ số rear đã trỏ đến cuối hàng đợi nên nó sẽ không cho phép ta enqueue nữa, mặc dù vùng nhớ ở đầu hàng đợi mà ta vừa dequeue giá trị, đang trống. Chính vì vậy nó sẽ gây lãng phí memory và có thể được coi là 1 nhược điểm của linear queue

<p align = "center">
<img src = "https://github.com/user-attachments/assets/df3db37c-321d-4489-b4ef-cde304b6d6e7" widht = "450" height = "250">

=> Khi ta dequeue hết tất cả phần tử trong queue, lúc này chỉ số front bằng với rear, khi đó chúng sẽ được reset về -1. Quá trình enqueue mới được cho phép

### b) Circular queue

+ Cơ chế của circular cũng tương tự như linear, tuy nhiên nó tối ưu hơn do giải quyết được vấn đề của linear. Nó cho phép ta tiếp tục enqueue au khi dequeue 1 full queue

## 2.3 Mô phỏng cấp phát cơ chế queue

+ đầu tiên ta tạo ra 1 struct lưu trữ các thuộc tính của queue

```bash
typedef struct Queue
{
    int *queue_item; //mảng để lưu các thành phần 
    int size;        //kích thước mảng queue
    int front;       //chỉ số truy cập vào phần tử đầu hàng đợi
    int rear;        //chỉ số truy cập vào phần tử cuối hàng đợi
}Queue;
```
+ Tiếp theo ta tạo ra 1 hàm để khởi tạo 1 queue 

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
+ Ta sẽ có 2 hàm để kiểm tra queue đầy hay rỗng

```bash
bool IsQueue_Empty(Queue queue)
{
    return ((queue.front == -1) ? true : false); 
}
```  
### a) Linear queue
+ Đối với linear queue thì điều kiện để 1 queue đầy sẽ khác circular queue
```  
bool IsQueue_Full(Queue queue)
{
    /* circular */
    return (queue.rear + 1) % queue.size == queue.front; //khi front = 0 và rear = size - 1
    /* linear */
    //return ((queue.rear == queue.size - 1) ? true : false); 
}

```  
+ Tiếp theo ta viết hàm để enqueue phần tử vào queue 
+ Để enqueue thì trước hết ta phải đảm bảo queue không đầy
+ Tiếp theo ta sẽ kiểm tra nếu queue rỗng thì sẽ cập nhật chỉ số front và rear đều bằng 0 
+ Nếu queue không rỗng thì ta chỉ tăng giá trị rear để enqueue phần tử vào, còn chỉ số front thì luôn luôn trỏ tới phần tử đầu tiên của hàng đợi
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
+ Ta viết hàm dequeue để lấy phần tử đầu tiên của hàng đợi ra
+ Trước khi dequeue ta cũng kiểm tra liệu có phần tử nào trong queue không
+ Nếu queue không rỗng ta sẽ in giá trị hiện tại ra và kiểm tra liệu chỉ số front có nhỏ hơn rear không
+ nếu front chưa bằng rear, có nghĩa là vẫn còn phần tử phía sau, lúc này ta tiếp tục tăng chỉ số front để dequeue phần tử tiếp theo
+ Nếu front bằng rear, nghĩa là không còn phần tử nào phía sau cã, lúc này ta sẽ reset giá trị front và rear để chuẩn bị cho lần enqueue tiếp theo

```bash

void dequeue(Queue *queue)
{
    if (!IsQueue_Empty(*queue))
    {
        printf("dequeue %d -> %p\n", queue->queue_item[queue->front], &queue->queue_item[queue->front]);
        if (queue->front == queue->rear)
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
+ In ra kết quả ta được

```bash
***enqueue process***
enqueue 1 -> 000001F5D4169690
enqueue 2 -> 000001F5D4169694
enqueue 3 -> 000001F5D4169698
enqueue 4 -> 000001F5D416969C
enqueue 5 -> 000001F5D41696A0
***dequeue 2 element***
dequeue: 1
dequeue: 2

elements in queue
queue 3
queue 4
queue 5

enqueue more
enqueue 6 -> 000001F5D4169690
enqueue 7 -> 000001F5D4169694

elements in queue
queue 6
queue 7
queue 3
queue 4
queue 5
```
# 3 So sánh stack và queue

<p align = "center">
<img src = "https://github.com/user-attachments/assets/d64c2f7c-3557-4701-850c-7302fbf944c9" wisth = "600" height = "400">


    














