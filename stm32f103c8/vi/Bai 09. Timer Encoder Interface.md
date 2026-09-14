# BÀI 09: TIMER ENCODER INTERFACE - ĐỌC ENCODER PHẦN CỨNG

Chào mừng bạn đến với bài học thứ 9 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Trong các hệ thống điều khiển tự động hóa, robot và xe tự hành (AGV), **Bộ mã hóa xung quay (Rotary Encoder)** là cảm biến quan trọng nhất để đo lường chính xác vị trí góc và vận tốc của động cơ.

Nếu sử dụng ngắt ngoài GPIO (EXTI) để đọc xung encoder, khi động cơ quay tốc độ cao (hàng nghìn xung mỗi giây), CPU sẽ bị "nghẹt thở" vì phải liên tục nhảy vào ngắt. May mắn thay, các Timer của STM32F103 được tích hợp sẵn mạch phần cứng chuyên dụng mang tên **Encoder Interface**, tự động giải mã chiều quay và tăng/giảm bộ đếm **hoàn toàn bằng phần cứng mà không tiêu tốn một chu kỳ CPU nào**!

---

## 1. Nguyên Lý Tín Hiệu Encoder Cặp Pha Vuông Góc (Quadrature Signals)

Một Rotary Encoder tiêu chuẩn (dạng quang học hoặc từ tính) xuất ra 2 kênh xung số **Phase A (TI1)** và **Phase B (TI2)** có dạng sóng lệch pha nhau đúng **90 độ điện (90^°)**:

<p align="center">
  <img src="images/bai09_encoder_signals.svg" width="100%" alt="Tín hiệu Encoder vuông góc và khối giải mã phần cứng">
  <br>
  <em>Hình 9.1: Dạng sóng lệch pha 90° của tín hiệu Encoder và sơ đồ khối giải mã phần cứng trong Timer</em>
</p>

### 1.1 Xác định chiều quay:
- **Quay thuận (CW)**: Khi TI1 có cạnh lên thì TI2 đang ở mức `0`. Bộ đếm **TĂNG**.
- **Quay nghịch (CCW)**: Khi TI1 có cạnh lên thì TI2 đang ở mức `1`. Bộ đếm **GIẢM**.

### 1.2 Các chế độ nhân độ phân giải:
1. **Chế độ X1 (Encoder Mode 1)**: Chỉ đếm trên các cạnh của kênh TI1.
2. **Chế độ X2 (Encoder Mode 2)**: Chỉ đếm trên các cạnh của kênh TI2.
3. **Chế độ X4 (Encoder Mode 3 - Khuyến nghị)**: Đếm trên **cả 2 cạnh (lên và xuống) của cả 2 kênh TI1 và TI2**.
   - *Ưu điểm*: Tăng độ phân giải của Encoder lên gấp 4 lần! Ví dụ encoder loại 100 xung/vòng (PPR) sẽ cho ra **400 xung đếm/vòng (CPR)**.

---

## 2. Khối Encoder Interface Trong STM32 Timer

Khối Timer của STM32F103 (TIM2, TIM3, TIM4) có mạch logic giải mã trực tiếp nối từ 2 chân Input TI1 và TI2 vào bộ đếm `TIMx_CNT` như minh họa ở sơ đồ phần cứng trên:
- Tín hiệu qua khối lọc số `IC1F`/`IC2F` chống dội tiếp điểm quang/từ tính.
- Khối phần cứng tự động tăng/giảm `TIMx_CNT` mà không cần bất kỳ hàm ngắt phần mềm nào.

- Không cần dùng bất kỳ hàm ngắt phần mềm nào.
- Bộ đếm `TIMx_CNT` tự động tăng khi quay theo chiều kim đồng hồ và tự động giảm khi quay ngược chiều kim đồng hồ.
- Bit **`DIR`** trong thanh ghi `TIMx_CR1` tự động cập nhật: `0` = Đang quay tiến, `1` = Đang quay lùi.

---

## 3. Các Thanh Ghi Điều Khiển Encoder Theo RM0008

