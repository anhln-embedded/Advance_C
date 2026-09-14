# BÀI 24: USB 2.0 FULL SPEED DEVICE - VIRTUAL COM PORT VÀ CUSTOM HID

Chào mừng bạn đến với bài học thứ 24 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Hầu hết mọi chiếc máy tính hiện đại ngày nay đều đã loại bỏ các cổng giao tiếp cổ điển như cổng RS-232 COM và cổng song song Parallel, thay vào đó là cổng **USB (Universal Serial Bus)**. 

Thay vì phải tốn thêm tiền mua các module chuyển đổi USB-to-UART rời (như CP2102, CH340, FT232), vi điều khiển **STM32F103C8T6 được tích hợp sẵn một bộ điều khiển phần cứng USB 2.0 Full Speed (12 Mbit/s)** kết nối trực tiếp vào cổng micro-USB trên bo mạch Blue Pill.

Bài học này sẽ hướng dẫn bạn hiểu rõ cấu trúc xung nhịp 48MHz của USB, khắc phục lỗi phần cứng kinh điển của mạch Blue Pill, và xây dựng 2 thiết bị USB công nghiệp phổ biến nhất: **Cổng COM ảo (Virtual COM Port - CDC)** và **Chuột/Bàn phím không cần cài driver (Custom HID)**.

---

## 1. Cấu Trúc Phần Cứng USB 2.0 Full Speed Trên STM32F103

Khối USB Device của STM32F103 hoạt động ở tốc độ **Full Speed (12 Mbit/s)**:
- Sử dụng 2 đường tín hiệu vi sai: **`USB_DP` (D+ / chân PA12)** và **`USB_DM` (D- / chân PA11)**.
- **Yêu cầu xung nhịp bắt buộc**: Khối USB **đòi hỏi nguồn xung nhịp chính xác tuyệt đối là 48MHz** với độ lệch cực nhỏ.

<p align="center">
  <img src="images/bai24_usb_clock_tree.svg" width="100%" alt="Hệ thống xung nhịp khối USB 2.0 Full Speed 48MHz">
  <br>
  <em>Hình 24.1: Hệ thống phân chia xung nhịp 48MHz từ PLL 72MHz cho khối ngoại vi USB</em>
</p>

### 1.1 Điện trở kéo lên 1.5kΩ trên chân D+ (USB Pull-Up):
- Theo tiêu chuẩn USB, để máy tính (Host) nhận diện có một thiết bị Full Speed vừa cắm vào, **đường tín hiệu D+ bắt buộc phải được kéo lên 3.3V qua một điện trở 1.5kΩ**.

> [!CAUTION]
> **Lỗi phần cứng kinh điển trên bo mạch "Blue Pill" của Trung Quốc:**
> Hầu hết các bo mạch Blue Pill giá rẻ trên thị trường đều bị nhà máy hàn nhầm điện trở kéo lên chân D+ (vị trí trở **R10**) thành **10kΩ hoặc 4.7kΩ** thay vì đúng 1.5kΩ!
> Trị số sai này khiến máy tính Windows không nhận diện được điện áp và lập tức báo lỗi: **`USB Device Not Recognized (Device Descriptor Request Failed)`**.
> **Cách khắc phục**:
> 1. Cách phần cứng: Hàn thay thế điện trở R10 trên mạch bằng điện trở dán 1.5kΩ (hoặc hàn một trở 1.8kΩ nối song song).
> 2. Cách phần mềm: Dùng chân PA12 cấu hình kéo xuống 0V trước khi bật USB để ép máy tính Re-enumerate (Tái nhận diện).

---

## 2. Hệ Thống Bộ Mô Tả USB (USB Descriptors)

Khi cắm cổng USB vào máy tính, máy tính sẽ thực hiện quá trình bắt tay điều tra thiết bị mang tên **Enumeration (Quá trình nhận dạng)** thông qua 4 tầng mô tả:

| Cấp Bộ Mô Tả | Tên Tiếng Anh | Nội Dung Quản Lý |
| :---: | :--- | :--- |
| **Cấp 1** | **Device Descriptor** | Mã nhà sản xuất (VID), Mã sản phẩm (PID), Phiên bản USB hỗ trợ. |
| **Cấp 2** | **Configuration Descriptor** | Khai báo dòng điện tiêu thụ (mA), số cổng giao tiếp (Interfaces), nguồn cấp. |
| **Cấp 3** | **Interface Descriptor** | Xác định phân lớp thiết bị (CDC Virtual COM, HID Bàn phím/Chuột, MSC Ổ đĩa...). |
| **Cấp 4** | **Endpoint Descriptors** | Thiết lập các đường ống truyền nhận gói tin (IN/OUT Endpoint, kích thước gói tin). |

