# LỘ TRÌNH KHÓA HỌC LẬP TRÌNH STM32F103 CHUYÊN SÂU
### Phương Pháp Tiếp Cận: Thanh Ghi Thuần (Bare-Metal Register) & Thư Viện Chuẩn (SPL)

Khóa học được thiết kế dành riêng cho kỹ sư nhúng muốn nắm vững bản chất phần cứng dòng vi điều khiển ARM Cortex-M3 (**STM32F103C8T6 - Blue Pill**). 

Tất cả bài học và ví dụ mẫu đều dựa trên:
1. **Lập trình thanh ghi (Bare-Metal Register & CMSIS)**: Hiểu sâu cách CPU giao tiếp trực tiếp với bộ nhớ và ngoại vi qua bus AHB/APB, tối ưu từng chu kỳ xung clock.
2. **Thư viện ngoại vi chuẩn SPL (Standard Peripheral Library - STSW-STM32054)**: Thư viện chuẩn mực, gọn nhẹ, dễ kiểm soát và không sử dụng các lớp trừu tượng nặng nề (Hoàn toàn không dùng HAL).

---

## 1. Khung Chương Trình 26 Bài Học Chi Tiết

### PHẦN 1: NỀN TẢNG KIẾN TRÚC ARM CORTEX-M3 & NGOẠI VI CƠ BẢN
- **[Bài 01: Tổng quan STM32F103, Thiết lập môi trường Keil C / SPL và Dự án Blink LED đầu tiên](/tutorials/stm32f103/bai-01-tong-quan-stm32f103-thiet-lap-moi-truong-keil-c-spl-va-du-an-blink-led)**
  - Cài đặt Keil MDK, tích hợp thư viện SPL & CMSIS.
  - Sơ đồ Pinout Blue Pill, kết nối mạch nạp ST-Link V2 (SWD).
  - Lập trình chớp tắt LED PC13 bằng Thanh ghi (`RCC->APB2ENR`, `GPIOC->CRH`, `BSRR`, `BRR`) và SPL (`GPIO_Init`, `GPIO_SetBits`, `GPIO_ResetBits`).
- **[Bài 02: Phân Tích Chuyên Sâu GPIO & Kỹ Thuật Bit-Banding](/tutorials/stm32f103/bai-02-phan-tich-chuyen-sau-gpio-va-ky-thuat-bit-banding)**
  - Cấu trúc vật lý bên trong 1 chân GPIO: Push-Pull vs Open-Drain, Pull-up/Pull-down.
  - Các thanh ghi `CRL`, `CRH`, `IDR`, `ODR`.
  - Kỹ thuật Bit-Banding trực tiếp trên vùng nhớ SRAM và Peripheral Alias (truy xuất bit đơn nguyên tử).
  - Xử lý đọc nút nhấn chống rung (Debounce) bằng phần mềm.
- **[Bài 03: Hệ Thống Xung Nhịp (RCC & Clock Tree)](/tutorials/stm32f103/bai-03-he-thong-xung-nhip-rcc-va-clock-tree)**
  - Các nguồn xung clock: HSI, HSE, LSI, LSE, PLL.
  - Phân tích bảng phân phối xung: Bus AHB, APB1 (max 36MHz), APB2 (max 72MHz).
  - Tự viết hàm cấu hình System Clock 72MHz từ thạch anh ngoài 8MHz bằng thanh ghi `RCC_CR`, `RCC_CFGR` và SPL.
- **[Bài 04: Ngắt Ngoài (EXTI) & Bộ Điều Khiển Ngắt NVIC](/tutorials/stm32f103/bai-04-ngat-ngoai-exti-va-bo-dieu-khien-ngat-nvic)**
  - Cơ chế Exception và Interrupt trong lõi ARM Cortex-M3, Vector Table.
  - Phân định mức độ ưu tiên ngắt: Priority Grouping, Preemption Priority vs Sub-priority.
  - Cấu hình thanh ghi `AFIO_EXTICRx`, `EXTI_IMR`, `EXTI_RTSR`, `EXTI_FTSR` và các hàm `NVIC_Init()`.

