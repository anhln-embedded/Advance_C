# 1. Struct 
Đây là từ khóa để định nghĩa 1 kiểu dữ liệu người dùng, mục đích để tạo nên 1 kiểu dũ liệu để mô tả 1 đối tượng cụ thể nào đó khác với các kiểu dữ liệu nguyên thủy như int,float,double,...
## 1.1 Khai báo
Ví dụ ta cần khai báo 1 struct để lưu trữ thông tin học sinh, thì ta sẽ làm như sau
```bash
  struct info{
    int tuoi;
    char name[30];
  }
```
ta sẽ tạo ra 1 biến struct và thực hiện gán data, in ra như sau

```bash
 int main(){
    struct info student;
    student.tuoi = 23;
    student.name = "duypham";
    printf("tuoi: %d\name: %s\n",student.tuoi,student.name);
    return 0;
};
```
Tuy nhiên cách khai báo biến struct như trên còn khá dài dòng khi ta phải gọi lại từ khóa struct. Vì vậy sẽ dùng từ khóa typedef và định nghĩa lại struct như sau
```bash
tyepdef struct{
    int tuoi;
    char name[30]; 
}info;
int main(){
    info student; //chỉ gọi tên struct không cần phải có từ khóa struct phía trước
}
```

## 1.2 Kích thước
kích thước của struct sẽ phụ thuộc vào 2 yếu tố sau
### a) Data Alignment
căn chỉnh data trong struct là việc 1 biến khi được cấp phát vùng nhớ thì nó phải được lưu ở giá trị địa chỉ được quy định bởi compiler và kiến trúc hệ thống, để đảm bảo được việc truy cập chính xác và nhanh chóng.

```bash
  typedef struct{
    uint8_t id;   //1 byte
    char* name;   //8 byte (x64)
    int tuoi; //1 byte
  }info;
```
Nhìn vào struct trên thì ta có thể tính được tổng kích thước của struct là 10 byte. Nhưng thực tế thì không phải như vậy. Để biết rõ kích thước ta sẽ thực hiện in ra như sau

```bash
int main(){
    info student = {23,"duysolo",25};
    printf("%d\n",sizeof(student));
    printf("&id:0x%p\n&name: 0x%p\n&tuoi: 0x%p",&student.id,&student.name,&student.tuoi);
    return 0;
}
```
kết quả 
```bash
size of info: 24
&id:0x000000D9A91FFBD0
&name: 0x000000D9A91FFBD8
&tuoi: 0x000000D9A91FFBE0
```
* Như vậy tổng kích thước thực của struct là 24 byte. Mõi lần nó sẽ cấp phát 8 byte do yêu cầu của việc căn chỉnh vùng nhớ và dựa vào biến có kiểu dữ liệu lớn nhất là char*
+ Do đó tổng kích thước của struct sẽ luôn là con số chia hết cho kiểu dữ liệu lớn nhất được khai báo, địa chỉ bắt đầu của các thành phần trong struct cũng sẽ tuân theo quy luật này
### b) Padding byte
+ Đây là những byte được thêm vào sau địa chỉ của mỗi biến được khai báo để đảm bảo được quy tắc căn chỉnh của từng thành viên hoặc cả struct. 
+ Dùng lại ví dụ trên ta hình dung được việc cấp phát vùng nhớ diễn ra như sau. 
![image](https://github.com/user-attachments/assets/4bcff813-7821-4f77-8232-033dd5384a0e)
Dựa vào bảng trên ta thấy:
+ 7 byte padding sau biến id: để đảm bảo biến name được cấp phát tại địa chỉ có giá trị chia hết cho kiểu dữ liệu của chính nó, và cũng là biến nó kiểu lớn nhất trong struct
+ 4 byte padding sau biến tuoi: giúp cho tổng số byte trong struct là 24 chia hết cho 8, là số byte mà biến có kiểu dữ liệu lớn nhất name được khai báo

Ngoài ra ta cũng có thể lưu các giá trị mảng trong struct như sau
```bash
typedef struct{
    char a[10];
    double b[2];
    int c[5]; 
}std;
```
+ biến b có kiểu dữ liệu lớn nhất double, vì vậy việc căn chỉnh dữ liệu sẽ phu thuộc vào biến này. Do đó struct sẽ cấp phát mỗi lần 8 byte để lưu trữ các biến.
+ Ta có thể hình dung được việc cấp phát memory diễn ra như sau
![image](https://github.com/user-attachments/assets/5f956f48-61de-4cbd-a3fe-f0762130ed0a)
+ Mảng a[10] sẽ được cấp phát memory 2 lần để lưu trữ các phần tử, và thừa ra 6 padding byte. Tổng là 16 byte
![image](https://github.com/user-attachments/assets/53278cea-0b60-4fa2-af4f-cd11158b8282)
+ Mảng b[2] sẽ được cấp phát memory 2 lần, và không có padding byte, do mỗi phần tử của nó đèu chiếm 8 byte, tồng là 16 byte
![image](https://github.com/user-attachments/assets/89f7d369-80ec-4621-bb8d-4a92f7f713e7)
+ Mảng c[5] sẽ được cấp phát memory 3 lần, mỗi lần cấp phát sẽ lưu trữ được 2 phần tử kiểu int, vì vậy ở lần cấp phát thứ 3, sẽ thừa ra 4 padding byte
Do đó dựa vào kích thước của mỗi thành phần ta có kích thước tổng của struct std sẽ là 56 byte

### c) Đặc điểm của cấp phát vùng nhớ trong struct
+ Địa chỉ bắt đầu của từng thành viên phải phụ thuộc vào yêu cầu căn chỉnh của chính thành viên đó
+ Tổng kích thước của struct là bội số của thành viên có kiểu dữ liệu lớn nhất trong 
# 2. union 
union cũng có cách sử dụng như stuct, tuy nhiên 
+ các biến khai báo bên trong sẽ sử dụng chung 1 vùng nhớ
+ kích thước của union sẽ phụ thuộc vào biến có số byte của chính nó và byte padding là lớn nhất
```bash
typedef union{
    int a[5];    // 8 byte + 8byte + 4 byte + 4 padding
    short b[4];  // 8 byte
    double c[2]; // 8 byte + 8 byte
}hi;
```
dựa vào số byte được tính như trên thì kích thước của struct sẽ là 24 byte với biến int a[5] chiếm số byte lớn nhất

## 2.1 Gán giá trị cho các thành phần union
Khi ta gán giá trị cho từng biến và in ra sẽ có sự khác biệt so với khi dùng struct
```bash
typedef union{
    int a;
    double b;
    short c;
}data;
int main(){
    data data1;
    sizeof(data);
    data1.a = 11;
    data1.b = 23;
    data1.c = 213;
    printf("a:%d\n",data1.a);
    printf("b:%d\n",data1.b);
    printf("c:%d\n",data1.c);
    return 0;
}
```
thực hiện 3 giá trị trên ta được kết quả như sau
```bash
a:213
b:213
c:213
```
Lý do là vì việc sử dụng chung vùng nhớ của các biến, các biến sau khi gán giá trị sẽ ghi đè lên giá trị của biến trước. Chính vì khi thực hiện ra 3 giá trị, thì ta chỉ in ra được giá trị của biến cuối cùng được gán giá trị.
