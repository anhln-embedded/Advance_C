# BÀI 11: ADC 12-BIT CƠ BẢN (POLLING & NGẮT EOC)

Chào mừng bạn đến với bài học thứ 11 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Trong thế giới thực, hầu hết các đại lượng vật lý (nhiệt độ, áp suất, ánh sáng, âm thanh, điện áp pin) đều tồn tại dưới dạng tín hiệu tương tự (Analog - liên tục theo thời gian). Để bộ xử lý số của vi điều khiển có thể tính toán và xử lý, chúng ta cần tới **Bộ chuyển đổi Tương tự - Số (Analog-to-Digital Converter - ADC)**.

STM32F103 tích hợp bộ ADC 12-bit tốc độ cao với kiến trúc xấp xỉ liên tiếp (SAR ADC). Trong bài học này, bạn sẽ nắm vững nguyên lý hoạt động, quy trình hiệu chuẩn phần cứng bắt buộc (Calibration) và cách đo điện áp chính xác bằng cả chế độ Polling và ngắt kết thúc chuyển đổi (End of Conversion - EOC).

---

## 1. Kiến Trúc Bộ Chuyển Đổi SAR ADC 12-Bit Trên STM32F103

STM32F103C8T6 tích hợp 2 khối ADC độc lập (**ADC1** và **ADC2**) với các đặc tính kỹ thuật ấn tượng:
- **Độ phân giải**: **12-bit** (Giá trị số xuất ra từ 0 đến 2^{12}-1 = 4095).
- **Dải điện áp đo (V_IN)**: Từ 0V (tương ứng giá trị 0) đến V_REF+ = 3.3V (tương ứng giá trị 4095).
- **Số kênh đo ngoài**: 16 kênh tương tự (ADC_IN0 đến ADC_IN15 nối với các chân GPIO Port A, B, C).
- **2 kênh nội đặc biệt**: Kênh 16 (Cảm biến nhiệt độ nội) và Kênh 17 (Điện áp tham chiếu nội V_REFINT ≈ 1.20V).
- **Thời gian chuyển đổi cực nhanh**: Tối thiểu chỉ mất **1µs** ở tần số ADC 14MHz.

<p align="center">
  <img src="images/bai11_adc_sar_structure.svg" width="940" alt="Kiến trúc bộ chuyển đổi ADC 12-bit SAR STM32F103">
</p>

---

## 2. Giới Hạn Tần Số Xung Clock Của ADC (ADCCLK)

Xung nhịp cấp cho khối ADC lấy từ bus ngoại vi tốc độ cao **APB2** (72MHz) thông qua một bộ chia tần số chuyên dụng trong thanh ghi `RCC_CFGR` (các bit `ADCPRE[1:0]`):

```
       Bus APB2 (72MHz) ──> [ ADC Prescaler (/2, /4, /6, /8) ] ──> ADCCLK (≤ 14MHz)
```

> [!CAUTION]
> **Giới hạn tốc độ tối đa của khối ADC:**
> Theo tài liệu RM0008, tần số xung nhịp cấp cho ADC (**ADCCLK**) **tuyệt đối không được vượt quá 14MHz**.
> Do bus APB2 chạy ở 72MHz, nếu chọn chia 2 (36MHz) hoặc chia 4 (18MHz) thì ADC sẽ bị sai lệch hoàn toàn hoặc hỏng phần cứng!
> **Phương án chuẩn xác**: Bắt buộc chọn hệ số chia là **6** (72MHz / 6 = 12MHz ≤ 14MHz) hoặc chia **8** (72MHz / 8 = 9MHz).

---

## 3. Thời Gian Lấy Mẫu Và Công Thức Tính Điện Áp

### 3.1 Thời gian chuyển đổi tổng cộng (T_conv):
T_conv = T_sample + 12.5  chu kỳ ADCCLK

Trong đó T_sample có thể cấu hình độc lập cho từng kênh (trong thanh ghi `ADC_SMPR1` và `ADC_SMPR2`) gồm 8 mức:
`1.5, 7.5, 13.5, 28.5, 41.5, 55.5, 71.5, 239.5` chu kỳ.
- *Ví dụ*: Với ADCCLK = 12MHz và chọn thời gian lấy mẫu 1.5 chu kỳ:
  T_conv = 1.5 + 12.5 = 14  chu kỳ = (14 / 12,000,000) ≈ 1.17 µs

