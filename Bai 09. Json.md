# KIỂU DỮ LIỆU CẤU TRÚC JSON
## 1.1 Định nghĩa
Đây là 1 định dạng để truyền tải dữ liệu giữa các hệ thống với nhau ,và dữ liệu thường được chuẩn hóa về dạng chuỗi (__json string__) chứa nhiều loại dữ liệu khác bên trong. 
## 1.2 Đặc điểm
+ Định dạng gọn nhẹ, dể đọc giúp dễ dàng phân tích
+ Cấu trúc gồm các cặp key-value, với key là chuỗi và value là bất kỳ kiểu dữ liệu nào
+ Được dùng để truyền dữ liệu giữa client và server 
## 1.2 Cấu trúc
Json là 1 chuỗi chứa các dữ liệu được chuẩn hóa như sau :

__+ Object__ : tập hợp của các cặp key - value được ngăn cách bởi dấu phẩy

+ key: là 1 chuỗi
+ value: bất kỳ loại dữ liệu nào

__Ví dụ:__ : 1 định dạng json được viết dưới dạng 1 object là tập hợp các cặp key-value đặt trong dấu ngoặc nhọn {}

```bash
{ 
  "name": "John Doe",
  "age": 30,
  "city": "New York",
  "isStudent": false,
  "grades": [85, 90, 78]
}"
```
__+ array__: bên trong array có thể là bất kỳ dữ liệu nào
+ Định dạng: thường được đặt trong 2 dấu ngoặc [ ]

```bash
  [23,"hello world",[64,35,true"]]
```
+ 1 array cùng có thể chức các thành phần là Object với các object cũng được ngăn cách bởi dấu phẩy ,
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
## 1.3 Ứng dụng trong lĩnh vực embedded
### a) Truyền nhận dữ liệu cảm biến trong lĩnh vực IoT
<p align = "center">
<img src = "https://github.com/user-attachments/assets/603c06ae-5bb6-462a-bb4f-8735051bf7c6" width = "700" height = "300">

+ __Gửi dữ liệu__ : ta có thể sử dụng chuỗi json để lưu các thông tin về nhiệt độ và độ ẩm và gửi lên server để xử lý
+ __Cấu hình điều khiển__: chuỗi json có thể được gửi từ server về thiết bị chứa các thông tin về cấu hình cài đặt như nhiệt độ,thời gian tương ứng để bật tắt các thiết bị ngoại vi
### b) So sánh với Struct 
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
            struct JsonValue *json_array;
            size_t count;
        } array;
        struct {
            char **keys; 
            struct JsonValue *json_object; 
            size_t count; 
        } object;
    } value;
} JsonValue;
```
__JsonValue__: đây là 1 kiểu dữ liệu để định nghĩa 1 chuỗi json gôm 2 thành viên

__+ JsonType type__ : xác đinh kiểu của giá trị json dựa vào enum đã khai báo trước đó

__+ union value__ : với 3 thành viên __boolean, number, string__ được dùng để gán giá trị cho dữ liệu json mà ta muốn và ở mỗi thời điểm sẽ chỉ có 1 thành viên được dùng và được xác định thông qua JsonType. 
```bash
  char* string; // dùng để trỏ tới chuỗi json
```
    
__array bên trong union__ : được dùng để tạo 1 array trong chuỗi json với __count__ dùng để xác định số phần tử của array, __values__ dùng để trỏ tới các phần tử của array

```bash
// mảng values sẽ được đệ quy liên tục để trỏ tới chính struct JsonValue gán giá trị cho biến thành viên cũng là thành phần của mảng
   struct JsonValue *json_array; 
```

__object bên trong union__ : được dùng để tạo ra 1 object trong chuỗi json, với __keys__ dùng để lưu trữ các chuỗi con, __values__ trỏ tới từng value tương ứng với key để cài đặt giá trị, __count__ dùng để xác định số cặp __key-value__

```bash
   struct JsonValue *json_object; // cách xử lý tương tự array 
