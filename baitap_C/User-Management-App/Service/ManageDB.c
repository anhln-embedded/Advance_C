#include "ManageDB.h"

//Biến cục bộ sử dụng trong file hiện tại
static UserData* Storage_UserDB;

//Biến cục bộ đếm số lượng UserData đọc từ database
static int count = 0;
/**
 * @brief     Phân tích chuỗi dữ liệu và lưu trữ vào từng trường thông tin của cấu trúc UserData.
 *
 * @details   Hàm này nhận vào một chuỗi chứa thông tin người dùng (ví dụ từ một dòng của file CSV),
 *            sau đó tách các trường dữ liệu (tên, địa chỉ, số điện thoại, tuổi, ...) và cấp phát bộ nhớ
 *            để lưu vào một đối tượng UserData mới.
 *
 * @param[in] line   Chuỗi ký tự chứa thông tin người dùng
 *                   (các trường được phân tách bằng dấu phẩy hoặc ký tự quy ước).
 *
 * @return    Con trỏ đến cấu trúc UserData mới được cấp phát và khởi tạo dữ liệu nếu thành công.
 * @retval    NULL   Nếu chuỗi đầu vào không hợp lệ hoặc cấp phát bộ nhớ thất bại.
 */
static UserData *parse_line(char *line);
                            ///////////////*ĐỊNH NGHĨA CÁC HÀM TOÀN CỤC*////////////////
Status WriteFile(const char* path){
    FILE* file = fopen(path,"w");
    if(file == NULL){
        return NOT_OK;
    }
    fprintf(file,"ten,tuoi,so dien thoai,dia chi\n");
    fprintf(file,"Pham Cao Duy,25,0972665872,91 Pham Van Hai P3 Q Tan Binh\n");
    fprintf(file,"Trinh Tran Phuong Tuan,24,0908234588,TP Tay Ninh \n");
    fprintf(file,"Trinh Le Hoang,28,0376572677,12 Nguyen Xien Q12\n");
    fprintf(file,"Nguyen Tan Tung,21,038764589,45 Tran Binh Trong\n");
    fprintf(file,"Le Quang Nhat,26,0978278121,17 Binh Phuoc\n");
    fprintf(file,"Nguyen Huu Hung,22,0978565342,17 Q Binh Thanh\n");
    fprintf(file,"Pham Cao Duy,18,090395678,220/8 Nguyen Phuc Nguuyen P9 Q3\n");
    fprintf(file,"Dinh Anh Tuan,24,0903478211,TP Tay Ninh\n");
    fprintf(file,"Nguyen Ho Duy,17,0906733209,22/5 Binh Thuan\n");
    fprintf(file,"Pham Cao Duy,20,0376572231,18 Nguyen Thi Minh Khai Q1 TPHCM\n");
    fprintf(file,"Nguyen Thi Thanh Thuy,27,038764987,21 Nguyen Thien Thuat P12 QTan Phu\n");
    fprintf(file,"Nguyen Ho Duy,27,038764912,22 Nguyen Thien Thuat P13 Q Tan Binh\n");
    fprintf(file,"Nguyen Thi Thanh Thu,27,038764997,23 Nguyen Thien Thuat P14  Q Binh Thanh\n");
    fprintf(file,"Pham Cao Duy,27,038764912,24 Nguyen Thien Thuat P9 Q 10\n");
    fclose(file);
    return E_OK;
}
Status Load_UserDB(const char *path)
{
    char line[100];
    FILE *file = fopen(path, "r");
    if (file == NULL)
    {
        return NOT_OK;
    }
    // đọc và không xử lý dòng tiêu đề
    fgets(line, sizeof(line), file);
    // cấp phát vùng nhớ động
    Storage_UserDB = (UserData *)malloc(sizeof(UserData));

    if(Storage_UserDB == NULL){
        return NOT_OK;
    }

    //đọc từng dòng của filem
    while (fgets(line, sizeof(line), file) != NULL)
    {
        //tách ra thông tin và trả kết quả về kết quả tạm thời
        UserData *temp = parse_line(line);
        //Tăng số lượng UserData
        count++;
        //điều chỉnh tăng kích thước vùng nhớ mỗi khi cập nhật thông tin user mới
        Storage_UserDB = (UserData *)realloc(Storage_UserDB, sizeof(UserData) * count);
        // copy vào vùng nhớ đã cáp phát
        Storage_UserDB[count - 1] = *temp;
        // Xóa vùng nhớ tạm mà không giải phóng vùng nhớ cấp phát cho các thành viên bên trong
        free(temp);
    }
    fclose(file);
    return E_OK;
}
Status Remove_UserDB()
{
    if(Storage_UserDB == NULL){
        return NOT_OK;
    }
    for (int i = 0; i < count; i++)
    {
        free(Storage_UserDB[i].name);
        free(Storage_UserDB[i].phone);
        free(Storage_UserDB[i].address);
        Storage_UserDB[i].name = NULL;
        Storage_UserDB[i].phone = NULL;
        Storage_UserDB[i].address = NULL;
    }
    free(Storage_UserDB);
    Storage_UserDB = NULL;
    return E_OK;
}
void Print_UserDB()
{
    for(int i = 0 ; i  < count ; i++)
    {
        printf("%s\t%d\t%s\t%s\n", 
            Storage_UserDB[i].name, 
            Storage_UserDB[i].age, 
            Storage_UserDB[i].phone, 
            Storage_UserDB[i].address);
    }
}
UserData* Read_UserDB(){
    return Storage_UserDB;
}
int Read_SizeUserDB(){
    return count;
}
                                ///////////////*ĐỊNH NGHĨA HÀM CỤC BỘ*////////////////
static UserData *parse_line(char *line)
{
    // cấp phát 1 vùn nhớ tạm để lưu trữ thông tin của user hiện tại
    UserData *temp = (UserData*)malloc(sizeof(UserData));
    char *token; // con trỏ lưu trữ giá trị tạm thời

    // Parse name
    token = strtok(line, ","); // tách từng ký tự cho đến khi gặp dấu ","
    temp->name = (char *)malloc(strlen(token) + 1);
    strcpy(temp->name, token); // sao chép vào vùng nhớ heap

    // Parse age
    token = strtok(NULL, ",");
    temp->age = (uint8_t)atoi(token);

    // Parse phone
    token = strtok(NULL, ",");
    temp->phone = (char *)malloc(strlen(token) + 1);
    strcpy(temp->phone, token);

    // Parse address
    token = strtok(NULL, ",");
    temp->address = (char *)malloc(strlen(token) + 1);
    strcpy(temp->address, token);

    return temp; // trả về thông tin của user hiện tại
}