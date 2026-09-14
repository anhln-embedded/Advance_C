# BÀI 06: GENERAL PURPOSE TIMER (TIM2 - TIM4)

Chào mừng bạn đến với bài học thứ 6 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Ở bài 5, chúng ta đã tìm hiểu SysTick Timer - một timer 24-bit cơ bản của lõi ARM. Tuy nhiên, để xử lý các tác vụ phức tạp của thế giới nhúng như đo xung, phát xung PWM, điều khiển động cơ hay định thời nhiều kênh độc lập, chúng ta cần đến các **Bộ định thời đa năng (General Purpose Timers - TIM2, TIM3, TIM4)**.

Trong bài học này, bạn sẽ nắm vững cấu trúc khối cơ sở thời gian (**Time-base Generator**), cơ chế thanh ghi bóng (**Shadow Registers**), công thức tính toán tần số ngắt chính xác tuyệt đối và triển khai bằng cả Bare-metal Register lẫn Thư viện chuẩn SPL.

---

## 1. Tổng Quan Phân Loại Timer Trên STM32F103C8T6

Vi điều khiển STM32F103C8T6 tích hợp 4 khối Timer phần cứng:

<p align="center">
  <img src="images/bai06_timer_architecture.svg" width="940" alt="Kiến trúc ngoại vi General Purpose Timer TIM2 - TIM5">
</p>

Trong bài này, chúng ta tập trung vào **TIM2, TIM3, TIM4** – bộ 3 Timer đa năng mạnh mẽ và được sử dụng nhiều nhất trên bus **APB1**.

---

## 2. Cấu Trúc Khối Time-Base Generator

Cốt lõi của mọi bộ định thời là khối **Time-base Generator** gồm 3 thanh ghi 16-bit chính:

<p align="center">
  <img src="images/bai06_timer_timebase.svg" width="900" alt="Nguyên lý hoạt động khối Time-Base Generator Timer">
</p>

### 2.1 Ba thanh ghi trụ cột:
1. **`TIMx_PSC` (Prescaler Register - 16-bit)**:
   - Chia tần số xung đầu vào f_TIM_CLK cho (PSC + 1) để tạo ra xung nhịp nhịp đếm f_CK_CNT:
     f_CK_CNT = (f_TIM_CLK / PSC + 1)
   - Giá trị có thể cấu hình từ `0` đến `65535`.
2. **`TIMx_CNT` (Counter Register - 16-bit)**:
   - Lưu trữ giá trị đếm hiện tại. Chạy tăng dần từ `0` lên `ARR` (ở chế độ Up-counting) hoặc giảm dần từ `ARR` về `0` (ở chế độ Down-counting).
3. **`TIMx_ARR` (Auto-Reload Register - 16-bit)**:
   - Xác định giá trị cực đại mà bộ đếm sẽ đạt tới trước khi tràn quay về 0 (chu kỳ của Timer).
   - Giá trị có thể cấu hình từ `0` đến `65535`.

---

## 3. Cơ Chế Thanh Ghi Bóng (Shadow Registers) & Preload

Một điểm đặc biệt trong kiến trúc Timer của STM32 là cơ chế **Shadow Register**:
- Các thanh ghi `PSC` và `ARR` thực tế gồm 2 tầng: **Thanh ghi tiền nạp (Preload Register)** mà lập trình viên có thể đọc/ghi, và **Thanh ghi bóng (Shadow Register)** được phần cứng trực tiếp sử dụng để đếm.
- Khi bạn ghi một giá trị mới vào `ARR`, giá trị đó chưa tác động ngay lập tức vào bộ đếm hiện tại. Chỉ khi xuất hiện một **Sự kiện cập nhật (Update Event - UEV)** (ví dụ khi đếm tràn), giá trị mới từ Preload Register mới được chuyển vào Shadow Register.
- Cơ chế này giúp ngăn chặn hiện tượng tạo xung méo dạng hoặc ngắt sai nhịp khi ta cập nhật chu kỳ Timer giữa chừng lúc nó đang chạy.