---

### PHẦN 2: TIMERS & BỘ ĐẾM THỜI GIAN
- **[Bài 05: SysTick Timer & Định Thời Không Chặn (Non-blocking)](/tutorials/stm32f103/bai-05-systick-timer-va-dinh-thoi-khong-chan-non-blocking)**
  - Thanh ghi `SysTick->CTRL`, `LOAD`, `VAL`.
  - Xây dựng hàm `delay_ms()` và `delay_us()` chính xác cấp thanh ghi.
  - Quản lý thời gian thực hiện đa nhiệm theo cơ chế millis() không gây nghẽn CPU.
- **[Bài 06: General Purpose Timer (TIM2 - TIM4)](/tutorials/stm32f103/bai-06-general-purpose-timer-tim2-tim4)**
  - Cấu trúc Time-base: Prescaler (`TIMx_PSC`), Auto-reload (`TIMx_ARR`), Counter (`TIMx_CNT`).
  - Xử lý ngắt tràn Timer (Update Event) để định thời chính xác bằng Register và SPL.
- **[Bài 07: Điều Xung PWM (Pulse Width Modulation)](/tutorials/stm32f103/bai-07-dieu-xung-pwm-pulse-width-modulation)**
  - Cơ chế so sánh ngõ ra (Output Compare), thanh ghi `TIMx_CCMR`, `TIMx_CCER`, `TIMx_CCR`.
  - Điều khiển độ sáng mượt mà cho LED và điều khiển góc quay động cơ Servo SG90/MG996R.
- **[Bài 08: Input Capture - Đo Xung & Cảm Biến Siêu Âm](/tutorials/stm32f103/bai-08-input-capture-do-xung-va-cam-bien-sieu-am)**
  - Chế độ bắt cạnh xung (Input Capture Mode) của Timer.
  - Đo chu kỳ, tần số và độ rộng xung tín hiệu PWM.
  - Đo khoảng cách chính xác bằng cảm biến siêu âm HC-SR04.
- **[Bài 09: Timer Encoder Interface](/tutorials/stm32f103/bai-09-timer-encoder-interface)**
  - Cấu hình chế độ phần cứng đọc Encoder 2 kênh Phase A & Phase B (`TIM_EncoderInterfaceConfig`).
  - Lọc nhiễu kỹ thuật số (Digital Filter) tích hợp sẵn trong Timer phần cứng.
- **[Bài 10: Watchdog Timers - Chống Treo Hệ Thống Công Nghiệp](/tutorials/stm32f103/bai-10-watchdog-timers-chong-treo-he-thong-cong-nghiep)**
  - Independent Watchdog (IWDG): Thanh ghi `IWDG_KR`, `IWDG_PR`, `IWDG_RLR` hoạt động bằng xung nội LSI độc lập.
  - Window Watchdog (WWDG): Giám sát phần mềm trong cửa sổ thời gian nghiêm ngặt.

---

### PHẦN 3: BỘ CHUYỂN ĐỔI TƯƠNG TỰ - SỐ (ADC)
- **[Bài 11: ADC 12-bit Cơ Bản (Polling & Interrupt)](/tutorials/stm32f103/bai-11-adc-12-bit-co-ban-polling-va-interrupt)**
  - Nguyên lý chuyển đổi SAR ADC 12-bit.
  - Thanh ghi cấu hình: `ADC_CR1`, `ADC_CR2`, `ADC_SQRx`, `ADC_DR`.
  - Hiệu chuẩn ADC (Calibration), đọc điện áp cảm biến bằng chế độ Polling và ngắt EOC (End of Conversion).
- **[Bài 12: ADC Nâng Cao (Scan Mode & Internal Temperature Sensor)](/tutorials/stm32f103/bai-12-adc-nang-cao-scan-mode-va-internal-temperature-sensor)**
  - Chế độ quét liên tục nhiều kênh (Scan Mode).
  - Đọc cảm biến nhiệt độ tích hợp sẵn trong chip (Channel 16) và điện áp tham chiếu nội Vrefint (Channel 17).

