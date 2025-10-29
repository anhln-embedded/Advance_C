#include "../inc/guess-employee.hpp"
vector<Guess> list_guess;
vector<string> Negative_content = {"Cần cải thiện tốc độ xử lý thanh toán.",
                                    "Dịch vụ tạm ổn, không có gì đặc biệt.",
                                    "Phải chờ đợi quá lâu mới được phục vụ.",
                                    };
vector<string> Positve_content = {"Nhân viên rất thân thiện.",
                                  "Nhà tắm sạch sẽ, ngăn náp.",
                                  "Bữa ăn được phục vụ đa dạng, nhiều món."};
Guess* GuessEmployee::findRoombyPhone(const string& phone){
    for(auto& guess : list_guess){    //duyet qua tung khach trong danh sach
        if(guess.getPhone() == phone) //kiem tra sdt can tim co trung voi khach hien tai khong
            return &guess;            //tra ve thong tin cua khach 
    }
    return NULL;
}
feedback_dtype GuessEmployee :: GenerateRandomFeedback(){
    srand(time(0));
    feedback_selection type = static_cast<feedback_selection>(rand() % TOTAL_FEEDBACK); //chon ngau nhien Negative/Positive feedback 
    int content = rand() % 3;   //chọn ngẫu nhiên các số từ 0 - 2 để truy xuất mô tả feedback tương ứng trong vector 
    feedback_dtype feedback_result;
    switch(type){
        case POSITIVE:
            feedback_result[POSITIVE] = Positve_content[content];
            break;
        case NEGATIVE:
            feedback_result[NEGATIVE] = Negative_content[content];
            break;
        case NONE_FEEDBACK:
            feedback_result[NONE_FEEDBACK] = "khong co y kien";
        default:
            break;
    }
    return feedback_result; 
}
string GuessEmployee:: GenerateRandomService(){
    srand(time(0));
    service_option number  = static_cast<service_option>(rand() % TOTAL_SERVICE);
    return service_description[number]; //tra ve mo ta dich vu tuong ung
}
void GuessEmployee::EraseGuessInfo(const int& room){
    int count = 0;
    //duyệt qua từng khách trong danh sách
    for(auto& guess : list_guess){
        //nếu phòng muốn kiểm tra trùng với dữ liệu của khách thì xóa thông tin của khách khỏi danh sách
        if(guess.getRoom() == room){
                list_guess.erase(list_guess.begin() + count);
                break;
        }
        count++;
    }
}
void GuessEmployee::ServiceFeedbackInfo(const Guess& guess){

    //lambda để tạo số ngẫu nhiên cho số lượng sử dụng dịch vụ
    auto GenerateRandomnumber = [](){
        srand(time(0));
        int total = 0;
        while(total == 0){
          total = rand() % 10;
        };
        return total;
    };
    //lambda để tách chuỗi và tính ra số ngày ở khách sạn
    auto totalday = [](const string& checkin,const string& checkout){
        int start_day = 0,end_day = 0;
        int i = 0; 
        while(checkin[i - 3] != '-'){
            if(checkin[i - 1] == '-' || checkin[i - 2] == '-'){
                start_day*= 10;                 //xử lý trường hợp khi giá trị cần chuyển đổi từ giá trị chục trở lên
                char index = checkin[i] - '0';  //chuyển đổi ký tự số sang dạng integer
                start_day+=index;               //cập nhật giá trị chuyển đổi 
            }
            i++;
        }
        i = 0;
        while(checkout[i - 3] != '-'){
            if(checkout[i - 1] == '-' || checkout[i - 2] == '-'){
                end_day*= 10;
                char index = checkout[i] - '0';
                end_day+=index;
            }
            i++;
        }
        return end_day - start_day;
    };

    //lambda để lấy giá dịch vụ
    auto getPrice = [guess](){
         for(auto& service : list_service){
            for(auto& service_ : service.getService()){
                if(service_.first == GYM && (guess.getService()) == service_description[1]) return service_.second;
                else if(service_.first == BIRTHDAY_PARTY && (guess.getService()) == service_description[2]) return service_.second;
                else if(service_.first == CAR_RENT && (guess.getService()) == service_description[3]) return service_.second;
                else if(service_.first == PET_CARE && (guess.getService()) == service_description[4]) return service_.second;
                else if(service_.first == FOOD_ORDER && (guess.getService()) == service_description[5]) return service_.second;
                else if(service_.first == SPA_MASSAGE && (guess.getService()) == service_description[6]) return service_.second;
                else return service_.second;
            }
        }
        return 0;
    };

    int price = getPrice();
    int quantity = GenerateRandomnumber();
    int raw_cost = price * quantity;
    int final_cost = ((raw_cost * 0.1) + raw_cost);
    int day_count =  totalday(guess.getCheckin(),guess.getCheckout());
    auto service_description = [guess](){
        for(auto feedback : guess.getFeedback()){
            return feedback.second;
        }
        return string("không sử dụng dịch vụ");
    };

    UI::showMessage("dịch vụ sử dụng");
    UI::showMessage("Tên\t\t\tĐơn giá\t\t\tsố lượng");
    UI::showMessage(guess.getService() + "\t\t|" + to_string(price) + "\t\t\t|" +  to_string(quantity));
    UI::showMessage("Thời gian ở: " + to_string(day_count));
    UI::showMessage("Tổng chi phí dịch vụ: " + to_string(raw_cost) + " $");
    UI::showMessage("Thuế VAT: 10%");
    UI::showMessage("feedback: " + service_description());    
    UI::showMessage("Thành tiền: " + to_string(final_cost) + " $");
}
Guess* GuessEmployee::GuessInfo(const string& phone){
    Guess* guess = findRoombyPhone(phone);
    if(guess != NULL){
        UI::showMessage("Thong tin khach");
        UI::showMessage("ten: " + guess->getName());
        UI::showMessage("sdt: " + guess->getPhone());
        UI::showMessage("phong o: " + to_string(guess->getRoom()));
        UI::showMessage("thoi gian checkIn: " + guess->getCheckin());
        guess->setFeedback(GenerateRandomFeedback()); // mo phong tra ve feedback cua khach
        guess->setService(GenerateRandomService());   // mo phong tra ve dich vu da su dung cua khach
        return guess;
    }
    return NULL;
}
bool GuessEmployee::BookRoom(const int& room_book,const string& name,const string& phone,const string& checkin){
    //duyệt qua từng phòng đã thêm bởi manager
    for(auto& room : list_room_available){

        //trích xuất dữ liệu của phòng hiện tại
        for(auto& room_avaliable : room.getRoomAvailable()){

            //nếu tìm thấy phòng nhưng đã đặt thì trả về thông báo
            if(room_avaliable.first == room_book && room_avaliable.second == Reserved){ 
                goto ERROR; //tra ve ket qua neu phong da co nguoi dat
            }

            //nếu tìm thấy phòng nhưng chưa đặt thì đặt phòng và trả về thông báo
            else if(room_avaliable.first == room_book && room_avaliable.second == Empty){

                //kiểm tra phòng muốn đặt đã có khách thuê trước đó chưa, nếu có thì xóa thông tin khách cũ
                EraseGuessInfo(room_book);

                //thêm thông tin khách mới
                list_guess.emplace_back(room_book,name,phone,checkin); //truyền trực tiếp danh sách đối số mà không cần khởi tạo object thông qua cơ chế emplace_back

                //cập nhật trạng thái phòng -> đặt phòng
                room.CheckInRoom(room_book);
                
                return SUCCESS; //tra ve ket qua neu dat phong thanh cong
            }    
        }
    }
    ERROR:
        return FAIL;
}
void GuessEmployee::UnbookRoom(Guess& guess,string& checkout){
    //cài đặt ngày trả phòng
    guess.setCheckOut(checkout);
    //duyệt qua từng phòng đã thêm bởi manager
    for(auto& room : list_room_available){
        //trích xuất dữ liệu của phòng hiện tại
        for(auto& room_ : room.getRoomAvailable()){
            if(room_.first == guess.getRoom()){ // xử lú nếu tìm thấy phòng cần trả trong danh sách 
                //cập nhật trạng thái phòng -> trả phòng
                room.CheckOutRoom(guess.getRoom());
            }
        } 
    }
}
bool GuessEmployee::ShowListGuess(){
    if(list_guess.empty()){
        return FAIL;
    }
    for(auto& guess : list_guess){
        UI::showMessage("So phong: " + to_string(guess.getRoom()) + 
                        ",ten: " + guess.getName() + 
                        ",phong: " + guess.getPhone() + 
                        ",checkin: " + guess.getCheckin() + 
                        ",checkout: " + guess.getCheckout());
    }
    return SUCCESS;
}

