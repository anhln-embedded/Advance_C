# BÀI 04: NGẮT NGOÀI (EXTI) VÀ BỘ ĐIỀU KHIỂN NGẮT NVIC

Chào mừng bạn đến với bài học thứ 4 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Trong kỹ thuật lập trình nhúng, kỹ thuật thăm dò vòng lặp (Polling) liên tục kiểm tra trạng thái chân I/O khiến CPU tiêu tốn 100% năng lực xử lý một cách lãng phí và dễ bỏ sót các sự kiện diễn ra chớp nhoáng.

Giải pháp tối ưu cho vấn đề này chính là **Cơ chế Ngắt (Interrupt)**. Bài học này sẽ giúp bạn nắm trọn kiến trúc bộ điều khiển ngắt lồng nhau **NVIC** của lõi ARM Cortex-M3 và làm chủ bộ điều khiển ngắt ngoài **EXTI** thông qua cả Thanh ghi thuần (Bare-metal) và Thư viện chuẩn (SPL).

---

## 1. Kiến Trúc Ngắt Lõi ARM Cortex-M3 (NVIC)

Khác với các vi điều khiển 8-bit cổ điển, lõi **ARM Cortex-M3** tích hợp sẵn một bộ điều khiển ngắt phần cứng cực kỳ mạnh mẽ mang tên **NVIC (Nested Vectored Interrupt Controller)**:
- **Độ trễ ngắt cực thấp (Low Latency)**: Chỉ mất đúng 12 chu kỳ clock để tự động lưu ngữ cảnh (Stack Frame gồm các thanh ghi `R0-R3`, `R12`, `LR`, `PC`, `xPSR`) vào bộ nhớ ngăn xếp RAM và nhảy vào hàm phục vụ ngắt ISR.
- **Ngắt lồng nhau (Nested Interrupts)**: Một ngắt có mức ưu tiên cao hơn hoàn toàn có thể chiếm quyền (preempt) một ngắt đang thực thi có mức ưu tiên thấp hơn.
- **Bảng Vector Ngắt (Vector Table)**: Chứa địa chỉ con trỏ hàm trỏ trực tiếp tới từng chương trình phục vụ ngắt trong Flash.

<p align="center">
  <img src="images/bai04_exti_nvic_routing.svg" width="950" alt="Kiến trúc điều hướng ngắt ngoại vi STM32: EXTI & NVIC">
</p>

---

## 2. Phân Cấp Mức Độ Ưu Tiên: Preemption Priority & Sub-priority

NVIC của STM32F103 sử dụng **4 bit** để định nghĩa mức độ ưu tiên cho mỗi ngắt (tổng cộng 16 cấp độ, giá trị số càng nhỏ thì độ ưu tiên càng cao: mức `0` ưu tiên cao hơn mức `1`). 

4 bit này được chia thành 2 nhóm thông qua thanh ghi **`AIRCR` (Application Interrupt and Reset Control Register)**:

| Priority Group | Số bit Preemption (Chiếm quyền) | Số bit Sub-priority (Ưu tiên phụ) | Mô tả hành vi |
| :---: | :---: | :---: | :--- |
| **`Group 0`** | 0 bit (0 cấp) | 4 bits (16 cấp) | Không có ngắt nào được chiếm quyền ngắt khác. |
| **`Group 1`** | 1 bit (2 cấp: 0-1) | 3 bits (8 cấp: 0-7) | Có 2 cấp chiếm quyền. |
| **`Group 2`** | 2 bits (4 cấp: 0-3) | 2 bits (4 cấp: 0-3) | Phổ biến nhất: 4 cấp chiếm quyền, 4 cấp phụ. |
| **`Group 3`** | 3 bits (8 cấp: 0-7) | 1 bit (2 cấp: 0-1) | 8 cấp chiếm quyền, 2 cấp phụ. |
| **`Group 4`** | 4 bits (16 cấp: 0-15) | 0 bit (0 cấp) | Toàn bộ 16 mức là ngắt chiếm quyền. |