---

### PHẦN 4: TRUYỀN THÔNG NGOẠI VI NỐI TIẾP (SERIAL PROTOCOLS)
- **[Bài 13: USART/UART Cơ Bản & Cấu Hình printf](/tutorials/stm32f103/bai-13-usart-uart-co-ban-va-cau-hinh-printf)**
  - Nguyên lý truyền thông UART, công thức tính Baudrate nạp vào thanh ghi `USART_BRR`.
  - Truyền nhận ký tự, chuỗi ký tự qua polling và ngắt `USART_IT_RXNE`.
  - Tái định hướng (Retarget) hàm `fputc()` sang UART để xuất dữ liệu qua `printf()`.
- **[Bài 14: UART Nâng Cao - Bộ Đệm Vòng (Ring Buffer) & Parser CLI](/tutorials/stm32f103/bai-14-uart-nang-cao-bo-dem-vong-ring-buffer-va-parser-cli)**
  - Xử lý ngắt nhàn rỗi `USART_IT_IDLE` để nhận gói dữ liệu độ dài linh hoạt.
  - Thiết kế cấu trúc dữ liệu Ring Buffer (Circular FIFO) tối ưu bộ nhớ.
  - Xây dựng chương trình phân tích và thực thi tập lệnh dòng lệnh (Command Line Interface - CLI).
- **[Bài 15: Giao Tiếp I2C Master Phần Cứng](/tutorials/stm32f103/bai-15-giao-tiep-i2c-master-phan-cung)**
  - Giao thức I2C: Khởi động (Start), Dừng (Stop), ACK/NACK, thanh ghi `I2C_CR1`, `I2C_CR2`, `I2C_SR1`, `I2C_SR2`.
  - Giao tiếp bộ nhớ EEPROM ngoài AT24C08 (đọc/ghi dữ liệu theo byte và page).
  - Điều khiển màn hình hiển thị OLED SSD1306 0.96 inch (128x64).
- **[Bài 16: Giao Tiếp SPI Master Phần Cứng](/tutorials/stm32f103/bai-16-giao-tiep-spi-master-phan-cung)**
  - Chuẩn SPI 4 dây: SCK, MISO, MOSI, CS/NSS, các mode SPI (CPOL, CPHA).
  - Thanh ghi `SPI_CR1`, `SPI_SR`, `SPI_DR`.
  - Giao tiếp bộ nhớ Flash SPI tốc độ cao W25Q64 (64M-bit).
  - Điều khiển màn hình màu TFT ST7735 / ILI9341.

---

### PHẦN 5: QUẢN LÝ BỘ NHỚ DMA & CHẾ ĐỘ TIẾT KIỆM NĂNG LƯỢNG
- **[Bài 17: DMA Controller (Direct Memory Access) Chuyên Sâu](/tutorials/stm32f103/bai-17-dma-controller-direct-memory-access-chuyen-sau)**
  - Bản chất truyền nhận dữ liệu trực tiếp không can thiệp CPU.
  - Thanh ghi `DMA_CPARx`, `DMA_CMARx`, `DMA_CNDTRx`, `DMA_CCRx`.
  - Ứng dụng thực tế: Truyền UART DMA không nghẽn CPU và lấy mẫu ADC đa kênh tự động bằng Circular DMA.
- **[Bài 18: Chế Độ Nguồn Thấp (Low Power Modes)](/tutorials/stm32f103/bai-18-che-do-nguon-thap-low-power-modes)**
  - 3 cấp độ tiết kiệm điện: Sleep Mode, Stop Mode, Standby Mode.
  - Đo đạc dòng tiêu thụ của vi điều khiển.
  - Đánh thức chip bằng chân Wakeup (WKUP) và ngắt báo thức thời gian thực RTC Alarm.