### 3.2 Công thức đổi giá trị thô thành điện áp thực (V_in):
Độ phân giải 1 bước (1 LSB) = (V_REF / 4095) = (3.3V / 4095) ≈ 0.8058  mV

V_in = (ADC_RAW × 3.3V / 4095)

---

## 4. Quy Trình Hiệu Chuẩn Phần Cứng Bắt Buộc (ADC Calibration)

Mỗi chip bán dẫn khi xuất xưởng đều có sai lệch nhỏ về dung sai tụ điện bên trong mạch SAR. Để triệt tiêu sai số này, STM32F103 tích hợp sẵn mạch **Tự hiệu chuẩn phần cứng**:
1. Bật nguồn cho ADC (`ADON = 1`) và chờ một vài micro-giây để mạch ổn định.
2. Kích hoạt Reset mạch hiệu chuẩn: ghi bit `RSTCAL = 1` trong `ADC_CR2` và chờ cho đến khi bit này tự xóa về `0`.
3. Kích hoạt quá trình tự hiệu chuẩn: ghi bit `CAL = 1` trong `ADC_CR2` và chờ cho đến khi bit này tự xóa về `0`.

> [!IMPORTANT]
> Nếu bỏ qua bước Calibration khi khởi động, giá trị đọc ADC có thể bị lệch (Offset) từ 10 đến 50 đơn vị!

---

## 5. Các Thanh Ghi ADC Theo RM0008

Địa chỉ cơ sở ADC1: `0x4001 2400`.

| Thanh Ghi | Offset | Bit Quan Trọng | Mô Tả |
| :--- | :---: | :--- | :--- |
| **`ADC_SR`**  | `0x00` | `EOC` (Bit 1) | **Status Register**: Cờ báo hoàn thành chuyển đổi (End of Conversion). |
| **`ADC_CR1`** | `0x04` | `EOCIE` (Bit 5)<br>`SCAN` (Bit 8) | Cho phép ngắt EOC và bật chế độ quét Scan Mode. |
| **`ADC_CR2`** | `0x08` | `ADON` (Bit 0)<br>`CONT` (Bit 1)<br>`CAL` (Bit 2)<br>`RSTCAL` (Bit 3)<br>`SWSTART` (Bit 22) | **Control Register 2**:<br>- `ADON`: Bật nguồn và kích hoạt chuyển đổi.<br>- `CONT`: 1 = Chuyển đổi liên tục, 0 = Chuyển đổi đơn (Single).<br>- `SWSTART`: Bắt đầu chuyển đổi bằng phần mềm. |
| **`ADC_SMPR2`**| `0x10`| `SMP0[2:0]` | Thời gian lấy mẫu cho kênh 0 đến kênh 9. |
| **`ADC_SQR1`**| `0x2C` | `L[3:0]` (Bits 20-23) | Số lượng kênh trong chuỗi chuyển đổi thông thường (Regular Sequence). |
| **`ADC_SQR3`**| `0x34` | `SQ1[4:0]` (Bits 0-4) | Số hiệu kênh được chuyển đổi đầu tiên (Kênh 0 nối với PA0). |
| **`ADC_DR`**  | `0x4C` | Bits [15:0] | **Data Register**: Lưu trữ kết quả đo 12-bit (Căn lề phải). |

---

## 6. Triển Khai Mã Nguồn Thực Chiến

### Kịch bản thực hành:
- Biến trở xoay (Potentiometer) 10kΩ: Hai chân bìa nối 3.3V và GND, chân giữa nối vào chân **PA0 (ADC1_IN0)**.
- Đèn LED **PC13**: Chớp tắt với tần số tỉ lệ thuận với điện áp biến trở (vặn áp thấp chớp chậm, vặn áp cao chớp nhanh).

---

### PHƯƠNG PHÁP 1: BARE-METAL REGISTER (CHẾ ĐỘ POLLING)

File: `main.c`

