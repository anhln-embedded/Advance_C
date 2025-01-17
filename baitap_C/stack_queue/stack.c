#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#define STACK_EMPTY -1
int giaithua(int n)
{
    if (n == 1)
    {
        return 1;
    }
    else
        return n * giaithua(n - 1);
}

typedef struct Stack
{
    int *items;
    int size;
    int top;
} Stack;


void initialize(Stack *stack, int size)
{
    stack->items = (int *)malloc(sizeof(int) * size); // mảng để lưu các giá trị của stack
    stack->size = size;                               // kích thuóc của stack
    stack->top = -1;                                  // cài đặt stack rỗng ban đầu
}

bool is_empty(Stack stack)
{
    return (stack.top == -1) ? true : false;
}

bool is_full(Stack stack)
{
    return (stack.top == stack.size - 1) ? true : false;
}

void push(Stack *stack, int value)
{
    if (is_full(*stack) == false)
    {
        stack->items[++stack->top] = value;
    }
    else
    {
        printf("Stack overflow\n");
    }
}

int pop(Stack *stack)
{
    if (is_empty(*stack) == false)
    {
        return stack->items[stack->top--];
    }
    else
    {
        printf("Stack underflow\n");
        return STACK_EMPTY;
    }
}

int top(Stack stack)
{
    if (is_empty(stack) == false)
    {
        return stack.items[stack.top];
    }
    else
    {
        printf("Stack is empty\n");
        return STACK_EMPTY;
    }
}

int main()
{
    Stack stack1;
    int8_t size = 5;
    initialize(&stack1, size);
    printf("push process\n");
    for (int8_t i = 0; i < size; i++)
    {
        push(&stack1, i + 2);
        printf("element: %d -> add:%p\n", stack1.items[i], &stack1.items[i]);
    }
    push(&stack1, 1111);
    printf("pop process\n");
    for (int8_t i = size - 1; i >= -1; i--)
    {
        printf("top element: %d -> add:%p\n", pop(&stack1), &stack1.items[i]);
    }
    return 0;
}