1. **Device Descriptor**: Chứa mã nhà sản xuất (**VID - Vendor ID**) và mã thiết bị (**PID - Product ID**). Ví dụ STMicroelectronics dùng `VID = 0x0483`.
2. **Configuration Descriptor**: Khai báo dòng điện tiêu thụ tối đa của thiết bị (ví dụ 100mA) và chế độ cấp nguồn (Bus-powered hay Self-powered).
3. **Interface Descriptor**: Xác định loại thiết bị:
   - **CDC (Communication Device Class)**: Cổng COM ảo Virtual Serial Port.
   - **HID (Human Interface Device)**: Chuột, Bàn phím, Gamepad (Không cần cài bất kỳ Driver nào trên Windows/Linux/macOS!).
   - **MSC (Mass Storage Class)**: Ổ đĩa USB Flash nhớ.
4. **Endpoint Descriptors**: Khai báo các "đường ống" (Pipes) để đẩy/nhận dữ liệu thực tế: Endpoint 0 (Control), Endpoint IN (Gửi lên PC), Endpoint OUT (Nhận từ PC).

---

## 3. Lớp Thiết Bị USB Human Interface Device (HID)

Lớp **HID** là lớp thiết bị thân thiện và tiện lợi nhất trong toàn bộ chuẩn USB:
- **Tự động nhận diện (Driverless)**: Windows, Linux, Android và macOS đều đã tích hợp sẵn Driver HID chuẩn. Bạn chỉ cần cắm vào là hệ điều hành nhận ngay lập tức mà không cần cài đặt bất kỳ file `.inf` hay phần mềm nào!
- **Báo cáo trạng thái (HID Report)**: Thiết bị gửi các mảng byte cố định lên máy tính theo chu kỳ (ví dụ mỗi 10ms gửi tọa độ chuột hoặc phím bấm).

### Cấu trúc 4 byte gói tin của một con chuột USB tiêu chuẩn (Standard Mouse Report):
- **Byte 0**: Trạng thái các nút bấm (Bit 0 = Chuột trái, Bit 1 = Chuột phải, Bit 2 = Chuột giữa).
- **Byte 1**: Độ dịch chuyển tọa độ trục X có dấu (`int8_t`: -127 → +127).
- **Byte 2**: Độ dịch chuyển tọa độ trục Y có dấu (`int8_t`: -127 → +127).
- **Byte 3**: Con lăn cuộn trang Wheel (`int8_t`).

---

## 4. Triển Khai Mã Nguồn Thực Chiến: Tạo Con Chuột USB Tự Động

### Kịch bản thực hành:
- Tích hợp bộ thư viện chuẩn `STM32_USB-FS-Device_Lib` vào dự án.
- Cấu hình xung nhịp USB đúng **48MHz** từ thạch anh ngoài 8MHz qua PLL 72MHz chia 1.5.
- Khi cắm cổng Micro-USB vào máy tính, Windows sẽ tự động phát ra âm thanh kết nối và nhận diện thành **"HID-compliant mouse"**.
- Vi điều khiển sẽ tự động điều khiển con trỏ chuột máy tính di chuyển mượt mà theo một quỹ đạo hình tròn trên màn hình!

---

File: `usb_mouse.c`

