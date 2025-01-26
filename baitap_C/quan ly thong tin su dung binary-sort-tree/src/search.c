//#include "search.h"
#include "..//inc//search.h"
CenterPoint *buildTree(User_node *head, int start, int end)
{
    // kiểm tra vị trí các node trái và phải có hợp lệ hay không -> cho biết điểm dừng xây dụng cây nhị phânphân
    if (head == NULL || start > end)
    {
        return NULL;
    }
    // xác định node giữa của danh sáchsách
    int mid = (start + end) / 2;
    User_node *node = head;
    // lặp cho đến khi gặp node giữagiữa
    for (int i = start; i < mid; i++)
    {
        if (node->next_user == NULL)
        {
            break;
        }
        // move to next node
        node = node->next_user;
    }

    // cấp phát vùng nhớ heap để lưu trữ nhánh gốc cho cây nhị phân
    CenterPoint *root = (CenterPoint *)malloc(sizeof(CenterPoint));
    root->user = node->next_user;
    //tạo ra các nhánh 2 trái phải từ nhánh gốc
    root->left = buildTree(head, start, mid - 1);
    root->right = buildTree(node->next_user, mid + 1, end);

    return root;
}
CenterPoint *centerPoint(User_node *head)
{
    int length = 0; 
    User_node *node = head;
    while (node != NULL)
    {
        node = node->next_user;
        length++; // xác định số lượng các node trong danh sáchsách
    }
    return buildTree(head, 0, length - 1); //trả về cây nhị phân 
}
int stringCompare(const char *str1, const char *str2)
{
    //kiểm tra ký tự str1 có khác null không và ký tự hiện tại của 2 chuỗi có giống nhau khôngkhông
    while (*str1 && (*str1 == *str2))
    {
        str1++;
        str2++;
    }
    return (*(const unsigned char *)str1 - *(const unsigned char *)str2);
}
static CenterPoint *binarySearch(CenterPoint **root, CenterPoint *current, const char *search)
{
    /* 
    *NOTE: the address of base root which is the pointer to the array of BST must not be changed
    -> therefore we have to pass root as input paramter everytime we call binarySearch function
    Lưu ý: 
     + root là con trỏ lưu giữ địa chỉ mảng chứa cây nhị phân, được sử dụng
       để giữ liên kết không bị lỗi mất đồng bộ khi ta thực hiện thay đổi địa chỉ trỏ đến trên cây nhị phân cụ thể
     + current là con trỏ đến cây nhị phân hiện tại, và sẽ được dùng để lặp qua từng nhánh để kiểm tra
     */
    if (current == NULL)
    {
        return NULL;
    }
    // kiểm tra và trả về thông tin name hoặc sdt dựa trên search
    char *current_info = isdigit(*search) ? current->user->info.phone : current->user->info.name;

    // if name is matched then return full info
    if (strcmp(current_info, search) == 0) // compare current info and search info
    {
        return current;
    }
    // if search < current -> find the left side of tree
    if (stringCompare(current_info, search) > 0)
        return binarySearch(root, current->left, search);
    // if search > current -> find the right side of tree
    else
        return binarySearch(root, current->right, search);
}
CenterPoint *Search_Info(CenterPoint **root, const char *search)
{
    //kiểm tra cây nhị phân có tồn tại không
    if (root == NULL || search == NULL)
    {
        return NULL;
    }
    //xác định cây nhị phân sẽ sử dụng tìm kiếm dựa trên chuỗi search -> nếu phát hiện ký tự số thì trả về cây nhị phân tìm kiếm dựa trên sdt
    CenterPoint* search_info = isdigit(*search) ? root[1] : root[0];
    //trả về kết quả tìm kiếm
    return binarySearch(root,search_info,search);
}
void print_Search_byPhone(CenterPoint *root)
{
    User_node *search_user = root->user;
    printf("%s %d %s %s\n", search_user->info.name,
           search_user->info.age,
           search_user->info.phone,
           search_user->info.address);
}
void print_Search_byName(CenterPoint *root, User_node *list_user)
{
    User_node *search_user = root->user;
    User_node *current = list_user;
    /* Find and print info of all user with the same name */
    //tìm và in ra tất cả thông tin của user có tên trùng nhau
    while (current != NULL)
    {
        // lặp cho đến khi user hiện tại và tiếp theo có name trùng nhau
        if (strcmp(current->info.name, search_user->info.name))
        {
            current = current->next_user;
        }
        else
        {
            //bỏ qua trường hợp tìm thấy sdt của user trong danh sách trùng với thông tin của user đang tìm kiếm theo name
            //-> tránh trường hợp in thông tin của user muốn tìm kiếm 2 lầnlần
            if (!strcmp(current->info.phone, search_user->info.phone))
                current = current->next_user;
            //in thông tin của tất cả user có name giống nhưng khác phone
            else
            {
                printf("%s %d %s %s\n", current->info.name,
                       current->info.age,
                       current->info.phone,
                       current->info.address);
                //tiếp tục lặp cho đến cuối danh sách
                current = current->next_user;
            }
        }
    }
    // print search user
    printf("%s %d %s %s\n", search_user->info.name,
           search_user->info.age,
           search_user->info.phone,
           search_user->info.address);
}
void freeBST(CenterPoint* user){
    if(user == NULL)
        return;
    freeBST(user->left);
    freeBST(user->right);
    free(user);
    
}