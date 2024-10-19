
# Chương trình quản lý thông tin học sinh và sắp xếp theo từng hạng mục
đầu tiên ta tạo ra 1 struct lưu trữ thông tin học sinh
```bash
typedef struct {
   char ten[50];
   float diemTrungBinh;
   int id;
} SinhVien;
```
sau đó trong hàm main ta tạo ra 1 mảngmảng struct kiểu SinhVien và truyền vào thông tin của từng học sinh
```bash
   SinhVien danhSachSV[] = {
       {  
           .ten = "Doang",
           .diemTrungBinh = 7.5,
           .id = 100
       },
       {
           .ten = "Cuan",
           .diemTrungBinh = 4.5,
           .id = 101
       },
       {
           .ten = "Cy",
           .diemTrungBinh = 6.8,
           .id = 102},
       {  
           .ten = "Agan",
           .diemTrungBinh = 5.6,
           .id = 10
       },
   };
```
tiếp theo ta tạo ra 1 hàm sorting tổng quát để sắp xếp danh sách học sinh theo hạng mục mong muốn 
```bash
void sort(SinhVien* array, size_t size, int (*compareFunc)(const void *, const void *)) {
   int i, j;
   SinhVien temp;
   for (i = 0; i < size-1; i++)    
       for (j = i+1; j < size; j++)
        //sắp xếp theo điều kiện tăng dần 
           if (compareFunc(array+i, array+j)>0) {
               temp = array[i];
               array[i] = array[j];
               array[j] = temp;
           }
}
``` 
#### Giải thích vai trò của con trỏ hàm compareFunc
* Con trỏ hàm compareFunc được sử dụng như 1 tham số đầu vào để lưu địa chỉ của các hàm theo từng hạng mục mà ta muốn sắp xếp 
+ tham số truyền vào của compareFunc cũng được khai báo là kiểu const void* cho biết hàm không quan tâm đến kiểu dữ liệu truyền vào của hàm đó là gì, và việc ép kiểu dữ liệu cụ thể sẽ được thực hiện bên trong hàm được trỏ đến
+ Tham số truyền vào được khai báo là const, để đảm bảo dũ liệu mà ta truyền vào hàm không thể can thiệp thay đổi mà chỉ có thể đọc ra và so sánh
### Tạo ra các hàm trỏ tới hạng mục cần so sánh

```bash
int compareByName(const void *a, const void *b) {
//ép lại kiểu dữ liệu mà ta muốn thao tác
   SinhVien *sv1 = (SinhVien *)a;
   SinhVien *sv2 = (SinhVien *)b;
//truyền vào địa chỉ của từng chuỗi
   return stringCompare(sv1->ten, sv2->ten);
}

int compareByID(const void *a, const void *b) {
   SinhVien *sv1 = (SinhVien *)a;
   SinhVien *sv2 = (SinhVien *)b;
   return sv1->id - sv2->id;
}

int compareByDiemTrungBinh(const void *a, const void *b) {
   SinhVien *sv1 = (SinhVien *)a;
   SinhVien *sv2 = (SinhVien *)b;
   if (sv1->diemTrungBinh > sv2->diemTrungBinh)
   {
       return 1;
   }
  
   return 0;
}
```
+ điểm chung của các hàm trên sẽ trả về 1 số nguyên bằng cách lấy giá trị đầu trừ cho giá trị sau, và giá trị này sẽ quyết định có thực hiện việc sắp xếp hay không 
#### Hàm so sánh chuỗi
```bash
int stringCompare(const char *str1, const char *str2) {
   while (*str1 && (*str1 == *str2)) {
       str1++;
       str2++;
   }
   return *(const unsigned char*)str1 - *(const unsigned char*)str2;
}
```
+ tham số const char* chỉ ra rằng chuỗi truyền vào chỉ dùng để so sánh chứ không thể thay đổi
+ việc ép kiểu thành const unsigned char* cho biết giá việc xử lý tính toán chỉ diễn ra ở giá trị dương, tránh việc hệ điều hành hiểu nhầm lấy các ký tự âm từ -127 đến 127.Có thể trả về những kết quả không mong muốn
#### trong hàm main ta gọi hàm sort 
+ có thẻ thấy địa chỉ của 1 trong 3 hàm mà ta vừa định nghĩa ở trên được truyền vào hàm sort
```bash
sort(danhSachSV, size, compareByName);
```
#### Quá trình xử lý hàm compareByName trong hàm sort 
```bash
int i, j;
   SinhVien temp;
   for (i = 0; i < size-1; i++)    
       for (j = i+1; j < size; j++)
           if (compareFunc(array+i, array+j)>0) {
               temp = array[i];
               array[i] = array[j];
               array[j] = temp;
           }
```
+ ta sẽ dùng 2 vòng lặp để quét qua từng phần tử của mảng struct, đồng thời gọi con trỏ hàm compareFunc và truyền vào đối số của phần tử i và j 
+ vì compareFunc lúc này đang trỏ tới hàm compareByName nên hàm này sẽ được gọi và xử lý, cùng với việc trả về giá trị lớn hơn hoặc bằng 0
+ Nếu giá trị trả về của compareFunc lớn hơn 0 thì sẽ thực hiện hoán vị 2 giá trị
+ Điều tương tự cũng lặp lại khi ta truyền địa chỉ của các hàm giữ đối tượng mà ta sắp xếp vào hàm sort
#### In ra kết quả sắp xếp
```bash
void display(SinhVien *array, size_t size) {
   for (size_t i = 0; i < size; i++) {
       printf("ID: %d, Ten: %s, Diem Trung Binh: %.2f\n", array[i].id, array[i].ten, array[i].diemTrungBinh);
   }
   printf("\n");
}
```
+ Ta truyền vào con trỏ, trỏ tới địa chỉ của danh sách mà ta vừa sắp xếp và in ra thông tin 




    
    

