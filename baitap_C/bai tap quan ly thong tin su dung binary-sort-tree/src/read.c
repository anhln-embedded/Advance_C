//#include"read.h"
#include "..//inc//read.h"
uint8_t total_user = 0; //biến đếm số lượng user
static Info *parse_line(char *line)
{
    //cấp phát 1 vùn nhớ tạm để lưu trữ thông tin của user hiện tại
    Info* info = (Info*)malloc(sizeof(Info));
    char *token; // con trỏ lưu trữ giá trị tạm thời

    // Parse name
    token = strtok(line, ","); //tách từng ký tự cho đến khi gặp dấu ","
    info->name = (char *)malloc(strlen(token) + 1);
    strcpy(info->name, token); //sao chép vào vùng nhớ heapheap

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

    return info; //trả về thông tin của user hiện tại
}
Info *readCSV(char *path)
{
    char line[100];
    FILE *file = fopen(path, "r");
    if (file == NULL)
    {
        printf("can't read file\n");
        return NULL;
    }
    //đọc và không xử lý dòng tiêu đề
    fgets(line, sizeof(line), file);
    //cấp phát vùng nhớ động 
    Info *line_info = (Info *)malloc(sizeof(Info));
    while (fgets(line, sizeof(line), file) != NULL)
    {
        // tách ra thông tin và trả kết quả về kết quả tạm thờithời
        Info *temp_info = parse_line(line);
        //cập nhật số lượng user
        total_user += 1;
        //điều chỉnh tăng kích thước vùng nhớ mỗi khi cập nhật thông tin user mới
        line_info = (Info *)realloc(line_info, sizeof(Info) * total_user);
        //copy vào vùng nhớ đã cáp phát
        line_info[total_user - 1] = *temp_info;
        //giải phóng vùng nhớ tạm
        free(temp_info);
    }
    fclose(file);
    printf("doc file thanh cong\n");
    return line_info; //trả về kết quả cuối cùng sau khi đã đọc hết thông tin của tất cả useruser
}
void print_info(Info* info)
{
    int current = 0;
    while (current < total_user)
    {
        printf("%s %d %s %s\n",info[current].name,info[current].age,info[current].phone,info[current].address);
        current++;
    }
}
void free_info(Info* info)
{
    Info* temp = info;
    int current = 0;
    while (current < total_user)
    {
        free(temp->name);
        free(temp->phone);
        free(temp->address);
        temp += (current++);

    }
}

