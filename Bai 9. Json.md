# Kiểu dữ liệu Json
## 1. Lý Thuyết
### 1.1 Định nghĩa
Đây là 1 định dạng để truyền tải dữ liệu giữa các hệ thống với nhau ,và dữ liệu thường được chuẩn hóa về dạng chuỗi (__json string__) chứa nhiều loại dữ liệu khác bên trong. 
### 1.2 Cấu trúc
Json là 1 chuỗi chứa các dữ liệu được chuẩn hóa như sau :

__+ Object__ : tập hợp của các cặp key - value được ngăn cách bởi dấu phẩy, 

+ key: có kiểu char* 
+ value: bất kỳ loại dữ liệu nàonào 
+ Định dạng: thường được đặt trong 2 dấu ngoặc { }

```bash
char *json = “ 
{ 
  "name": "John Doe",
  "age": 30,
  "city": "New York",
  "isStudent": false,
  "grades": [85, 90, 78]
}
```
__+ array__: bên trong array có thể là bất kỳ dữ liệu nào
+ Định dạng: thường được đặt trong 2 dấu ngoặc [ ]

```bash
  [23,"hello world",[64,35,true"]]
```
+ 1 array cùng có thể chức các thành phần là ObjectObject với các object cũng được ngăn cách bởi dấu phẩy ,
```bash
[
  {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "occupation": "Software Engineer",
    "isStudent": false
  },
  {
    "name": "Jane Smith",
    "age": null,
    "city": "Los Angeles",
    "contact": {
      "email": "jane.smith@example.com",
      "phone": "555-1234"
    }
  },
  {
    "name": "Bob Johnson",
    "age": 35,
    "city": "Chicago"
  }
]
```
### 1.3 Ứng dụng trong lĩnh vực embedded
__TRUYỀN NHẬN DỮ LIỆU CẢM BIẾN TRONG CÁC HỆ THỐNG IOT__
+ __Gửi dữ liệu__ : ta có thể sử dụng chuỗi json để lưu các thông tin về nhiệt độ và độ ẩm và gửi lên server để xử lý
+ __Cấu hình điều khiển__: chuỗi json có thể được gửi từ server về thiết bị chứa các thông tin về cấu hình cài đặt như nhiệt độ,thời gian tương ứng để bật tắt các thiết bị ngoại vi
### So sánh với Struct 
__Quản lý memory__ :
+ struct sẽ cấp phát vùng nhớ cho tất cả các thành viên được định nghĩa 1 khi khai báo. vì vậy sẽ có 1 số trường hợp người dùng không muốn 1 số thành viên của struct, điều này sẽ gây lãng phí memory
+ Json hiệu quả hơn so với struct do chỉ chứa các trường định nghĩa chung về loại dữ liệu mà người dùng muốn cấu hình,chính vì vậy người dùng có thể nhập các dữ liệu cấu hình mong muốn mà không gây dư thừa memory 
__Ứng dụng thực tế__:

+ struct sẽ phù hợp cho các ứng dụng có memory thấp, tốc độ xử lý nhanh chủ yếu là giữa thiết bị và ngoại vi và không yêu cầu về kết nối hay trao đổi dữ liệu qua mạng
+ json sẽ linh hoạt đối với ứng dụng yêu cầu trao đổi dữ liệu qua mạng

## 2. Cách tạo ra 1 kiểu dữ liệu Json
### 2.1 Tạo struct cấu hình cho json
+ Đẻ có thể cấu hình cho 1 chuỗi json chứa nhiều loại dữ liệu bên trong ta cần phải xác định kiểu json bằng cách tạo ra 1 danh sách như sau:

```bash
  typedef enum {
    JSON_NULL,
    JSON_BOOLEAN,
    JSON_NUMBER,
    JSON_STRING,
    JSON_ARRAY,
    JSON_OBJECT
} JsonType;
```
+ Tiếp theo ta cần tạo ra 1 kiểu dữ liệu để cài đặt các cấu hình dữ liệu bên trong json
```bash
typedef struct JsonValue {
    JsonType type;
    union {
        bool boolean;
        double number;
        char *string;
        struct {
            struct JsonValue *values;
            size_t count;
        } array;
        struct {
            char **keys; 
            struct JsonValue *values; 
            size_t count; 
        } object;
    } value;
} JsonValue;
```
__JsonValue__: đây là 1 kiểu dữ liệu để định nghĩa 1 chuỗi json gôm 2 thành viên

__+ JsonTyoe type__ : xác đinh kiểu của giá trị json dựa vào enum đã khai báo trước đó

__+ union value__ : với 3 thành viên __boolean, number, string__ được dùng để gán giá trị cho dữ liệu json mà ta muốn và ở mỗi thời điểm sẽ chỉ có 1 thành viên được dùng và được xác định thông qua JsonType. 
```bash
  char* string; // dùng để trỏ tới chuỗi json
```
    
__array bên trong union__ : được dùng để tạo 1 array trong chuỗi json với __count__ dùng để xác định số phần tử của array, __values__ dùng để trỏ tới các phần tử của array

```bash
   struct JsonValue *values; // con trỏ values sẽ được gọi liên tục để xử lý các thành phần bên trong mãng
```

__object bên trong union__ : được dùng để tạo ra 1 object trong chuỗi json, với __keys__ dùng để lưu trữ các chuỗi con, __values__ trỏ tới từng value tương ứng với key để cài đặt giá trị, __count__ dùng để xác định số cặp __key-value__

```bash
   struct JsonValue *values; // con trỏ values sẽ được gọi liên tục để xử lý các value tương ứng với mỗi key bên trong object 
```
### 2.2 Gán giá trị cho json
Ví dụ: ta sẽ cấu hình các giá trị của định dạng dữ liệu sau

__[43.23 , "duy pham" , true , [35 , "tuoi"]]__ 

+ Đầu tiên ta sẽ cấu hình loại json và các thông tin chung 
```bash
//cấp phát memory cho 1 đối tương kiểu json 
JsonValue* info_list = (JsonValue*)malloc(sizeof(JsonValue*));
int total_json = 5; // số lượng thành phần trong mảng 
int total_arr = 2;  // số lượng thành phần trong 1 thành phần kiểu array
info_list->type = JSON_ARRAY; //xác đinh kiểu json là mảng
info_list->value.array.count = total_json; 
```
+ tiếp theo ta tiến hành cấu hình từng thành phần cu thể
```bash
//cấp phát memory cho các thành phần trong mảng
info_list->value.array.values = (JsonValue*)malloc(info_list->value.array.count * sizeof(JsonValue)); 

//xác định kiểu dữ liệu của thành phần hiện tại
info_list->value.array.values[0].type = JSON_NUMBER; 
//gán giá trị cho thành phần hiện tại
info_list->value.array.values[0].value.number = 45.23;

info_list->value.array.values[1].type = JSON_STRING; 
info_list->value.array.values[1].value.string = "Duysolo";

info_list->value.array.values[2].type = JSON_BOOLEAN; 
info_list->value.array.values[2].value.boolean = true;

info_list->value.array.values[3].type = JSON_ARRAY;
info_list->value.array.values[3].value.array.count = total_arr;

info_list->value.array.values[3].value.array.values[0].type = JSON_NUMBER;
info_list->value.array.values[3].value.array.values[0].value.number = 35;
info_list->value.array.values[3].value.array.values[1].value.string = "Tuoi"; 
```

  

    


