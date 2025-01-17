#include"..//inc//list.h"    
#include"..//inc//write.h"
#include"..//inc//read.h"
#include"..//inc//search.h"
#define PATH_FILE ".//database//data.csv"
const char *str[] = {"File has been written\n", "Failed to open file\n"};

int main()
{
    //chỉ chạy đoạn if else sau đây 1 lần duy nhất để ghi file
    /* if (writeCSV(PATH_FILE) == SUCCESS_CREATED_FILE)
        log_status(str[0]);
    else
        log_status(str[1]); */
    
    //dọc file csv và trả về con trỏ heap tới vùng nhớ lưu trữ thông tin
    Info *info = readCSV(PATH_FILE);
    //print_info(info);

    //tạo ra 2 con trỏ tới danh sách liên kết lưu trữ theo tên và sdt
    User_node *list_userName = NULL, *list_userPhone = NULL;

    //tạo danh sách liên kết theo tên và sdtsdt
    
    Create_UserList(info, &list_userName, &list_userPhone);
 

    //xây dưng cấu trúc cây nhị phân để tìm kiếm kiếm thông tin theo tên và sdt

    CenterPoint *BST_Phone = centerPoint(list_userPhone);
    CenterPoint *BST_Name = centerPoint(list_userName);

    //mảng lưu trữ cây nhị phân
    CenterPoint *BST_Arr[] = {BST_Name, BST_Phone};


    //nếu tìm kiếm theo thông tin nào thì thông tin còn lại được đặt là NULL để chương trình phân biệt để xử lý 
    char *phone = "0376572677"; 
    char *name = NULL;

   
    CenterPoint *result = Search_Info(BST_Arr,phone); //nhập vào name hoặc phone để tìm kiếm
    if (result != NULL)
    {
        if (name != NULL)
        {
            printf("Tim thay user voi ten %s\n", name);
            print_Search_byName(result,list_userName);
        }
        if (phone != NULL)
        {
            printf("Tim thay user voi sdt %s\n", phone);
            print_Search_byPhone(result);
        }
    }
    else
    {
        if (name != NULL)
            printf("Khong tim thay user voi ten %s\n", name);
        if (phone != NULL)
            printf("Khong tim thay user voi sdt %s\n", phone);
    }

    //giải phóng vùng nhớ các danh sách liên kết và cây nhị phân
    free_list_user(list_userName);
    free_list_user(list_userPhone);
    free_info(info);
    freeBST(BST_Name);
    freeBST(BST_Phone);


    //gán giá trị NULL để tránh lỗi truy cập vùng nhớ không xác định
    for(int i = 0 ; i < 2 ; i++){
        BST_Arr[i] = NULL;
    }
    BST_Name = NULL;
    BST_Phone = NULL;
    info = NULL;
    list_userName = NULL;
    list_userPhone = NULL;
    result = NULL;
    return 0;
}
