#include "../inc/file-handle.hpp"
// sử dụng lại biến này để khôi phục lại danh sách các phòng khởi tạo ban đầu với trạng thái là Unavailable/Available
extern vector<room_default_dtype> list_room_default;        
                                            /* GHI FILE */
bool File_Handle::SaveData(const char* path,Storage_dtype infotype){
    FILE *file = fopen(path, "w");
    if (file == NULL){
        error_handle:
        return FAIL;
    }
    switch (infotype)
    {
    case GUESS_CSV:
        if(list_guess.empty())
        {
            UI::showMessage("không có thông tin khách");
            goto error_handle;
        } 
        SaveGuessInfo(file);
        break;
    case ROOM_CSV:
        if(list_room_available.empty()) 
        {
            UI::showMessage("không có thông tin phòng");
            goto error_handle;
        }
        SaveRoomInfo(file);
        break;
    case SERVICE_CSV:
        if(list_service.empty()) 
        {
            UI::showMessage("không có thông tin dịch vụ");
            goto error_handle;
        }
        SaveServiceInfo(file);
        break;
    case EMMPLOYEE_CSV:
        if(list_employee.empty()) 
        {
            UI::showMessage("không có thông tin nhân viên");
            goto error_handle;
        }
        SaveEmployeeInfo(file);
        break;
    default:
        fclose(file);
        return FAIL;
    }
    fclose(file);
    return SUCCESS;
}
void File_Handle::SaveGuessInfo(FILE* file){
    auto it= list_guess.begin();
    static bool head_line = false;
    //chỉ in dòng tiêu đề 1 lần duy nhất, những lần gọi hàm sau không cần phải in
    if(!head_line){
        fprintf(file,"so phong,ten khach,so dien thoai,ngay dat phong,ngay tra phong\n");
        head_line = true;
    }
    for (;it!= list_guess.end() ; it++){
        fprintf(file, "%d,%s,%s,%s,%s,\n", (*it ).getRoom(),
                                        (*it ).getName().c_str(),
                                        (*it ).getPhone().c_str(),
                                        (*it ).getCheckin().c_str(),
                                        (*it ).getCheckout().c_str());
    }
}
void File_Handle::SaveRoomInfo(FILE* file){
    auto it = list_room_available.begin();
    static bool head_line = false;
    if(!head_line)
    {
        fprintf(file,"so phong (Available),trang thai phong (Reserved: 1 , Empty: 0)\n");
        head_line = true;    
    }
    for(;it != list_room_available.end();it++){
        for(auto room : (*it).getRoomAvailable()){
            //first : so phong , second : trang thai phong -> Reserved: 1 , Empty: 0
            fprintf(file,"%d,%d,\n",room.first,room.second);       
        }
    }
}
void File_Handle::SaveServiceInfo(FILE* file){
    auto it = list_service.begin();
    static bool head_line = false;
    if(!head_line){ 
        fprintf(file,"so thu tu dich vu,gia dich vu\n");
        head_line = true;
    }
    for(;it != list_service.end();it++){
        for(auto Service : (*it).getService()){
            fprintf(file,"%d,%d\n",Service.first,Service.second); // first : lua chon dich vu , second : gia dich vu
        }
    }
}
void File_Handle::SaveEmployeeInfo(FILE* file){

    //lambda tìm mật khảu của nhân viên hiện tại dựa trên user_name 
    auto password = [=](const string& phone) -> string {
        for(auto& account : accountList){     //lặp qua từng tài khoản
            if(account.getUsername() == phone){ //kiểm tra sdt có trùng với user_name hay không
               return account.getPassword();
            }
        }
        return "chưa có mật khẩu";
    };
    static bool head_line = false;
    if(!head_line){
        fprintf(file,"ID,ten nhan vien,so dien thoai(user_name),vi tri,ca lam,mat khau\n");
        head_line = true;
    }
    auto it = list_employee.begin();
    for(;it != list_employee.end();it++){
        fprintf(file,"%s,%s,%s,%s,%s,%s,\n",(*it).getId().c_str(),
                                         (*it).getName().c_str(),
                                         (*it).getPhoneNumber().c_str(),
                                         (*it).getPosition().c_str(),
                                         (*it).getWorkshift().c_str(),
                                         password((*it).getPhoneNumber()).c_str()
                                         );
    }
}

                                            /* DOC FILE */