---

## 4. Công Thức Tính Tần Số Và Thời Gian Ngắt Tràn Timer

Xung nhịp cấp cho TIM2 - TIM4 từ bus APB1 luôn là **f_TIM_CLK = 72MHz** (nhờ bộ nhân đôi xung khi hệ số chia APB1 Prescaler = 2).

Tần số xảy ra sự kiện tràn Update Event (f_Update) được tính theo công thức:

f_Update = (f_TIM_CLK / (PSC + 1) × (ARR + 1))

Chu kỳ thời gian giữa hai lần ngắt (T_Update):

T_Update = (1 / f_Update) = ((PSC + 1) × (ARR + 1) / f_TIM_CLK)

### Ví dụ thực tế: Cấu hình ngắt chính xác 1 giây (T = 1s, f = 1Hz)
- Chúng ta có f_TIM_CLK = 72,000,000 Hz.
- Cần (PSC + 1) × (ARR + 1) = 72,000,000.
- Chọn hệ số chia tần `PSC = 7199` → (PSC + 1) = 7200.
  Lúc này, tần số đếm nhịp f_CK_CNT = (72,000,000 / 7200) = 10,000 Hz (tức mỗi nhịp đếm mất đúng 0.1ms).
- Suy ra giá trị chu kỳ `ARR`:
  (ARR + 1) = (72,000,000 / 7200) = 10,000 \implies ARR = 9999
- **Kết quả**: Cài đặt `PSC = 7199`, `ARR = 9999` sẽ tạo ra ngắt tràn đúng chính xác **1.0000 giây**!

---

## 5. Các Thanh Ghi Cơ Bản Của Timer Theo RM0008

Địa chỉ cơ sở TIM2: `0x4000 0000`, TIM3: `0x4000 0400`, TIM4: `0x4000 0800`.

| Thanh Ghi | Offset | Bit Quan Trọng | Mô Tả |
| :--- | :---: | :--- | :--- |
| **`TIMx_CR1`** | `0x00` | `CEN` (Bit 0)<br>`UDIS` (Bit 1)<br>`URS` (Bit 2)<br>`DIR` (Bit 4)<br>`ARPE` (Bit 7) | **Control Register 1**:<br>- `CEN`: 1 để kích hoạt bộ đếm chạy.<br>- `DIR`: 0 = Đếm lên (Up), 1 = Đếm xuống (Down).<br>- `ARPE`: 1 để bật tính năng Auto-reload preload. |
| **`TIMx_DIER`**| `0x0C` | `UIE` (Bit 0)<br>`UDE` (Bit 8) | **DMA/Interrupt Enable Register**:<br>- `UIE`: 1 để cho phép ngắt tràn Update Interrupt. |
| **`TIMx_SR`**  | `0x10` | `UIF` (Bit 0) | **Status Register**:<br>- `UIF`: Cờ báo ngắt tràn (Ghi `0` vào bit này để xóa cờ). |
| **`TIMx_EGR`** | `0x14` | `UG` (Bit 0) | **Event Generation Register**:<br>- `UG`: Ghi 1 để tạo sự kiện Update bằng phần mềm (nạp ngay PSC/ARR). |
| **`TIMx_CNT`** | `0x24` | Bits [15:0] | Giá trị đếm tức thời 16-bit. |
| **`TIMx_PSC`** | `0x28` | Bits [15:0] | Giá trị bộ chia tần số Prescaler. |
| **`TIMx_ARR`** | `0x2C` | Bits [15:0] | Giá trị chu kỳ nạp lại Auto-Reload. |

---

## 6. Triển Khai Mã Nguồn Thực Chiến

### Kịch bản:
Sử dụng **TIM2** tạo ngắt định kỳ chính xác **1 giây (1Hz)**. Trong hàm phục vụ ngắt `TIM2_IRQHandler`, ta đảo trạng thái của đèn LED **PC13**.