- **[Bài 19: Bộ Nhớ Flash Nội (Flash Memory Controller - FPEC)](/tutorials/stm32f103/bai-19-bo-nho-flash-noi-flash-memory-controller-fpec)**
  - Tổ chức bộ nhớ Flash: Phân trang (Page 1KB), vùng nhớ ứng dụng.
  - Trình tự mở khóa Flash (`FLASH_KEYR`), xóa Page (`FLASH_CR_PER`) và ghi dữ liệu Half-Word vào Flash để lưu tham số cài đặt vĩnh viễn.

---

### PHẦN 6: HỆ ĐIỀU HÀNH THỜI GIAN THỰC (FreeRTOS)
- **[Bài 20: Nhập Môn FreeRTOS Trên STM32 Với SPL & CMSIS](/tutorials/stm32f103/bai-20-nhap-mon-freertos-tren-stm32-voi-spl-va-cmsis)**
  - Tích hợp mã nguồn FreeRTOS vào dự án SPL: Porting cho lõi ARM Cortex-M3.
  - Cơ chế đa nhiệm: Task, Scheduler, Con trỏ lệnh `PSP`/`MSP`, Context Switch.
  - Cấu hình quản lý bộ nhớ Heap (Heap_4).
- **[Bài 21: Cơ Chế Đồng Bộ Hóa & Giao Tiếp Đa Task](/tutorials/stm32f103/bai-21-co-che-dong-bo-hoa-va-giao-tiep-da-task)**
  - Hàng đợi (Queue): Truyền nhận dữ liệu an toàn giữa các tiến trình.
  - Khóa nhị phân (Binary Semaphore) và Đếm Semaphore (Counting Semaphore) xử lý đồng bộ hóa ngắt ISR với Task.
  - Mutex: Khóa loại trừ tương hỗ bảo vệ tài nguyên chia sẻ và cơ chế chống nghịch đảo mức ưu tiên (Priority Inversion).
- **[Bài 22: Event Groups, Software Timers & Task Notifications](/tutorials/stm32f103/bai-22-event-groups-software-timers-va-task-notifications)**
  - Cờ sự kiện (Event Groups) đồng bộ nhiều điều kiện.
  - Bộ định thời phần mềm (Software Timers).
  - Kỹ thuật Task Notifications: Tăng tốc độ chuyển ngữ cảnh và tiết kiệm tối đa bộ nhớ RAM.

---

### PHẦN 7: CHUYÊN ĐỀ NÂNG CAO & CHUẨN CÔNG NGHIỆP
- **[Bài 23: Mạng Truyền Thông Công Nghiệp CAN Bus](/tutorials/stm32f103/bai-23-mang-truyen-thong-cong-nghiep-can-bus)**
  - Cấu trúc vật lý CAN: Bộ thu phát (Transceiver) TJA1050/MCP2551, đường truyền vi sai CAN_H, CAN_L.
  - Thanh ghi CAN trên STM32: `CAN_MCR`, `CAN_BTR`.
  - Cấu hình bộ lọc phần cứng (Filter Banks) để chọn lọc ID tin nhắn.
  - Truyền nhận dữ liệu cảm biến ô tô / công nghiệp theo chuẩn CAN 2.0B.
- **[Bài 24: USB 2.0 Full Speed Device](/tutorials/stm32f103/bai-24-usb-2-0-full-speed-device)**
  - Kiến trúc phần cứng USB tích hợp trên STM32F103 (12 Mbit/s, dùng chân PA11, PA12).
  - Tích hợp bộ thư viện STM32 USB-FS-Device development kit.
  - Xây dựng thiết bị USB Virtual COM Port (VCP) giao tiếp tốc độ cao với máy tính.
  - Tạo thiết bị ngoại vi USB Custom HID (Bàn phím, Chuột điều khiển từ xa).
