#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include "testcase.c"

//list of general datatype being selected 
typedef enum {
    JSON_NULL,
    JSON_BOOLEAN,
    JSON_NUMBER,
    JSON_STRING,
    JSON_ARRAY,
    JSON_OBJECT
} JsonType;
//struct provides configured parameters after select jsontype 
typedef struct JsonValue {
    JsonType type;
    union {
        bool boolean;
        double number;
        char *string; //store Json string
    //declare a struct to store json array
        struct {
        // pointer -> points to JsonValue array
            struct JsonValue *values;
            size_t count;
        } array;
        struct {
            char **keys; //store key string within Json
            struct JsonValue *values; //store values corresspoding to key
            size_t count; // numbers of pairs key-value within json
        } object;
    } value;
}JsonValue;

JsonValue *parse_json(const char **json);
JsonValue *parse_null(const char **json);
JsonValue *parse_boolean(const char **json);
JsonValue *parse_number(const char **json);
JsonValue *parse_string(const char **json);
JsonValue *parse_array(const char **json);
JsonValue *parse_object(const char **json);
static void skip_whitespace(const char **json);
void test(JsonValue* json_value);
void free_json_value(JsonValue *json_value);

int main(int argc, char const *argv[])
{
    JsonValue* json_value = parse_json(&json_array);
    test(json_value);
    free_json_value(json_value);
    return 0;
   

}

static void skip_whitespace(const char **json) {
    while (isspace(**json)) {
        (*json)++;
    }
}

JsonValue *parse_null(const char **json) {
    if (strncmp(*json, "null", 4) == 0) {
        JsonValue *value = (JsonValue *) malloc(sizeof(JsonValue));
        value->type = JSON_NULL;
        *json += 4;
        return value;
    }
    return NULL;
}
JsonValue *parse_boolean(const char **json) {
    JsonValue *value = (JsonValue *) malloc(sizeof(JsonValue));
    if (strncmp(*json, "true", 4) == 0) {
        value->type = JSON_BOOLEAN;
        value->value.boolean = true;
        *json += 4;
    } else if (strncmp(*json, "false", 5) == 0) {
        value->type = JSON_BOOLEAN;
        value->value.boolean = false;
        *json += 5;
    } else {
        free(value);
        return NULL;
    }
    return value;
}
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
JsonValue *parse_string(const char **json) {
	(*json)++;									 //dịch tới địa chỉ tiếp theo để bắt đầu xử lý từ ký tự đầu tiên 
	const char *start = *json;					 //lưu địa chỉ bắt đầu của chuỗi 
	const char *end = start;                      //biến để kiểm tra độ dài chuỗi
    while(*end!= '\"' && *end!= '\0') {
		end++; 							     //kiểm tra độ dài chuỗi
	}
	if (*end == '\"') {
		size_t length = end - start;           //cập nhật kích thước chuỗi

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

JsonValue *parse_array(const char **json) {
   (*json)++;                      //dịch sang ký tự tiếp theo để bắt đầu xử lý
   skip_whitespace(json);           //nếu phát hiện khoảng trắng đầu chuỗi thì bỏ qua

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

JsonValue *parse_object(const char **json) {
    (*json)++;
    skip_whitespace(json);

    JsonValue *object_value = (JsonValue *)malloc(sizeof(JsonValue));
    object_value->type = JSON_OBJECT;
    object_value->value.object.count = 0;
    object_value->value.object.keys = NULL;
    object_value->value.object.values = NULL;

    while (**json != '}' && **json != '\0') {
        JsonValue *key = parse_string(json); //temp var -> will be free after assign to final result
        if (key) {
            skip_whitespace(json);
            if (**json == ':') {
                (*json)++;
                JsonValue *value = parse_json(json); //temp var -> will be free after assign to final result
                if (value) {
                    object_value->value.object.count++;
                    object_value->value.object.keys = (char **)realloc(object_value->value.object.keys, object_value->value.object.count * sizeof(char *));
                    object_value->value.object.keys[object_value->value.object.count - 1] = key->value.string;

                    object_value->value.object.values = (JsonValue *)realloc(object_value->value.object.values, object_value->value.object.count * sizeof(JsonValue));
                    object_value->value.object.values[object_value->value.object.count - 1] = *value;
                    free(value);
                } else {
                    free_json_value(key);
                    break;
                }
            } else {
                free_json_value(key);
                break;
            }
        } else {
            break;
        }
        skip_whitespace(json);
        if (**json == ',') {
            (*json)++;
        }
    }
    if (**json == '}') {
        (*json)++;
        return object_value;
    } else {
        free_json_value(object_value);
        return NULL;
    }
    return NULL;
}
JsonValue *parse_json(const char **json) { 
    skip_whitespace(json);
//process and parse data corresspoinding to json type
    switch (**json) {
        case 'n':
            return parse_null(json); //return nullif there is no json string is existed
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

void free_json_value(JsonValue *json_value) {
    if (json_value == NULL) {
        return;
    }
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
void test(JsonValue* json_value){
    if (json_value != NULL && json_value->type == JSON_OBJECT) {
        // Truy cập giá trị của các trường trong đối tượng JSON
        size_t num_fields = json_value->value.object.count;
        size_t num_fields2 = json_value->value.object.values->value.object.count;
        for (size_t i = 0; i < num_fields; ++i) {

            char* key = json_value->value.object.keys[i];
            JsonValue* value = &json_value->value.object.values[i];

            JsonType type = (int)(json_value->value.object.values[i].type);


            if(type == JSON_STRING){
                printf("%s: %s\n", key, value->value.string);
            }

            else if(type == JSON_NUMBER){
                printf("%s: %f\n", key, value->value.number);
            }

            else if(type == JSON_BOOLEAN){
                printf("%s: %s\n", key, value->value.boolean ? "True":"False");
            }

            else if(type == JSON_OBJECT){
                printf("%s: \n", key);
                test(value);
            }

            else if(type == JSON_ARRAY){
                printf("%s: ", key);
                for (int i = 0; i < value->value.array.count; i++)
                {
                   test(value->value.array.values + i);
                } 
                printf("\n");
            }
        }
     
    }
    else 
    {
            if(json_value->type == JSON_STRING){
                printf("%s ", json_value->value.string);
            }

            else if(json_value->type == JSON_NUMBER){
                printf("%f ", json_value->value.number);
            }

            else if(json_value->type == JSON_BOOLEAN){
                printf("%s ", json_value->value.boolean ? "True":"False");
            }

            else if(json_value->type == JSON_OBJECT){
                printf("%s: \n", json_value->value.object.keys);
                test(json_value->value.object.values);
                           
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

}


