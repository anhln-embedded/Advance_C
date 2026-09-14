# BÀI 03: HỆ THỐNG XUNG NHỊP (RCC & CLOCK TREE 72MHZ)

Chào mừng bạn đến với bài học thứ 3 trong khóa học **Lập trình STM32F103 chuyên sâu**. Xung nhịp (Clock) được ví như "trái tim" của vi điều khiển. Nếu không có xung nhịp, CPU và các ngoại vi sẽ hoàn toàn ngừng hoạt động. Nếu xung nhịp bị cấu hình sai, tốc độ baud UART sẽ lệch, thời gian trễ Timer sẽ sai và hệ thống có thể bị treo ngay khi khởi động.

Trong bài này, chúng ta sẽ mổ xẻ toàn diện **Cây phân phối xung nhịp (Clock Tree)** của STM32F103, hiểu rõ cách cấu hình Flash Latency, và tự tay viết hàm đưa hệ thống lên tốc độ cực đại **72MHz** bằng cả Thanh ghi thuần (Bare-metal) và Thư viện chuẩn (SPL).

---

## 1. Tổng Quan Các Nguồn Xung Nhịp (Clock Sources)

STM32F103 có 5 nguồn xung nhịp chính, chia thành 2 nhóm:

<p align="center">
  <img src="images/bai03_clock_tree.svg" width="920" alt="Sơ đồ cây xung nhịp STM32F103 Clock Tree">
</p>

1. **HSI (High-Speed Internal)**: Mạch dao động RC nội tần số 8MHz. Sai số khoảng ±1% ở nhiệt độ phòng. Đây là nguồn xung mặc định cấp cho CPU ngay sau khi chip vừa được cấp nguồn hoặc vừa Reset.
2. **HSE (High-Speed External)**: Dao động từ thạch anh ngoài (trên mạch Blue Pill là thạch anh ống kim loại 8.000MHz). Độ ổn định và chính xác rất cao, bắt buộc phải dùng cho các giao tiếp tốc độ cao như USB, CAN.
3. **PLL (Phase-Locked Loop)**: Bộ nhân tần số phần cứng. Tín hiệu đầu vào từ HSI/2 hoặc HSE, sau đó nhân lên từ 2 đến 16 lần để tạo ra xung nhịp hệ thống (SYSCLK) tối đa **72MHz**.
4. **LSI (Low-Speed Internal)**: Dao động RC nội tần số khoảng 30kHz đến 60kHz (danh định 40kHz), dùng làm nguồn chạy độc lập cho khối Independent Watchdog (IWDG) và RTC khẩn cấp.
5. **LSE (Low-Speed External)**: Thạch anh ngoài 32.768kHz (thạch anh nhỏ trên board Blue Pill), chuyên cấp cho khối đồng hồ thời gian thực RTC (Real-Time Clock) để duy trì giờ/ngày chính xác khi ngủ đông.

---

## 2. Phân Tích Cây Phân Phối Xung Nhịp (Clock Tree)

Dưới đây là lưu đồ đường truyền xung nhịp từ nguồn phát tới các bus nội:

<p align="center">
  <img src="images/bai03_clock_tree.svg" alt="Sơ đồ cây phân phối xung nhịp STM32F103 Clock Tree (RM0008)" width="100%" />
  <br>
  <em>Hình 3.1: Sơ đồ cây phân phối xung nhịp STM32F103 (Cấu hình chuẩn 72MHz từ thạch anh 8MHz HSE)</em>
</p>


### 2.1 Giới hạn tốc độ các Bus chính:
- **SYSCLK (System Clock)**: Tối đa **72MHz**.
- **AHB Bus (HCLK)**: Tối đa **72MHz** (cấp cho Core CPU, DMA, Bộ nhớ Flash, SRAM).
- **APB2 Bus (PCLK2 - Xung ngoại vi tốc độ cao)**: Tối đa **72MHz** (cấp cho GPIOA/B/C/D, USART1, SPI1, TIM1, ADC1, ADC2, AFIO).
- **APB1 Bus (PCLK1 - Xung ngoại vi tốc độ thấp)**: Tối đa **36MHz** (cấp cho TIM2, TIM3, TIM4, USART2, USART3, I2C1, I2C2, SPI2, CAN, USB, WWDG).
- **ADC Prescaler**: Bộ chia xung cho ADC từ APB2 (`/2, /4, /6, /8`). Tần số vào bộ biến đổi ADC **tuyệt đối không được vượt quá 14MHz** (chuẩn là 72MHz / 6 = 12MHz).

