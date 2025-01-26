#include <stdio.h>
#include <setjmp.h>
#include <string.h>
#define ERROR_DIVIDE_BY_0        1
#define ERROR_A_IS_ODD           2
#define ERROR_B_IS_EVEN          3

jmp_buf buf;
int exception_code;
char* error_list[] = {
                "Error: Divide by 0!",
                "Error: a must be an even number",
                "Error: b must be an odd number"
            };
char error_code[30];    
#define TRY if ((exception_code = setjmp(buf)) == 0) 
#define CATCH(code) else if (exception_code == (code)) 
#define THROW(code,error_list) {\
int i = 0;                \
while(error_list[i] != '\0'){         \
    error_code[i] = error_list[i]; \
    i++;                  \
}                         \
error_code[i] = '\0';     \
longjmp(buf,(code));      \
}


double divide(int a, int b) {
    if (b == 0) {THROW(ERROR_DIVIDE_BY_0,error_list[0]);}
    else if(a % 2) {THROW(ERROR_A_IS_ODD,error_list[1]);}
    else if(b % 2 == 0) {THROW(ERROR_B_IS_EVEN,error_list[2]);}
    return (double)a / b;
}
int a = 0,b = 0;

int main() {
    //int a = 0,b = 0;
    double result = 0.0;
    while(1){
        printf("nhap a:");
        scanf("%d",&a);
        printf("nhap b:");
        scanf("%d",&b);
        TRY {
            result = divide(a, b);
            printf("Result: %f\n", result);
        } 
        CATCH(ERROR_DIVIDE_BY_0)    printf("%s\n",error_code);
        CATCH(ERROR_A_IS_ODD)      printf("%s\n",error_code);
        CATCH(ERROR_B_IS_EVEN)       printf("%s\n",error_code);
    }
    // Các xử lý khác của chương trình
    return 0;
}