> [!IMPORTANT]
> **Quy tắc giải quyết xung đột ngắt:**
> 1. **Preemption Priority (Ưu tiên chiếm quyền)**: Nếu ngắt B có Preemption Priority cao hơn ngắt A, ngắt B **sẽ tạm dừng ngắt A ngay lập tức** để CPU chuyển sang xử lý ngắt B.
> 2. **Sub-priority (Ưu tiên phụ)**: Nếu hai ngắt có cùng Preemption Priority xảy ra cùng một thời điểm, ngắt nào có Sub-priority nhỏ hơn sẽ được CPU xử lý trước. Tuy nhiên, ngắt có Sub-priority cao hơn **không thể chiếm quyền** nếu ngắt kia đã bắt đầu chạy.

---

## 3. Bộ Điều Khiển Ngắt Ngoài (EXTI) Và Thanh Ghi AFIO

STM32F103 có 20 kênh ngắt/sự kiện ngoài:
- **EXTI0 đến EXTI15**: Nối với các chân GPIO tương ứng từ Pin 0 đến Pin 15.
- **EXTI16**: Kết nối bộ phát hiện điện áp nguồn thấp PVD (Programmable Voltage Detector).
- **EXTI17**: Kết nối sự kiện báo thức thời gian thực RTC Alarm.
- **EXTI18**: Kết nối sự kiện đánh thức chip USB Wakeup.
- **EXTI19**: Kết nối sự kiện Ethernet Wakeup (chỉ có trên dòng Connectivity).

### 3.1 Cơ Chế Ghép Kênh Của Khối AFIO (Alternate Function I/O)
Vì có tới 5 Port GPIO (A, B, C, D, E...) nhưng chỉ có 16 đường EXTI (0-15), do đó tại một thời điểm, mỗi đường EXTI chỉ được chọn kết nối với **duy nhất một chân cùng số thứ tự**:

| Chân GPIO vật lý | Thanh ghi dồn kênh AFIO | Tuyến đường EXTI | Vector Ngắt NVIC phục vụ |
| :--- | :--- | :--- | :--- |
| **PA0, PB0, PC0, PD0...** | `AFIO_EXTICR1` [3:0] | **EXTI Line 0** | `EXTI0_IRQHandler` |
| **PA1, PB1, PC1, PD1...** | `AFIO_EXTICR1` [7:4] | **EXTI Line 1** | `EXTI1_IRQHandler` |
| **PA2, PB2, PC2...** | `AFIO_EXTICR1` [11:8] | **EXTI Line 2** | `EXTI2_IRQHandler` |
| **PA3, PB3, PC3...** | `AFIO_EXTICR1` [15:12] | **EXTI Line 3** | `EXTI3_IRQHandler` |
| **PA4, PB4, PC4...** | `AFIO_EXTICR2` [3:0] | **EXTI Line 4** | `EXTI4_IRQHandler` |
| **PA5..PA9, PB5..PB9...** | `AFIO_EXTICR2..3` | **EXTI Line 5..9** | `EXTI9_5_IRQHandler` (Dùng chung) |
| **PA10..PA15...** | `AFIO_EXTICR3..4` | **EXTI Line 10..15**| `EXTI15_10_IRQHandler` (Dùng chung)|

> [!WARNING]
> Bạn **không thể** sử dụng đồng thời chân PA0 và PB0 cho ngắt ngoài cùng lúc vì cả hai chân này đều đi qua bộ chọn kênh `EXTI0`. Nhưng bạn hoàn toàn có thể dùng PA0 và PB1 cùng lúc (vì PA0 đi vào `EXTI0`, PB1 đi vào `EXTI1`).

---

## 4. Các Thanh Ghi EXTI Cần Thiết (Theo RM0008)

<p align="center">
  <img src="images/bai04_exti_structure.svg" width="100%" alt="Sơ đồ khối phần cứng bộ điều khiển ngắt ngoài EXTI (RM0008 Figure 19)">
  <br>
  <em>Hình 4.1: Sơ đồ khối chức năng chi tiết của kênh ngắt ngoài EXTI (Theo ST RM0008)</em>
