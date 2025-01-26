#include <stdio.h>
#include <string.h>
#include <setjmp.h>
#include <stdint.h>

enum ErrorCodes{NO_ERROR, FILE_ERROR, NETWORK_ERROR, CALCULATION_ERROR };

jmp_buf buf;
int error_name;
char error_message[30];
char* file = "sadawd";
char* pass = "Advance_C";

#define TRY if((error_name = setjmp(buf)) == NO_ERROR)
#define CATCH(ERROR_CODE) else if(error_name == ERROR_CODE)
#define THROW(ERROR_CODE,STR) {\
int len = strlen(STR);\
for(int i = 0 ; i < len ;i++){  \
    error_message[i] = STR[i];\
}                       \
error_message[len] = '\0'; \
longjmp(buf,ERROR_CODE); \
}

void readFile(char* str) {
    printf("Doc file...\n");
    if(str == NULL)
        THROW(FILE_ERROR,"Loi doc file: file khong ton tai");
    printf("doc file thanh cong\n");
}

void calculateData(int tuso,int mauso) {
    printf("dang tinh toan...\n");
    if(mauso==0)
      THROW(CALCULATION_ERROR,"loi chia cho 0");
    int result = tuso / mauso;
    printf("ket qua: %d/%d = %d\n",tuso,mauso,result);
}

void networkOperation(char* str) {
    printf("dang ket noi:...\n");
    if(strcmp(str,pass))
        THROW(NETWORK_ERROR,"Loi ket noi wifi: mat khau khong dung");
    printf("wifi da ket noi\n");
}
int main(void){
    TRY{
        readFile(file);
        networkOperation(pass);
        calculateData(21,23);
    } 
    CATCH(FILE_ERROR) printf("%s\n", error_message);
    CATCH(NETWORK_ERROR) printf("%s\n", error_message);
    CATCH(CALCULATION_ERROR) printf("%s\n",error_message);
    printf("ket thuc chuong trinh");
    return 0;
}