bool GuessEmployee::ShowListRoomAvailable(){
    //kiểm tra danh sách phòng được thêm bởi manager có rỗng hay không
    if(list_room_available.empty()){
        return FAIL;
    }

    int floor = 1;

    //lambda trả về kết quả chuyển đổi sang ký tự tương ứng trạng thái phòng hiện tại
    auto status = [](available_roomstatus st){
                    return st == Reserved ? 'X' : 'O';};

    //lambda trả về kết quả phòng cuối cùng
    auto final_room = [=](){auto it = list_room_available.back();
                    for(auto value : it.getRoomAvailable()){
                        return value.first;
                    }
                    return 0;
    };
    
    //in ra tầng đầu tiên
    UI::showMessage("floor " + to_string(floor));

    //duyệt qua từng phòng 
    for(size_t i = 0 ; i < list_room_available.size() ; i++){
        bool update_floor = false;
        room_number current = 0,next = 0;   //lưa số phòng hiện tại và kế tiếp 
        available_roomstatus st;             //trạng thái của phòng 
       
        //trích xuất ra số thứ tự và trạng thái của phòng hiện tại 
        for(auto& room_available : list_room_available[i].getRoomAvailable()){
            current =  room_available.first;
            st = room_available.second;
        }

        //trích xuất dữ liệu phòng tiếp theo cho đến khi gặp phòng cuối cùng
        if(current != final_room()){
            for(auto& room_available : list_room_available[i+1].getRoomAvailable())
                next =  room_available.first;
        }
        if((next - current) > 5){
            UI::showMessage("\t" + to_string(current) + "(" + status(st) + ")");   // in ra tâng phòng cuối của tầng hiện tại
            UI::showMessage("\nfloor " + to_string(++floor));    
            update_floor = true;    
        }
        //in ra số thứ tự và trạng thái của các phòng trên 1 tầng
        if(!update_floor || current == final_room())
            cout << "\t" << to_string(current) << "(" << status(st) << ")" << "\t";
    }
    cout << endl;
    return SUCCESS;
}

