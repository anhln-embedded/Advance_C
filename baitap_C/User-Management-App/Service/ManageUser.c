#include "ManageUser.h"
#include "SharedData.h"
//Biến cục bộ sử dụng trong file hiện tại 
static UserNode* List_User_NameSorted; //danh sách liên kết sắp xếp theo tên
static UserNode* List_User_PhoneSorted;//danh sách liên kết sắp xếp theo sdt
                ///////////////*KHAI BÁO CÁC HÀM CỤC BỘ*////////////////
/**
 * @brief   So sánh tên giữa hai người dùng.
 *
 * @param[in] current  Con trỏ đến UserData hiện tại.
 * @param[in] next     Con trỏ đến UserData kế tiếp.
 *
 * @retval  >0  current->name lớn hơn next->name. 
 * @retval   0  current->name bằng next->name.
 * @retval  <0  current->name nhỏ hơn next->name.
 */
static int CompareName(UserData* current,UserData* next);
/** @copydoc CompareName */
static int ComparePhone(UserData* current,UserData* next);
/**
 * @brief     Thực hiện sắp xếp danh sách liên kết theo tiêu chí được chỉ định.
 *
 * @details   Hàm này thêm 1 node và lựa chọn vị trí chèn trên danh sách liên kết
 *            các phần tử kiểu UserNode. Tiêu chí so sánh được truyền vào thông qua con trỏ hàm
 *            @p Compare, cho phép sắp xếp theo tên hoặc số điện thoại.
 *
 * @param[in,out] head     Con trỏ đến con trỏ đầu danh sách cần sắp xếp.
 * @param[in]     value    Con trỏ đến dữ liệu người dùng (UserData) phục vụ quá trình so sánh và 
 *                         cập nhật vị trí chèn của value
 * @param[in]     Compare  Con trỏ tới hàm so sánh hai đối tượng UserData.
 *                         - CompareName()  : So sánh dựa trên tên.
 *                         - ComparePhone() : So sánh dựa trên số điện thoại.
 *
 * @return     none
 */
static void Build_SelectSortType(UserNode** head,UserData* value,int (*Compare)(UserData*,UserData*));
/**
 * @brief   Hàm xóa bỏ danh sách liên kết mà người dùng chỉ định
 * @param[in] search  con trỏ đến con trỏ đầu danh sách tên hoặc sdt
 * @retval  E_OK    Hàm xử lý thành công
 * @retval  NOT_OK  Hàm xử lý thất bại
 */
static Status free_LinkedList(UserNode **head);
                ///////////////*ĐỊNH NGHĨA CÁC HÀM TOÀN CỤC*////////////////
Status Build_ListUser()
{
    int total_user = Read_SizeUserDB();

    UserData* Storage_UserDB = Read_UserDB();

    for(int i = 0 ; i < total_user ; i++)
    {
        Build_SelectSortType(&List_User_NameSorted,&Storage_UserDB[i],CompareName); 
    }
    for(int i = 0 ; i < total_user ; i++){
        Build_SelectSortType(&List_User_PhoneSorted,&Storage_UserDB[i],ComparePhone);
    }

    if(List_User_NameSorted != NULL && List_User_PhoneSorted != NULL)
        return E_OK;
    else   
        return NOT_OK;

}
Status Print_ListUser(SortType type)
{
    UserNode* head = (type == SORT_NAME) ? List_User_NameSorted : List_User_PhoneSorted;
    if (head == NULL)
    {
        return NOT_OK;
    }
    while (head != NULL)
    {
        printf("%s\t%d\t%s\t%s\n", head->value.name,
               head->value.age,
               head->value.phone,
               head->value.address);
        head = head->next;
    }
    return E_OK;
}
Status Remove_ListUser(){
    if(free_LinkedList(&List_User_NameSorted) == E_OK){
        if(free_LinkedList(&List_User_PhoneSorted) == E_OK){
            return E_OK;
        }
        return NOT_OK;
    }
    return NOT_OK;
}
UserNode* Read_ListUser(SortType type){
    return (type == SORT_NAME) ? List_User_NameSorted : List_User_PhoneSorted;
}
                ///////////////*ĐỊNH NGHĨA CÁC HÀM CỤC BỘ*////////////////
static int CompareName(UserData* current,UserData* next){
    return stringCompare(current->name,next->name);
}
static int ComparePhone(UserData* current,UserData* next){
    return stringCompare(current->phone,next->phone);
}
static void Build_SelectSortType(UserNode** head,UserData* value,int (*Compare)(UserData*,UserData*)){
    UserNode *new_node = (UserNode *)malloc(sizeof(UserNode));
    new_node->value = *value; // sao chép thông tin của user tiếp theo vào node mới tạo
    new_node->next = NULL;

    //Kiểm tra nếu nếu node mới lớn hơn node hiện tại thì chèn đầu danh sách
    if (*head == NULL || Compare(&((*head)->value),&new_node->value) > 0)
    {
        new_node->next = *head; 
        *head = new_node; 
        return;
    }


    //trỏ đến vị trí ban đầu của danh sách 
    UserNode *current = *head;
    //duyệt lần lượt các node đến vị trí cần chèn
    while (current->next != NULL && Compare(&(current->next->value),&new_node->value) < 0)
    {
            current = current->next; 
    }
    //cập nhật node mới tạo ra vào vị trí chèn
    new_node->next = current->next;
    current->next = new_node; 
}
static Status free_LinkedList(UserNode **head)
{
    if (*head == NULL){
        return NOT_OK;
    }
    UserNode *current= *head;
    while (current!= NULL)
    {
        UserNode *next = current->next;
        free(current);
        current= next;
    }
    *head = NULL; 
    return E_OK;
}