```
### 2.2 Gán giá trị thủ công cho json
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
### 2.3 Các hàm phân tách chuỗi json
#### 2.3.1 Ứng dụng của con trỏ 2 cấp trong xữ lý chuỗi json
Để xử lý 1 chuỗi json, thông thường ta phải tách ra các chuỗi con bên trong và lưu vào 1 vùng nhớ. Chính vì vậy trước hết ta sẽ phải sử dụng con trỏ để dịch qua từng địa chỉ của ký tự trong chuỗi để đọc ra từng ký tự bên trong.

+ __Trường hợp sử dụng con trỏ cấp 1__

Ta sẽ viết 1 hàm để thay đổi địa chỉ con trỏ như sau
```bash

void single_ptr(const char *ptr)
{
    ptr += 4;
    printf("inside: %s\n", ptr);
}
int main()
{
    const char *str = "hello world";
    printf("outside: %s\n", str);
    single_ptr(str);
    printf("outside: %s\n", str);
    return 0;
}
```
+ Kết quả 

```bash
    
outside: hello world
inside: o world
outside: hello world
```
+ Ta có thẻ thấy trong đoạn code trên, thực chất ta chỉ đang truyền giá trị của str hay nói cách khác là địa chỉ của chuỗi "hello world" vào bên trong 1 hàm 
+ Và ở bên trong hàm này sẽ tạo ra 1 bản sao của giá trị str truyền vào, có nghĩa là nó sẽ tạo ra 1 địa chỉ mới sử dụng con trỏ __ptr__ cùng trỏ đến chuỗi "hello world" giống như __string__
+ Hình minh họa sau đây sẽ mô tả cách mà __str__ và __ptr__ nó hoản toàn được lưu ở 2 địa chỉ khác nhau. Dẫn đến việc ta thay đổi địa chỉ của __ptr__ sẽ không ảnh hưởng đến __str__

<p align = "center">
<img src = "https://github.com/user-attachments/assets/459101c3-ae3b-4eff-908b-8bc4eb5fdfcd" width = "600" height = "300">


+ __Trường hợp sử dụng con trỏ cấp 2__
Ta cũng sẽ thay đổi địa chỉ con trỏ đến chuỗi "hello world", nhưng bằng double pointer

```bash
void double_ptr(const char **ptr)
{
    // ptr -> address of ptr
    //*ptr -> dereference to string "hello world" pointed by ptr
    //**ptr -> derefernce to the first character in string "hello world"
    (*ptr) += 4;
    printf("inside: %c -> %s -> %p\n", **ptr, *ptr, ptr);
}

