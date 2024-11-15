# 1. Binary Search
# 1.1 Định Nghĩa
Thuật toán dùng để tìm kiếm và trả về 1 giá trị nếu nó tồn tại trong 1 mảng đã được sắp xếp bằng cách so sánh giá trị cần tìm với giá trị ở chính giữa mảng.
# 1.2 So sánh Binary và Linear Search

<img src = "https://github.com/user-attachments/assets/d0eea437-3207-4bcc-91f0-54c30a8c3a6d" width = "700" height = "250">

__+ Linear Search:__ Mỗi phần tử trong mảng sẽ được so sánh với tất cả các phần tử còn lại và số lần kiểm tra sẽ là kích thước của mảng trừ đi 1. Đối với mảng lớn có số lượng phần tử không xác định thì cách này sẽ tốn thời gian xử lý và giảm hiệu suất CPU

__+ Binary Search:__ Giá trị cần tìm sẽ được so sánh vói phần tử ở giữa mảng thay vì tát cả phần tử, và giá trị __mid__ này sẽ được cập nhật qua mỗi lần kiểm tra để thu hẹp phạm vi tìm kiếm, dẫn đến hiệu suất nhanh và hiệu quả hơn. Tuy nhiên cách này sẽ yêu cầu 1 mảng đã sắp xếp
# 1.3 Triển khai 
### a) Giải thích thuật toán
+ Ví dụ ta muốn tìm giá trị __search__ =  25 trong mảng sau đây
<p align = "center">
<img src = "https://github.com/user-attachments/assets/0ee2ac98-9db3-4d50-8a59-6623c898f52d" width = "750" height = "350">

__+ Bước 1:__ ta sẽ sử dụng 2 chỉ số left (đầu mảng) và right(cuối mảng) để xác định được phần tử mid (giữa mảng)

__+ Bước 2:__ Ta so sánh giá trị mid và __search__

__+ Bước 3:__ Ta thu họn vùng giá trị kiểm tra dựa vào kết quả bước 2 

=> nếu giá trị mid > search : ta cập nhật mid += 1 -> left = mid __(vùng kiểm tra bỏ phần bên trái mid)__

=> nếu giá trị mid < search : ta cập nhật mid -= 1 -> right = mid  __(vùng kiểm tra bỏ phần bên phải mid)__

__+ Bước 4:__ Ta lặp lại bước 1 cho đến khi giá trị mid = search 

### b) Demo code thuật toán
+ Đầu tiên ta sẽ cần phải sắp xếp lại các phần tử trong mảng theo thứ tự trước khi thực hiện việc tìm kiếm binary search. Ta sẽ sử dụng thuật toán __bubble sort__ 
=> Đặc điểm của thuật toán bubble sort đó là sau mỗi lần lặp kiểm tra, số lượng phần tử được duyệt qua cũng sẽ giảm dần do các giá trị lớn hơn sẽ được đẩy về cuối mảng. 

```bash
void bubble_sort(int* pArr,int len){
    int temp = 0;
//vòng for ngoài chứa mảng đã sắp xếp
    for(int i = 0 ; i < len - 1 ; i++){
//vòng for trong sẽ so sánh giá trị hiện tại với tiếp theo
        for(int j = 0 ; j < len - i - 1; j++){
            if(pArr[j] > pArr[j + 1]){
                temp = pArr[j];
                pArr[j] = pArr[j+1];
                pArr[j+1] = temp;
            }
        }
    }
}
```
Tiếp theo ta sẽ triển khai hàm binary search như sau

+ Ta kiểm tra mảng có hợp lệ không, Nếu thỏa mới xử lý tiếp
+ Ta thực hiện tính toán giá trị mid và so sánh với search
+ Nếu bàng nhau ta trả về kết quả là true __(tìm thấy search)__
+ Nếu giá trị mid > hoặc < hơn search thì thực hiện cập nhật chỉ số mid mới và gán cho chỉ số left hoặc right và thực hiện đệ quy để quay lại kiểm tra tiếp
+ Nếu chỉ số left >= right mà giá trị mid khác search thì trả về false__(không tìm thấy search)__ 
    
