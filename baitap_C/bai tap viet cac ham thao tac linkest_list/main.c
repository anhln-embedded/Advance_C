#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
typedef struct Node
{
    struct Node *next; // address of next node in linkest list
    int val;
} Node;
Node *CreateNode(int val);
int size(Node *head);
int get_postion(Node *head, int pos);
bool empty(Node *head);
void Total_Node(Node *head);

int front(Node *head);
int back(Node *head);
void push_back(Node **head, int value);
void push_front(Node **head, int value);
void push_arr(Node **head, int *arr, int len, bool PUSH_TYPE);
void insert(Node **head, int value, int position);

void pop_back(Node **head);
void pop_front(Node **head);
void delete_node(Node **head, int pos);
void free_list(Node **head);

#define FRONT 0
#define BACK 1
#define CHECK_EMPTY_LIST(head)                  \
                                                \
    {                                           \
        if (empty(head))                        \
        {                                       \
            printf("no node in linked list\n"); \
        }                                       \
    }

int main()
{
    int pos = 3;
    int arr[] = {12, 13, 141, 15, 16, 124};
    int len = sizeof(arr) / sizeof(arr[0]);
    Node *head = CreateNode(4);
    push_front(&head,24);
    push_arr(&head, arr, len, BACK);
    Total_Node(head);
    free_list(&head);
    Total_Node(head);
    return 0;
}
bool empty(Node *head)
{
    return (head == NULL) ? true : false;
}
Node *CreateNode(int val)
{
    Node *node = (Node *)malloc(sizeof(Node)); // allocate memory for node
    node->next = NULL;
    node->val = val;
    return node;
}
int size(Node *head)
{
    if (empty(head))
        return 0;
    Node *current = head;
    int size = 1;
    while (current->next != NULL)
    {
        current = current->next;
        size++;
    }
    return size;
}
int front(Node *head)
{
    if (empty(head))
        printf("no node in linkest list\n");
    else
    {
        int front = head->val;
        return front;
    }
}
int back(Node *head)
{
    CHECK_EMPTY_LIST(head);
    Node *current = head;
    while (current->next != NULL)
    {
        current = current->next;
    }
    int back = current->val;
    return back;
}
void Total_Node(Node *head)
{
    Node *current = head;
    CHECK_EMPTY_LIST(head);
    for (int i = 0;; i++)
    {
        printf("node %d : %d\n", i, current->val);
        if (current->next == NULL)
        {
            break;
        }
        current = current->next;
    }
    printf("front: %d\tback: %d\n", front(head), back(head));
}
int get_postion(Node *head, int position)
{
    if (empty(head) || position == 0 || position > size(head))
        return 0;
    Node *current = head;
    int index = 0;
    while (index < position - 1)
    {
        current = current->next;
        index++;
    }
    int val = current->val;
    return val;
}

void push_back(Node **head, int value)
{
    Node *node = CreateNode(value);
    // if no node is created then assign address of node node to list
    if (empty(*head))
    {
        *head = node;
    }
    else
    {
        Node *current = *head; // use temp pointer to store address of first node in linkest likst
        // loop through every node untill reaches the last one
        while (current->next != NULL)
        {
            current = current->next; // move to next node
        }
        current->next = node;
    }
}
void push_front(Node **head, int value)
{
    Node *node = CreateNode(value);
    if (empty(*head))
    {
        *head = node;
    }
    else
    {
        node->next = *head; // update address of previous head
        *head = node;       // update address of new node
    }
}
void push_arr(Node **head, int *arr, int len, bool PUSH_TYPE)
{
    for (int i = 0; i < len; i++)
    {
        if (PUSH_TYPE == FRONT)
            push_front(head, arr[i]);
        else
            push_back(head, arr[i]);
    }
}
void insert(Node **head, int value, int position)
{
    // Tạo node mới
    Node *node = CreateNode(value);

    // Trường hợp chèn vào vị trí đầu (position == 0)
    if (position == 0)
    {
        push_front(head, value);
        return;
    }
    else
    {
        Node *current = *head;
        int index = 0;

        // Duyệt đến vị trí chèn hoặc cuối danh sách
        while (current != NULL && index < position - 1)
        {
            current = current->next;
            index++;
        }

        // Kiểm tra nếu vị trí hợp lệ
        if (current == NULL)
        {
            printf("khong tim thay vi tri insert \n", position);
            return;
        }
        else
        {
            // Chèn node tại vị trí đã cho
            node->next = current->next;
            current->next = node;
        }
    }
}

void pop_back(Node **head)
{
    if (empty(*head))
    {
        printf("no node in linked list\n");
        return;
    }
    Node *current = *head;
    if (current->next == NULL)
        pop_front(head);
    else
    {
        while (current->next->next != NULL)
        {
            current = current->next;
        }
        Node *final_node = current->next; // save final node
        free(final_node);
        current->next = NULL; // update next address is null
    }
}
void pop_front(Node **head)
{
    if (empty(*head))
    {
        printf("no node in linked list\n");
        return;
    }
    // use temp to store first node
    Node *first_node = *head;
    // move to address of second node
    *head = (*head)->next;
    free(first_node);
}
void delete_node(Node **head, int position)
{
    if (empty(*head))
    {
        printf("no node in linked list\n");
        return;
    }
    if (position == 0)
    {
        pop_front(head);
        return;
    }

    Node *current = *head;
    int index = 0;
    while (current != NULL && index < position - 1)
    {
        current = current->next;
        index++;
    }

    if (current == NULL || current->next == NULL)
    {
        printf("no node at position %d\n", position);
        return;
    }

    Node *temp = current->next;
    current->next = current->next->next;
    free(temp);
}

void free_list(Node **head)
{
    if (empty(*head))
    {
        printf("no node in linked list\n");
        return;
    }
    Node *current = *head;
    Node *next;
    while (current != NULL)
    {
        next = current->next;
        free(current);
        current = next;
    }
    *head = NULL;
}