int main()
{
    const char *str = "hello world";
    printf("outside: %s -> %p\n",str,&str);
    double_ptr(&str);
    printf("outside: %s\n", str);
    return 0;
}
```
```bash
outside: hello world -> 00000031373FF718
inside: o -> o world -> 00000031373FF718
outside: o world
```

+ Ta có thể thấy trước và sau khi thay đổi địa chỉ con trỏ trong hàm double_ptr thì ở bên ngoài địa chỉ của str cũng thay đổi theo.
+ Điều này là do ta đã truyền địa chỉ của str vào trong hàm, và sử dụng 1 con trỏ cấp 2 để trỏ đến địa chỉ của 1 con trỏ cấp 1. 
+ Tiếp theo ta sẽ thực hiện thay đỗi địa chỉ mà con trỏ __str__ trỏ đến bằng cách truy xuất __ptr__ bằng __*ptr__, bằng cách này ta sẽ có thể thay đổi được địa chỉ của __str__

<p align = "center">
<img src = "https://github.com/user-attachments/assets/f85f9025-0bb7-4472-bc18-4a3bf9c4cd75" width = "600" height = "300">

#### 2.3.2 Các hàm để xử lý chuỗi Json
__a) Hàm phân loại kiểu dữ liệu để xử lý__ 
+ Hàm để phân tích các chuỗi con bên trong json tương ứng với các kiểu dữ liệu được thể hiện dưới dạng chuỗi
+ Ta sẽ sử dụng cơ chế switch-case để kiểm tra và nhảy vào các hàm tách chuỗi tương ứng và trả về kết quả là giá trị tương ứng với chính xác kiểu dữ liệu của nó
```bash
JsonValue *parse_json(const char **json) { 
    skip_whitespace(json); // bỏ qua các khoảng trắng bên trong chuỗi
    switch (**json) {
        case 'n':
            return parse_null(json); string is existed
        case 't':
        case 'f':
            return parse_boolean(json);
        case '\"':
            return parse_string(json);
        case '[':
            return parse_array(json);
        case '{':
            return parse_object(json);
        default:
            if (isdigit(**json) || **json == '-') {
                return parse_number(json);
            } else {
                // Lỗi phân tích cú pháp
                return NULL;
            }
    }
}
```
__b) Các Hàm con phụ thuộc để xử lý từng loại dữ liệu__ 

+ Sau khi hàm __parse_json__ được gọi thì nếu chuỗi hiện tại là kiểu string với ký tự xác định là ' \\" ', thì nó sẽ nhảy vào hàm sau đây để xử lý 

```bash
JsonValue *parse_string(const char **json) {
	(*json)++;									 //dịch tới địa chỉ tiếp theo để bắt đầu xử lý từ ký tự đầu tiên 
	const char *start = *json;					 //lưu địa chỉ bắt đầu của chuỗi 
	const char *end = start                      //biến để kiểm tra độ dài chuỗi
  while (**json != '\"' && **json != '\0') {
		(*json)++; 							     //kiểm tra độ dài chuỗi
	}
	if (**json == '\"') {
		size_t length = *json - start;           //cập nhật kích thước chuỗichuỗi 

    //cấp phát vùng nhớ và lưu tạm thời chuỗi vừa tách được 
		char *str = (char *) malloc((length + 1) * sizeof(char)); 
		strncpy(str, start, length);
		str[length] = '\0';

    //cấp phát vùng nhớ để lưu chuỗi trả về thực sự
		JsonValue *value = (JsonValue *) malloc(sizeof(JsonValue));
		value->type = JSON_STRING; //xác định kiểu dữ liệu 
		value->value.string = str; //gán vào biến tương ứng
		*json = ++end;             //cập nhật lại địa chỉ chuỗi json để xử lý chuỗi kế tiếp
		return value;
	}
    return NULL;
}
```
+ Nếu chuỗi hiện tại có kiểu là các con số thì hàm sau sẽ được gọi với  hàm __strtod(const char* string , char** endptr)__ được dùng để chuyển đổi từ 1 chuỗi char* sang số double
 ```bash
JsonValue *parse_number(const char **json) {
    char *end;                        //biến dùng để trỏ tới địa chỉ của ký tự trong chuỗi
    double num = strtod(*json, &end); //hàm để chuyển đổi chuỗi sang kiểu số double 
  
  //nếu địa chỉ lưu trong con trỏ end khác *json thì tiến hành cấp phát vùng nhớ và gán giá trị trả về
    if (end != *json) {
        JsonValue *value = (JsonValue *) malloc(sizeof(JsonValue));
        value->type = JSON_NUMBER;
        value->value.number = num;
        *json = end; //cập nhật địa chỉ của chuỗi json -> nhảy đến cuối chuỗi để chuẩn bị xử lý chuỗi tiếp theo
        return value;
    }
    return NULL;
}
```


+ Nếu chuỗi hiện tại có ký tự xác định là '[', thì hàm sau sẽ được gọi

 ```bash
