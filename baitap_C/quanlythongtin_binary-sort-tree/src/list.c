//#include "list.h"
#include "..//inc//list.h"
extern int total_user;
static void sort_byName(User_node **list_user_sortName,Info *next_user_value){
    User_node *new_user = (User_node *)malloc(sizeof(User_node));
    new_user->info = *next_user_value; // sao chép thông tin của user tiếp theo vào node mới tạotạo
    new_user->next_user = NULL;

    /* kiểm tra danh sách có node nào chưa hoặc giá trị name của node hiện tại có lớn hơn node mới không -> thực hiện sắp xếp tăng dần */
    if (*list_user_sortName == NULL || stringCompare((*list_user_sortName)->info.name, new_user->info.name) > 0)
    {
        new_user->next_user = *list_user_sortName; //cập nhật node hiện tại thành node tiếp theo
        *list_user_sortName = new_user; //cập nhật node mói tạo thành node đầu của danh sách 
        return;
    }


    //trỏ đến vị trí ban đầu của danh sách 
    User_node *current = *list_user_sortName;

    //kiểm tra lần lượt các node trong danh sách có lớn hơn node mới tạo 
    while (current->next_user != NULL && stringCompare(current->next_user->info.name, new_user->info.name) < 0)
    {
            current = current->next_user; //lặp qua từn node
    }
    //-> thực hiện gán node mới sau node có giá trị name lớn hơn nó
    new_user->next_user = current->next_user;
    current->next_user = new_user; // update addres of previous next before back node
}
static void sort_byPhone(User_node **list_user_sortPhone,Info *next_user_value){
    User_node *new_user = (User_node *)malloc(sizeof(User_node)); //cấp phát vùng nhớ cho node mới
    new_user->info = *next_user_value; //
    new_user->next_user = NULL;

    /*if list is empty or first node > new_node -> add new_node as first one*/
    //
    if (*list_user_sortPhone == NULL || stringCompare((*list_user_sortPhone)->info.phone, new_user->info.phone) > 0)
    {
        new_user->next_user = *list_user_sortPhone;
        *list_user_sortPhone = new_user;
        return;
    }
    /*loop through each node*/
    User_node *current = *list_user_sortPhone;

    /*if current node < new_node then keep traversing*/
    while (current->next_user != NULL && stringCompare(current->next_user->info.phone, new_user->info.phone) < 0)
    {
        current = current->next_user;
    }

    new_user->next_user = current->next_user;
    current->next_user = new_user; // update addres of previous next before back node
}
void Create_UserList(Info *info, User_node **list_user_sortName, User_node **list_user_sortPhone)
{
    int user_count = 0;
    while (user_count < total_user)
    {
        //tạo danh sách liên kết sắp xếp theo tên và sdt
        sort_byName(list_user_sortName,(info + user_count));
        sort_byPhone(list_user_sortPhone,(info + user_count));
        user_count++;
    }
}
void print_user(User_node *head)
{
    if (head == NULL)
    {
        printf("no user avaliable\n");
        return;
    }
    User_node *head_user = head;
    while (head_user != NULL)
    {
        printf("%s %d %s %s\n", head_user->info.name,
               head_user->info.age,
               head_user->info.phone,
               head_user->info.address);
        head_user = head_user->next_user;
    }
}
void free_list_user(User_node* head)
{
    if (head == NULL)
    {
        printf("no user avaliable for being released\n");
        return;
    }
    User_node *current = head;
    User_node *next = NULL;
    while (current != NULL)
    {
        next = current->next_user;
        free(current->info.name);
        free(current->info.address);
        free(current->info.phone);
        free(current);
        current = next;
    }
}