```c
#include "stm32f10x.h"

void ADC1_Init_Register(void)
{
    // 1. Enable clocks for GPIOA and ADC1 on APB2 bus
    RCC->APB2ENR |= (1 << 2); // IOPAEN = 1
    RCC->APB2ENR |= (1 << 9); // ADC1EN = 1

    // 2. Configure ADC prescaler: APB2 (72MHz) / 6 = 12MHz (<= 14MHz max)
    RCC->CFGR &= ~(0x03 << 14);
    RCC->CFGR |= (0x02 << 14); // ADCPRE = 10b (PCLK2 / 6)

    // 3. Configure PA0 pin: Analog Input mode
    GPIOA->CRL &= ~(0x0F << 0); // MODE0 = 00b, CNF0 = 00b (Analog Mode)

    // 4. Configure conversion sequence: 1 single channel
    ADC1->SQR1 &= ~(0x0F << 20); // L[3:0] = 0000b (Sequence length = 1 channel)
    ADC1->SQR3 &= ~(0x1F << 0);
    ADC1->SQR3 |= (0x00 << 0);  // SQ1 = 0 (Channel ADC_IN0 mapped to rank 1)

    // 5. Configure Channel 0 sample time: 55.5 cycles
    ADC1->SMPR2 &= ~(0x07 << 0);
    ADC1->SMPR2 |= (0x05 << 0); // SMP0 = 101b (55.5 cycles)

    // 6. Configure Single conversion mode
    ADC1->CR2 &= ~(1 << 1); // CONT = 0

    // 7. Power on ADC (ADON = 1)
    ADC1->CR2 |= (1 << 0);

    // Wait for ADC power stabilization (~few microseconds)
    for (volatile int i = 0; i < 1000; i++);

    // 8. EXECUTE HARDWARE CALIBRATION
    // Reset calibration registers
    ADC1->CR2 |= (1 << 3); // RSTCAL = 1
    while (ADC1->CR2 & (1 << 3)); // Wait until RSTCAL bit clears to 0

    // Start calibration process
    ADC1->CR2 |= (1 << 2); // CAL = 1
    while (ADC1->CR2 & (1 << 2)); // Wait until CAL bit clears to 0
}

uint16_t ADC1_Read_Polling(void)
{
    // Start conversion by software (SWSTART)
    ADC1->CR2 |= (1 << 22); // SWSTART = 1
    ADC1->CR2 |= (1 << 0);  // ADON = 1 second time to trigger conversion

    // Wait until EOC (End Of Conversion) flag is set to 1
    while (!(ADC1->SR & (1 << 1)));

    // Read conversion data from ADC_DR (Reading DR clears EOC flag)
    return (uint16_t)(ADC1->DR & 0x0FFF);
}

int main(void)
{
    // Configure LED PC13
    RCC->APB2ENR |= (1 << 4);
    GPIOC->CRH &= ~(0x0F << 20);
    GPIOC->CRH |= (0x02 << 20);

    ADC1_Init_Register();

    while (1)
    {
        uint16_t raw_value = ADC1_Read_Polling();

        // Convert raw value to millivolts (mV)
        // V_in_mV = (raw_value * 3300) / 4095;

        // Adjust LED blink rate according to potentiometer reading
        GPIOC->ODR ^= (1 << 13);
        
        // Delay proportional to measured ADC value (approx 50ms to 500ms)
        uint32_t delay_count = (raw_value * 1000) + 100000;
        for (volatile uint32_t i = 0; i < delay_count; i++);
    }
}
```

---

### PHƯƠNG PHÁP 2: LẬP TRÌNH BẰNG THƯ VIỆN CHUẨN SPL (DÙNG NGẮT EOC)

File: `main.c`

