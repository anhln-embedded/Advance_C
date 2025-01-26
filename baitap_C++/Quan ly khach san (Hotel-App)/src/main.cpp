#include "../inc/manager.hpp"
#include "../inc/employee.hpp"

											/*CÁC HÀM ĐỂ TEST*/
/*
void writeCSV(){
    File_Handle file;

    bool result = file.SaveData(ROOM_CSV_PATH,ROOM_CSV);
    cout << "\nluu danh sach phong ";
    if(result == FAIL) cout << "that bai";
    else cout << "thanh cong";
    cout << endl;

    result = file.SaveData(SERVICE_CSV_PATH,SERVICE_CSV);
    cout << "luu danh sach dich vu ";
    if(result == FAIL) cout << "that bai";
    else cout << "thanh cong";
    cout << endl;

    result = file.SaveData(GUESS_CSV_PATH,GUESS_CSV);
    cout << "luu danh sach khach ";
    if(result == FAIL) cout << "that bai";
    else cout << "thanh cong";
    cout << endl;

   
    result = file.SaveData(EMPLOYEE_CSV_PATH,EMMPLOYEE_CSV);
    cout << "luu danh sach nhan vien ";
    if(result == FAIL) cout << "that bai";
    else cout << "thanh cong";
    cout << endl;


}

void readCSV(){
    File_Handle file;
    cout << "doc danh sach phong ";
    int result = file.LogData(ROOM_CSV_PATH,ROOM_CSV);
    if(result == FILE_EMPTY) cout << "khong co thong tin";
    else if(result == FAIL) cout << "that bai";
    else cout << "thanh cong";
    cout << endl;
    
    cout << "doc danh sach dich vu ";
    result = file.LogData(SERVICE_CSV_PATH,SERVICE_CSV);
    if(result == FILE_EMPTY) cout << "khong co thong tin";
    else if(result == FAIL) cout << "that bai";
    else cout << "thanh cong";
    cout << endl;

    cout << "doc danh sach khach ";
    result = file.LogData(GUESS_CSV_PATH,GUESS_CSV);
    if(result == FILE_EMPTY) cout << "khong co thong tin";
    else if(result == FAIL) cout << "that bai";
    else cout << "thanh cong";
    cout << endl;

    cout << "doc danh sach nhan vien";
    result = file.LogData(EMPLOYEE_CSV_PATH,EMMPLOYEE_CSV);
    if(result == FILE_EMPTY) cout << "khong co thong tin";
    else if(result == FAIL) cout << "that bai";
    else cout << "thanh cong";
    cout << endl;

}

void add_room(){
    RoomManager room;
    int arr[] = {101,102,103,201,202,301,302};
    for(auto& number : arr)
        room.AddRoom(number);
}


void book_room(){
    GuessEmployee guess;
    guess.BookRoom(101, "Duysolo", "0972665812", "12h30-16/1/2022");
    guess.BookRoom(301, "DuyPham", "0972665830", "20h30-16/1/2022");
    guess.BookRoom(201, "DuyKhanh", "0972665890", "3h30-16/1/2022");    
}   


void unbook_room(){
    GuessEmployee guess;
    string checkout = "20h50-22/1/2022";
    guess.UnbookRoom(*guess.GuessInfo("0972665830"),checkout);
    guess.ServiceFeedbackInfo(*guess.GuessInfo("0972665830"));
}

void add_employee(){
    EmployeeManager manageemp;
    manageemp.addEmployee(accountList,"Duypham","0972665872","LT");
    manageemp.addEmployee(accountList,"LeHoang","0972665873","TV");
    manageemp.addEmployee(accountList,"TanTung","0972665874","BV");
    manageemp.addEmployee(accountList,"MinhNhat","0972665852","DB");

    manageemp.setWorkShift("LT001", "2-c");

    manageemp.setWorkShift("TV002", "6-c");

    manageemp.setWorkShift("BV003", "4-c");

    manageemp.setWorkShift("DB004", "5-t");

    
    //manageemp.ShowWorkshiftTable();

    //manageemp.ShowWorkshiftTablebyPhone("0972665874");

}
void add_service(){
    ServiceManager service;
    service.AddService(GYM,122);
    service.AddService(SPA_MASSAGE,231);
    service.AddService(FOOD_ORDER,426);
    service.AddService(CAR_RENT,426);
}

void test(){
    GuessEmployee guess;
    RoomManager room;
    ServiceManager service;
    EmployeeManager Manager;
    cout <<"\t\tDANH SACH PHONG MAC DINH" << endl;
    room.ShowListRoomDefault();
    cout <<"\t\tDANH SACH PHONG DA THEM" << endl;
    guess.ShowListRoomAvailable();
    cout <<"\t\tDANH SACH KHACH DAT PHONG" << endl;
    guess.ShowListGuess();
    cout <<"\t\tDANH SACH DICH VU" << endl;
    service.ShowListService();
    cout <<"\t\tDANH SACH NHAN VIEN" << endl;
    Manager.listEmployees();
    cout <<"\t\tDANH SACH TAI KHOAN NHAN VIEN" << endl;
    Account::showListAccount();
    cout << "\t\tCA LAM VIEC" << endl;
    Manager.ShowWorkshiftTable();
}
*/

int main()
{  
    //khởi tạo và cài đặt các dữ liệu ban đầu bao gồm
    /* 
        1.tài khoản manager 
        2.đọc dữ liệu từ file csv: thông tin danh sách nhân viên, khách, phòng , dịch vụ
        3.khởi tạo mặc định các phòng ở chế độ unavailable 
     */
    Account account;
    Manager manager;
    Employee employee;

    while (1)
    {
        cout << "\n---- Thông tin đăng nhập ----" << endl;
        string account,password;
        cout << "nhập tài khoản (account/sdt): ";
        cin >> account;
        cout << "Nhập mật khẩu: ";
        cin >> password;
        if (Account::login(accountList, account, password)) {
            cout << "Đăng nhập thành công!" << endl;
            // Kiểm tra nếu tài khoản là "admin"
            if(Account::VerifyManagerAccount(password)) {
                cout << "Xin chào Quản lý!" << endl;
                manager.ShowManagerMenu();  // Hiển thị menu quản lý
            }else{
                cout << "Xin chào người dùng!" << endl;
                employee.ShowEmployeeMenu(account);
            }
        } 
        else    
            cout << "Đăng nhập thất bại! Tài khoản hoặc mật khẩu không đúng." << endl;
     }
    return 0;
}