```bash
bool Binary_Search(int* pArr,int left,int right,int search){
    if(left <= right){
        int mid = (left + right) / 2;
        if(search == pArr[mid])           return true;
        else{
            if(search > pArr[mid])      return Binary_Search(pArr,mid + 1,right,search);
            else                        return Binary_Search(pArr,left,mid - 1,search);
        }
    }
   return false;
}
```
Trong chương trình chính, ta thực hiện kiểm tra như sau
```bash
void Sorting_print(int arr[],int len){
    for(int i = 0 ; i < len ;i++)
        printf("%d\t",arr[i]);
}
int main(){
    int arr[] = {12,52,15,62,457,21,58,31,5};
    int len = sizeof(arr)/sizeof(arr[0]);
    bubble_sort(arr,len);
    Sorting_print(arr,len);
    int search = 21;
    bool result = Binary_Search(arr,0,len-1,search);
    printf("\n%s gia tri %d",(result == true)? "tim thay " : "khong tim thay",search);
    return 0;
}
```
Kết quả in ra màn hình
    
```bash
5       12      15      21      31      52      58      62      457
tim thay  gia tri 21
```
# 2.Binary Tree và Sorting linkest list
Giống như việc tìm kiếm 1 phần tử trong mảng, ta cũng có thể áp dụng thuật tìm kiếm nhị phân cho 1 linkest list. Tuy nhiên ta sẽ cần phải chuyển đổi 1 nó sang dạng binary tree như sau

<p align = "center">
<img src = "https://github.com/user-attachments/assets/13602b61-cf2f-4d28-984e-4d20bdc9e35b" width = "800" height = "300">

+ Sau khi chuyển đổi linkest list được tổ chức theo dạng tuyến tính sang binary tree có thể chia đôi không gian tìm kiếm, và loại trừ khu vực không chứa giá trị tìm cần tìm. Ta có thể đơn giản hóa và nhanh chóng tìm được giá trị mong muốn 

## 2.1 Sorting Linkest List
Để có thể tìm kiếm 1 node trong danh sách liên kết đầu tiên ta cũng sẽ thực hiện sắp xếp các node theo thứ tự từ min đến max
+ Ta sẽ có 1 hàm để tạo ra 1 node, và sẽ thực hiện sắp xếp đồng thời với mỗi 1 node mới được thêm vào 

```bash
void add_node(Node **head, int value) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    new_node->data = value;
    new_node->next = NULL;

/*kiem tra list va them node theo thu tu min -> max*/
    
//Nếu node đầu trong list lớn hơn node mới
    if (*head == NULL || (*head)->data >= value){
        new_node->next = *head;
        *head = new_node;
        return;
    }
  / 
//nếu các node nhỏ hơn node mới
    Node *current = *head;
    while (current->next != NULL && current->next->data < value) {
        current = current->next;
    }
//chen node mới vào trước node hiện tại có giá trĩ lớn hơn nó
    new_node->next = current->next; 
    current->next = new_node; 
}
```
+ Ta có thể hình dung đoạn code trên như sau 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/1d4af506-0024-4a2c-8921-209fd7c5bc49" width = "450" height = "250">

## 2.2 Binary tree 
Đầy là 1 cấu trúc dữ liệu dạng cây, với 1 node cha trỏ đến 2 node con bên trái và phải của cây, mỗi node sẽ chứa value của nó và tham chiếu đến các node con bên dưới nó. Một binary tree sẽ có 1 __root__ node gốc và liên kết tới các node con bên dưới. Cấu trúc này được áp dụng để tìm kiếm và sắp xếp, tổ chức dữ liệu 1 cách hiệu quả
### a) Viết hàm xây dựng binary tree
+ Ta sẽ có 1 struct để mô tả 1 node trong binary tree như sau

```bash
typedef struct CenterPoint {
    int value; //giá trị của node parents
    struct CenterPoint *left;  // node children bên trái
    struct CenterPoint *right; // node children phải
} CenterPoint;
```