int File_Handle::LogData(const char *path, Storage_dtype infotype)
{
    FILE *file = fopen(path, "r");
    if (file == NULL)
    {
        fclose(file);
        return FAIL;
    }
    char line[100];
    //lambda kiểm tra file có thông tin không 
    auto IsFileEmpty = [=](const char *line)
    {
        //kiểm tra dòng đầu tiên có khoảng trắng không và trả về kết quả tương ứng
        return isspace(static_cast<unsigned char>(*line)) ? FILE_EMPTY : FILE_NOT_EMPTY;
    };
    
    //đọc dòng tiêu đề
    fgets(line,sizeof(line),file);
    
    //đọc từng dòng của file
    while(fgets(line, sizeof(line), file) != NULL)
    {
        switch (infotype)
        {
        case GUESS_CSV:
            LogGuessInfo(line);
            break;
        case ROOM_CSV:
            LogRoomInfo(line);
            break;
        case SERVICE_CSV:
            LogServiceInfo(line);
            break;
        case EMMPLOYEE_CSV:
            LogEmployeeInfo(line);
            break;
        default:
            fclose(file);
            return FAIL;
        }
    }
    fclose(file);

    //trả về kết quả kiểm tra dòng đầu tiên nếu file = NULL 
    int line_status = IsFileEmpty(line);
    if(line_status == FILE_EMPTY)            return FILE_EMPTY;
    else                                     return SUCCESS;
}
void File_Handle::LogGuessInfo(char *line)
{
    char *token = NULL;
    // doc so phong
    token = strtok(line, ",");
    int room_number = atoi(token);

    // doc ten
    token = strtok(NULL, ",");
    string name = token;

    // doc sdt
    token = strtok(NULL, ",");
    string phone = token;

    // doc ngay checkin
    token = strtok(NULL, ",");
    string checkin = token;
    
    token = strtok(NULL,",");
    string checkout = token;
    //cập nhật thông tin khách 
    list_guess.emplace_back(room_number, name, phone, checkin);

    //cập nhật trạng thái phòng đã đặt 
    /* 
        Reserved: đã đặt 
        empty : còn trống
     */
    for(auto& room : list_room_available){
        for(auto& room_ : room.getRoomAvailable()){
            if(room_.first == room_number){
                room.CheckInRoom(room_number); //phương thức để đặt trạng thái phòng là Reserved
                break;
            }
        }
    }

    for(auto& guess : list_guess){
        if(guess.getName() == name){
            guess.setCheckOut(checkout);
            break;
        }
    }
}
void File_Handle::LogRoomInfo(char *line){
    char *token = NULL;
    // doc so phong
    token = strtok(line, ",");
    int number = atoi(token);

    // doc trang thai phong
    token = strtok(NULL, ",");
    int status = atoi(token);
    
    room_available_dtype room; //bién lưu kiểu dữ liệu của phòng 
    
    //cập nhật dữ liệu của phòng bao gồm só phòng và trạng thái 
    room[number] = static_cast<available_roomstatus>(status); 
    
    //lưu vào vector có kiểu dữ liệu của phòng (được thêm bởi manager)
    list_room_available.emplace_back(room);

    //cập nhật trạng thái các phòng trên danh sách mặc định quản lý bởi manager
    /* 
        Unavailable: chưa thêm
        Available : đã thêm
     */
    for(auto& room : list_room_default){
        //duyệt qua từng phòng và trích xuất dữ liệu
        for(auto& room_ : room){
            if(room_.first == number){
                room_.second = Available; //lưu trạng thái trả về cho các phòng đã thêm bởi manager
                break;
            }
        }
    }

}
void File_Handle::LogServiceInfo(char *line){
     char *token = NULL;
    // doc lua chon
    token = strtok(line, ",");
    int option = atoi(token);
    service_option option_service = static_cast<service_option>(option); //chuyen doi sang dang enum 
    
    //doc gia tien
    token = strtok(NULL, ",");
    int price = atoi(token);
    
    list_service.emplace_back(option_service,price);
}
void File_Handle::LogEmployeeInfo(char *line){
    char* token = NULL;

    token = strtok(line,",");
    string id = token;
    
    token = strtok(NULL,",");
    string name = token;
    
    token = strtok(NULL,",");
    string phone = token;

    token = strtok(NULL,",");
    string position = token;

    token = strtok(NULL,",");
    string workshift = token;

    token = strtok(NULL,",");
    string password = token;

    //lambda tìm nhân viên dựa trên sdt và đọc về ca làm việc từ file csv    
    auto LogWorkshift = [phone,workshift](vector<Employee_Info> list_employee,string id){
        EmployeeManager manager;
        for(auto& employee : list_employee){ 
            if(employee.getPhoneNumber() == phone){
                manager.setWorkShift(id,workshift);
            }
        }
    };

    //lưu thông tin của nhân viên cùng với tài khoản
    list_employee.emplace_back(id,name,phone,position);
    accountList.emplace_back(phone,password);

    //gọi lambda để đọc về ca làm việc sau khi đã lưu về thông tin sdt và id của nhân viên
    LogWorkshift(list_employee,id);
}