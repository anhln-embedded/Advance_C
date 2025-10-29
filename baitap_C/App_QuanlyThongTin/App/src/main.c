#include <stdio.h>
#include <search.h>
#include "list.h"
#include "write.h"
#include "read.h"

typedef enum
{
    SEARCH_NAME = 1,
    SEARCH_AGE,
    SORT_BY_NAME,
    SORT_BY_AGE,
    STOP_PROGRAM
} ScreenChoice;
#define PATH_FILE ".//database//data.csv"

int main()
{
    if (writefile(PATH_FILE))
    {

        // dọc file csv và trả về con trỏ heap tới vùng nhớ lưu trữ thông tin
        Info *info = readfile(PATH_FILE);

        // tạo ra 2 con trỏ tới danh sách liên kết lưu trữ theo tên và sdt
        User_node *list_userName = NULL, *list_userPhone = NULL;

        // tạo danh sách liên kết theo tên và sdt
        Create_UserList(info, &list_userName, &list_userPhone);

        // xây dưng cấu trúc cây nhị phân để tìm kiếm kiếm thông tin theo tên và sdt
        CenterPoint *BST_Phone = centerPoint(list_userPhone);
        CenterPoint *BST_Name = centerPoint(list_userName);

        // mảng lưu trữ cây nhị phân
        CenterPoint *BST_Arr[] = {BST_Name, BST_Phone};

        while (1)
        {
            int prompt = 0;  // nhập lựa chọn trên menu
            char search[30]; // nhập tên hoặc tuổi
            printf("\n/*****************/\n1.tìm theo tên\n"
                   "2.Tìm theo sdt\n"
                   "3.danh sách user sắp xếp theo tên\n"
                   "4.danh sách user sắp xếp theo sdt\n"
                   "5.Dừng chương trình\n/*****************/\nnhập lựa chọn:");
            fgets(search, sizeof(search), stdin);
            search[strcspn(search, "\n")] = '\0'; // xóa ký tự xuống dòng nếu có
            prompt = atoi(search);
            CenterPoint *result = NULL; // nhập vào name hoặc phone để tìm kiếm

            switch (prompt)
            {
            case SEARCH_NAME:
                printf("vui lòng nhập tên cần tìm:");
                fgets(search, sizeof(search), stdin);
                search[strcspn(search, "\n")] = '\0';  // xóa ký tự xuống dòng nếu có
                result = Search_Info(BST_Arr, search); // nhập vào name hoặc phone để tìm kiếm
                if (result)
                {
                    printf("Tìm thấy thông tin user: %s\n\n", search);
                    print_Search_byName(result, list_userName);
                }
                else
                    printf("không Tìm thấy thông tin user: %s\n\n", search);
                break;
            case SEARCH_AGE:
                printf("vui lòng nhập sdt cần tìm:");
                fgets(search, sizeof(search), stdin);
                search[strcspn(search, "\n")] = '\0';  // xóa ký tự xuống dòng nếu có
                result = Search_Info(BST_Arr, search); // nhập vào name hoặc phone để tìm kiếm
                if (result)
                {
                    printf("Tìm thấy thông tin user với sdt %s\n\n", search);
                    print_Search_byPhone(result);
                }
                else
                    printf("Không Tìm thấy thông tin user voi sdt %s\n", search);
                break;
            case SORT_BY_NAME:
                print_UserList(list_userName);
                break;
            case SORT_BY_AGE:
                print_UserList(list_userPhone);
                break;
            case STOP_PROGRAM:
                goto endProgram;
            default:
                printf("vui lòng nhập lựa chọn hợp lệ từ (1 - 4)\n");
                break;
            }
        }
    endProgram:
        // giải phóng vùng nhớ theo thứ tự info -> user_node -> centerpoint
        freeBST(&BST_Name);
        freeBST(&BST_Phone);
        // giải phóng danh sách user của node hiện tại
        free_UserInfo(info);
        info = NULL;
        free_UserList(&list_userName);
        free_UserList(&list_userPhone);
    }
    printf("chương trình đã kết thúc");
    return 0;
}