JsonValue *parse_array(const char **json) {
    (*json)++;                      //dịch sang ký tự tiếp theo để bắt đầu xử lý
    skipwhitespace(json);           //nếu phát hiện khoảng trắng đầu chuỗi thì bỏ qua

//cấp phát vùng nhớ ban đầu cho mảng và khởi tạo các giá trị ban đầu
    JsonValue *array_value = (JsonValue *)malloc(sizeof(JsonValue));
    array_value->type = JSON_ARRAY;
    array_value->value.array.count = 0;
    array_value->value.array.values = NULL;

//kiểm tra chuỗi hiện tại có hợp lệ không thì tiếp tục xử lý
    while (**json != ']' && **json != '\0') {
//tạo 1 con trỏ để luu giá trị trả về -> lý do phải gọi ra hàm parse_json là ta muốn tiếp tục kiểm tra thành phần của mảng là thuộc kiểu gì và trả về kiểu tương ứng
        JsonValue *element = parse_json(json);  

//nếu giá trị trả về hợp lệ ta tiến hành mở rộng kích thước vùng nhớ đã cấp phát trước đó và gán giá trị tương ứng
        if (element) {
            array_value->value.array.count++;
          
            array_value->value.array.values = 
            (JsonValue *)realloc(array_value->value.array.values, array_value->value.array.count * sizeof(JsonValue));
       
            array_value->value.array.values[array_value->value.array.count - 1] = *element;
            
            free(element); //giải phóng vùng nhớ tạm trước đó dùng đẻ lưu giá trị trả về

        }
// 
        else { 
            break; //nếu không còn thành phần trong mảng nữa thì thoát khỏi while
        }
        skip_whitespace(json); //nếu có khoảng tráng sau mỗi thành phần trong chuỗi thì bỏ qua

        //nếu phát hiện ký tự phân tách thành phần thì tăng địa chỉ sang ký tự tiếp theo
        if (**json == ',') {
            (*json)++;
        }
    }

    //nếu phát hiện ký tự kết thúc mảng thì dịch sang địa chỉ của chuỗi con json kế tiếp và trả về toàn bộ giá trị trong mảng
    if (**json == ']') {
        (*json)++; 
        return array_value;
    } 
    //nếu ký tự kết thúc mảng không hợp lệ thì sẽ giải phóng vùng nhớ và trả về NULL
    else {
        free_json_value(array_value);
        return NULL;
    }
    return NULL;
}
```

__c) Hàm in và giải phóng memory__ 
+ Ta có hàm in ra các phần tử bên trong chuỗi json như sau
+ Đối với kiểu dữ liệu json là array thì ta sẽ thực hiện gọi lại chính hàm test để kiểm tra kiểu dữ liệu của các phần tử bên trong và thực hiện nhảy vào các câu lệnh if tương ứng và in ra
+ Nếu kiểu json khác array, thì ta tiến hành in trực tiếp ra giá trị tương ứng với kiểu dữ liệu của chúng
```bash
void test(JsonValue* json_value){
    if(json_value->type == JSON_STRING){
        printf("%s ", json_value->value.string);
    }

    else if(json_value->type == JSON_NUMBER){
        printf("%f ", json_value->value.number);
    }

    else if(json_value->type == JSON_BOOLEAN){
        printf("%s ", json_value->value.boolean ? "True":"False");
    }
    else if(json_value->type == JSON_ARRAY){
        for (int i = 0; i < json_value->value.array.count; i++)
        {
            test(json_value->value.array.values + i);
        } 
        printf("\n");
    }
    else if (json_value->type ==JSON_NULL) printf("null");
}
```

+ Ta sẽ có hàm sau để giải phóng memory của biến kiểu json sau khi đã lưu các trường dữ liệu được xử lý phân tách chuỗi vào các biến thuộc các kiẻu dữ liệu tương ứng 
+ đầu tiên thì ta sẽ kiểm tra kiểu dữ liệu của chuỗi json là gì, thông qua switch-case
+ đối với chuỗi json kiểu __array__ và __object__: ta gọi lại chính hàm đó để kiểm tra kiểu dữ liệu của phần tử bên trong là gì, và tiến hành giải phóng vùng nhớ 
+ Đối với chuỗi json kiểu __string__: ta thực hiện giải phóng vùng nhớ trực tiếp

```bash
void free_json_value(JsonValue *json_value) {

    if (json_value == NULL) {
        return 0`; //Nếu con trỏ json_value trỏ tới vùng nhớ không chứa dữ liệu 
    }

    // nếu con trỏ json_value chứa dữ liệu thì sẽ so sánh đó là loại dữ liệu gì để tiến hành giải phóng memory tương ứng với kiẻu dữ liệu đó
    switch (json_value->type) {
        case JSON_STRING:
            free(json_value->value.string);
            break;
        case JSON_ARRAY:
            for (size_t i = 0; i < json_value->value.array.count; i++) {
                free_json_value(&json_value->value.array.values[i]);
            }
            free(json_value->value.array.values);
            break;
        case JSON_OBJECT:
            for (size_t i = 0; i < json_value->value.object.count; i++) {
                free(json_value->value.object.keys[i]);
                free_json_value(&json_value->value.object.values[i]);
            }
            free(json_value->value.object.keys);
            free(json_value->value.object.values);
            break;
        default:
            break;
    }
}
```
    

    