+ Tiếp theo ta cần xác định điểm giữa của linkest list, để tạo ra được node gốc (__root__) cho binary tree

```bash
CenterPoint *centerPoint(Node *head) {
    int length = 0;
    Node *node = head;
    while (node != NULL) {
        node = node->next;
        length++;// number of nodes
    }
    return buildTree(head, 0, length - 1);
}
```

+ Hàm trên sẽ tìm kiếm node root đồng thời gọi đến hàm __buildTree__ để tạo ra các nhánh và trả về toàn bộ node đã được liên kết thành 1 binary tree hoàn chỉnh, hàm __buildTree__ sẽ được triển khai như sau

```bash
CenterPoint *buildTree(Node *head, int start, int end) {
//if linkest list doesn't have node 
    if (head == NULL || start > end) {
        return NULL;
    }
//locate mid position of list
    int mid = (start + end) / 2;
    Node *node = head;
//traverse through list untill encounter mid node
    for (int i = start; i < mid; i++) {
        if (node->next == NULL) {
            break;
        }
        //move to next node
        node = node->next;
    }

//allocate memory for storing current root of tree
    CenterPoint *root = (CenterPoint *) malloc(sizeof(CenterPoint));
    root->value = node->data;
//create left and right root 
    root->left = buildTree(head, start, mid - 1); 
    root->right = buildTree(node->next, mid + 1, end);

    return root;
}
```
+ Sau khi xác định được node root của binary tree ta sẽ xác dịnh 2 node con của node nó và mỗi node con cũng sẽ trỏ tới các node bên dưới nữa
+ Các node còn này sẽ được xác định ở vị trí của các điểm giữa của linkest list mà binary tree dựa trên để xây dưng
+ Node con __bên trái__ sẽ nằm ở giữa tính từ vị trí node đầu của linkest list đến vị trí của root node là __mid - 1__ 
+ Node con __bên phải__ sẽ nằm ở giữa tính từ vị trí sau root node là __mid + 1__ của linkest list đến node cuối của linkest list 
+ Các nhánh nhỏ hơn của binary tree cũng sẽ được tiếp tục tạo ra dựa trên quy tắc trên 

### b) Viết Hàm binary search

+ Ta sẽ thực hiện tìm kiếm dựa trên binary tree đã xây dựng
+ Nếu giá trị tìm kiếm lớn hay nhỏ hơn giá trị hiện tại trong binary tree thì ta sẽ thực hiện kiểm tra đến node con của các nhánh phía dưới của tree

```bash
CenterPoint *binarySearch(CenterPoint *root, int search) {
    static int loop = 0;
    loop++; // số lần tìm kiếm
    printf("so lan lap: %d\n", loop);
    if (root == NULL) {
        return NULL;
    }

    if (root->value == search) {
        return root;
    }

    if (search < root->value) {
        return binarySearch(root->left, search);
    } else {
        return binarySearch(root->right, search);
    }
}
```


## 2.3 Triển khai trong chương trình chính 
+ Đầu tiên ta sẽ viết 1 hàm để in ra các node hiện có trong linkest list
```bash
void print_list(Node *head) {
    while (head != NULL) {
        printf("%d ", head->data);
        head = head->next;
    }
    printf("\n");
}

```
+ Trong chương trình chính ta sẽ tạo ra 1 linkest list và thêm vào các node
+ Tiếp theo tạo ra 1 binary tree và dùng con trỏ ptr để trỏ tới nó 
+ Ta sẽ trả về kết quả tìm kiếm thông qua hàm __binarySearch__ 
```bash
int main() {
    Node *head = NULL;
    add_node(&head,98);
    int arr[] = {321,12,15,90,112,86,14,521,46,13,64,1,35};
    int len = sizeof(arr)/ sizeof(arr[0]);
    // tao ngau nhien 10000 node
    //srand(time(NULL));
    for (int i = 0; i < len; i++) {
        //int value = rand() % 10 + 1;
        add_node(&head,arr[i]);
    }

    //add_node(&head, 5639);

    print_list(head);
    //use ptr storing address of created binary tree
    CenterPoint *ptr = centerPoint(head);

    int value = 86;
    CenterPoint *result = binarySearch(ptr, value);
    if (result != NULL) {
        printf("Tim thay %d\n", result->value);
    } else {
        printf("Khong tim thay\n");
    }

    return 0;
}
```
+ Kết quả in ra màn hình 