```c
#include "stm32f10x.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_gpio.h"
#include "stm32f10x_adc.h"
#include "misc.h"

volatile uint16_t adc_result = 0;

void ADC1_Interrupt_Config_SPL(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
    ADC_InitTypeDef  ADC_InitStructure;
    NVIC_InitTypeDef NVIC_InitStructure;

    // 1. Enable clocks
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_ADC1, ENABLE);
    RCC_ADCCLKConfig(RCC_PCLK2_Div6); // 72MHz / 6 = 12MHz

    // 2. Configure PA0: Analog Mode
    GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_0;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN;
    GPIO_Init(GPIOA, &GPIO_InitStructure);

    // 3. Configure ADC
    ADC_InitStructure.ADC_Mode               = ADC_Mode_Independent;
    ADC_InitStructure.ADC_ScanConvMode       = DISABLE;
    ADC_InitStructure.ADC_ContinuousConvMode = ENABLE; // Continuous conversion
    ADC_InitStructure.ADC_ExternalTrigConv   = ADC_ExternalTrigConv_None;
    ADC_InitStructure.ADC_DataAlign          = ADC_DataAlign_Right; // Right alignment of data
    ADC_InitStructure.ADC_NbrOfChannel       = 1;
    ADC_Init(ADC1, &ADC_InitStructure);

    // 4. Select Channel 0, rank 1, 55.5 cycles sample time
    ADC_RegularChannelConfig(ADC1, ADC_Channel_0, 1, ADC_SampleTime_55Cycles5);

    // 5. Enable End of Conversion (EOC) interrupt
    ADC_ITConfig(ADC1, ADC_IT_EOC, ENABLE);

    // 6. Configure NVIC
    NVIC_InitStructure.NVIC_IRQChannel                   = ADC1_2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority        = 1;
    NVIC_InitStructure.NVIC_IRQChannelCmd                = ENABLE;
    NVIC_Init(&NVIC_InitStructure);

    // 7. Enable ADC and perform calibration
    ADC_Cmd(ADC1, ENABLE);

    ADC_ResetCalibration(ADC1);
    while (ADC_GetResetCalibrationStatus(ADC1));

    ADC_StartCalibration(ADC1);
    while (ADC_GetCalibrationStatus(ADC1));

    // 8. Start continuous conversion
    ADC_SoftwareStartConvCmd(ADC1, ENABLE);
}

// ADC1 and ADC2 shared interrupt service routine (ISR)
void ADC1_2_IRQHandler(void)
{
    if (ADC_GetITStatus(ADC1, ADC_IT_EOC) != RESET)
    {
        // Read conversion value (This automatically clears EOC flag)
        adc_result = ADC_GetConversionValue(ADC1);

        ADC_ClearITPendingBit(ADC1, ADC_IT_EOC);
    }
}

int main(void)
{
    ADC1_Interrupt_Config_SPL();

    while (1)
    {
        // adc_result is continuously updated in background ISR
        __WFI();
    }
}
```

---

## 7. Những Lưu Ý Sống Còn Khi Sử Dụng ADC

> [!WARNING]
> **1. Điện áp ngõ vào tối đa chỉ là 3.3V:**
> Mặc dù một số chân GPIO của STM32F103 có tính năng chịu áp 5V (5V-Tolerant) ở chế độ số, **nhưng khi chân đã được cấu hình sang chế độ Analog (`GPIO_Mode_AIN`), tính năng bảo vệ chịu áp 5V sẽ bị vô hiệu hóa**!
> Nếu cấp điện áp lớn hơn 3.6V vào chân Analog, bạn sẽ làm cháy khối ADC bên trong chip ngay lập tức! Bắt buộc phải dùng mạch phân áp điện trở nếu muốn đo điện áp cao hơn 3.3V (như Ắc quy 12V hoặc Pin Li-Po 4.2V).

> [!TIP]
> **2. Lọc nhiễu tín hiệu Analog bằng phần mềm:**
> Tín hiệu Analog thực tế rất dễ bị nhiễm gai nhiễu từ nguồn xung và môi trường xung quanh. Hãy áp dụng thuật toán **Lọc trung bình trượt (Moving Average Filter)** bằng cách đọc liên tiếp 16 mẫu rồi lấy giá trị trung bình cộng để kết quả đo đạt độ phẳng và ổn định tuyệt đối.

---

## 8. Bài Tập Thực Hành

1. **Bài tập 1 (Vôn-kế số DC 0 - 30V)**: Thiết kế mạch cầu phân áp gồm điện trở 10kΩ và 1kΩ nối vào chân PA0. Viết chương trình đo điện áp từ 0 đến 30V DC và tính toán bù trừ sai số điện trở thực tế.
2. **Bài tập 2 (Bộ lọc trung bình 16 mẫu)**: Viết hàm `ADC_Read_Filtered(uint8_t channel)` đọc 16 lần giá trị ADC liên tiếp, loại bỏ giá trị lớn nhất và nhỏ nhất (Outliers), sau đó tính trung bình 14 mẫu còn lại.
3. **Bài tập 3 (Thước đo khoảng cách quang học)**: Kết nối cảm biến khoảng cách tương tự Sharp GP2Y0A21YK0F (ngõ ra analog 0.4V → 3.1V tương ứng cự ly 10cm → 80cm). Viết công thức giải mã phi tuyến tính từ điện áp ra khoảng cách centimet.
