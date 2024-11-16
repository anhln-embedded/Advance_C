class: 
+ thư viện: <iostream>,using namespace std, <string>
+ định nghĩa các kiểu dữ liệu phức tạp hơn struct và union 
+ chứa hàm 
+ có định nghĩa phạm vi truy cập 
+ biến: properties
+ hàm: method
+ biến kiểu class: object
ví dụ: 
1. về các hàm nhập/xuất và truy cập hàm/biến
+ gọi properties trong method 
+ gọi properties ở bên ngoài class -> cú pháp ten_class :: property
2. Các phương pháp khởi tạo giá trị class
cách 1: tạo object class -> truy cập properties thông qua object để gán
- Hàm tạo: tên trùng với class, sẽ tự động chạy khi khởi tạo 1 object class 
cách 2: ko có tham số: properties có thể được khởi tạo bên trong constructor 
cách 3: có tham số: khi khởi tạo object -> truyền đối số vào 
cách 4: truyền tham số trực tiếp cho hàm tạo bên trong class
+ gọi method trong constructor -> khi tạo class object -> các method cũng sẽ được chạy tự động 
- Hàm hủy (deconstructor): cùng tên hàm tạo có dấu ~ -> giải phóng object bên trong class theo cơ chế LIFO 
3. biến và hàm static trong class 
- static property có thể được dùng bởi các class object khác nhau 
-> ứng dụng trong chia sẻ dữ liệu của cảm biến giữa các luồng khác nhau
- static method có thể được truy cập trực tiếp từ tên class thông qua toán tữ phạm vi ::
