#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#define QUEUE_EMPTY -1
typedef struct queue
{
    int *queue_item;
    int size;
    int front;
    int rear;
} Queue;

Queue *initialize(int size)
{
    Queue *queue = (Queue *)malloc(size * sizeof(Queue));
    queue->queue_item = (int *)malloc(size * sizeof(int));
    queue->size = size;
    queue->front = queue->rear = -1;
    return queue;
}
bool IsQueue_Empty(Queue queue)
{
    return ((queue.front == -1) ? true : false);
}
bool IsQueue_Full(Queue queue)
{
    /* circular */
    return (queue.rear + 1) % queue.size == queue.front; //
    /* linear */
    //return ((queue.rear == queue.size - 1) ? true : false);
}

void enqueue(Queue *queue, int value)
{
    if (!IsQueue_Full(*queue))
    {
        if (IsQueue_Empty(*queue))
        {
            queue->front = queue->rear = 0;
        }
        else
        {
            /* linear */
            //queue->rear++;
            /* circular */
            queue->rear = (queue->rear + 1) % queue->size;
        }
        queue->queue_item[queue->rear] = value;
        printf("enqueue %d -> %p\n", queue->queue_item[queue->rear], &queue->queue_item[queue->rear]);
    }
    else
        printf("queue overflow, can't add more item\n");
}
int dequeue(Queue *queue)
{
    if (!IsQueue_Empty(*queue))
    {
        int dequeue_value = queue->queue_item[queue->front];
        if (queue->front == queue->rear)
        {
            queue->front = queue->rear = -1;
        }
        else
        {
            /* linear */
            queue->front++;
            /* circular */
            //queue->front = (queue->front + 1) % queue->size;
        }
        return dequeue_value;
    }
    else
    {
        printf("queue underflow\n");
        return QUEUE_EMPTY;
    }
}
int front(Queue queue)
{
    if (IsQueue_Empty)
    {
        printf("queue is empty\n");
        return -1;
    }
    return queue.queue_item[queue.front];
}

void implement_enqeue_dequeue(Queue *queue, int *ptr)
{
    printf("***enqueue process***\n");
    for (int8_t i = 0; i < queue->size; i++)
    {
        enqueue(queue, ptr[i]);
    }
    
   /*  printf("***dequeue process***\n");
    for (int8_t i = queue->front; i <= queue->rear; i++)
    {
        printf("dequeue %d -> %p \n", dequeue(queue),&queue->queue_item[i]);
    } */
   
}
void display(Queue *queue)
{
    printf("\nelements in queue\n");
//khi chỉ số rear chưa trỏ về đầu hàng đợi để enqueue 
    if (queue->rear > queue->front) 
    {
        for (int8_t i = queue->front; i <= queue->rear; i++)
        {
            printf("queue %d\n", queue->queue_item[i]);
        }
    }
//khi cơ chế circular queue được kích hoạt -> rear trỏ về đầu hàng đợi
    else if (queue->rear < queue->front)
    {
        for (int8_t i = 0; i < queue->size; i++)
        {
            printf("queue %d\n", queue->queue_item[i]);
        }
    }
}
int main()
{
    int arr[] = {1, 2, 3, 4, 5};
    int size = sizeof(arr) / sizeof(arr[0]);
    Queue *queue = initialize(size);
    implement_enqeue_dequeue(queue, arr);
    printf("***dequeue 2 element***\n");
    printf("dequeue: %d\n", dequeue(queue));
    printf("dequeue: %d\n", dequeue(queue));
    display(queue);
    printf("\nenqueue more\n");
    enqueue(queue, 6);
    enqueue(queue, 7);
    display(queue);
    return 0;
}