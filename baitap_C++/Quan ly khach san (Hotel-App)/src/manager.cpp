#include "../inc/Manager.hpp"
/* Menu lớn */
Manager::Manager(){
    int read_result = file_manager.LogData(ROOM_CSV_PATH,ROOM_CSV);
    if(read_result == FILE_EMPTY) UI::showMessage("chưa có thông tin danh sách phòng");
    else if(read_result == FAIL)  UI::showMessage("Tải danh sách dịch vụ thất bai");
    else                          UI::showMessage("Tải danh sách phòng thành công");
    read_result = file_manager.LogData(SERVICE_CSV_PATH,SERVICE_CSV);
    if(read_result == FILE_EMPTY) UI::showMessage("chưa có thông tin dịch vụ phòng");
    else if(read_result == FAIL)  UI::showMessage("Tải danh sách dịch vụ thất bại");
    else                          UI::showMessage("Tải danh sách dịch vụ thành công");
    read_result = file_manager.LogData(EMPLOYEE_CSV_PATH,EMMPLOYEE_CSV);
    if(read_result == FILE_EMPTY) UI::showMessage("chưa có thông tin nhân viên");
    else if(read_result == FAIL)  UI::showMessage("Tải danh sách nhân viên thất bai");
    else                          UI::showMessage("Tải danh sách nhân viên thành công");
  
}
void Manager::ShowManagerMenu()
{
    
    Menu mainmenu{"Quan Ly", {{1,"Quản lý nhân viên", [this](){ manageEmployee(); }},
                              {2, "Quản lý phòng", [this](){ manageRoom(); }},
                              {3, "Quản lý dịch vụ", [this](){ manageService(); }},
                              {4, "Lưu trữ thông tin", [this](){ SaveDataCSV(); }},
                              {0, "quay lại", [](){ UI::showMessage("Vui lòng chọn tính năng"); }}}};
    mainmenu.showMenu();
}

void Manager::manageEmployee() {
    Menu employeeMenu("Quản lý nhân viên", {
        {1, "Thêm nhân viên", [this]() { addEmployee(); }},
        {2, "Sửa thông tin nhân viên", [this]() { editEmployee(); }},
        {3, "Xóa nhân viên", [this]() { deleteEmployee(); }},
        {4, "Xem danh sách nhân viên", [this]() { listEmployees(); }},
        {5, "Set ca làm cho nhân viên",[this](){setWorkShift();}},
        {6, "Thời gian làm việc",[this](){TableSchedule();}},
        {0, "Quay lại", []() { UI::showMessage("Quay lại"); }}
    });

    employeeMenu.showMenu();  // Hiển thị menu quản lý nhân viên
}

void Manager::addEmployee() {
   
    while (true) {
        UI::showMessage("=== Thêm Nhân Viên ===");

        user_input:
        // Nhập thông tin từ người dùng
        std::string name = UI::getInputString("Nhập tên nhân viên: ");
        std::string phoneNumber = UI::getInputString("Nhập số điện thoại (ID): ");
        std::string position = UI::getInputString("Nhập vị trí công việc (Tạp vụ/Bảo vệ/Đầu bếp/Lễ Tân): ");

        // Thêm nhân viên mới vào danh sách
        if(employeeManage.addEmployee(accountList, name, phoneNumber, position) == FAIL){
            UI::showMessage("vui lòng nhập lại thông tin: ");
            goto user_input;
        }

        // In ra tên của nhân viên mới
        UI::showMessage("Thêm thành công nhân viên " + name);

        // Tự động đăng ký tài khoản cho nhân viên với mật khẩu mặc định
        UI::showMessage("----------------------------");
        inputvalidchoice:
        UI::showMessage("1.Thêm nhân viên khác");
        UI::showMessage("0.Quay lai");
        // Hiển thị tùy chọn để thêm nhân viên khác
        int choice = UI::getUserChoice("vui lòng chọn tính năng: ");        
        if (choice == 0) {
            system("cls");
            break;  // Quay lại nếu người dùng chọn 0
        }
        else
        {
            if (choice != 1){
                system("cls");
                UI::showMessage("Lua chon khong hop le, vui long nhap lai");
                goto inputvalidchoice;
            }
        }
    }
    
}