```bash
1 2 6 9 12 13 14 15 35 46 64 86 90 98 112 321 521 
so lan lap: 1
so lan lap: 2
so lan lap: 3
so lan lap: 4
Tim thay 86
```
### c) Ưu và Nhược điểm 

__Ưu điểm:__ 

+ Tìm kiếm nhanh chóng với mảng có số lượng phần tử lớn

__Nhược điểm:__

+ Phải tốn bộ nhở cấp phát cho nỗi 1 nhánh tạo ra trong binary tree
+ Tăng độ phức tạp khi phải quản lý cùng lúc 2 kiểu dữ liệu __(struct)__ là linkest list và binary tree

# 3. File Operation
# 3.1 Khái niệm
Là quy trình thao tác với 1 file định dạng .txt hoặc .csv, là các file được dùng để lưu trữ 1 cơ sở dữ liệu mà ta sẽ sử dụng để trích xuất những thông tin cần thiết để thực hiện 1 công việc nào đó.

<p align = "center">
<img src = "https://github.com/user-attachments/assets/456ab4fe-19d8-4d59-9922-948ad62c68af" width = "500" height = "250">

## 3.2 Các hàm thao tác file
### a) Hàm mở file 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/1a435226-c955-434b-ace2-8db0b2d45dbb" width = "400" height = "100">

__file__: con trỏ lưu trữ file trả về

__file_name:__ đường dẫn đến file 

__access_mode:__ chế độ thao tác với file

__+ Các chế độ thao tác phổ biến__

+ __"r"__: Mở file với chế độ đọc. Nếu mở thành công trả về địa chỉ của phần tử đầu tiên trong file, nếu không không trả về NULL
+ __"r+__:  Mở file với chế độ đọc và ghi file. Nếu mở thành công trả về địa chỉ của phần tử đầu tiên trong file, nếu không trả về NULL
+ __"w"__: Mỡ file với chế độ ghi. Nếu file chưa có thì tạo file mới, nếu đã tồn tại thì ghi đè nội dung. Nếu mở thất bại trả về NULL
+ __"w+"__: Mở file với chế độ ghi và đọc. Nếu file tồn tại trả về địa chỉ của phần tử đầu. Nếu file chưa tồn tại tạo một file mới
+ __"a"__: Mở file với chế độ nối. Nếu mở thành công trả về địa chỉ của phần tử cuối cùng trong file. Nếu file chưa tồn tại thì sẽ tạo mới. Nếu không mở được file trả về NULL.
+ __"a+"__:  Mở file với chế độ nối và đọc. Nếu file đã tồn tại trả về địa chỉ của phần tử cuối cùng của file. Nếu file chưa tồn tại tạo một file mới

### b) Hàm ghi file 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/9b1f07f3-d287-4ff1-bd51-c55c538acfc9" width = "500" height = "200">

### c) Hàm đọc file

<p align = "center">
<img src = "https://github.com/user-attachments/assets/a5b8eb8e-8fd5-4bd8-84c1-bf3567785e99" width = "500" height = "200">

## 3.3 Quy trình đọc và ghi file

### a) Quy trình tạo và Ghi file

+ Đầu tiên ta sẽ tạo ra 1 file database để lưu trữ dũ liệu sẽ ghi/đọc bằng cách tạo folder đặt tên database nằm trong thư mục dự án, bên trong database ta tạo ra 1 file csv như sau

<p align = "center">
<img src = "https://github.com/user-attachments/assets/fcd98dda-04a9-4e9d-a862-250cd119587d" width = "600" height = "300">

+ Tiếp theo ta viết 1 hàm để ghi file như sau 