| Thanh Ghi | Offset | Bit Quan Trọng | Chức Năng |
| :--- | :---: | :--- | :--- |
| **`TIMx_SMCR`** | `0x08` | `SMS[2:0]` (Bits 0-2) | **Slave Mode Control Register**:<br>- `001`: Encoder Mode 1 (Đếm theo TI1).<br>- `010`: Encoder Mode 2 (Đếm theo TI2).<br>- **`011`**: **Encoder Mode 3 (Đếm cả 2 cạnh TI1 và TI2 - Mode X4)**. |
| **`TIMx_CCMR1`**| `0x18` | `CC1S[1:0]`, `CC2S[1:0]`<br>`IC1F[3:0]`, `IC2F[3:0]` | Cấu hình TI1 và TI2 làm ngõ vào và thiết lập **bộ lọc nhiễu số phần cứng (Digital Filter)**. |
| **`TIMx_CCER`** | `0x20` | `CC1P`, `CC2P` | Đảo cực tính xung (Nếu encoder quay thuận mà bộ đếm lại giảm, chỉ cần đảo bit `CC1P` để đảo chiều đếm mà không cần đảo dây nối phần cứng). |
| **`TIMx_CNT`**  | `0x24` | Bits [15:0] | Giá trị đếm vị trí xung hiện tại. |

---

## 4. Triển Khai Mã Nguồn Thực Chiến

### Kịch bản thực hành:
- Sử dụng **TIM4** để đọc Encoder.
- Chân **PB6** nối kênh Phase A (TIM4_CH1).
- Chân **PB7** nối kênh Phase B (TIM4_CH2).
- Bật điện trở kéo lên nội (Pull-up) cho PB6 và PB7.
- Sử dụng chế độ **Encoder Mode 3 (X4)** có bật bộ lọc số chống rung phím cơ học.
- Mỗi lần xoay núm Encoder, giá trị `TIM4->CNT` thay đổi, nếu quay sang phải thì LED PC13 chớp tắt nhanh, quay sang trái thì LED chớp tắt chậm.

---

### PHƯƠNG PHÁP 1: BARE-METAL REGISTER & CMSIS

File: `main.c`

```c
#include "stm32f10x.h"

void Encoder_TIM4_Init_Register(void)
{
    // 1. Enable clocks for GPIOB and TIM4
    RCC->APB2ENR |= (1 << 3); // IOPBEN = 1
    RCC->APB1ENR |= (1 << 2); // TIM4EN = 1

    // 2. Configure PB6 and PB7: Input with Pull-Up
    // PB6 (TIM4_CH1): MODE6 = 00b, CNF6 = 10b
    GPIOB->CRL &= ~(0x0F << 24);
    GPIOB->CRL |= (0x08 << 24);
    GPIOB->ODR |= (1 << 6); // Pull-up PB6

    // PB7 (TIM4_CH2): MODE7 = 00b, CNF7 = 10b
    GPIOB->CRL &= ~(0x0F << 28);
    GPIOB->CRL |= (0x08 << 28);
    GPIOB->ODR |= (1 << 7); // Pull-up PB7

    // 3. Map input channels CC1S and CC2S in CCMR1
    TIM4->CCMR1 &= ~((0x03 << 0) | (0x03 << 8));
    TIM4->CCMR1 |= (0x01 << 0) | (0x01 << 8); // CC1S = 01b (TI1), CC2S = 01b (TI2)

    // 4. Configure hardware digital filter (Filter = 6 clock cycles)
    TIM4->CCMR1 |= (0x06 << 4) | (0x06 << 12); // IC1F = 0110b, IC2F = 0110b

    // 5. Configure polarity (Non-inverted: CC1P = 0, CC2P = 0)
    TIM4->CCER &= ~((1 << 1) | (1 << 5));

    // 6. Configure Encoder Mode 3 (X4: Count on both TI1 and TI2 edges)
    TIM4->SMCR &= ~(0x07 << 0);
    TIM4->SMCR |= (0x03 << 0); // SMS = 011b (Encoder Mode 3)

    // 7. Configure ARR auto-reload register limit
    TIM4->ARR = 0xFFFF; // Max count 65535
    TIM4->CNT = 0;      // Set initial position to 0

    // 8. Enable Timer operation
    TIM4->CR1 |= (1 << 0); // CEN = 1
}

int16_t Encoder_GetCount(void)
{
    return (int16_t)TIM4->CNT;
}

uint8_t Encoder_GetDirection(void)
{
    // Read DIR bit in TIM4_CR1: 0 = Forward (Up), 1 = Reverse (Down)
    return (TIM4->CR1 & (1 << 4)) ? 1 : 0;
}

int main(void)
{
    // Configure LED PC13
    RCC->APB2ENR |= (1 << 4);
    GPIOC->CRH &= ~(0x0F << 20);
    GPIOC->CRH |= (0x02 << 20);

    Encoder_TIM4_Init_Register();

    int16_t last_count = 0;

    while (1)
    {
        int16_t current_count = Encoder_GetCount();

        if (current_count != last_count)
        {
            last_count = current_count;
            // Toggle LED upon encoder rotation
            GPIOC->ODR ^= (1 << 13);
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
#include "stm32f10x_tim.h"

void Encoder_TIM4_Init_SPL(void)
{
    GPIO_InitTypeDef        GPIO_InitStructure;
    TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;

    // 1. Enable clocks
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM4, ENABLE);

    // 2. Pins PB6, PB7: Input Pull-Up
    GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_6 | GPIO_Pin_7;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_Init(GPIOB, &GPIO_InitStructure);

    // 3. Initialize Time-base
    TIM_TimeBaseStructure.TIM_Prescaler     = 0; // Prescaler /1 (Direct edge counting)
    TIM_TimeBaseStructure.TIM_Period        = 0xFFFF;
    TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1;
    TIM_TimeBaseStructure.TIM_CounterMode   = TIM_CounterMode_Up;
    TIM_TimeBaseInit(TIM4, &TIM_TimeBaseStructure);

    // 4. Enable hardware Encoder Interface
    TIM_EncoderInterfaceConfig(TIM4, 
                               TIM_EncoderMode_TI12,           // Mode X4
                               TIM_ICPolarity_Rising,          // TI1 polarity
                               TIM_ICPolarity_Rising);         // TI2 polarity

    // 5. Configure digital filter
    TIM_SetIC1Prescaler(TIM4, TIM_ICPSC_DIV1);
    TIM_SetIC2Prescaler(TIM4, TIM_ICPSC_DIV1);

    // 6. Reset counter and enable Timer
    TIM_SetCounter(TIM4, 0);
    TIM_Cmd(TIM4, ENABLE);
}

int main(void)
{
    Encoder_TIM4_Init_SPL();

    while (1)
    {
        uint16_t pulse = TIM_GetCounter(TIM4);
        // Process encoder tick counts
    }
}
```