void Manager::editEmployee() {
    while(1){
        UI::showMessage("Sửa thông tin nhân viên...");
        // Danh sách nhân viên
        employeeManage.listEmployees();

        //nhập thông tin chỉnh sửa
        UI::showMessage("Vui lòng nhập tên của nhân viên muốn sửa thông tin: ");
        std::string id = UI::getInputString("Nhập ID: ");
        std::string newname = UI::getInputString("Nhập tên mới: ");
        std::string newposition= UI::getInputString("Nhập công việc mới: ");
    
        //thực hiện cập nhật thông tin nhân viên
        employeeManage.editEmployeeById(id,newname,newposition);

        UI::showMessage("1.Tiếp tục sửa thông tin");
        UI::showMessage("0.Quay lại");
        int choice = UI::getUserChoice("nhập lựa chọn: ");
        if(choice == 0){
            system("cls");
            break;
        }
    }
}

void Manager::deleteEmployee() {
    while(1){
        UI::showMessage("Xóa nhân viên...");
        employeeManage.listEmployees();
        UI::showMessage("------------------");
        std::string id = UI::getInputString("Nhập ID của nhân viên muốn xóa: ");
        employeeManage.deleteEmployeeById(id);

        UI::showMessage("0.Quay lại");
        option:
        int choice = UI::getUserChoice("Nhấn 0 để quay lại: ");
        if(choice == 0){
            system("cls");
            break;
        }
        else{
            UI::showMessage("Lua chon khong hop le vui long nhap lai");
            goto option;
        }
            
    }
}

void Manager::listEmployees() {
    while(1){
        UI::showMessage("=== Danh Sách Nhân Viên ===");

        employeeManage.listEmployees();

        UI::showMessage("------------------");
        option:
        int choice = UI::getUserChoice("Quay lai (0): ");
        if(choice == 0){
            system("cls");
            break;
        }
        else{
            UI::showMessage("Lua chon khong hop le vui long nhap lai");
            goto option;
        }
    }
}

void Manager::setWorkShift(){
    UI::showMessage("------------------SET CA LÀM CHO NHÂN VIÊN--------------------");
    while(1){
        employeeManage.listEmployees();
        UI::showMessage("-------------------------");
        setschedule:
        string id = UI::getInputString("Nhập id của nhân viẹn muốn set ca làm: ");
        UI::showMessage(" Vui lòng nhập ca làm việc trong tuần tương ứng với định dạng như sau \n( Thứ - Buổi, Thứ - Buổi, Thứ - Buổi): 2-S, 2-C, 3-C, 4-T, 5-C, 6-S ");
        string workShift = UI::getInputString("Thứ - Buổi:");
        employeeManage.setWorkShift(id,workShift);
        UI::showMessage("-------------------------");
        UI::showMessage("1.Tiếp tục set ca làm việc");
        UI::showMessage("0. Quay lại");
        int choice = UI::getUserChoice("vui lòng chọn tính năng: ");
        if(choice == 0){
            system("cls");
            break;
        }
        goto setschedule;
    }
}

void Manager::TableSchedule(){
    while(1){
    UI::showMessage("-------Thời gian làm việc của nhân viên-------");
       employeeManage.ShowWorkshiftTable();
       int choice = UI::getUserChoice("Chọn 0 để quay lại: ");
       if(choice == 0){
          system("cls");
          break; 
       }
    }

}

                                    /* QUẢN LÝ PHÒNG */
