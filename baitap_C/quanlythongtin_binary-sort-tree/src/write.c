//#include"write.h"
#include "..//inc//write.h"
bool writeCSV(char* path){
    FILE* file = fopen(path,"w");
    if(file == NULL){
        printf("cannot open file\n");
        return FAIL_CREATED_FILE;
    }
    fprintf(file,"ten,tuoi,so dien thoai,dia chi\n");
    fprintf(file,"Pham Cao Duy,25,0972665872,91 Pham Van Hai P3 Q Tan Binh\n");
    fprintf(file,"Trinh Tran Phuong Tuan,24,0908234588,TP Tay Ninh \n");
    fprintf(file,"Trinh Le Hoang,28,0376572677,12 Nguyen Xien Q12\n");
    fprintf(file,"Nguyen Tan Tung,21,038764589,45 Tran Binh Trong\n");
    fprintf(file,"Le Quang Nhat,26,0978278121,17 Binh Phuoc\n");
    fprintf(file,"Nguyen Huu Hung,22,0978565342,17 Q Binh Thanh\n");
    fprintf(file,"Pham Cao Duy,18,090395678,220/8 Nguyen Phuc Nguuyen P9 Q3\n");
    fprintf(file,"Dinh Anh Tuan,24,0903478211,TP Tay Ninh\n");
    fprintf(file,"Nguyen Ho Duy,17,0906733209,22/5 Binh Thuan\n");
    fprintf(file,"Pham Cao Duy,20,0376572231,18 Nguyen Thi Minh Khai Q1 TPHCM\n");
    fprintf(file,"Nguyen Thi Thanh Thuy,27,038764987,21 Nguyen Thien Thuat P12 QTan Phu\n");
    fprintf(file,"Nguyen Ho Duy,27,038764912,22 Nguyen Thien Thuat P13 Q Tan Binh\n");
    fprintf(file,"Nguyen Thi Thanh Thu,27,038764997,23 Nguyen Thien Thuat P14  Q Binh Thanh\n");
    fprintf(file,"Pham Cao Duy,27,038764912,24 Nguyen Thien Thuat P9 Q 10\n");
    fclose(file);
    return SUCCESS_CREATED_FILE;
}
void log_status(const char* str){
    printf("%s\n",str);
}