> [!IMPORTANT]
> **Quy tắc nhân đôi xung nhịp Timer trên Bus APB1:**
> Nếu hệ số chia của APB1 Prescaler = 1, tần số cấp cho các Timer (TIM2, TIM3, TIM4) bằng chính tần số APB1.
> Nhưng nếu hệ số chia của APB1 Prescaler > 1 (ví dụ chia 2 để đưa từ 72MHz xuống 36MHz), phần cứng tự động kích hoạt bộ nhân đôi tần số (×2) cho khối Timer. Do đó, **xung nhịp của TIM2, TIM3, TIM4 vẫn chạy ở tốc độ 72MHz**!

---

## 3. Flash Memory Latency (Độ Trễ Đọc Bộ Nhớ Flash)

Lõi vi điều khiển ARM Cortex-M3 có thể chạy ở tốc độ 72MHz, nhưng chip nhớ Flash nội (chứa mã lệnh chương trình) lại có tốc độ truy xuất chậm hơn (~24MHz).
Để CPU không đọc phải dữ liệu rác khi đang chạy tốc độ cao, STM32F103 tích hợp bộ điều khiển Flash (`FLASH_ACR`) với cơ chế **Wait States (Chu kỳ chờ)**:

| Tần số SYSCLK | Số chu kỳ chờ (Wait States) | Giá trị ghi vào `FLASH_ACR` (Bits `LATENCY[2:0]`) |
| :--- | :---: | :---: |
| 0 < SYSCLK ≤ 24MHz | 0 Wait State | `000` (`0x00`) |
| 24MHz < SYSCLK ≤ 48MHz | 1 Wait State | `001` (`0x01`) |
| 48MHz < SYSCLK ≤ 72MHz | 2 Wait States | `010` (`0x02`) |

> [!CAUTION]
> **Nguyên tắc sống còn:**
> Trước khi chuyển nguồn xung hệ thống SYSCLK lên 72MHz, bạn **bắt buộc phải cấu hình 2 Wait States và bật bộ đệm nạp trước lệnh (Prefetch Buffer)** trong thanh ghi `FLASH->ACR`. Nếu chuyển sang 72MHz trước khi tăng chu kỳ chờ, chip sẽ lập tức văng vào **HardFault Handler** và treo vĩnh viễn!

---

## 4. Các Thanh Ghi RCC Theo RM0008

Địa chỉ cơ sở của RCC: `0x4002 1000`.

| Thanh Ghi | Offset | Bit Quan Trọng | Mô Tả |
| :--- | :---: | :--- | :--- |
| **`RCC_CR`** | `0x00` | `HSEON` (Bit 16)<br>`HSERDY` (Bit 17)<br>`PLLON` (Bit 24)<br>`PLLRDY` (Bit 25) | Bật/tắt các bộ dao động và kiểm tra cờ sẵn sàng (Ready flags). |
| **`RCC_CFGR`** | `0x04` | `SW[1:0]` (Bit 0-1)<br>`SWS[1:0]` (Bit 2-3)<br>`HPRE[3:0]` (Bit 4-7)<br>`PPRE1[2:0]` (Bit 8-10)<br>`PPRE2[2:0]` (Bit 11-13)<br>`PLLSRC` (Bit 16)<br>`PLLMUL[3:0]` (Bit 18-21)<br>`MCO[2:0]` (Bit 24-26) | Chọn nguồn SYSCLK, thiết lập tỉ lệ chia AHB, APB1, APB2, chọn hệ số nhân PLL (x2 đến x16) và cấu hình chân xuất xung MCO. |
| **`RCC_CIR`** | `0x08` | Các cờ ngắt xung nhịp | Clock Interrupt Register. |
| **`RCC_APB2ENR`**| `0x18` | `AFIOEN`, `IOPAEN`.. | Cấp xung ngoại vi trên bus APB2. |
| **`RCC_APB1ENR`**| `0x1C` | `TIM2EN`, `USART2EN`.. | Cấp xung ngoại vi trên bus APB1. |

---

## 5. Quy Trình Cấu Hình SYSCLK Lên 72MHz Từ Thạch Anh 8MHz

Trình tự cấu hình an toàn từng bước:
1. Bật thạch anh ngoài HSE (`HSEON = 1`).
2. Chờ cho đến khi cờ `HSERDY` báo thạch anh đã dao động ổn định.
3. Cấu hình độ trễ Flash: 2 Wait States (`LATENCY = 2`) và bật Prefetch Buffer.
4. Cấu hình các bộ chia bus:
   - AHB Prescaler = 1 (`HCLK = SYSCLK = 72MHz`).
   - APB2 Prescaler = 1 (`PCLK2 = 72MHz`).
   - APB1 Prescaler = 2 (`PCLK1 = 36MHz`).
