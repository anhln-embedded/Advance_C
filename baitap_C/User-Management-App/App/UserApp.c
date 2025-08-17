#include "UserApp.h"

static void feature1() { printf("Đã chọn tiêu đề 1\n"); }
static void feature2() { printf("Đã chọn tiêu đề 2\n"); }
static void feature3() { printf("Đã chọn tiêu đề 3\n"); }
static void feature4() { printf("Đã chọn tiêu đề 4\n"); }

SystemEvent ExecuteInitProgram(const char* filename){
    if(Load_UserDB(filename) == E_OK){
        UI_ShowMessage("Load Database thành công");
    }
    else{
        UI_ShowMessage("Load Database thất bại"); 
        return INIT_FAIL;
    }
    if(Build_ListUser() == E_OK){
        UI_ShowMessage("Tạo danh sách User sắp xếp theo tên và sdt thành công");
    }
    else{
        UI_ShowMessage("Tạo danh sách User sắp xếp theo tên và sdt thất bại");  
        return INIT_FAIL; 
    }
   
    if(Build_SearchList() == E_OK){
        UI_ShowMessage("Chuyển đổi danh sách User thành định dạng tìm kiếm thành công");
    }
    else{
        UI_ShowMessage("Chuyển đổi danh sách User thành định dạng tìm kiếm thất bại");
        return INIT_FAIL;
    }

    return INIT_SUCCES;
}
SystemEvent ShowMainMenu(){
    UI_ShowMessage("***MENU CHÍNH***");
    UI_ShowMessage("/**********************/");
    PRINT_MENU("Xem thông tin user", "Tìm kiếm User","Thoát chương trình");
    UI_ShowMessage("/**********************/");
    input:    
    int option = UI_InputChoice();
    HANDLE_OPTION(option,
        CASE_OPTION(1, feature1) 
        CASE_OPTION(2, feature2)
        CASE_OPTION(3, feature3)
        CASE_OPTION(4, feature3)
        CASE_OPTION(5, feature3)
    )
    if(option == 1) return LIST_USER;
    else if(option == 2) return SEARCH_USER;
    else if(option == 3) return STOP;
    else{
        UI_ShowMessage("Vui lòng nhập lựa chọn từ (1 -> 3)");
        goto input;
    }
}
void ShowMenuListUser(){
    input:  
    UI_ShowMessage("/**********************/");
    PRINT_MENU("Dữ liệu từ database (đọc từ file csv)", 
               "Dữ liệu sắp xếp theo tên",
               "Dữ liệu Sắp xếp theo sdt", 
               "Quay lại Menu chính");  
    UI_ShowMessage("/**********************/");
    int option = UI_InputChoice();
    HANDLE_OPTION(option,
        CASE_OPTION(1, feature1) 
        CASE_OPTION(2, feature2)
        CASE_OPTION(3, feature3)
        CASE_OPTION(4, feature4)
    )
    if(option == 1){
        UI_ShowMessage("***Dữ liệu User từ database***");
        Print_UserDB();
    }
    else if(option == 2){
        UI_ShowMessage("***Danh sách User sắp xếp theo tên***");
        Print_ListUser(SORT_NAME);
    }
    else if(option == 3){
        UI_ShowMessage("***Danh sách User sắp xếp theo sdt***");
        Print_ListUser(SORT_PHONE);
    }
    else if(option == 4){
        return;
    }
    else UI_ShowMessage("Vui lòng nhập lựa chọn từ (1 -> 4)");
    
    goto input;
}
void ExecuteSearchUser(){
    while(1){
        char* Search = UI_InputString();
        printf("%s\n",Search);
        if(Search_User(Search) != E_OK){
            UI_ShowMessage("Không tìm thấy User");
        }
        UI_ShowMessage("Tiếp tục tìm kiếm ?");
        UI_ShowMessage("1.Có");
        UI_ShowMessage("0.Không");
        input:
        int choice = UI_InputChoice();    

        if(choice != 0 && choice != 1){
            UI_ShowMessage("Vui lòng chọn 1 hoặc 0");
            goto input;
        }
        if(choice == 0) break;
    }
}
void ExecuteEndProgram(){
    if(Remove_SearchList() == E_OK){
        if(Remove_UserDB() == E_OK){
            if(Remove_ListUser() == E_OK){
                UI_ShowMessage("Đã xóa dữ liệu User thành công");
                UI_ShowMessage("Thoát chương trình");
                return;
            }
        }
    }
    UI_ShowMessage("Xóa dữ liệu thất bại");
    
}