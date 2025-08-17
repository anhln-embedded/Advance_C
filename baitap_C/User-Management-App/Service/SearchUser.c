#include "SearchUser.h"
#include "SharedData.h"
#include <ctype.h>

/**
 * @brief Trạng thái Tìm kiếm user theo tiêu chí tương ứng
 * 
 * Enum này dùng để quản lý việc lựa cách xử lý trả về thông tin user dựa trên cách mà người dùng nhập tên/sdt
 * Phạm vi sử dụng: file hiện tại
 */
typedef enum{
    FOUND_BY_NAME,
    FOUND_BY_PHONE
}UserFoundType;

//Biến cục bộ lưu trữ cấu trúc cây nhị phân được tạo ra theo tên/sdt
static CenterPoint* RootByName;
static CenterPoint* RootByPhone;
                         ///////////////*KHAI BÁO CÁC HÀM CỤC BỘ*////////////////
/**
 * @brief     xóa bỏ cấu trúc cây nhị phân 
 *
 * @param[in] proot   con trỏ đến con trỏ đầu của cây nhị phân có thể là 
 *                    - RootByName : lưu trữ các UserNode sắp xếp theo tên
 *                    - RootByPhone : lưu trữ các UserNode sắp xếp theo sdt
 * @return    NOT_OK  Hàm xử lý thành công
 * @retval    E_OK    Hàm xử lý thất bại
 */
static Status FreeBinaryTree(CenterPoint **proot);
/**
 * @brief    tìm kiếm thông tin của user dựa trên thuật toán binarysearch
 *
 * @param[in] proot   con trỏ đến con trỏ đầu của cây nhị phân có thể là 
 *                    - RootByName : lưu trữ các UserNode sắp xếp theo tên
 *                    - RootByPhone : lưu trữ các UserNode sắp xếp theo sdt
 * @param[in] search  chuỗi ký tự đại diện cho tên hoặc sdt do người dùng nhập
 * @retval    NULL    Không tìm thấy con trỏ đến cấu trúc CenterPoint chứa user muốn tìm 
 */
static CenterPoint *BinarySearch(CenterPoint *proot, const char *search);
/**
 * @brief    Hàm triển khai thuật toàn xây dựng cấu trúc cây nhị phân tìm kiếm user
 *
 * @param[in] head   con trỏ đến cây nhị phân có thể là 
 *                    - RootByName : lưu trữ các UserNode sắp xếp theo tên
 *                    - RootByPhone : lưu trữ các UserNode sắp xếp theo sdt
 * @param[in] start   vị trí bắt đầu
 * @param[in] end     vị trí kết thúc
 * @return    Centerpoint   con trỏ đến cấu trúc cây nhị phân tìm kiếm đã xây dựng
 */
static CenterPoint *BuildTree(UserNode *head, int start, int end);
/**
 * @brief    Hàm in thông tin của user tìm được
 *
 * @param[in] Search_root con trỏ đến kết quả trả về từ hàm BinarySearch
 * @param[in] type    biến kiểu enum để điều hướng luồng xử lý in ra thông tin user theo tên hoặc sdt
 *                    có thể là 
 *                    - FOUND_BY_NAME  : tìm thông tin user theo tên
 *                    - FOUND_BY_PHONE : tìm thông tin user theo sdt
 * 
 * @retval    none 
 */
static void Print_FoundUser(CenterPoint* Search_root,UserFoundType type);
/**
 * @brief    Hàm trừu tượng quá trình xây dựng cây nhị phân 
 * @details  Hàm này nhận vào con trỏ đến danh sách liên kết có kiểu UserNode để xác định điểm giữa 
 *           và các điểm start,end chuẩn bị cho bước gọi ra hàm xử lý thuật toán xây dựng cây nhị phân
 * @param[in] head    con trỏ đến danh sách liên kết kiểu UserNode* lưu trữ tên hoặc sdt
 * 
 * @retval    none 
 */
static CenterPoint* Build_SelectedTree(UserNode* head);
                         ///////////////*ĐỊNH NGHĨA CÁC HÀM TOÀN CỤC*////////////////
