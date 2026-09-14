# BÀI 08: INPUT CAPTURE - ĐO XUNG VÀ CẢM BIẾN SIÊU ÂM HC-SR04

Chào mừng bạn đến với bài học thứ 8 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Ở bài trước, chúng ta đã dùng khối Output Compare để phát xung PWM ra ngoài. Ngược lại hoàn toàn với Output Compare, **Input Capture (Bắt cạnh xung ngõ vào)** là tính năng cho phép vi điều khiển ghi lại chính xác thời điểm xuất hiện các cạnh tín hiệu điện tử bên ngoài với độ phân giải lên tới từng micro-giây (µs).

Tính năng này được ứng dụng rộng rãi trong việc: đo tần số và chu kỳ xung máy phát, đo tốc độ vòng quay động cơ, giải mã tín hiệu điều khiển từ xa hồng ngoại (IR Remote NEC), và đo khoảng cách chính xác bằng **Cảm biến siêu âm HC-SR04**.

---

## 1. Nguyên Lý Khối Input Capture Của STM32 Timer

Input Capture hoạt động như một chiếc máy ảnh chụp nhanh (Snapshot) giá trị thời gian:

<p align="center">
  <img src="images/bai08_input_capture.svg" width="100%" alt="Nguyên lý hoạt động khối Input Capture Timer">
  <br>
  <em>Hình 8.1: Nguyên lý hoạt động khối Input Capture và cơ chế chốt tự động vào CCR1</em>
</p>

### Quy trình phần cứng:
1. Tín hiệu xung từ bên ngoài đi vào chân I/O (ví dụ chân PA6 ứng với kênh TI1 của TIM3).
2. Tín hiệu đi qua khối **bộ lọc số (Input Filter)** để loại bỏ các gai nhiễu điện áp cao tần.
3. Khối **dò cạnh (Edge Detector)** phát hiện cạnh lên (Rising Edge) hoặc cạnh xuống (Falling Edge) tùy theo cấu hình.
4. Ngay khi cạnh tín hiệu xuất hiện, phần cứng **ngay lập tức sao chép (Capture) giá trị hiện tại của bộ đếm `TIMx_CNT` vào thanh ghi `TIMx_CCR1`**.
5. Cờ ngắt **`CC1IF`** trong thanh ghi `TIMx_SR` được kéo lên mức 1 để thông báo cho CPU vào đọc dữ liệu.

---

## 2. Phương Pháp Đo Độ Rộng Xung Tín Hiệu

Để đo độ rộng xung mức cao (T_high) của một tín hiệu:
1. Ban đầu, cấu hình Timer bắt **cạnh lên (Rising Edge)**.
2. Khi có cạnh lên, CPU ghi nhận thời điểm bắt đầu: t_1 = CCR1.
3. Lập tức đảo cấu hình bộ dò cạnh sang bắt **cạnh xuống (Falling Edge)**.
4. Khi có cạnh xuống, CPU ghi nhận thời điểm kết thúc: t_2 = CCR1.
5. Độ rộng xung được tính bằng:
   Δ t = t_2 - t_1
   *(Nếu xảy ra hiện tượng tràn bộ đếm giữa t_1 và t_2: Δ t = (ARR - t_1) + t_2 + 1).*

---

## 3. Nguyên Lý Hoạt Động Của Cảm Biến Siêu Âm HC-SR04

Module siêu âm **HC-SR04** gồm 4 chân: `VCC` (5V), `GND`, `TRIG` (Ngõ vào kích hoạt) và `ECHO` (Ngõ ra phản hồi):

<p align="center">
  <img src="images/bai08_hcsr04_timing.svg" width="100%" alt="Giản đồ thời gian cảm biến siêu âm HC-SR04">
  <br>
  <em>Hình 8.2: Giản đồ thời gian phát xung kích và nhận tín hiệu phản xạ ECHO của HC-SR04</em>
</p>