---

### PHƯƠNG PHÁP 1: BARE-METAL REGISTER & CMSIS

File: `main.c`

```c
#include "stm32f10x.h"

void TIM2_Config_Register(void)
{
    // 1. Enable clocks for TIM2 on APB1 and GPIOC on APB2
    RCC->APB1ENR |= (1 << 0); // TIM2EN = 1
    RCC->APB2ENR |= (1 << 4); // IOPCEN = 1

    // 2. Configure PC13 pin: Output Push-Pull 2MHz
    GPIOC->CRH &= ~(0x0F << 20);
    GPIOC->CRH |= (0x02 << 20);
    GPIOC->BSRR = (1 << 13); // Default: turn off LED

    // 3. Configure TIM2 time-base for 1-second interrupt (1Hz)
    // f_CK_CNT = 72MHz / (7199 + 1) = 10kHz
    TIM2->PSC = 7200 - 1;

    // Overflow period: 10000 ticks / 10kHz = 1 second
    TIM2->ARR = 10000 - 1;

    // Reset counter to 0
    TIM2->CNT = 0;

    // 4. Enable Update Interrupt Enable (UIE)
    TIM2->DIER |= (1 << 0); // UIE = 1

    // 5. Configure NVIC for TIM2 interrupt channel
    NVIC_SetPriority(TIM2_IRQn, 1); // Interrupt priority level 1
    NVIC_EnableIRQ(TIM2_IRQn);       // Enable TIM2 interrupt in NVIC

    // 6. Enable timer counter (CEN = 1)
    TIM2->CR1 |= (1 << 0);
}

// TIM2 interrupt service routine (ISR)
void TIM2_IRQHandler(void)
{
    // Check Update Interrupt Flag (UIF)
    if (TIM2->SR & (1 << 0))
    {
        // MANDATORY: Clear interrupt flag by writing 0 to UIF bit
        TIM2->SR &= ~(1 << 0);

        // Toggle LED PC13 state
        GPIOC->ODR ^= (1 << 13);
    }
}

int main(void)
{
    TIM2_Config_Register();

    while (1)
    {
        // CPU is completely idle, can enter low-power Sleep mode
        __WFI();
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

void TIM2_Config_SPL(void)
{
    GPIO_InitTypeDef        GPIO_InitStructure;
    TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
    NVIC_InitTypeDef        NVIC_InitStructure;

    // 1. Enable clocks for GPIOC and TIM2
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);

    // 2. Configure PC13: Output Push-Pull
    GPIO_InitStructure.GPIO_Pin   = GPIO_Pin_13;
    GPIO_InitStructure.GPIO_Mode  = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_2MHz;
    GPIO_Init(GPIOC, &GPIO_InitStructure);
    GPIO_SetBits(GPIOC, GPIO_Pin_13);

    // 3. Configure TIM2 time-base: 1Hz (1 second)
    TIM_TimeBaseStructure.TIM_Period        = 10000 - 1; // ARR
    TIM_TimeBaseStructure.TIM_Prescaler     = 7200 - 1;  // PSC
    TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1;
    TIM_TimeBaseStructure.TIM_CounterMode   = TIM_CounterMode_Up; // Upcounter mode
    TIM_TimeBaseInit(TIM2, &TIM_TimeBaseStructure);

    // 4. Enable Update Event interrupt
    TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);

    // 5. Configure NVIC
    NVIC_InitStructure.NVIC_IRQChannel                   = TIM2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority        = 1;
    NVIC_InitStructure.NVIC_IRQChannelCmd                = ENABLE;
    NVIC_Init(&NVIC_InitStructure);

    // 6. Enable TIM2
    TIM_Cmd(TIM2, ENABLE);
}

void TIM2_IRQHandler(void)
{
    if (TIM_GetITStatus(TIM2, TIM_IT_Update) != RESET)
    {
        // Toggle PC13 pin state
        if (GPIO_ReadOutputDataBit(GPIOC, GPIO_Pin_13) == Bit_SET)
        {
            GPIO_ResetBits(GPIOC, GPIO_Pin_13);
        }
        else
        {
            GPIO_SetBits(GPIOC, GPIO_Pin_13);
        }

        // Clear Update interrupt flag
        TIM_ClearITPendingBit(TIM2, TIM_IT_Update);
    }
}

int main(void)
{
    TIM2_Config_SPL();

    while (1)
    {
        __WFI();
    }
}
```

