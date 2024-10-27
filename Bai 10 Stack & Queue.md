
# STACK & QUEUE
# 1. STACK 
## 1.1. Đặc điểm
+ Vùng nhớ lưu trữ biến cục bô,tham số hàm, địa chỉ trả về của hàm
+ Được giải phóng khi hàm kết thúc
+ Quyền truy cập: đọc/ghi 
+ Cấp phát và giải phóng vùng nhó theo cơ chế LIFO
## 1.2. Quy trình quản lý memory trên stack
### 1.2.1. Hoạt động của stack
Mỗi khi có 1 biến được khai báo cục bộ, hay 1 hàm được gọi. Vùng nhớ của nó sẽ được đẩy vào stack, thành phần được cấp phát sau cùng cũng sẽ được giải phóng đầu tiên, trong khi vùng nhớ cấp phát đầu tiên sẽ được giải phóng sau cùng. 

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

## 1.3 Ứng dụng của stack

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

1.3.2 Mô phỏng code cấp phát trên stack

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
void push(Stack *stack, int value) {
    if (is_full(*stack) == false) {
        stack->items[++stack->top] = value; //gán giá trị trước khi dịch đến địa chỉ tiếp theo
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

+ Ta sẽ kết hợp các hàm đã tạo ở trên để gọi trong hàm main 
```bash
int main() {
    Stack stack1;
    size_t size = 5;
    initialize(&stack1,size);
    printf("push process\n");
    for(size_t i = 0 ; i < size ; i++){
        push(&stack1,i);
        printf("element: %d -> add:%p\n",i,stack1.items[i],&stack1.items[i]);
    }
    printf("pop process\n");
    for(size_t i = 0; i < size ; i++){
        printf("top element: %d -> add:%p\n",i,pop(&stack1),&stack1.items[i]);
    }
    printf("top element: %d",top(stack1));
    return 0;
}
```

Kết quả in ra màn hình
```bash
push process
element: 0 -> add:0000000000000000
element: 1 -> add:0000000000000001
element: 2 -> add:0000000000000002
element: 3 -> add:0000000000000003
element: 4 -> add:0000000000000004
pop process
top element: 0 -> add:0000000000000004
top element: 1 -> add:0000000000000003
top element: 2 -> add:0000000000000002
top element: 3 -> add:0000000000000001
top element: 4 -> add:0000000000000000
Stack is empty
top element: -1
```