5. Cấu hình PLL: Nguồn từ HSE, nhân tần 9 lần (8MHz × 9 = 72MHz).
6. Bật bộ nhân tần PLL (`PLLON = 1`) và chờ cờ `PLLRDY = 1`.
7. Chuyển nguồn xung hệ thống (SYSCLK) sang PLL (`SW = 10b`).
8. Chờ đến khi cờ trạng thái xác nhận SYSCLK đã chuyển sang PLL thành công (`SWS = 10b`).

---

## 6. Triển Khai Mã Nguồn Thực Chiến

### PHƯƠNG PHÁP 1: TỰ VIẾT BẰNG THANH GHI BARE-METAL REGISTER

File: `main.c`

```c
#include "stm32f10x.h"

void SystemClock_Config_72MHz(void)
{
    // 1. Enable external crystal oscillator (HSE)
    RCC->CR |= (1 << 16); // HSEON = 1

    // 2. Wait until HSE is ready (HSERDY)
    while (!(RCC->CR & (1 << 17)));

    // 3. Configure Flash Latency = 2 wait states and enable Prefetch Buffer
    FLASH->ACR |= (1 << 4);     // PRFTBE = 1 (Prefetch Buffer Enable)
    FLASH->ACR &= ~(0x07 << 0); // Clear LATENCY bits
    FLASH->ACR |= (0x02 << 0);  // LATENCY = 010b (2 Wait States)

    // 4. Set AHB, APB1, APB2 prescalers
    RCC->CFGR &= ~(0x0F << 4);  // HPRE = 0000 -> AHB Prescaler = 1 (HCLK = 72MHz)
    RCC->CFGR |= (0x04 << 8);   // PPRE1 = 100b -> APB1 Prescaler = 2 (PCLK1 = 36MHz)
    RCC->CFGR &= ~(0x07 << 11); // PPRE2 = 000b -> APB2 Prescaler = 1 (PCLK2 = 72MHz)

    // 5. Configure PLL: HSE source, multiply by 9 (8MHz * 9 = 72MHz)
    RCC->CFGR |= (1 << 16);      // PLLSRC = 1 (HSE as PLL input source)
    RCC->CFGR &= ~(1 << 17);     // PLLXTPRE = 0 (HSE not divided by 2)
    RCC->CFGR &= ~(0x0F << 18);  // Clear PLLMUL bits
    RCC->CFGR |= (0x07 << 18);   // PLLMUL = 0111b (Multiplier x9)

    // 6. Enable PLL and wait until stabilized
    RCC->CR |= (1 << 24); // PLLON = 1
    while (!(RCC->CR & (1 << 25))); // Wait for PLLRDY = 1

    // 7. Select PLL as system clock (SYSCLK)
    RCC->CFGR &= ~(0x03 << 0);
    RCC->CFGR |= (0x02 << 0); // SW = 10b (PLL Selected as System Clock)

    // 8. Wait for successful clock switch confirmation via SWS bits
    while ((RCC->CFGR & (0x03 << 2)) != (0x02 << 2));
}

void delay_ms_72mhz(volatile uint32_t ms)
{
    // At 72MHz, this loop takes approximately 1ms
    volatile uint32_t i;
    for (; ms > 0; ms--)
    {
        for (i = 0; i < 7200; i++)
        {
            __NOP();
        }
    }
}

int main(void)
{
    // Configure MCU to run at 72MHz
    SystemClock_Config_72MHz();

    // Enable GPIOC clock and configure PC13 to blink LED
    RCC->APB2ENR |= (1 << 4);
    GPIOC->CRH &= ~(0x0F << 20);
    GPIOC->CRH |= (0x02 << 20);

    while (1)
    {
        GPIOC->BRR = (1 << 13);  // Turn on LED
        delay_ms_72mhz(500);
        GPIOC->BSRR = (1 << 13); // Turn off LED
        delay_ms_72mhz(500);
    }
}
```

---

### PHƯƠNG PHÁP 2: CẤU HÌNH BẰNG THƯ VIỆN CHUẨN SPL

File: `main.c`