### Quy trình đo:
1. Vi điều khiển phát một xung mức High tối thiểu **10µs** vào chân **TRIG**.
2. Module HC-SR04 tự động phát ra 8 xung siêu âm tần số 40kHz và kéo chân **ECHO** lên mức High (3.3V / 5V).
3. Khi sóng siêu âm chạm vào vật cản và phản xạ dội ngược lại đầu thu, chân **ECHO** sẽ được kéo tụt xuống mức Low.
4. Thời gian chân ECHO ở mức High (T_echo) chính là tổng thời gian sóng âm truyền đi và về.

### Công thức tính khoảng cách (S):
Vận tốc âm thanh trong không khí là v ≈ 340 m/s = 0.034 cm/µs.
Khoảng cách tới vật cản:

S = (v × T_echo / 2) = (0.034 × T_echo / 2) = (T_echo (µs) / 58.8) ≈ (T_echo / 58)  (cm)

---

## 4. Các Thanh Ghi Input Capture Theo RM0008

| Thanh Ghi | Offset | Bit Quan Trọng | Chức Năng |
| :--- | :---: | :--- | :--- |
| **`TIMx_CCMR1`** | `0x18` | `CC1S[1:0]` (Bits 0-1)<br>`IC1F[3:0]` (Bits 4-7)<br>`IC1PSC[1:0]` (Bits 2-3) | **Capture/Compare Mode Register 1**:<br>- `CC1S = 01b`: Cấu hình kênh 1 làm Input, kết nối với chân TI1.<br>- `IC1F`: Bộ lọc số (khử nhiễu gai điện áp).<br>- `IC1PSC`: Bộ chia xung ngõ vào (chia 1, 2, 4, 8). |
| **`TIMx_CCER`**  | `0x20` | `CC1E` (Bit 0)<br>`CC1P` (Bit 1) | **Capture/Compare Enable Register**:<br>- `CC1E = 1`: Bật tính năng Capture.<br>- `CC1P`: 0 = Bắt cạnh lên, 1 = Bắt cạnh xuống. |
| **`TIMx_CCR1`**  | `0x34` | Bits [15:0] | Nơi phần cứng lưu giá trị `CNT` chụp được. |

---

## 5. Triển Khai Mã Nguồn Thực Chiến

### Sơ đồ kết nối phần cứng:
- **Chân TRIG**: Nối với chân **PA5** (Output Push-Pull).
- **Chân ECHO**: Nối với chân **PA6** (TIM3 Channel 1 - Input Floating).
- **Đèn LED PC13**: Bật sáng nếu phát hiện vật cản ở cự ly gần (S < 15 cm).

> [!CAUTION]
> Chân ECHO của một số module HC-SR04 phát xung mức logic 5V. Chân PA6 của STM32F103 **không phải chân chịu áp 5V (Non-FT)**. Hãy lắp một cầu phân áp gồm 2 điện trở (1kΩ và 2kΩ) hoặc trở 4.7kΩ giữa chân ECHO và PA6 để hạ áp an toàn về 3.3V!

---

### PHƯƠNG PHÁP 1: BARE-METAL REGISTER & CMSIS

File: `main.c`

