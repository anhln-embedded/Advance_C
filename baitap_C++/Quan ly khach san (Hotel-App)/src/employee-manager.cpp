#include "../inc/employee-manager.hpp"
vector<Employee_Info> list_employee;

// Tạo ID tự động cho nhân viên mới
bool EmployeeManager::setWorkshiftfromString(Employee_Info &employee, const string &workshift)
{
    employee.setWorkShift(workshift);
    auto parseSession = [](char session)
    {
        switch (toupper(session))
        {
        case 'S':
            return morning;
        case 'C':
            return afternoon; // Chiều
        case 'T':
            return evening; // Tối
        default:
            return none; // Không hợp lệ
        }
    };
    auto parseDay = [](char day)
    {
        switch (day)
        {
        case '2':
            return Mon; // Thứ 2
        case '3':
            return Tue; // Thứ 3
        case '4':
            return Wed; // Thứ 4
        case '5':
            return Thu; // Thứ 5
        case '6':
            return Fri; // Thứ 6
        default:
            return totalday; // Không hợp lệ
        };
    };
    
    // kiẻm tra định dạng có hợp lệ
    if (workshift.size() != 3 || workshift[1] != '-') // Định dạng phải là "2-C"
    {
        return FAIL;
    }

    // Parse ngày và ca làm từ chuỗi
    dayinWeek day = parseDay(workshift[0]);
    session sess = parseSession(workshift[2]);

    // Kiểm tra giá trị hợp lệ
    if (day == totalday || sess == none)
    {
        return FAIL;
    }

    // Thêm ca làm vào lịch trình
    employee.setSchedule(day, sess);
    return SUCCESS;
}

void printSchedule(const Employee_Info& employee)
{
    vector<string> list_session = {"X", "Sáng", "Chiều", "Tối"};
    // In dữ liệu của từng nhân viên và căn lề
    cout << setw(17) << left << employee.getName();
    cout << " | ";

    // in ra lần lượt các ca làm giống nhau của các ngày trong tuần trên cùng 1 hàng
    bool new_line = false;
    for (int shift = morning; shift <= evening; ++shift)
    {
        // xử lý căn lề bát đầu từ các dòng kế tiếp
        if (new_line)
        {
            cout << setw(17) << left << " ";
            //cout << " |";
            cout << " | ";
            new_line = false;
        }

        // Lặp qua từng ngày để in ra tất cả ca làm giống nhau
        for (int day = Mon; day < totalday; ++day)
        {
            // Tìm kiếm ngày trong ca làm của nhân viên 
            auto it = employee.getSchedule().find(static_cast<dayinWeek>(day));
            // Lặp qua từng
            if (it != employee.getSchedule().end() &&
            // Tìm và trả về ca làm tương ứng với ngày hiện tại
            find(it->second.begin(), it->second.end(), static_cast<session>(shift)) != it->second.end())
            {
                cout << list_session[shift] << "      | ";
            }
            else
            {
                cout << "X         | ";
            }
        }
        new_line = true;
        cout << endl;
    }
   UI::showMessage("---------------------------------------------------------------------------");
}

string EmployeeManager::generateEmployeeId(const string &position)
{
    employeeCounter_++;
    stringstream ss; // được sử dụng để xây dựng mã với nhiều thành phần (text, số, định dạng)

    // Tạo tiền tố ID theo chức vụ
    if (position == "TV")
    {
        ss << "TV";
        position == "Tạp Vụ";
    }
    else if (position == "BV")
    {
        ss << "BV";
        position == "Bảo Vệ";
    }
    else if (position == "DB")
    {
        ss << "DB";
        position == "Đầu Bếp";
    }
    else if (position == "LT")
    {
        ss << "LT";
        position == "Lễ Tân";
    }
    else
    {
        ss << "NV"; // Mặc định nếu không có chức vụ đặc biệt
        position == "Nhân Viên";
    }

    // Tạo số thứ tự cho ID và đảm bảo có 3 chữ số
    /*
    Mô tả hàm:
    sử dụng thư viện iomanip để để đảm bảo số thứ tự có độ dài chính xác là
    3 ký tự, thêm các chữ số 0 ở bên trái
     */
    ss << setw(3) << setfill('0') << employeeCounter_;

    return ss.str();
}
// Thêm nhân viên mới với ID tự động và tự động đăng ký tài khoản
bool EmployeeManager::addEmployee(vector<Account> &accountList, const string &name, const string &phoneNumber, const string &position)
{
    // Kiểm tra nếu số điện thoại đã tồn tại trong hệ thống tài khoản
    if (Account::accountExists(accountList, phoneNumber))
    {
        UI::showMessage("Số điện thoại này đã được đăng ký.");
        return FAIL;
    }

    // Tạo ID tự động cho nhân viên mới
    string id = generateEmployeeId(position);

    // Thêm nhân viên mới vào danh sách
    list_employee.emplace_back(id, name, phoneNumber, position);
    UI::showMessage("Nhân viên " + name + " với ID " + id + " đã được thêm thành công.");

    // lambda tạo mật khẫu ngẫu nhiên với 6 chữ số
    auto generateRandompassword = [=]()
    {
        string pass = "";
        for (int i = 0; i < 6; i++)
        {
            int index = rand() % 10;
            pass += to_string(index);
        }
        return pass;
    };

    // Tự động đăng ký tài khoản cho nhân viên
    Account::registerAccount(accountList, phoneNumber, generateRandompassword());
    UI::showMessage("Tài khoản cho nhân viên đã được đăng ký với mật khẩu mặc định " + generateRandompassword());
    return SUCCESS;
}

