#include "read.h"
uint8_t total_user = 0; // biến toàn cục đếm số lượng user

static Info *parse_line(char *line)
{
    // cấp phát 1 vùn nhớ tạm để lưu trữ thông tin của user hiện tại
    Info *info = (Info *)malloc(sizeof(Info));
    char *token; // con trỏ lưu trữ giá trị tạm thời

    // Parse name
    token = strtok(line, ","); // tách từng ký tự cho đến khi gặp dấu ","
    info->name = (char *)malloc(strlen(token) + 1);
    strcpy(info->name, token); // sao chép vào vùng nhớ heap

    // Parse age
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

    return info; // trả về thông tin của user hiện tại
}
Info *readfile(char *path)
{
    char line[100];
    FILE *file = fopen(path, "r");
    if (file == NULL)
    {
        printf("đọc file thất bại\n");
        return NULL;
    }
    // đọc và không xử lý dòng tiêu đề
    fgets(line, sizeof(line), file);
    // cấp phát vùng nhớ động
    Info *line_info = (Info *)malloc(sizeof(Info));
    while (fgets(line, sizeof(line), file) != NULL)
    {
        // tách ra thông tin và trả kết quả về kết quả tạm thời
        Info *temp_info = parse_line(line);
        // cập nhật số lượng user
        total_user += 1;
        // điều chỉnh tăng kích thước vùng nhớ mỗi khi cập nhật thông tin user mới
        line_info = (Info *)realloc(line_info, sizeof(Info) * total_user);
        // copy vào vùng nhớ đã cáp phát
        line_info[total_user - 1] = *temp_info;
        // Xóa vùng nhớ tạm mà không giải phóng vùng nhớ cấp phát cho các thành viên bên trong
        free(temp_info);
    }
    printf("Thông tin từ file csv đã được lưu thành công vào bộ nhớ\n");
    fclose(file);
    return line_info; // trả về kết quả cuối cùng sau khi đã đọc hết thông tin của tất cả useruser
}
void print_UserInfo(Info *info)
{
    int current = 0;
    printf("danh sách thông tin user đọc từ file csv\n");
    while (current < total_user)
    {
        printf("%s\t%d\t%s\t%s\n", info[current].name, info[current].age, info[current].phone, info[current].address);
        current++;
    }
}
void free_UserInfo(Info *info)
{
    for (int i = 0; i < total_user; i++)
    {
        free(info[i].name);
        free(info[i].phone);
        free(info[i].address);
        info[i].name = NULL;
        info[i].phone = NULL;
        info[i].address = NULL;
    }
    free(info);
}