- **[Bài 25: Thiết Kế Custom In-System Programming (ISP) Bootloader](/tutorials/stm32f103/bai-25-thiet-ke-custom-in-system-programming-isp-bootloader)**
  - Cơ chế Bootloader: Phân vùng bộ nhớ Flash (Bootloader Area & User Application Area).
  - Chuyển hướng bảng Vector ngắt (Vector Table Relocation - `SCB->VTOR`).
  - Viết hàm vô hiệu hóa ngoại vi, Reset Stack Pointer và nhảy vào ứng dụng (`Jump_To_Application`).
  - Nhận và nạp firmware mã hóa qua cổng UART.
- **[Bài 26: Kỹ Thuật Debugging Chuyên Sâu & Xử Lý Sự Cố HardFault](/tutorials/stm32f103/bai-26-ky-thuat-debugging-chuyen-sau-va-xu-ly-su-co-hardfault)**
  - Tận dụng Keil Logic Analyzer để đo xung tín hiệu trực tiếp trên phần mềm.
  - Kỹ thuật Debug qua SWO / ITM Trace xuất log thời gian thực mà không làm chậm vi điều khiển.
  - Phân tích thanh ghi ngăn xếp CPU (`MSP`, `PSP`, `LR`, `PC`) khi xảy ra lỗi sập chip **HardFault Handler**, tìm chính xác dòng lệnh gây tràn mảng, chia cho 0 hoặc truy cập vùng nhớ cấm.

---

## 2. Phần Cứng Thực Hành Cần Thiết

1. **Board vi điều khiển STM32F103C8T6 Blue Pill** (Lõi ARM Cortex-M3, 72MHz, 64KB Flash, 20KB SRAM).
2. **Mạch nạp ST-Link V2 (SWD)** kèm dây nạp 4 chân (3.3V, SWCLK, SWDIO, GND).
3. **Module USB to UART (CP2102 hoặc CH340)** để truyền nhận dữ liệu với máy tính.
4. **Màn hình hiển thị**: OLED SSD1306 0.96 inch (I2C) hoặc TFT LCD ST7735 (SPI).
5. **Cảm biến và linh kiện**: Biến trở, Cảm biến siêu âm HC-SR04, EEPROM 24C08, Flash W25Q64, Động cơ Servo SG90, Module thu phát CAN TJA1050.

---

## 3. Tổng Hợp Link Tải Phần Mềm & Thư Viện

> [!NOTE]
> **Kho lưu trữ trọn bộ phần mềm, Driver và Thư viện SPL (Tải trực tiếp tốc độ cao):**  
> 📥 **Link Google Drive:** [Thư mục cài đặt STM32F103 (Google Drive)](https://drive.google.com/drive/folders/16sOEv58T-pTNdUQKuu2fwyhj0MC2kBx4?usp=drive_link)  
> *(Bao gồm sẵn: Keil MDK, Thư viện chuẩn SPL STM32F10x, Driver ST-Link, Device Pack F1xx và công cụ nạp).*

| Phần mềm / Thư viện | Vai trò | Link tải chính thức |
| :--- | :--- | :--- |
| **Keil MDK-ARM v5** | IDE lập trình và Debug thời gian thực chuyên sâu | [Arm Keil - MDK Community](https://www.keil.arm.com/mdk-community/) |
| **STM32F10x Standard Peripheral Library (STSW-STM32054)** | Toàn bộ mã nguồn thư viện SPL + CMSIS | [STMicroelectronics - STSW-STM32054](https://www.st.com/en/embedded-software/stsw-stm32054.html) |
| **Gói chip STM32F1xx DFP (v2.4.1)** | Device Family Pack cho Keil MDK | [Keil STM32F1xx_DFP](https://pack-flat.keil.arm.com/Keil.STM32F1xx_DFP.2.4.1.pack) |
| **ST-LINK USB Driver (STSW-LINK009)** | Driver mạch nạp ST-Link V2 cho Windows | [STMicroelectronics - STSW-LINK009](https://www.st.com/en/development-tools/stsw-link009.html) |
| **STM32CubeProgrammer** | Công cụ nạp trực tiếp file `.hex`, kiểm tra Flash | [STMicroelectronics - STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html) |