void Manager::manageRoom()
{
    Menu Roommenu{"Quản lý phòng", {{1, "thêm phòng", [this](){ AddRoom(); }},
                                    {2, "xóa phòng", [this](){ DeleteRoom(); }},
                                    {3, "xem trạng thái phong", [this](){ ShowListRoom(); }},
                                    {0, "quay lại", [](){ UI::showMessage("vui lòng chọn tính năng"); }}}};
    Roommenu.showMenu();
}
void Manager::AddRoom()
{
    UI::showMessage("---------THEM PHONG---------");
    while (1)
    {
        inputvalidroom:
        int new_room = UI::getUserChoice("Nhap phong can them:");
        if(roomManage.IsRoomDefaultExist(new_room) == NOT_EXIST){
            UI::showMessage("phong khong ton tai, vui long nhap phong khac");
            goto inputvalidroom;
        }
        if(roomManage.AddRoom(new_room) == FAIL)
        {
            UI::showMessage("phong da duoc them, vui long nhap phong khac");
            goto inputvalidroom;
        }
        
        UI::showMessage("them phong thanh cong");
        inputvalidchoice:
        UI::showMessage("1.tiep tuc them");
        UI::showMessage("0.Quay lai");
        int choice = UI::getUserChoice("Vui long nhap lua chon:");
        UI::showMessage("--------------------------------");
        if (choice == 0){
            system("cls");
            break;
        } 
        else{
            if(choice != 1){
                UI::showMessage("Lua chon khong hop le");
                goto inputvalidchoice;
            }
        }
    }
}
void Manager::ShowListRoom()
{
    UI::showMessage("---------XEM TRANG THAI PHONG---------");
    while (1)
    {
        roomManage.ShowListRoomDefault();
        UI::showMessage("\nU:\tUnavailable");
        UI::showMessage("A:\tAvailable");
        inputvalidchoice:
        UI::showMessage("\n1.Xem thong tin phong");
        UI::showMessage("0.Quay lai");
        int choice = UI::getUserChoice("\nVui long lua chon:");
        if (choice == 0){
            system("cls");
            break;
        }
        else if (choice == 1)
        {
            UI::showMessage("---------XEM THONG TIN PHONG---------");
            inputvalidroom:
            int room = UI::getUserChoice("vui long nhap so phong:");
            if (RoomManager::IsRoomAvailableExist(room) == EXIST)
            {
                if (roomManage.RoomInfo(room) == FAIL)
                {
                    UI::showMessage("Khong co thong tin khach");  
                }
                inputvalidchoice1:
                UI::showMessage("1.tiep tuc xem thong tin cac phong");
                UI::showMessage("0.Quay lai");
                int choice = UI::getUserChoice("\nvui long nhap lua chon:");
                if (choice == 0){
                    system("cls");
                    break;
                }
                else if(choice == 1){
                    system("cls");
                    goto inputvalidroom;
                }
                else{
                    system("cls");
                    UI::showMessage("Lua chon khong hop le");
                    goto inputvalidchoice1;
                }
            }
            else
            {
                system("cls");
                UI::showMessage("Phong khong co san");
                goto inputvalidchoice1;
            }
        }
        else
        {
            system("cls");
            UI::showMessage("Lua chon khong hop le, vui long nhap lai");
            goto inputvalidchoice;
        }
    }
}
void Manager::DeleteRoom()
{
    UI::showMessage("---------XOA PHONG---------");
    while (1)
    {
        roomManage.ShowListRoomDefault();
        int room_delete = UI::getUserChoice("Nhap phong can xoa:");
        roomManage.deleteRoom(room_delete);
        UI::showMessage("\n1.tiep tuc xoa");
        UI::showMessage("0.Quay lai");
        inputvalidchoice:
        int choice = UI::getUserChoice("Vui long nhap lua chon:");
        if (choice == 0){
            system("cls");
            break;
        }
        else
        {
            if (choice != 1){
                system("cls");
                UI::showMessage("Lua chon khong hop le, vui long nhap lai");
                goto inputvalidchoice;
            }
        }
    }
}
                                           /* QUẢN LÝ DỊCH VỤ */