// Sửa thông tin nhân viên dựa trên Id
void EmployeeManager::editEmployeeById(const string &id, const string &newName, string &newPosition)
{
    // trỏ đến địa chỉ của id nhân viên hiện tại để thay đổi
    Employee_Info *employee = findEmployeeById(id);
    if (employee)
    {
        if (newPosition == "BV")
            newPosition = "Bảo Vệ";
        else if (newPosition == "LT")
            newPosition = "Lễ Tân";
        else if (newPosition == "DB")
            newPosition = "Đâu Bếp";
        else if (newPosition == "TV")
            newPosition = "Tạp Vụ";
        else
            newPosition = "Nhân Viên";
        employee->setName(newName);
        employee->setPosition(newPosition);
        UI::showMessage("Thông tin nhân viên đã được cập nhật.");
    }
    else
    {
        UI::showMessage("Không tìm thấy nhân viên với tên này.");
    }
}

// Tìm nhân viên theo id
Employee_Info *EmployeeManager::findEmployeeById(const string &id)
{
    for (auto &employee : list_employee)
    {
        if (employee.getId() == id)
        {
            return &employee;
        }
    }
    return nullptr;
}

// chỉnh sửa mật khẩu bởi nhân viên
bool EmployeeManager::editEmployeePassword(vector<Account> &accountList, const string &user_name, const string &old_pass, const string &new_pass)
{
    // đảm bảo mật khẩu mới hợp lệ
    if (new_pass.length() != 6)
        return FAIL;
    for (auto &account : accountList)
    {
        if (account.getPassword() == old_pass && account.getUsername() == user_name)
        {
            account.setPassword(new_pass);
            return SUCCESS;
        }
    }
    return FAIL;
}

// Xóa nhân viên dựa trên ID
void EmployeeManager::deleteEmployeeById(const string &id)
{
    // duyệt lần lượt các employee và nếu gặp employee cần xóa
    // lambda sử dụng ID để quyết định emp cần xòa

    auto it = remove_if(list_employee.begin(), list_employee.end(), [&id](const Employee_Info &emp)
                        { return emp.getId() == id; });
    // biến it lưu trữ id của emp cần xóa
    if (it != list_employee.end())
    {
        list_employee.erase(it, list_employee.end());
        UI::showMessage("Nhân viên với ID " + id + " đã được xóa.");
    }
    else
    {
        UI::showMessage("Không tìm thấy nhân viên với ID này.");
    }
}

// Đặt ca làm việc cho nhân viên
void EmployeeManager::setWorkShift(const string &id, const string &shift)
{

    Employee_Info *employee = findEmployeeById(id);
    if (employee == nullptr)
    {
        UI::showMessage("Không tìm thấy nhân viên với ID: " + id);
        return;
    }

    if(setWorkshiftfromString(*employee, shift))
    {
        UI::showMessage("Ca làm việc của nhân viên " + employee->getName() + " đã được cập nhật thành công thành: " + shift);
    }
    else{
         cout << "chuỗi sai định dạng hoặc không hợp lệ" << endl;
    }
}

// Xem danh sách thông tin của tất cả nhân viên
void EmployeeManager::listEmployees() const
{
    if (list_employee.empty())
    {
        UI::showMessage("Không có nhân viên nào.");
    }
    else
    {
        cout << left << setw(10) <<  "ID" << setw(15) << "Tên" << setw(25) << "Số điện thoại" << setw(15) << "Chức vụ" <<  setw(15) << "Ca làm" << endl;
        cout << setfill('-') << setw(70) << "-" << endl;
        // Reset fill về mặc định (space)
        cout << setfill(' ');

        for (const auto &employee : list_employee)
        {
             cout << left << setw(10) <<  employee.getId() 
                          << setw(15) << employee.getName()  
                          << setw(17) << employee.getPhoneNumber() 
                          << setw(12) <<  employee.getPosition()
                          << setw(10) << employee.getWorkshift()  
                          << endl;
        }
    }
}

// xem ca làm của tất cả nhân viên
void EmployeeManager::ShowWorkshiftTable() const
{
    if (list_employee.empty())
    {
        UI::showMessage("Chưa có nhân viên");
    }
    else
    {
        vector<string> list_day = {"T2", "T3", "T4", "T5", "T6"};
        cout << "Tên nhân viên     | ";
        for (size_t i = 0; i < list_day.size(); ++i)
        {
            cout << list_day[i] << "        | ";
        }
        cout << endl;
        for(auto& employee : list_employee){
            printSchedule(employee);
        }
    }
}

// xem ca làm của nhân viên dựa trên sdt
void EmployeeManager::ShowWorkshiftTablebyPhone(const string& user_name){
    vector<string> list_day = {"T2", "T3", "T4", "T5", "T6"};
    cout << "Tên nhân viên     | ";
    for (size_t i = 0; i < list_day.size(); ++i)
    {
        cout << list_day[i] << "        | ";
    }
    cout << endl;
    for(auto& employee : list_employee){
        if(employee.getPhoneNumber() == user_name){
            printSchedule(employee);
        }
    }
}