---

## 7. Những Lưu Ý Sống Còn Về Phần Cứng & Phần Mềm

> [!CAUTION]
> **1. Quy tắc xóa cờ ngắt Timer:**
> Khác với EXTI (xóa cờ bằng cách ghi bit 1 vào `EXTI_PR`), trong thanh ghi trạng thái của Timer **`TIMx_SR`**, cờ ngắt `UIF` được xóa bằng cách **ghi bit 0** (`TIMx->SR &= ~(1 << 0)`). Nếu bạn ghi `1` vào, cờ vẫn giữ nguyên mức 1 và hàm ISR sẽ bị gọi đệ quy liên tục gây treo chương trình!

> [!WARNING]
> **2. Xung đột sự kiện Update giả khi vừa khởi tạo:**
> Khi gọi hàm khởi tạo `TIM_TimeBaseInit()` trong thư viện SPL, hàm này sẽ sinh ra một lệnh cập nhật phần mềm (`TIMx->EGR = TIM_PSCReloadMode_Immediate`) để nạp giá trị Prescaler vào thanh ghi bóng ngay tức khắc. Lệnh này vô tình kích hoạt luôn cờ `UIF` lên mức 1 trước cả khi bạn bật Timer!
> Do đó, hãy luôn gọi `TIM_ClearFlag(TIMx, TIM_FLAG_Update)` ngay trước khi gọi `TIM_ITConfig()` để tránh một ngắt giả bị kích hoạt ngay lập tức lúc vừa bật chip.

---

## 8. Hướng Dẫn Debug Trên Keil MDK

1. Khởi động Debug (`Ctrl + F5`).
2. Mở cửa sổ ngoại vi Timer: **Peripherals -> General Purpose Timers -> TIM2**.
3. Bạn sẽ quan sát được các thông số trực quan:
   - **Counter**: Con số tăng liên tục từ `0` đến `9999`.
   - **Prescaler**: Giá trị `7199`.
   - **Auto-Reload**: Giá trị `9999`.
   - Khi `Counter` chạm mốc `9999`, bit `UIF` trong thanh ghi Status chớp sáng và thanh ghi Counter tự động Reset về 0.

---

## 9. Bài Tập Thực Hành

1. **Bài tập 1 (Đồng hồ bấm giờ Stopwatch)**: Cấu hình TIM3 tạo ngắt chu kỳ đúng **10ms (100Hz)**. Xây dựng đồng hồ bấm giờ hiển thị Giờ : Phút : Giây : Phần trăm giây xuất ra cổng UART hoặc màn hình LCD.
2. **Bài tập 2 (Bộ định thời đa tần số)**: Cấu hình TIM4 chạy với tần số ngắt 1kHz (1ms). Trong hàm ngắt, quản lý 3 biến đếm phần mềm để điều khiển 3 chân GPIO chớp tắt ở các chu kỳ khác nhau: 100ms, 500ms và 2000ms.
3. **Bài tập 3 (Chế độ đếm Center-aligned)**: Tìm hiểu chế độ đếm đồng tâm (`CMS[1:0]` trong `TIMx_CR1`). Cấu hình Timer đếm từ 0 lên ARR rồi đếm ngược từ ARR về 0. Đo đạc xem chu kỳ ngắt thay đổi như thế nào so với chế độ Up-counting thông thường.
