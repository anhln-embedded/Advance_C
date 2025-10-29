# AUTOSAR CLASSIC (AUTomotive Open System ARchitecture)
# 1. Tổng quát

## 1.1 Vấn đề và giải pháp đối với cách triển khai thông thường dự án phần mềm 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/d20a1da5-31c6-45c7-8296-75d90259a6f2" width = "600" height = "300">

+ Đối với các chương trình đon giản, các task thường được triển khai trong 1 mã nguồn duy nhất và chạy tuyến tính với nhau. Thích hợp cho các dự án nhỏ
+ Ở các dự án lớn, cách làm trên không còn thích hợp do yêu cầu về 
  
  => Nhiều tính năng chạy đồng thời trên 1 hệ điều hành thời gian thực (OS)

  => Cần tối ưu về mặt tài nguyên, ổn định,xử lý chính xác của hệ thống

  => Tiêu chuẩn chung để triển khai trong 1 nhóm lớn

+ Đối với các hệ thống lớn,phức tạp cần có 1 OS để quản lý việc thực hiện nhiều tính năng song song với nhau để đảm bảo hệ thông hoạt động 1 cách trơn tru và phản hồi với ảnh hưởng từ môi trường bên ngoài 1 cách nhanh chóng và ổn định nhất 

## 1.2 Các thành phần chạy trên Os

<p align = "Center">
<img src ="https://github.com/user-attachments/assets/d52ffc8e-71c5-41b2-9803-74781ed94201" width = "600" height = "300">

+ Các task chạy trên 1 hệ điều hành sẽ phân chia thời gian thực hiện theo mức độ ưu tiên và tầm quan trọng, đây chính là những tính năng thực tế mà người kỹ sư sẽ lập trình để hệ thống tương tác với môi trường bên ngoài.

## 1.2 Sơ lược về Autosar 
+ Kiến trúc phân lớp cung cấp  các APIs trừu tượng theo tiêu chuẩn để phát triển phần mềm trong lĩnh vực ô tô. Với mục tiêu là để đơn giản hóa và thống nhất về 1 quy tắc chung để phát triển phần mềm có thể áp dụng cho bất kỳ hệ thống điện tử __(ECU)__, cũng như là tăng khả năng tái sử dụng mã nguồn,tối ưu chi phí, thời gian phát triển. 
# 2. Ứng dụng trong lĩnh vực Ô tô
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

__+ ASW__ : Lớp để phát triển các chức năng ứng dụng thực tế cho xe, sử dụng các API hoàn toàn tách biệt với các tầng phía dưới. Các chức năng sẽ được phát triển dựa trên các __SWC__(software component).

=> Lớp này chỉ quan tâm đén logic xử lý, tính toán dữ liệu

=> đọc và ghi dữ liệu xuống phần cứng mà không cần biết nó đến từ đầu

=> Lớp này đóng vai trò như 1 người marketing sản phẩm. Chỉ quan tâm đến việc giới thiệu các tính năng cụ thể mà 1 hệ thống được phát triển

__+ RTE__: Đây là lớp trung gian để giao tiếp giữa __ASW__ và các tầng bên dưới, ngoài ra nó còn thực hiện việc giao tiếp, trao đổi dữ liệu giữa các __SWC__

=> Giúp lớp phần mềm và phần cứng có thể hiểu nhau

=> Cấu hình các thông số hệ thống như ngoại vi MCU và giá trị điều chỉnh cảm biến

__+ BSW__: Đây là lớp phát triển các phần cơ bản dựa trên phần cứng __MCU__, Nó cũng được chia ra các tầng khác nhau bên trong 

__+ Service layer:__ cung cấp các API để quản lý luồng thực thi của các __SWC__, cũng như quản lý lỗi,trạng thái của hệ thống

=> Đóng vai trò như 1 lớp áo khoác phủ bên ngoài hệ thống, cung cấp các task đã được gói bên trong, và cung cấp cho ASW để gọi ra và thực thi

__+ ECUAbstraction layer:__ cung cấp các API để giao tiếp giữa __ECU__ và __SWC__ 

=> Trừu tượng hóa những ngoại vi như cảm biến,actuator, chỉ quan tâm đến intput/output mà không cần biết quá trình xử lý như thế nào. 

=> Khi cần đọc cảm biến nhiệt độ. Khong cần biết đó là loại nào, chỉ cần gọi ra và đọc về giá trị 

__+ MCAL:__ Cung cấp các API để cấu hình các chân I/O, driver của ngoại vi trên MCU

=> Trưu tượng việc xử lý đọc/ghi dữ liệu trên ngoại vi của MCU

__+ CDD:__ Cho phép truy cập trực tiếp từ __ASW__ vào __MCAL__ mà không thông qua các lớp trung gian

=> Giúp xử lý các task yêu cầu về thời gian tức thời và khẩn cấp, ví dụ như kích hoạt túi khí

# 5. Triển khai dự án mẫu 

