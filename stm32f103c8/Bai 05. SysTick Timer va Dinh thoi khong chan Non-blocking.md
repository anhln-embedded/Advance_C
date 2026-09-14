# BÀI 05: SYSTICK TIMER VÀ ĐỊNH THỜI KHÔNG CHẶN (NON-BLOCKING)

Chào mừng bạn đến với bài học thứ 5 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Ở các bài học trước, chúng ta đã dùng các vòng lặp `for` hoặc `while` rỗng để tạo thời gian trễ (Software Delay). Phương pháp này có 2 nhược điểm chết người:
1. **Không chính xác**: Thời gian trễ thay đổi phụ thuộc vào mức tối ưu hóa của Compiler (-O0, -O2, -O3) và tần số CPU.
2. **Nghẽn CPU (Blocking)**: CPU bị giam cầm trong vòng lặp vô nghĩa, không thể đọc cảm biến, không thể xử lý phím bấm hay nhận dữ liệu UART.

Trong bài học này, chúng ta sẽ khắc phục triệt để vấn đề trên bằng **SysTick Timer** tích hợp sẵn trong lõi ARM Cortex-M3, xây dựng hàm tạo trễ chính xác đến từng micro-giây (µs) và triển khai mô hình đa nhiệm hợp tác không chặn (**Non-blocking Cooperative Multitasking**) theo cơ chế `millis()`.

---

## 1. Cấu Trúc Khối SysTick Timer (System Timer)

**SysTick** là một bộ định thời 24-bit đếm lùi (Down-counter) được ARM thiết kế nằm **ngay bên trong lõi Cortex-M3** (không phải ngoại vi trên bus APB của ST). Mục đích chính của nó là tạo ra nhịp đập thời gian định kỳ (Tick Heartbeat) cho các hệ điều hành thời gian thực như FreeRTOS.

<p align="center">
  <img src="images/bai05_systick_timer.svg" width="900" alt="Kiến trúc đồng hồ định thời cốt lõi SysTick Timer">
</p>

### 1.1 Nguyên lý hoạt động:
- Bộ đếm nạp giá trị từ thanh ghi **`LOAD`** vào thanh ghi hiện tại **`VAL`**.
- Cứ mỗi chu kỳ xung nhịp, giá trị trong **`VAL`** giảm đi 1 đơn vị.
- Khi **`VAL`** đếm chạm mốc `0`, cờ **`COUNTFLAG`** được kéo lên mức `1`. Đồng thời, nếu bật ngắt, hàm `SysTick_Handler()` sẽ được gọi.
- Ngay sau đó, phần cứng tự động nạp lại giá trị từ **`LOAD`** vào **`VAL`** và tiếp tục đếm lùi lặp lại chu trình.

---

## 2. Các Thanh Ghi SysTick Trong Lõi ARM Cortex-M3

SysTick được điều khiển thông qua cấu trúc `SysTick_Type` trong file CMSIS `core_cm3.h`:

| Thanh Ghi | Địa Chỉ Cơ Sở / Offset | Bit Quan Trọng | Mô Tả Chức Năng |
| :--- | :---: | :--- | :--- |
| **`SysTick->CTRL`** | `0xE000 E010` | `ENABLE` (Bit 0)<br>`TICKINT` (Bit 1)<br>`CLKSOURCE` (Bit 2)<br>`COUNTFLAG` (Bit 16) | **Control and Status Register**:<br>- `ENABLE`: 1 để kích hoạt Timer.<br>- `TICKINT`: 1 để sinh ngắt khi đếm về 0.<br>- `CLKSOURCE`: 0 = HCLK/8 (9MHz), 1 = HCLK (72MHz).<br>- `COUNTFLAG`: 1 khi bộ đếm vừa chạm 0 (đọc thanh ghi này sẽ tự động xóa cờ). |
| **`SysTick->LOAD`** | `0xE000 E014` | Bits [23:0] | **Reload Value Register**: Giá trị nạp lại ban đầu (Tối đa 2^{24}-1 = 16,777,215). |
| **`SysTick->VAL`**  | `0xE000 E018` | Bits [23:0] | **Current Value Register**: Giá trị đếm hiện thời (Ghi bất kỳ số nào vào thanh ghi này sẽ xóa nó về 0). |
| **`SysTick->CALIB`**| `0xE000 E01C` | Bits [23:0] | **Calibration Register**: Giá trị hiệu chuẩn xuất xưởng cho nhịp 10ms. |

---

## 3. Xây Dựng Hàm Delay Chính Xác Cấp Thanh Ghi

Giả sử hệ thống chạy ở xung nhịp cực đại **HCLK = 72MHz** và chọn nguồn xung SysTick là `CLKSOURCE = 1` (72MHz):
- Thời gian cho 1 nhịp đếm: T = (1 / 72,000,000) s ≈ 13.88  ns.
- Để đếm được 1 µs: Cần 72 nhịp đếm (1 µs × 72MHz = 72).
- Để đếm được 1 ms: Cần 72,000 nhịp đếm (1ms × 72MHz = 72,000).

