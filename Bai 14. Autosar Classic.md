# AUTOSAR CLASSIC (AUTomotive Open System ARchitecture)
# 1. Khái niệm
Đây là 1 kiến trúc phân lớp cung cấp  các APIs tiêu chuẩn được sử dụng để phát triển phần mềm trong lĩnh vực ô tô. Với mục tiêu là để đơn giản hóa và thống nhất về 1 quy tắc chung để phát triển phần mềm có thể áp dụng cho bất kỳ hệ thống điện tử __(ECU)__, cũng như là tăng khả năng tái sử dụng mã nguồn,tối ưu chi phí, thời gian phát triển. 
# 2. Tại sao nó cần thiết 
+ Như ta đã biết trong lĩnh vực embedded nói chung thì việc phát triển 1 phần mềm luôn phụ thuộc vào phần cứng. Chính vì vậy code phát triển cho 1 MCU nào đó có thể sẽ không thể sử dụng cho 1 MCU khác. 
+ Đối với lĩnh vực automotive cũng vậy, khi trong 1 chiếc xe ta có thể sử dụng các bộ điều khiển điện tử __(ECU)__ khác nhau, để thực hiện 1 chức năng cụ thể. Với mỗi __ECU__ cũng sẽ sữ dụng các __MCU__ khác nhau để đảm bảo tính tương thích cũng như tối ưu về hiệu suất 
=> Điều đó dẫn đến việc ta sẽ phải phát triển phần mềm cho các ECU khác nhau -> tăng độ phức tạp, cũng như không thể tái sử dụng khi phát triển cho 1 hệ thống mới -> tốn thời gian, tăng chi phí 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/a064bb87-b189-4ae5-b4b0-d9ccb66b72b2" width = "600" height = "300">

Chính vì thể Autosar ra đời để giải quyết vấn đề trên, khi nó cung cấp những Interface tiêu chuẩn để ta phát triển phần mềm mà không cần phải quan tâm đến sự khác biệt về phần cứng. với các ưu điểm như:
+ Dễ bảo trì mã nguồn, dễ tìm kiếm và chữa lỗi nhanh chóng 
+ tối ưu thời gian,chi phí phát triển
+ Khả năng tái sử dụng cho các dự án mới
+ Dễ dàng thích ứng với sự thay đổi phần cứng
+ Tính độc lập giữa phần mềm với nhau cũng như với phần cứng 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/bf6a4b52-b55d-44af-81ce-40c61e1638dc" width = "350" height = "200">

# 3. So sánh với Non Autosar software
Ta sẽ có 1 ví dụ sau đây để chỉ ra sự khác biệt giữa 1 phần mềm viết theo cách thông thường khác tiêu chuẩn Autosar sẽ ảnh hưởng như thế nào 

__Ví dụ:__  Ta sẽ dùng 1 MCU  đọc dữ liệu từ cảm biến, và sử dụng bộ ADC để chuyển đổi sang giá trị nhiệt độ, sau đó sẽ thực hiện tắt/mở quạt làm mát tương ứng với các mức nhiệt độ.

<p align = "center">
<img src = "https://github.com/user-attachments/assets/13f02570-0548-4019-9d3f-da66b63ce347" width = "500" height = "400">

+ Ta có thể thấy rõ khi thay đổi MCU thì phần mềm cũng thay đổi theo -> dẫn đến sự kém linh hoạt trong việc thích ứng với sự thay đỏi phần cứng -> phải tốn thời gian sửa đổi hoặc viết lại phần mềm

<p align = "center">
<img src = "https://github.com/user-attachments/assets/e23b9745-6d85-48b9-afa3-cf95464c50d4" width = "700" height = "400">

+ Tóm lại ta đúc kết được sự khác biệt như sau

<p align = "center">
<img src ="https://github.com/user-attachments/assets/e34c7653-d8b3-406d-89cc-4e8f36480220" width ="500" height = "200">

# 4. Kiến trúc 

<p align = "center">
<img src ="https://github.com/user-attachments/assets/14775d5e-2bc4-4f6c-8b08-02c3a3719ada" width ="600" height = "400">

Kiến trúc Autosar sẽ được chia làm 3 lớp lần lượt là

__+ ASW__ : đây là tâng để chúng ta phát triển các chức năng ứng dụng thực tế cho xe, sử dụng các API hoàn toàn tách biệt với các tầng phía dưới. Các chức năng s4 được phát triển dựa trên các __SWC__(software component).

__+ RTE__: Đây là lớp trung gian để giao tiếp giữa __ASW__ và các tầng bên dưới, ngoài ra nó còn thực hiện việc giao tiếp, trao đổi dữ liệu giữa các __SWC__

__+ BSW__: Đây là lớp phát triển các phần cơ bản dựa trên phần cứng __MCU__, Nó cũng được chia ra các tầng khác nhau bên trong 

__+ Service layer:__ cung cấp các API để quản lý luồng thực thi của các __SWC__, cũng như quản lý lỗi,trạng thái của hệ thống

__+ ECUAbstraction layer:__ cung cấp các API để giao tiếp giữa __ECU__ và __SWC__ 

__+ MCAL:__ Cung cấp các API để cấu hình các chân I/O, driver của ngoại vi trên MCU

__+ CDD:__ Cho phép truy cập trực tiếp từ __ASW__ vào __MCAL__ mà không thông qua các lớp trung gian