## 5.1 Chương trình chính quản lý việc gọi các task

```c
// Task để khởi tạo và cập nhật hệ thống điều khiển mô-men xoắn
void* Task_TorqueControl(void* arg) {
    // Gọi hàm khởi tạo Torque Control
    TorqueControl_Init();

    // Liên tục cập nhật hệ thống điều khiển mô-men xoắn
    while (1) {
        TorqueControl_Update();
        
        // Tạm dừng 1 giây trước khi cập nhật tiếp
        Os_Delay(1000);
    }

    return NULL;
}


int main(void) {
    // Khởi tạo hệ điều hành
    Os_Init();

    // Tạo task chung cho Torque Control (khởi tạo + cập nhật)
    Os_CreateTask(Task_TorqueControl, "Torque Control");
    
    // Chờ các task hoàn thành
    Os_Shutdown();

    return 0;
}
```

## 5.2 Triển khai cụ thể các task
```c
// Hàm khởi tạo hệ thống điều khiển mô-men xoắn
void TorqueControl_Init(void) {
    // Khởi tạo các cảm biến bàn đạp ga, tốc độ và tải trọng
    Std_ReturnType status;

    printf("Khởi tạo hệ thống Torque Control...\n");

    // Khởi tạo cảm biến bàn đạp ga
    status = Rte_Call_RpThrottleSensor_Init();
    if (status == E_OK) {
        printf("Cảm biến bàn đạp ga đã khởi tạo thành công.\n");
    } else {
        printf("Lỗi khi khởi tạo cảm biến bàn đạp ga.\n");
        return;
    }
```

## 5.3 Cấu hình thông số và xử lý đọc/ghi dữ liệu qua RTE

```c
// API khởi tạo cảm biến bàn đạp ga
Std_ReturnType Rte_Call_RpThrottleSensor_Init(void) {
    ThrottleSensor_ConfigType throttleSensorConfig = {
        .ThrottleSensor_Channel = 0  // Kênh ADC cho cảm biến bàn đạp ga
    };
    return IoHwAb_ThrottleSensor_Init(&throttleSensorConfig);  // Gọi API từ IoHwAb để khởi tạo cảm biến bàn đạp ga
}
```

## 5.4 Lưu trữ cấu hình từ RTE và gửi xuống cho MCAL từ EAL

```c
// Giả lập cấu hình của cảm biến bàn đạp ga
static ThrottleSensor_ConfigType ThrottleSensor_CurrentConfig;

// Hàm khởi tạo cảm biến bàn đạp ga với cấu hình
Std_ReturnType IoHwAb_ThrottleSensor_Init(const ThrottleSensor_ConfigType* ConfigPtr) {
    if (ConfigPtr == NULL) {
        printf("Error: Null configuration pointer passed to IoHwAb_ThrottleSensor_Init.\n");
        return E_NOT_OK;
    }

    // Lưu cấu hình cảm biến bàn đạp ga vào biến toàn cục
    ThrottleSensor_CurrentConfig.ThrottleSensor_Channel = ConfigPtr->ThrottleSensor_Channel;

    // Gọi API từ MCAL để khởi tạo ADC
    Adc_ConfigType adcConfig;
    adcConfig.Adc_Channel = ThrottleSensor_CurrentConfig.ThrottleSensor_Channel;
   
    Adc_Init(&adcConfig);

    // Gọi API từ MCAL để khởi tạo DIO nếu cần
    //Dio_Init();

    // In ra thông tin cấu hình của cảm biến bàn đạp ga
    printf("Throttle Sensor Initialized with ADC Channel %d\n", ThrottleSensor_CurrentConfig.ThrottleSensor_Channel);

    return E_OK;
}
```

## 5.5 Cấu hình thông số cho ngoại vi mong muốn trên MCU

```c
// Hàm khởi tạo ADC với cấu trúc cấu hình
void Adc_Init(const Adc_ConfigType* ConfigPtr) {
    if (ConfigPtr == NULL) {
        printf("Error: Null configuration pointer passed to Adc_Init.\n");
        return;
    }

    // Lưu cấu hình ADC từ ConfigPtr vào biến toàn cục
    Adc_CurrentConfig.Adc_Channel = ConfigPtr->Adc_Channel;
    Adc_CurrentConfig.Adc_SamplingRate = ConfigPtr->Adc_SamplingRate;
    Adc_CurrentConfig.Adc_Resolution = ConfigPtr->Adc_Resolution;

    // Khởi tạo seed cho việc sinh số ngẫu nhiên để mô phỏng ADC
    srand(time(0));

    // In ra thông tin cấu hình ADC
    printf("ADC Initialized with Configuration:\n");
    printf(" - Channel: %d\n", Adc_CurrentConfig.Adc_Channel);
    printf(" - Sampling Rate: %d Hz\n", Adc_CurrentConfig.Adc_SamplingRate);
    printf(" - Resolution: %d-bit\n", Adc_CurrentConfig.Adc_Resolution);
}
```