int stringCompare(const char *str1, const char *str2)
{
    // kiểm tra ký tự str1 có khác null không và ký tự hiện tại của 2 chuỗi có giống nhau không
    while (*str1 && (*str1 == *str2))
    {
        str1++;
        str2++;
    }
    return (*(const unsigned char *)str1 - *(const unsigned char *)str2);
}
Status Build_SearchList()
{
    //đọc dữ liệu của user lưu trữ trên 2 linked list sắp xếp theo tên và sdt
    UserNode* List_User_NameSorted = Read_ListUser(SORT_NAME);
    UserNode* List_User_PhoneSorted = Read_ListUser(SORT_PHONE);

    //trả về kết quả xây dựng cây nhị phân cho tên và sdt
    RootByName = Build_SelectedTree(List_User_NameSorted);
    RootByPhone = Build_SelectedTree(List_User_PhoneSorted);

    //kiểm tra và trả về kết quả xử lý
    if(RootByName != NULL && RootByPhone != NULL)   
        return E_OK;
    else 
        return E_OK;
}
Status Search_User(const char *search)
{    
    CenterPoint* result;

    //xử lý tìm kiếm thông tin của user theo sdt
    if(isdigit(*search)){
        result = BinarySearch(RootByPhone, search);
        if(result == NULL){
            return NOT_OK;
        }
        else{
            Print_FoundUser(result,FOUND_BY_PHONE);
            return E_OK;
        }
    }
    //xử lý tìm kiếm thông tin của user theo tên
    else{
        result = BinarySearch(RootByName, search);
        if(result == NULL){
            return NOT_OK;
        }
        else{
            Print_FoundUser(result,FOUND_BY_NAME);
            return E_OK;
        }
    }
}
Status Remove_SearchList(){
    //xóa lần lượt các cây nhị phân tìm kiếm theo tên và sdt
    if(FreeBinaryTree(&RootByName) == E_OK){
        if(FreeBinaryTree(&RootByPhone) == E_OK){
            return E_OK;
        }
        return NOT_OK;
    }
    return NOT_OK;
}
                        ///////////////*ĐỊNH NGHĨA CÁC HÀM CỤC BỘ*////////////////
static Status FreeBinaryTree(CenterPoint **proot)
{
    if (proot == NULL || *proot == NULL){
        return NOT_OK;
    }
    CenterPoint *root = *proot;
    FreeBinaryTree(&root->left);
    FreeBinaryTree(&root->right);

    free(root);
    *proot = NULL; // tránh để lại con trỏ treo ở phía gọi
    return E_OK;
}
static CenterPoint *BinarySearch(CenterPoint *proot, const char *search)
{
    if (proot == NULL)
    {
        return NULL;
    }
    // kiểm tra và trả về thông tin name hoặc sdt dựa trên search
    char *result = isdigit(*search) ? proot->root->value.phone : proot->root->value.name;

    //trả về kết quả tìm được nếu 2 chưỡi giống nhau
    if (strcmp(result, search) == 0) 
    {
        return proot;
    }
    // nếu search < current -> tìm bên trái
    if (stringCompare(result, search) > 0)
        return BinarySearch(proot->left,search);
    // nếu search > current -> tìm bên phải
    else
        return BinarySearch(proot->right,search);
}
static CenterPoint *BuildTree(UserNode *head, int start, int end)
{
    // kiểm tra vị trí các node trái và phải có hợp lệ hay không -> cho biết điểm dừng xây dụng cây nhị phânphân
    if (head == NULL || start > end)
    {
        return NULL;
    }
    // xác định node giữa của danh sáchsách
    int mid = (start + end) / 2;
    UserNode *node = head;
    // lặp cho đến khi gặp node giữa
    for (int i = start; i < mid; i++)
    {
        if (node->next == NULL)
        {
            break;
        }
        // move to next node
        node = node->next;
    }

    // cấp phát vùng nhớ heap để lưu trữ nhánh gốc cho cây nhị phân
    CenterPoint *proot = (CenterPoint *)malloc(sizeof(CenterPoint));
    proot->root = node->next;
    // tạo ra các nhánh 2 trái phải từ nhánh gốc
    proot->left = BuildTree(head, start, mid - 1);
    proot->right = BuildTree(node->next, mid + 1, end);

    return proot;
}
static void Print_FoundUser(CenterPoint* Search_root,UserFoundType type)
{
    //xử lý tìm thông tin user dựa trên tên
    if(type == FOUND_BY_NAME)
    {
        //sao chép danh sách liên kết chứa thông user sắp xếp theo tên
        UserNode *current = Read_ListUser(SORT_NAME);
        // tìm và in ra tất cả thông tin của user có tên trùng nhau
        while (current != NULL)
        {
            // lặp cho đến khi user hiện tại và tiếp theo có name trùng nhau
            if (strcmp(current->value.name, Search_root->root->value.name))
            {
                current = current->next;
            }
            else
            {
                    printf("Tên:%s\n"
                        "Tuổi:%d\n"
                        "sdt:%s\n"
                        "Địa chỉ:%s\n",
                        current->value.name,
                        current->value.age,
                        current->value.phone,
                        current->value.address);
                    // tiếp tục lặp cho đến cuối danh sách
                    current = current->next;
            }
        }
    }
    //xử lý in ra thông tin của user dựa trên sdt
    else{
        printf("Tên:%s\n"
            "Tuổi:%d\n"
            "sdt:%s\n"
            "Địa chỉ:%s\n",
            Search_root->root->value.name,
            Search_root->root->value.age,
            Search_root->root->value.phone,
            Search_root->root->value.address);
    }
}
static CenterPoint* Build_SelectedTree(UserNode* head){
    int length = 0;
    //duyệt từng node để đém số lượng
    UserNode* current = head;
    while (current != NULL)
    {
        current = current->next;
        length++; // xác định số lượng các node trong danh sách
    }
    //
   return BuildTree(head, 0, length - 1); // trả về cây nhị phân
}