```c
#include "stm32f10x.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_flash.h"
#include "stm32f10x_gpio.h"

void SetSysClockTo72_SPL(void)
{
    ErrorStatus HSEStatus;

    // Reset RCC to factory default configuration
    RCC_DeInit();

    // 1. Enable HSE
    RCC_HSEConfig(RCC_HSE_ON);
    HSEStatus = RCC_WaitForHSEStartUp();

    if (HSEStatus == SUCCESS)
    {
        // 2. Enable Prefetch Buffer & set 2 Wait States
        FLASH_PrefetchBufferCmd(FLASH_PrefetchBuffer_Enable);
        FLASH_SetLatency(FLASH_Latency_2);

        // 3. Configure bus clocks
        RCC_HCLKConfig(RCC_SYSCLK_Div1); // AHB = 72MHz
        RCC_PCLK2Config(RCC_HCLK_Div1);  // APB2 = 72MHz
        RCC_PCLK1Config(RCC_HCLK_Div2);  // APB1 = 36MHz (Maximum)

        // 4. Configure PLL: HSE * 9 = 72MHz
        RCC_PLLConfig(RCC_PLLSource_HSE_Div1, RCC_PLLMul_9);

        // 5. Enable PLL & wait for Ready flag
        RCC_PLLCmd(ENABLE);
        while (RCC_GetFlagStatus(RCC_FLAG_PLLRDY) == RESET);

        // 6. Switch SYSCLK to PLL
        RCC_SYSCLKConfig(RCC_SYSCLKSource_PLLCLK);
        while (RCC_GetSYSCLKSource() != 0x08);
    }
    else
    {
        // Fault fallback: If HSE fails, chip continues running on 8MHz HSI
        while (1);
    }
}

int main(void)
{
    SetSysClockTo72_SPL();

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin   = GPIO_Pin_13;
    GPIO_InitStructure.GPIO_Mode  = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_2MHz;
    GPIO_Init(GPIOC, &GPIO_InitStructure);

    while (1)
    {
        GPIO_ResetBits(GPIOC, GPIO_Pin_13);
        for (volatile int i = 0; i < 1000000; i++);
        GPIO_SetBits(GPIOC, GPIO_Pin_13);
        for (volatile int i = 0; i < 1000000; i++);
    }
}
```

---

## 7. Xuất Xung Kiểm Tra Qua Chân MCO (Microcontroller Clock Output)

Làm sao để biết chắc chắn chip đang thực sự chạy đúng 72MHz hay thạch anh 8MHz ngoài có dao động hay không?
STM32F103 cung cấp chân **MCO (PA8)** cho phép đưa trực tiếp tín hiệu xung nhịp nội ra ngoài để cắm vào máy đo hiện sóng (Oscilloscope) hoặc máy phân tích logic:

```c
// Configure PA8 to output SYSCLK / 2 or HSE
void MCO_Output_Config(void)
{
    // 1. Enable clock for GPIOA
    RCC->APB2ENR |= (1 << 2);

    // 2. Configure PA8: Alternate Function Output Push-Pull 50MHz
    GPIOA->CRH &= ~(0x0F << 0);
    GPIOA->CRH |= (0x0B << 0); // MODE8 = 11 (50MHz), CNF8 = 10 (AF-PP)

    // 3. Select MCO output clock source in RCC_CFGR:
    // Bits 26-24:
    // 100: SYSCLK
    // 101: HSI
    // 110: HSE
    // 111: PLL clock / 2 (36MHz)
    RCC->CFGR |= (0x06 << 24); // Output 8MHz HSE directly to PA8 pin
}
```

---

## 8. Hướng Dẫn Debug Trên Keil MDK

1. Khởi động Debug Session (`Ctrl + F5`).
2. Mở cửa sổ kiểm tra xung nhịp: **Peripherals -> Reset and Clock Control (RCC)**.
3. Quan sát các giá trị trạng thái thực tế:
   - Mục **System Clock**: Hiển thị chính xác `72 000 000 Hz`.
   - Mục **HCLK**: Hiển thị `72 000 000 Hz`.
   - Mục **PCLK1**: Hiển thị `36 000 000 Hz`.
   - Cờ `HSERDY` và `PLLRDY` có dấu tích màu xanh (Ready).

---

## 9. Bài Tập Thực Hành

1. **Bài tập 1 (Ép xung an toàn)**: Hãy thử cấu hình hệ số nhân PLL lên × 8 (64MHz) và × 9 (72MHz). Dùng vòng lặp đo thời gian chớp tắt của đèn LED PC13 để so sánh tốc độ thực thi giữa 2 tần số này.
2. **Bài tập 2 (Clock Security System - CSS)**: Tìm hiểu tính năng CSS trong thanh ghi `RCC_CR` (Bit 19: `CSSON`). Viết hàm kích hoạt CSS để vi điều khiển tự động kích hoạt ngắt NMI chuyển về dùng HSI nếu thạch anh HSE đột ngột bị đứt chân hoặc mất dao động.
3. **Bài tập 3 (Đo xung MCO)**: Cấu hình chân PA8 xuất xung PLL chia 2 (36MHz). Cắm chân đo vào Oscilloscope hoặc Logic Analyzer để kiểm tra độ ổn định và đo độ lệch tần số thực tế của thạch anh trên bo mạch của bạn.