```c
#include "stm32f10x.h"
#include <math.h>

// Define USB Mouse HID Report structure (4 Bytes)
typedef struct {
    uint8_t buttons; // Bit 0: Left, Bit 1: Right, Bit 2: Middle
    int8_t  x;       // Relative X displacement (-127 to +127)
    int8_t  y;       // Relative Y displacement (-127 to +127)
    int8_t  wheel;   // Wheel scroll value
} MouseReport_t;

MouseReport_t mouse_report = { 0, 0, 0, 0 };

void SetSysClockTo72_USB(void)
{
    // Configure SYSCLK = 72MHz from 8MHz HSE
    // ... [Configure Flash Latency 2, HSE, PLL x9 as in Lesson 03] ...

    // CONFIGURE USB PRESCALER IN RCC_CFGR:
    // Bit 22: USBPRE = 0 -> PLL divided by 1.5 (72MHz / 1.5 = EXACT 48MHz!)
    RCC->CFGR &= ~(1 << 22);

    // Enable peripheral clock for USB on APB1 bus
    RCC->APB1ENR |= (1 << 23); // USBEN = 1
}

// Send mouse HID report to host via Endpoint 1 IN
void USB_SendMouseReport(int8_t dx, int8_t dy, uint8_t buttons)
{
    mouse_report.buttons = buttons;
    mouse_report.x = dx;
    mouse_report.y = dy;
    mouse_report.wheel = 0;

    // Copy 4 report bytes into USB Endpoint 1 IN buffer
    // (Using USB-FS Device library function: UserToPMABufferCopy)
    // UserToPMABufferCopy((uint8_t *)&mouse_report, ENDP1_TXADDR, 4);
    // SetEPTxCount(ENDP1, 4);
    // SetEPTxValid(ENDP1);
}

void delay_ms(volatile uint32_t ms)
{
    volatile uint32_t i;
    for (; ms > 0; ms--)
        for (i = 0; i < 7200; i++)
            __NOP();
}

int main(void)
{
    SetSysClockTo72_USB();

    // Initialize USB hardware and endpoints
    // USB_Init();

    // Wait for host USB Enumeration to complete (~2 seconds)
    delay_ms(2000);

    float angle = 0.0f;
    const float radius = 5.0f;

    while (1)
    {
        // Calculate differential coordinates with trigonometric functions to draw a circle
        int8_t delta_x = (int8_t)(cosf(angle) * radius);
        int8_t delta_y = (int8_t)(sinf(angle) * radius);

        // Send mouse displacement packet to host
        USB_SendMouseReport(delta_x, delta_y, 0);

        angle += 0.1f;
        if (angle > 6.28f) angle = 0.0f;

        // Mouse report update rate: every 20ms (50Hz)
        delay_ms(20);
    }
}
```

---

## 5. Lớp Thiết Bị Cổng COM Ảo (Virtual COM Port - CDC)

Khi cấu hình thiết bị theo lớp **USB Communication Device Class (CDC)**:
- Máy tính sẽ nhận bo mạch STM32 như một cổng Serial COM vật lý thông thường (ví dụ `COM3` hoặc `COM7`).
- Bạn có thể dùng bất kỳ phần mềm Terminal nào (Putty, TeraTerm, Hercules, Arduino Serial Monitor) để truyền nhận dữ liệu.
- **Tốc độ truyền dữ liệu thực tế**: Có thể đạt tới **800 KiloBytes/giây đến 1 MegaByte/giây** (nhanh hơn tốc độ 115200 bps của UART truyền thống gấp gần 100 lần!).

---

## 6. Những Lỗi Thường Gặp Khi Phát Triển Ứng Dụng USB

> [!WARNING]
> **1. Sai lệch tần số xung nhịp 48MHz của USB:**
> Tiêu chuẩn USB đòi hỏi sai số tần số nghiêm ngặt trong khoảng ± 0.25%. Do đó, **bạn KHÔNG THỂ sử dụng dao động RC nội HSI để chạy cổng USB**! Bắt buộc phải sử dụng thạch anh ngoài HSE chất lượng cao (8.000MHz).

> [!CAUTION]
> **2. Xung đột ngắt ưu tiên:**
> Quá trình bắt tay Enumeration của USB đòi hỏi phản hồi từ vi điều khiển trong vòng vài mili-giây. Nếu trong hệ thống có một ngắt khác (như Timer hay UART) chiếm dụng CPU quá lâu khiến ngắt `USB_LP_CAN1_RX0_IRQn` không được phục vụ kịp, máy tính sẽ coi thiết bị bị lỗi và ngừng giao tiếp.

---

## 7. Bài Tập Thực Hành

1. **Bài tập 1 (Bàn phím ma trận USB Keyboard)**: Cấu hình lớp USB Custom HID làm Bàn phím máy tính. Kết nối nút bấm PA0: Mỗi lần bấm nút, STM32 sẽ tự động gõ một chuỗi văn bản `"Hello from STM32F103 USB Native!"` vào văn bản Notepad trên máy tính.
2. **Bài tập 2 (Bộ điều khiển Gamepad chuyên dụng)**: Kết hợp module cần gạt Joystick 2 trục Analog (kết nối ADC PA0, PA1) và 4 nút bấm để tạo thành một chiếc tay cầm chơi game USB tiêu chuẩn nhận diện trên Windows.
3. **Bài tập 3 (Đo băng thông truyền nhận USB CDC)**: Viết chương trình đẩy liên tục một khối dữ liệu lớn (100 MegaBytes) từ STM32 lên máy tính qua cổng Virtual COM Port. Viết một script Python trên máy tính để đo chính xác tốc độ truyền tải megabytes/giây thực tế của chip.