void Manager::manageService()
{
    //doc danh sach dich vu tu file csv

    Menu Roommenu{"Dich vu", {{1, "them dich vu", [this](){ AddService(); }},
                              {2, "xoa dich vu", [this](){ DeleteService(); }},
                              {3, "danh sach dich vu", [this](){ ShowListService(); }},
                              {0, "quay lai", [](){ UI::showMessage("vui long chon tinh nang"); }}}};
    Roommenu.showMenu();
}
void Manager::AddService()
{
    UI::showMessage("---------THEM DICH VU---------");
    while (1)
    {
        UI::showMessage("Dich vu co san");
        UI::showMessage("----------------------------");
        UI::showMessage("1.phong gym\n2.to chuc sinh nhat\n3.cho thue xe\n4.cham soc thu cung\n5.dat do an\n6.spa va massage");
        UI::showMessage("----------------------------");
        InputValidService:
        int service_number = UI::getUserChoice("Nhap so thu tu cua dich vu can them:");
        
        //kiem tra dich vu co hop le khong
        auto IsServiceInputValid = [service_number]()
        {
            return (service_number < TOTAL_SERVICE) ? true : false;
        };

        if (!IsServiceInputValid())
        {
            UI::showMessage("vui long nhap lua chon hop le");
            goto InputValidService;
        }

        int price = UI::getUserChoiceFloat("Nhap gia dich vu VND:");

        if(serviceManage.AddService(service_number, price) == FAIL)
        {
            UI::showMessage("dich vu da co san, vui long chon dich vu khac");
        }
        else UI::showMessage("\nThem dich vu thanh cong");
        UI::showMessage("1.Tiep tuc them dich vu");
        UI::showMessage("0.Quay lai");
        inputvalidchoice:
        int choice = UI::getUserChoice("Vui long nhap lua chon:");
        UI::showMessage("--------------------------------");
        if (choice == 0){
            system("cls");
            break;
        }
        else
        {
            if (choice != 1){
                system("cls");
                UI::showMessage("Lua chon khong hop le, vui long nhap lai");
                goto inputvalidchoice;
            }
        }
        system("cls");
    }
}
void Manager::DeleteService()
{
    UI::showMessage("---------XOA DICH VU---------");
    while (1)
    {

        int service_number = UI::getUserChoice("Vui long nhap so thu tu cua dich vu can xoa:");
        if (serviceManage.deleteService(service_number) == FAIL)
        {
            UI::showMessage("Khong co dich can xoa");
        }
        else UI::showMessage("\nXoa dich vu thanh cong");
        UI::showMessage("1.Tiep tuc xoa dich vu");
        UI::showMessage("0.Quay lai");
        inputvalidchoice:
        int choice = UI::getUserChoice("Vui long nhap lua chon:");
        if (choice == 0){
            system("cls");
            break;
        }
        else
        {
            if (choice != 1){
                system("cls");
                UI::showMessage("Lua chon khong hop le, vui long nhap lai");
                goto inputvalidchoice;
            }
        }
    }
}
void Manager::ShowListService()
{
    UI::showMessage("---------DANH SACH DICH VU---------");
    while (1)
    {
        if (serviceManage.ShowListService() == FAIL)
        {
            UI::showMessage("Khong co san dich vu");
        }
        UI::showMessage("0.Quay lai");
        inputvalidchoice:
        int choice = UI::getUserChoice("Vui long nhap lua chon:");
        if (choice == 0){
            system("cls");
            break;
        }
        else
        {
            if (choice != 1){
                system("cls");
                UI::showMessage("Lua chon khong hop le, vui long nhap lai");
                goto inputvalidchoice;
            }
        }
    }
}

void Manager::SaveDataCSV(){
    UI::showMessage("---------LUU TRU THONG TIN----------");
    while(1){
        intputvalidchoice:
        UI::showMessage("1.luu tru danh sach phong");
        UI::showMessage("2.luu tru danh sach dich vu");
        UI::showMessage("3.Luu tru danh sach thong tin nhan vien");
        int choice = UI::getUserChoice("Vui long nhap lua chon:");
        bool save_result;
        if(choice == 1) {
            save_result = file_manager.SaveData(ROOM_CSV_PATH,ROOM_CSV);
            if(save_result == SUCCESS)  UI::showMessage("luu tru thanh cong");
            else UI::showMessage("khong co thong tin");
        }
        else if(choice == 2) {
            save_result = file_manager.SaveData(SERVICE_CSV_PATH,SERVICE_CSV);
            if(save_result == SUCCESS) UI::showMessage("luu tru thanh cong");
            else UI::showMessage("khong co thong tin");
        }
        else if(choice == 3){
            save_result = file_manager.SaveData(EMPLOYEE_CSV_PATH,EMMPLOYEE_CSV);
            if(save_result == SUCCESS) UI::showMessage("luu tru thanh cong");
            else UI::showMessage("khong co thong tin");
        }
        else{
            system("cls");
            UI::showMessage("lựa chọn không hợp lệ, vui lòng nhập lại");
            goto intputvalidchoice;
        }
        UI::showMessage("1.tiếp tục lưu trữ:");
        UI::showMessage("0.Quay lại");
        choice = UI::getUserChoice("Vui lòng nhập lựa chọn: ");
        if(choice == 0){
            system("cls");
            break;
        }
        goto intputvalidchoice;
    }

}