```c
#include "stm32f10x.h"

volatile uint32_t echo_start = 0;
volatile uint32_t echo_end = 0;
volatile uint8_t  capture_state = 0; // 0: Wait for rising edge, 1: Wait for falling edge, 2: Measurement complete
volatile uint32_t pulse_width_us = 0;

void HCSR04_Init_Register(void)
{
    // 1. Enable clocks for GPIOA, GPIOC, and TIM3
    RCC->APB2ENR |= (1 << 2) | (1 << 4); // IOPAEN = 1, IOPCEN = 1
    RCC->APB1ENR |= (1 << 1);            // TIM3EN = 1

    // 2. PA5 (TRIG): Output Push-Pull 50MHz
    GPIOA->CRL &= ~(0x0F << 20);
    GPIOA->CRL |= (0x03 << 20); // MODE5 = 11b, CNF5 = 00b
    GPIOA->BRR = (1 << 5);      // Default: pull TRIG pin LOW

    // 3. PA6 (ECHO - TIM3_CH1): Input Floating
    GPIOA->CRL &= ~(0x0F << 24);
    GPIOA->CRL |= (0x04 << 24); // MODE6 = 00b, CNF6 = 01b

    // 4. PC13: Output Push-Pull for buzzer/LED alarm indicator
    GPIOC->CRH &= ~(0x0F << 20);
    GPIOC->CRH |= (0x02 << 20);
    GPIOC->BSRR = (1 << 13);

    // 5. Configure TIM3 time-base: 1us tick (f = 1MHz)
    TIM3->PSC = 72 - 1;   // 72MHz / 72 = 1MHz -> 1 tick = 1us
    TIM3->ARR = 0xFFFF;   // Count up to 65535us (~65ms, covers up to 4 meters)
    TIM3->CNT = 0;

    // 6. Configure Input Capture Channel 1 in TIM3_CCMR1
    TIM3->CCMR1 &= ~(0x03 << 0);
    TIM3->CCMR1 |= (0x01 << 0); // CC1S = 01b (Map TI1 to CC1)
    TIM3->CCMR1 &= ~(0x0F << 4); // IC1F = 0000b (No digital filter)

    // 7. Configure initial rising edge and enable Capture in CCER
    TIM3->CCER &= ~(1 << 1); // CC1P = 0 (Capture on rising edge)
    TIM3->CCER |= (1 << 0);  // CC1E = 1 (Enable Capture)

    // 8. Enable Channel 1 Capture interrupt
    TIM3->DIER |= (1 << 1);  // CC1IE = 1

    // 9. Configure NVIC
    NVIC_SetPriority(TIM3_IRQn, 1);
    NVIC_EnableIRQ(TIM3_IRQn);

    // 10. Enable Timer
    TIM3->CR1 |= (1 << 0); // CEN = 1
}

// Microsecond delay using short busy-loop for Trigger pulse
void delay_us(uint32_t us)
{
    volatile uint32_t count = us * 8; // Approximate at 72MHz
    while (count--) __NOP();
}

void HCSR04_Trigger(void)
{
    capture_state = 0;
    
    // Pull TRIG pin HIGH for 12us
    GPIOA->BSRR = (1 << 5);
    delay_us(12);
    GPIOA->BRR  = (1 << 5);
}

// TIM3 interrupt service routine (ISR)
void TIM3_IRQHandler(void)
{
    // Check Channel 1 Capture interrupt flag (CC1IF)
    if (TIM3->SR & (1 << 1))
    {
        if (capture_state == 0) // Captured rising edge of ECHO pulse
        {
            echo_start = TIM3->CCR1;
            capture_state = 1;
            
            // Switch capture polarity to falling edge (CC1P = 1)
            TIM3->CCER |= (1 << 1);
        }
        else if (capture_state == 1) // Captured falling edge of ECHO pulse
        {
            echo_end = TIM3->CCR1;
            
            if (echo_end >= echo_start)
                pulse_width_us = echo_end - echo_start;
            else
                pulse_width_us = (0xFFFF - echo_start) + echo_end + 1;

            capture_state = 2; // Single cycle measurement complete

            // Restore rising edge capture for next measurement
            TIM3->CCER &= ~(1 << 1);
        }

        // Clear CC1IF capture flag by writing 0
        TIM3->SR &= ~(1 << 1);
    }
}

int main(void)
{
    HCSR04_Init_Register();

    uint32_t distance_cm = 0;

    while (1)
    {
        HCSR04_Trigger();

        // Wait for completion or timeout (~60ms)
        for (volatile int i = 0; i < 500000; i++)
        {
            if (capture_state == 2) break;
        }

        if (capture_state == 2)
        {
            // Calculate distance
            distance_cm = pulse_width_us / 58;

            // If distance < 15cm -> Turn on warning LED PC13
            if (distance_cm < 15 && distance_cm > 2)
            {
                GPIOC->BRR = (1 << 13); // Turn on LED (Active-Low)
            }
            else
            {
                GPIOC->BSRR = (1 << 13); // Turn off LED
            }
        }

        // Periodic measurement every 100ms
        for (volatile int i = 0; i < 1000000; i++);
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
#include "stm32f10x_tim.h"
#include "misc.h"

void TIM3_InputCapture_Init_SPL(void)
{
    GPIO_InitTypeDef        GPIO_InitStructure;
    TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
    TIM_ICInitTypeDef       TIM_ICInitStructure;
    NVIC_InitTypeDef        NVIC_InitStructure;

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);

    // PA6 (TIM3_CH1): Input Floating
    GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_6;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
    GPIO_Init(GPIOA, &GPIO_InitStructure);

    // Time Base: 1us tick rate
    TIM_TimeBaseStructure.TIM_Prescaler     = 72 - 1;
    TIM_TimeBaseStructure.TIM_Period        = 0xFFFF;
    TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1;
    TIM_TimeBaseStructure.TIM_CounterMode   = TIM_CounterMode_Up;
    TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure);

    // Configure Input Capture Channel 1
    TIM_ICInitStructure.TIM_Channel     = TIM_Channel_1;
    TIM_ICInitStructure.TIM_ICPolarity  = TIM_ICPolarity_Rising; // Rising edge capture
    TIM_ICInitStructure.TIM_ICSelection = TIM_ICSelection_DirectTI;
    TIM_ICInitStructure.TIM_ICPrescaler = TIM_ICPSC_DIV1;
    TIM_ICInitStructure.TIM_ICFilter    = 0x0;
    TIM_ICInit(TIM3, &TIM_ICInitStructure);

    // Enable Capture interrupt
    TIM_ITConfig(TIM3, TIM_IT_CC1, ENABLE);

    // NVIC
    NVIC_InitStructure.NVIC_IRQChannel                   = TIM3_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority        = 0;
    NVIC_InitStructure.NVIC_IRQChannelCmd                = ENABLE;
    NVIC_Init(&NVIC_InitStructure);

    TIM_Cmd(TIM3, ENABLE);
}
```