</p>

Địa chỉ cơ sở của EXTI: `0x4001 0400`.

| Thanh Ghi | Offset | Chức Năng Chi Tiết |
| :--- | :---: | :--- |
| **`EXTI_IMR`** | `0x00` | **Interrupt Mask Register**: Cho phép/cấm ngắt trên đường EXTI tương ứng (Ghi `1` để bật ngắt). |
| **`EXTI_EMR`** | `0x04` | **Event Mask Register**: Mặt nạ cho chế độ sự kiện (đánh thức CPU). |
| **`EXTI_RTSR`**| `0x08` | **Rising Trigger Selection**: Kích hoạt ngắt khi có cạnh lên (0 → 1). |
| **`EXTI_FTSR`**| `0x0C` | **Falling Trigger Selection**: Kích hoạt ngắt khi có cạnh xuống (1 → 0). |
| **`EXTI_SWIER`**| `0x10`| **Software Interrupt Event**: Tạo ngắt ngoài bằng phần mềm. |
| **`EXTI_PR`**  | `0x14` | **Pending Register**: Cờ báo có ngắt đang chờ phục vụ. |

> [!CAUTION]
> **Cách xóa cờ ngắt `EXTI_PR`:**
> Để xóa cờ báo ngắt trong thanh ghi `EXTI_PR`, bạn phải **ghi bit 1 vào vị trí bit tương ứng** (`EXTI->PR = (1 << 0)`). Nếu không xóa cờ này ở cuối hàm ISR, ngắt sẽ bị kích hoạt lặp đi lặp lại vô tận và CPU bị treo!

---

## 5. Triển Khai Mã Nguồn Thực Chiến

### Kịch bản thực hành:
- Đèn LED kết nối chân **PC13** (Active-Low).
- Nút bấm kết nối chân **PA0** kéo xuống GND (cấu hình Input Pull-Up).
- Kích hoạt ngắt ngoài **EXTI0** khi có cạnh xuống (nhấn nút: điện áp từ 3.3V tụt xuống 0V).
- Hàm ngắt `EXTI0_IRQHandler` lập tức đảo trạng thái LED PC13 mà không tốn tài nguyên thăm dò của vòng lặp `while(1)`.

---

### PHƯƠNG PHÁP 1: BARE-METAL REGISTER & CMSIS

File: `main.c`

```c
#include "stm32f10x.h"

// Flag variable signaling button press event from ISR
volatile uint8_t button_pressed_flag = 0;

void EXTI0_Config_Register(void)
{
    // 1. Enable clocks for GPIOA, GPIOC, and AFIO multiplexer
    RCC->APB2ENR |= (1 << 0); // Bit 0: AFIOEN
    RCC->APB2ENR |= (1 << 2); // Bit 2: IOPAEN
    RCC->APB2ENR |= (1 << 4); // Bit 4: IOPCEN

    // 2. Configure PC13 as Output Push-Pull 2MHz
    GPIOC->CRH &= ~(0x0F << 20);
    GPIOC->CRH |= (0x02 << 20);
    GPIOC->BSRR = (1 << 13); // Default: turn off LED

    // 3. Configure PA0 as Input Pull-Up
    GPIOA->CRL &= ~(0x0F << 0);
    GPIOA->CRL |= (0x08 << 0); // CNF0 = 10b, MODE0 = 00b
    GPIOA->ODR |= (1 << 0);    // Enable internal pull-up resistor

    // 4. Map PA0 to EXTI0 interrupt line via AFIO_EXTICR1 register
    // Bits [3:0] of AFIO_EXTICR1: 0000b selects Port A for EXTI0
    AFIO->EXTICR[0] &= ~(0x0F << 0);

    // 5. Configure falling edge trigger on EXTI0
    EXTI->RTSR &= ~(1 << 0); // Disable rising edge trigger
    EXTI->FTSR |= (1 << 0);  // Enable falling edge trigger (when PA0 button is pressed to GND)

    // 6. Enable interrupt mask on EXTI0 line
    EXTI->IMR |= (1 << 0);

    // 7. Configure NVIC: Enable EXTI0 interrupt and set priority
    // EXTI0 interrupt vector number EXTI0_IRQn = 6
    NVIC_SetPriority(EXTI0_IRQn, 2); // Priority = 2
    NVIC_EnableIRQ(EXTI0_IRQn);       // Enable interrupt in NVIC
}

// EXTI Line 0 ISR (Standard function name per Vector Table in startup_stm32f10x_md.s)
void EXTI0_IRQHandler(void)
{
    // Check EXTI0 interrupt flag
    if (EXTI->PR & (1 << 0))
    {
        // Toggle event flag state
        button_pressed_flag = 1;

        // MANDATORY: Clear interrupt flag by writing 1 to PR register
        EXTI->PR = (1 << 0);
    }
}

int main(void)
{
    EXTI0_Config_Register();

    while (1)
    {
        // CPU is completely idle or can enter Sleep mode (WFI)
        if (button_pressed_flag)
        {
            button_pressed_flag = 0;
            GPIOC->ODR ^= (1 << 13); // Toggle LED PC13
        }
    }
}
```