---

## 5. Thuật Toán Tính Tốc Độ Vòng Quay Động Cơ (RPM)

Để tính tốc độ động cơ theo đơn vị vòng/phút (Revolutions Per Minute - RPM):
1. Thiết lập một Timer khác (ví dụ TIM2 hoặc SysTick) tạo ngắt định kỳ lấy mẫu thời gian: Δ t = 100ms = 0.1s.
2. Trong hàm ngắt định kỳ:
   - Đọc số xung đếm được: Δ Pulses = CNT - CNT_old.
   - Cập nhật lại CNT_old = CNT.
   - Biết Encoder có N xung/vòng (sau khi nhân 4 là 4N xung/vòng):

RPM = (Δ Pulses / 4N) × (60 / Δ t) = (Δ Pulses × 600 / 4N)

---

## 6. Những Lưu Ý Quan Trọng Khi Sử Dụng Encoder Interface

> [!TIP]
> **Khử nhiễu phím cơ học (Rotary Encoder núm vặn):**
> Các núm vặn Encoder cơ học rẻ tiền (như module KY-040) tạo ra nhiễu tiếp điểm cơ khí rất lớn. Bạn bắt buộc phải cấu hình các bit lọc số `IC1F` và `IC2F` lên mức tối thiểu là `0110b` (hoặc `1111b`), hoặc lắp thêm 2 tụ gốm 100nF nối từ chân A/B xuống GND để hấp thụ gai nhiễu.

> [!WARNING]
> **Xử lý số âm khi quay ngược chiều:**
> Khi bộ đếm đang ở mức `0` mà xoay ngược chiều kim đồng hồ, giá trị `CNT` 16-bit sẽ bị tràn lùi (Underflow) về `65535` (`0xFFFF`). Nếu muốn lưu trữ giá trị vị trí có cả số âm và số dương, hãy ép kiểu giá trị `TIMx->CNT` sang kiểu số nguyên có dấu `int16_t`!

---

## 7. Bài Tập Thực Hành

1. **Bài tập 1 (Menu điều hướng trên màn hình)**: Dùng Encoder xoay để điều hướng thanh cuộn menu trên màn hình OLED hoặc cổng UART: xoay phải menu cuộn xuống, xoay trái menu cuộn lên, nhấn nút trung tâm của encoder để chọn mục.
2. **Bài tập 2 (Bộ đo vận tốc động cơ DC)**: Kết nối một động cơ giảm tốc có gắn Encoder đĩa từ (ví dụ động cơ GA25 hoặc JGB37). Viết chương trình đo tốc độ RPM thực tế và xuất ra cổng UART mỗi 200ms.
3. **Bài tập 3 (Khóa góc quay servo theo encoder)**: Kết hợp bài PWM Servo và bài Encoder: Khi người dùng xoay núm Encoder từ 0 đến 100 xung, tay gắp động cơ Servo SG90 sẽ quay theo một góc tương ứng từ 0^° đến 180^° theo thời gian thực.