---

## 6. Những Lỗi Thường Gặp Khi Sử Dụng Input Capture

> [!WARNING]
> **1. Bỏ sót hiện tượng tràn Timer khi đo khoảng cách xa:**
> Khi vật cản ở quá xa hoặc không có vật cản (sóng không dội về), chân ECHO sẽ giữ mức High trong khoảng 30ms - 40ms. Nếu giá trị bộ đếm bị tràn từ `0xFFFF` về `0` nhiều lần trước khi có cạnh xuống, kết quả đo sẽ bị sai lệch hoàn toàn. Bạn cần đếm thêm số lần xảy ra ngắt tràn `Update Event (UIF)` để cộng bù thời gian.

> [!IMPORTANT]
> **2. Xóa cờ ngắt Capture đúng cách:**
> Trong thư viện SPL, đọc thanh ghi `TIM_GetCapture1(TIM3)` sẽ **tự động xóa cờ `CC1IF` bằng phần cứng**. Nhưng khi lập trình thanh ghi, nếu bạn không đọc thanh ghi `CCR1`, bạn bắt buộc phải xóa thủ công bằng lệnh `TIM3->SR &= ~(1 << 1)`.

---

## 7. Bài Tập Thực Hành

1. **Bài tập 1 (Đo tần số máy phát xung)**: Kết nối chân PA6 với một chân phát xung PWM bất kỳ. Viết chương trình đo tần số thực tế của tín hiệu xung từ 10Hz đến 50kHz và hiển thị sai số.
2. **Bài tập 2 (Cảm biến lùi xe ô tô)**: Kết hợp cảm biến siêu âm HC-SR04 với một còi Buzzer (phát xung PWM). Khoảng cách càng gần vật cản (S < 30cm → 5cm), tần suất còi bíp bíp kêu càng dồn dập, và khi S < 5cm thì còi kêu liên tục.
3. **Bài tập 3 (Chế độ PWM Input Mode phần cứng)**: Tìm hiểu tính năng phần cứng đặc biệt **PWM Input Mode** của STM32 (sử dụng đồng thời cả 2 kênh CH1 và CH2 kết nối cùng vào 1 chân TI1). Chế độ này cho phép đo đồng thời cả chu kỳ T và Duty Cycle mà không cần đổi cực tính thủ công trong ngắt!