---

### PHƯƠNG PHÁP 2: LẬP TRÌNH BẰNG THƯ VIỆN CHUẨN SPL

File: `main.c`

```c
#include "stm32f10x.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_gpio.h"
#include "stm32f10x_exti.h"
#include "misc.h" // Library containing NVIC configuration functions

void EXTI0_Config_SPL(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
    EXTI_InitTypeDef EXTI_InitStructure;
    NVIC_InitTypeDef NVIC_InitStructure;

    // 1. Enable clocks for GPIOA, GPIOC, and AFIO
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_GPIOC | RCC_APB2Periph_AFIO, ENABLE);

    // 2. Configure PC13 pin: Output Push-Pull
    GPIO_InitStructure.GPIO_Pin   = GPIO_Pin_13;
    GPIO_InitStructure.GPIO_Mode  = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_2MHz;
    GPIO_Init(GPIOC, &GPIO_InitStructure);
    GPIO_SetBits(GPIOC, GPIO_Pin_13);

    // 3. Configure PA0 pin: Input Pull-Up
    GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_0;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_Init(GPIOA, &GPIO_InitStructure);

    // 4. Connect EXTI Line 0 to GPIOA Pin 0
    GPIO_EXTILineConfig(GPIO_PortSourceGPIOA, GPIO_PinSource0);

    // 5. Configure EXTI Line 0
    EXTI_InitStructure.EXTI_Line    = EXTI_Line0;
    EXTI_InitStructure.EXTI_Mode    = EXTI_Mode_Interrupt;
    EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling; // Falling edge trigger
    EXTI_InitStructure.EXTI_LineCmd = ENABLE;
    EXTI_Init(&EXTI_InitStructure);

    // 6. Configure NVIC interrupt controller
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); // 2 bit Preempt, 2 bit Sub-priority
    NVIC_InitStructure.NVIC_IRQChannel                   = EXTI0_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority        = 0;
    NVIC_InitStructure.NVIC_IRQChannelCmd                = ENABLE;
    NVIC_Init(&NVIC_InitStructure);
}

void EXTI0_IRQHandler(void)
{
    // Check interrupt flag
    if (EXTI_GetITStatus(EXTI_Line0) != RESET)
    {
        // Toggle LED PC13 state
        if (GPIO_ReadOutputDataBit(GPIOC, GPIO_Pin_13) == Bit_SET)
        {
            GPIO_ResetBits(GPIOC, GPIO_Pin_13);
        }
        else
        {
            GPIO_SetBits(GPIOC, GPIO_Pin_13);
        }

        // Clear EXTI Line 0 interrupt flag
        EXTI_ClearITPendingBit(EXTI_Line0);
    }
}

int main(void)
{
    EXTI0_Config_SPL();

    while (1)
    {
        // Idle loop waiting for interrupts
        __WFI(); // Wait For Interrupt instruction: Enter low-power Sleep mode
    }
}
```