```c
#include "stm32f10x.h"

// Initialize polling-based SysTick (using COUNTFLAG)
void SysTick_Init(void)
{
    SysTick->CTRL = 0; // Disable SysTick prior to configuration
    SysTick->VAL  = 0; // Clear current counter value
}

// High-precision microsecond delay function
void delay_us(uint32_t us)
{
    // At 72MHz: 72 clock cycles per microsecond
    SysTick->LOAD = (us * 72) - 1;
    SysTick->VAL  = 0;
    SysTick->CTRL = SysTick_CTRL_CLKSOURCE_Msk | SysTick_CTRL_ENABLE_Msk; // 72MHz HCLK clock source, Enable Timer

    // Wait until COUNTFLAG bit (bit 16) is set to 1
    while (!(SysTick->CTRL & SysTick_CTRL_COUNTFLAG_Msk));

    SysTick->CTRL = 0; // Disable SysTick
}

// Millisecond delay function
void delay_ms(uint32_t ms)
{
    while (ms--)
    {
        delay_us(1000);
    }
}
```

---

## 4. Thiết Kế Đa Nhiệm Bất Đồng Bộ Với Hàm `millis()` (Non-Blocking)

Kỹ thuật Non-blocking cho phép vi điều khiển làm nhiều việc cùng lúc bằng cách kiểm tra mốc thời gian trôi qua thay vì dừng CPU chờ đợi.

### 4.1 Nguyên lý ngắt định kỳ 1ms
Chúng ta cấu hình SysTick sinh ngắt đúng **mỗi 1 mili-giây (1000Hz)**. Mỗi lần ngắt xảy ra, một biến toàn cục `system_millis` sẽ tự động tăng thêm 1 đơn vị:

LOAD = (72,000,000  Hz / 1000  Hz) - 1 = 71,999

```c
volatile uint32_t system_millis = 0;

void SysTick_Handler(void)
{
    system_millis++;
}

uint32_t millis(void)
{
    return system_millis;
}
```

---

## 5. Triển Khai Mã Nguồn Thực Chiến

### Kịch bản thực hành đa nhiệm không chặn:
1. **Task 1**: Chớp tắt đèn LED PC13 chu kỳ đúng 500ms một lần.
2. **Task 2**: Chớp tắt một đèn LED rời ở chân PB0 chu kỳ 100ms một lần (tần số 5Hz).
3. **Task 3**: Liên tục đọc nút nhấn PA0 ngay tức thì mà không bị trễ bởi bất kỳ tác vụ nào ở trên.

---

### PHƯƠNG PHÁP 1: BARE-METAL REGISTER HOÀN TOÀN

File: `main.c`

```c
#include "stm32f10x.h"

volatile uint32_t system_millis = 0;

void SysTick_Handler(void)
{
    system_millis++;
}

uint32_t millis(void)
{
    return system_millis;
}

void SysTick_Config_1ms(void)
{
    // Configure 1ms tick rate at 72MHz: LOAD = 71999
    SysTick->LOAD = 72000 - 1;
    SysTick->VAL  = 0;
    
    // Set SysTick interrupt priority (Lowest priority to yield to critical peripherals)
    NVIC_SetPriority(SysTick_IRQn, 15);

    // Enable: HCLK source (bit 2 = 1), TICKINT enabled (bit 1 = 1), ENABLE (bit 0 = 1)
    SysTick->CTRL = SysTick_CTRL_CLKSOURCE_Msk | 
                    SysTick_CTRL_TICKINT_Msk   | 
                    SysTick_CTRL_ENABLE_Msk;
}

void GPIO_Config(void)
{
    // Enable GPIOC and GPIOB clocks
    RCC->APB2ENR |= (1 << 3) | (1 << 4);

    // PC13: Output Push-Pull 2MHz
    GPIOC->CRH &= ~(0x0F << 20);
    GPIOC->CRH |= (0x02 << 20);

    // PB0: Output Push-Pull 2MHz
    GPIOB->CRL &= ~(0x0F << 0);
    GPIOB->CRL |= (0x02 << 0);
}

int main(void)
{
    GPIO_Config();
    SysTick_Config_1ms();

    uint32_t last_led_pc13_time = 0;
    uint32_t last_led_pb0_time  = 0;

    while (1)
    {
        uint32_t current_time = millis();

        // Task 1: Toggle LED PC13 every 500ms
        if (current_time - last_led_pc13_time >= 500)
        {
            last_led_pc13_time = current_time;
            GPIOC->ODR ^= (1 << 13); // Toggle LED PC13 state
        }

        // Task 2: Fast blink LED PB0 every 100ms
        if (current_time - last_led_pb0_time >= 100)
        {
            last_led_pb0_time = current_time;
            GPIOB->ODR ^= (1 << 0);  // Toggle LED PB0 state
        }

        // CPU is free to execute other tasks here without blocking for a single nanosecond!
    }
}
```

