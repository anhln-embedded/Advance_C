#include "UserApp.h"
#define PATH_FILE ".//Data//database.csv"
int main(){
    SystemEvent state = ExecuteInitProgram(PATH_FILE);
    if(state == INIT_SUCCES){
        while(state != STOP){
            state = ShowMainMenu();
            switch (state)
            {
            case LIST_USER:
                ShowMenuListUser();
                break;
            case SEARCH_USER:
                ExecuteSearchUser();
                break;
            case STOP:
                ExecuteEndProgram();
                break;
            default:
                break;
            }
        }
    }
    else{
        ExecuteEndProgram();
    }
    return 0;
}