---

## 6. Những Lỗi Thường Gặp Và Nguyên Tắc Vàng Khi Viết ISR

> [!CAUTION]
> **1. TUYỆT ĐỐI KHÔNG DÙNG HÀM DELAY NGHẼN TRONG ISR:**
> Không bao giờ gọi các hàm vòng lặp bận như `delay_ms()` bên trong hàm ngắt. Hàm phục vụ ngắt phải thực thi và kết thúc trong vài micro giây (µs). Việc giữ CPU quá lâu trong ISR sẽ làm nghẽn toàn bộ hệ thống và vô hiệu hóa các ngắt khác.

> [!IMPORTANT]
> **2. Từ khóa `volatile` cho biến dùng chung:**
> Bất kỳ biến toàn cục nào được sửa đổi trong hàm ngắt ISR và được đọc ở vòng lặp `main()` (ví dụ: biến `volatile uint8_t button_pressed_flag`) **bắt buộc phải khai báo với từ khóa `volatile`**. Nếu thiếu từ khóa này, trình biên dịch tối ưu (Optimization -O2/O3) sẽ lưu giá trị biến vào thanh ghi CPU và vòng lặp `while(1)` sẽ không bao giờ thấy giá trị mới được cập nhật từ ngắt!

> [!WARNING]
> **3. Quên cấp xung cho AFIO:**
> Để sử dụng ngắt ngoài EXTI cho bất kỳ chân GPIO nào, bạn bắt buộc phải bật bit `AFIOEN` trong thanh ghi `RCC->APB2ENR`. Quên lệnh này sẽ khiến bộ chọn kênh `AFIO_EXTICRx` không hoạt động.

---

## 7. Hướng Dẫn Debug Trên Keil MDK

1. Nhấn `Ctrl + F5` để khởi động trình Debug.
2. Mở cửa sổ quản lý ngắt: **Peripherals -> Core Peripherals -> Nested Vectored Interrupt Controller**.
3. Quan sát mục **EXTI0**:
   - Kiểm tra cột **Enable** có được tích chọn không.
   - Cột **Priority** hiển thị đúng mức ưu tiên bạn đã cài đặt.
4. Mở cửa sổ **Peripherals -> External Interrupt (EXTI)**:
   - Khi nhấn nút PA0 trên thực tế hoặc mô phỏng, bit `PR0` sẽ sáng đỏ lên trước khi hàm `EXTI0_IRQHandler` được gọi và xóa nó.

---

## 8. Bài Tập Thực Hành

1. **Bài tập 1 (Ngắt đa kênh trên các nhóm khác nhau)**: Hãy cấu hình thêm một nút nhấn thứ hai ở chân **PB1**. Khi nhấn nút PA0 (EXTI0) thì LED bật, khi nhấn nút PB1 (EXTI1) thì LED tắt. Chú ý cấu hình đúng `AFIO_EXTICR1` cho cả 2 kênh.
2. **Bài tập 2 (Phân cấp ngắt lồng nhau - Nested ISR)**:
   - Cấu hình EXTI0 có `Preemption Priority = 2`.
   - Cấu hình Timer ngắt định kỳ có `Preemption Priority = 0` (ưu tiên cao nhất).
   - Đặt breakpoint trong hàm `EXTI0_IRQHandler` để kiểm chứng khi Timer xảy ra, CPU có lập tức nhảy sang xử lý ngắt Timer rồi mới quay lại hoàn thành nốt `EXTI0` hay không.
3. **Bài tập 3 (Khử rung nút bấm phần cứng cho ngắt)**: Viết cơ chế lưu mốc thời gian (Timestamp bằng SysTick) khi ngắt EXTI xảy ra. Nếu lần kích hoạt tiếp theo cách lần trước ít hơn 50ms thì bỏ qua để chống hiện tượng rung phím gây ra hàng loạt ngắt liên tiếp.