---

### PHƯƠNG PHÁP 2: SỬ DỤNG HÀM CHUẨN CMSIS `SysTick_Config()`

File: `main.c`

```c
#include "stm32f10x.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_gpio.h"

volatile uint32_t ms_ticks = 0;

void SysTick_Handler(void)
{
    ms_ticks++;
}

uint32_t GetTick(void)
{
    return ms_ticks;
}

int main(void)
{
    // Enable peripheral clock for PORT C
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);

    GPIO_InitTypeDef GPIO_InitStruct;
    GPIO_InitStruct.GPIO_Pin   = GPIO_Pin_13;
    GPIO_InitStruct.GPIO_Mode  = GPIO_Mode_Out_PP;
    GPIO_InitStruct.GPIO_Speed = GPIO_Speed_2MHz;
    GPIO_Init(GPIOC, &GPIO_InitStruct);

    // CMSIS standard function: Automatically configures LOAD, enables interrupt and starts SysTick
    // SystemCoreClock holds system frequency (72000000)
    if (SysTick_Config(SystemCoreClock / 1000))
    {
        // Error if reload value exceeds 24-bit range
        while (1);
    }

    uint32_t prev_time = GetTick();

    while (1)
    {
        if (GetTick() - prev_time >= 1000) // 1-second timer delay
        {
            prev_time = GetTick();
            GPIOC->ODR ^= GPIO_Pin_13;
        }
    }
}
```

---

## 6. Những Lỗi Thường Gặp Và Cơ Chế Xử Lý Tràn Biến (Overflow)

> [!TIP]
> **Vấn đề tràn số của biến thời gian 32-bit (`system_millis`):**
> Biến `uint32_t` sẽ bị tràn khi đạt giá trị cực đại 2^{32}-1 = 4,294,967,295 (tương đương khoảng **49.7 ngày** chạy liên tục).
> Nhờ vào tính chất số học số nguyên không dấu (Unsigned Integer Underflow/Wrap-around), phép toán trừ thời gian:
> ```c
> if (current_time - previous_time >= INTERVAL)
> ```
> **vẫn cho kết quả toán học hoàn toàn chính xác ngay cả khi biến `current_time` bị tràn về 0!** Bạn tuyệt đối không được viết `if (current_time >= previous_time + INTERVAL)` vì điều kiện này sẽ bị sai hoàn toàn khi xảy ra tràn số.

> [!WARNING]
> **Giới hạn 24-bit của thanh ghi `SysTick->LOAD`:**
> Giá trị tối đa bạn có thể ghi vào thanh ghi `LOAD` là `0x00FFFFFF` (16,777,215). Nếu bạn tính toán giá trị chia xung vượt quá con số này, các bit cao sẽ bị mất và chu kỳ thời gian bị sai lệch hoàn toàn.

---

## 7. Hướng Dẫn Debug Trên Keil MDK

1. Nhấn `Ctrl + F5` để khởi động Debug.
2. Mở cửa sổ theo dõi SysTick: **Peripherals -> Core Peripherals -> System Tick Timer**.
3. Cửa sổ hiển thị trực quan:
   - **Control**: Hiển thị trạng thái các bit `Enable`, `TickInt`, `ClkSource`.
   - **Reload**: Giá trị nạp lại ban đầu (ví dụ: `71999`).
   - **Value**: Giá trị đếm lùi giảm liên tục thời gian thực.
4. Đặt biến `system_millis` vào cửa sổ **Watch 1** để quan sát số mili-giây đếm tăng đều đặn.

---

## 8. Bài Tập Thực Hành

1. **Bài tập 1 (Hàm delay_us chính xác)**: Dùng hàm `delay_us()` tạo một chuỗi xung vuông tần số đúng 100kHz trên chân PA1 (5µs mức cao, 5µs mức thấp). Cắm máy đo Logic Analyzer để kiểm tra sai số.
2. **Bài tập 2 (Xây dựng Finite State Machine không chặn)**: Sử dụng hàm `millis()` để xây dựng máy trạng thái điều khiển hệ thống đèn giao thông ngã tư (Đèn Xanh 10s → Đèn Vàng 3s → Đèn Đỏ 13s) kết hợp nút bấm ưu tiên cho người đi bộ.
3. **Bài tập 3 (Đo chu kỳ thực thi hàm)**: Tận dụng giá trị tức thời trong thanh ghi `SysTick->VAL` để đo xem một thuật toán tính toán phức tạp (như tính ma trận hoặc mã hóa) tốn chính xác bao nhiêu chu kỳ clock CPU.