```bash
#define FAIL_CREATED_FILE    0
#define SUCCESS_CREATED_FILE 1
bool writeCSV(char* path){
    FILE* file = fopen(path,"w");
    if(file == NULL){
        printf("cannot open file\n");
        return FAIL_CREATED_FILE;
    }
    fprintf(file,"ten,tuoi,so dien thoai,dia chi\n");
    fprintf(file,"Nguyen Ho Duy,17,0906733209,22/5 Binh Thuan\n");
    fprintf(file,"Nguyen Thanh Tai,20,0376572231,18 Nguyen Thi Minh Khai Q1 TPHCM\n");
    fprintf(file,"Nguyen Thi Thanh Thuy,27,038764987,21 Nguyen Thien Thuat P12 QTan Phu\n");
    fclose(file); 
    return SUCCESS_CREATED_FILE;
}
```
+ trong chương trình chính ta sẽ thực hiện việc ghi file như sau


```bash
#define PATH_FILE   ".\\database\\thongtin.csv" // định nghĩa đường dẫn đến file
const char* str[] = {"File has been written\n","Failed to open file\n"};
int main(){
    if(writeCSV(PATH_FILE) == SUCCESS_CREATED_FILE)
        log_status(str[0]);
    else
        log_status(str[1]);
    return 0;
}
```
### b) Quy trình Đọc file và xử lý dữ liệu
+ Đầu tiên ta cần tạo ra 1 struct để lưu trữ thông tin đọc về từ file như sau
    
```bash
typedef struct{
    char* name;
    int age;
    char* phone;
    char* address;
}Info;
```
+ Ta sẽ sử dụng hàm sau để đọc ra hàm đầu tiên trong file cũng là hàm để in ra tiêu đề chứa các trường thông tin mà ta sẽ xử lý và lưu các thành viên trong struct trên
```bash
void readCSV(char *path)
{
//mảng tạm để luu trữ thông tin đọc về ở dòng hiện tại
    char line[100];
//mở file và đọc
    FILE *file = fopen(path, "r");
    if (file == NULL)
    {
        printf("can't read file\n");
        return NULL;
    }
//đọc dòng đầu của file
    fgets(line, sizeof(line), file);
    printf("%s", line);
    /*
        xử lý dọc và tách các thông tin ứng với các trường 
    */
}
```
+ Tiếp theo ta sẽ có đoạn code sau để đọc lần lượt từng dòng và phân tích chuỗi lưu vào các biến struct 


```bash
//cấp phát vùng nhớ cho biến con trỏ kiểu struct Info
Info* info = (Info*)malloc(sizeof(Info));
//đọc và kiểm tra đến khi không còn ký tự nào ttrong file
while (fgets(line, sizeof(line), file) != NULL){
    char* tokken = NULL;
    //duyệt qua từng ký tự cho đến khi gặp ',' trả về địa chỉ của chuỗi vừa phân tách được 
    token = strtok(line, ",");    
    
    //cấp phát vùng nhớ cho thành viên bên trong struct
    info->name = (char *)malloc(strlen(token) + 1);

    //copy chuỗi trỏ đến bởi token vào vùng nhớ vừa được cấp phát
    strcpy(info->name, token); // copy token into heap memory

    //ở lần gọi hàm strtok thứ hai trở đi những phần tử đã duyệt qua đều được coi là NULL
    token = strtok(NULL, ",");
    info->age = (uint8_t)atoi(token);

    // Parse phone
    token = strtok(NULL, ",");
    info->phone = (char *)malloc(strlen(token) + 1);
    strcpy(info->phone, token);

    // Parse address
    token = strtok(NULL, ",");
    info->address = (char *)malloc(strlen(token) + 1);
    strcpy(info->address, token);

    //in ra thông tin từng dòng và giải phóng vùng nhớ
    printf("%s %d %s %s\n",info->name,info->age,info->phone,info->address);
    free(info->name);
    free(info->phone);
    free(info->address);
}
```
+ Kết quả chạy chương trình ta được 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/12dc404b-72e5-44e4-a4ad-d24e4e4c177e" width = "700" height = "400">
