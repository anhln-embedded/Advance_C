import os
import re
import glob

# Comprehensive dictionary of exact translations and regex rules for Embedded C comments
EXACT_MAP = {
    # General / GPIO
    "Bật LED": "Turn on LED",
    "Tắt LED": "Turn off LED",
    "Bật LED (Active-Low)": "Turn on LED (Active-Low)",
    "Bật LED (Active-Low: kéo chân xuống mức 0)": "Turn on LED (Active-Low: pull pin LOW)",
    "Bật LED (ghi mức 0 do Active-Low)": "Turn on LED (Active-Low: write LOW)",
    "Bật LED PC13": "Turn on LED PC13",
    "Tắt LED PC13": "Turn off LED PC13",
    "Đảo trạng thái LED": "Toggle LED state",
    "Đảo trạng thái LED PC13": "Toggle LED PC13",
    "Đảo trạng thái PC13": "Toggle PC13 state",
    "Đảo trạng thái LED PC13 mỗi 500ms": "Toggle LED PC13 every 500ms",
    "Đảo trạng thái LED PC13 mỗi giây": "Toggle LED PC13 every second",
    "Đảo trạng thái LED PC13 bằng Bit-Banding nguyên tử": "Toggle LED PC13 atomically via Bit-Banding",
    "Mặc định tắt LED": "Default: turn off LED",
    "Ban đầu tắt LED (ghi mức 1)": "Initial state: turn off LED (write HIGH)",
    "Ban đầu tắt LED": "Initial state: turn off LED",
    "Trễ chống rung phím (Debounce)": "Button debounce delay",
    "Trễ chống rung khi nhả phím": "Button release debounce delay",
    "Lọc chống rung phím": "Button debounce filter",
    "Chờ nhả phím": "Wait for button release",
    "Chờ cho người dùng nhả nút bấm để tránh đảo liên tục": "Wait for button release to prevent continuous toggling",
    "Xác nhận chắc chắn nút vẫn đang được giữ": "Confirm button is still pressed",
    "Kiểm tra nút nhấn PA0 (bấm = 0 do kéo xuống GND)": "Check button PA0 (pressed = LOW due to pull-up)",
    "Nút nhấn PA0 (bấm = 0 do kéo xuống GND)": "Button PA0 (pressed = LOW due to pull-up)",
    "Khởi tạo GPIO": "Initialize GPIO",
    "Cấu hình GPIO": "Configure GPIO",

    # Clock / RCC
    "Cấp xung nhịp cho GPIOC": "Enable peripheral clock for GPIOC",
    "Cấp xung nhịp GPIOC": "Enable peripheral clock for GPIOC",
    "Cấp xung nhịp cho GPIOA và GPIOC": "Enable peripheral clock for GPIOA and GPIOC",
    "Cấp xung clock cho GPIOA và GPIOC": "Enable peripheral clock for GPIOA and GPIOC",
    "1. Bật nguồn dao động thạch anh ngoài HSE": "1. Enable external crystal oscillator (HSE)",
    "2. Chờ thạch anh ngoài sẵn sàng (HSERDY)": "2. Wait until HSE is ready (HSERDY)",
    "1. Kích hoạt HSE": "1. Enable HSE",
    "2. Chờ HSE ổn định": "2. Wait until HSE is stable",
    "3. Cấu hình Flash Latency = 2 Wait States (Bắt buộc khi HCLK > 48MHz)": "3. Configure Flash Latency = 2 Wait States (Required when HCLK > 48MHz)",
    "4. Cấu hình các bộ chia bus: AHB = 1, APB2 = 1, APB1 = 2": "4. Configure bus prescalers: AHB = /1, APB2 = /1, APB1 = /2",
    "5. Cấu hình PLL: Nguồn HSE (8MHz), nhân 9 -> 72MHz": "5. Configure PLL: HSE source (8MHz), multiplier x9 -> 72MHz",
    "6. Bật bộ nhân tần PLL": "6. Enable PLL multiplier",
    "7. Chờ PLL khóa tần số thành công (PLLRDY)": "7. Wait until PLL is locked (PLLRDY)",
    "8. Chuyển nguồn xung hệ thống SYSCLK sang PLL": "8. Switch system clock (SYSCLK) to PLL",
    "9. Chờ xác nhận hệ thống đã chạy trên PLL": "9. Wait until system clock switch to PLL is confirmed",

    # SysTick
    "Khởi tạo SysTick đếm 1ms (72MHz / 1000 = 72000 nhịp)": "Initialize SysTick for 1ms tick (72MHz / 1000 = 72000 ticks)",
    "Hàm xử lý ngắt SysTick (Gọi tự động mỗi 1ms)": "SysTick interrupt handler (Called automatically every 1ms)",
    "Hàm ngắt SysTick (Tự động gọi mỗi 1ms)": "SysTick ISR (Called automatically every 1ms)",
    "Hàm delay không chặn (Non-blocking delay)": "Non-blocking delay function",

    # Timers / PWM
    "1. Cấp xung clock cho TIM2 trên bus APB1 và GPIOC trên APB2": "1. Enable clocks for TIM2 (APB1) and GPIOC (APB2)",
    "2. Cấu hình Time-Base cho TIM2: Tạo chu kỳ ngắt đúng 1ms": "2. Configure Time-Base for TIM2: Generate 1ms update interrupt",
    "3. Kích hoạt ngắt cập nhật tràn bộ đếm (Update Interrupt)": "3. Enable counter overflow update interrupt (UIE)",
    "4. Cấu hình NVIC cho ngắt TIM2": "4. Configure NVIC for TIM2 interrupt",
    "5. Bật bộ đếm Timer 2": "5. Enable Timer 2 counter",
    "Hàm xử lý ngắt TIM2": "TIM2 interrupt handler",
    "Kiểm tra cờ ngắt Update": "Check update interrupt flag",
    "Xóa cờ ngắt sau khi xử lý": "Clear interrupt flag after handling",
    "Thiết lập Duty Cycle cho kênh PWM": "Set Duty Cycle for PWM channel",

    # Watchdogs
    "1. Kích hoạt Watchdog chạy bằng cách ghi mã lệnh 0xCCCC vào IWDG_KR": "1. Start IWDG by writing key 0xCCCC to IWDG_KR",
    "Lệnh này cũng tự động bật nguồn dao động nội LSI": "This command also automatically enables internal LSI oscillator",
    "2. Mở khóa cho phép ghi vào thanh ghi PR và RLR bằng cách ghi 0x5555": "2. Unlock write access to PR and RLR by writing 0x5555",
    "3. Cấu hình hệ số chia tần số Prescaler": "3. Configure prescaler divider",
    "4. Nạp giá trị chu kỳ timeout (tối đa 4095)": "4. Set reload value for timeout period (max 4095)",
    "5. Chờ thanh ghi trạng thái SR báo giá trị đã nạp thành công": "5. Wait until SR status register confirms update is complete",
    "6. Nạp lại giá trị ban đầu vào bộ đếm (Nuôi chó lần đầu)": "6. Reload initial counter value (First watchdog feed)",
    "Ghi mã 0xAAAA để nạp lại bộ đếm lùi": "Write key 0xAAAA to reload downcounter",
    "Nuôi chó định kỳ": "Feed watchdog periodically",
    "Cho chó ăn (Refresh Watchdog)": "Feed watchdog (Refresh counter)",
    "1. Cho phép ghi vào các thanh ghi IWDG": "1. Enable write access to IWDG registers",
    "2. Thiết lập Prescaler: Chia 64 (Tần số nhịp đếm: 40kHz / 64 = 625Hz)": "2. Set Prescaler: /64 (Tick frequency: 40kHz / 64 = 625Hz)",
    "3. Thiết lập giá trị nạp lại Reload: 624 (Timeout xấp xỉ 1000ms)": "3. Set reload value: 624 (Approx. 1000ms timeout)",
    "4. Nạp lại bộ đếm": "4. Reload counter",
    "5. Kích hoạt IWDG": "5. Enable IWDG",
    "Khởi tạo IWDG: Prescaler /64 (PR = 4), RLR = 624 -> Timeout = 1000ms": "Initialize IWDG: Prescaler /64 (PR = 4), RLR = 624 -> Timeout = 1000ms",
    "Rơi vào vòng lặp vô tận, KHÔNG GỌI IWDG_Feed()": "Enter infinite loop WITHOUT calling IWDG_Feed()",
    "Sau đúng 1 giây, IWDG sẽ tự động kích hoạt RESET vi điều khiển!": "After exactly 1 second, IWDG will automatically trigger MCU RESET!",
    "KIỂM TRA NGUYÊN NHÂN RESET TRONG THANH GHI RCC_CSR": "Check reset cause flags in RCC_CSR register",
    "Lần Reset này do IWDG kích hoạt!": "This reset was triggered by IWDG!",
    "Xóa cờ Reset bằng cách set bit 24 (RMVF)": "Clear reset flags by setting bit 24 (RMVF)",
    "Nháy LED chậm báo hiệu sự cố": "Slow LED blink to indicate fault condition",
    "Khởi động bình thường (Cắm nguồn)": "Normal system startup (Power-on reset)",
    "NẾU BẤM NÚT PA0: Cố tình treo vòng lặp để test Watchdog": "IF PA0 BUTTON PRESSED: Intentionally hang loop to test Watchdog",
    "Hệ thống vừa bị cứu bởi Watchdog!": "System was recovered by Watchdog!",
    "Xóa các cờ reset": "Clear reset flags",

    # ADC
    "1. Cấp clock cho GPIOA và ADC1 trên bus APB2": "1. Enable clocks for GPIOA and ADC1 on APB2 bus",
    "2. Cấu hình chân PA0 (ADC1_IN0): Chế độ Analog Input": "2. Configure pin PA0 (ADC1_IN0): Analog Input mode",
    "3. Cấu hình bộ chia tần số ADCCLK: 72MHz / 6 = 12MHz": "3. Configure ADCCLK prescaler: 72MHz / 6 = 12MHz (max 14MHz)",
    "4. Cấu hình số kênh chuyển đổi": "4. Configure number of conversion channels",
    "5. Cấu hình thời gian lấy mẫu": "5. Configure sampling time",
    "6. Bật nguồn bộ chuyển đổi ADC": "6. Power on ADC converter",
    "7. Hiệu chuẩn ADC (Bắt buộc theo tài liệu ST)": "7. Calibrate ADC (Mandatory per ST reference manual)",
    "Khởi động chuyển đổi phần mềm": "Start software conversion",
    "Chờ chuyển đổi hoàn tất": "Wait for conversion complete (EOC)",
    "Đọc giá trị dữ liệu 12-bit": "Read 12-bit conversion result",

    # USART
    "Cấu hình chân PA9 (USART1_TX): Alternate Function Push-Pull 50MHz": "Configure PA9 (USART1_TX): Alternate Function Push-Pull 50MHz",
    "Cấu hình chân PA10 (USART1_RX): Input Floating": "Configure PA10 (USART1_RX): Input Floating",
    "Cấu hình Baud Rate": "Configure Baud Rate",
    "Bật bộ truyền và bộ nhận": "Enable Transmitter and Receiver",
    "Bật module USART": "Enable USART module",
    "Gửi một chuỗi ký tự qua UART": "Send string over UART",
    "Gửi một ký tự qua UART": "Send single character over UART",
    "Nhận một ký tự từ UART": "Receive single character from UART",
    "Chờ bộ đệm truyền rỗng (TXE)": "Wait until transmit data register empty (TXE)",
    "Chờ truyền xong toàn bộ khung dữ liệu (TC)": "Wait until transmission complete (TC)",
    "Chờ nhận được dữ liệu (RXNE)": "Wait until receive data register not empty (RXNE)",
    "Ghi đè hàm fputc để dùng hàm printf chuẩn": "Retarget fputc to enable standard printf support",

    # I2C
    "Gửi tín hiệu START": "Generate START condition",
    "Gửi tín hiệu STOP": "Generate STOP condition",
    "Chờ tín hiệu START phát thành công (SB)": "Wait for START condition generated (SB flag)",
    "Gửi địa chỉ thiết bị Slave": "Send Slave device address",
    "Chờ gửi xong địa chỉ (ADDR)": "Wait for address sent (ADDR flag)",
    "Chờ bộ đệm dữ liệu truyền rỗng (TXE)": "Wait for transmit buffer empty (TXE flag)",

    # SPI
    "Kéo chân CS xuống mức 0 để chọn chip": "Pull CS LOW to select chip",
    "Kéo chân CS lên mức 1 để hủy chọn chip": "Pull CS HIGH to deselect chip",
    "Chờ bộ đệm truyền rỗng (TXE)": "Wait for transmit buffer empty (TXE flag)",
    "Chờ nhận dữ liệu hoàn tất (RXNE)": "Wait for receive buffer not empty (RXNE flag)",

    # FreeRTOS
    "Định nghĩa Task 1": "Task 1 definition",
    "Định nghĩa Task 2": "Task 2 definition",
    "Tạo Task 1": "Create Task 1",
    "Tạo Task 2": "Create Task 2",
    "Khởi chạy hệ điều hành FreeRTOS": "Start FreeRTOS scheduler",
    "Vòng lặp Task không bao giờ được return": "Task loop must never return",
    "Delay tương đối trong FreeRTOS": "FreeRTOS relative delay",
    "Delay chính xác chu kỳ trong FreeRTOS": "FreeRTOS exact periodic delay",
}

# Regex replacement rules (pattern, replacement)
REGEX_RULES = [
    # Numbered clock steps
    (r'//\s*(\d+)\.\s*Cấp\s+(?:xung\s+)?clock\s+cho\s+(.+?)(?:\s+trên\s+bus\s+(.+?))?$',
     lambda m: f"// {m.group(1)}. Enable peripheral clock for {m.group(2)}" + (f" on {m.group(3)} bus" if m.group(3) else "")),
    (r'//\s*(\d+)\.\s*Cấp\s+xung\s+nhịp\s+cho\s+(.+?)(?:\s+trên\s+bus\s+(.+?))?$',
     lambda m: f"// {m.group(1)}. Enable peripheral clock for {m.group(2)}" + (f" on {m.group(3)} bus" if m.group(3) else "")),
    
    # Numbered pin configuration
    (r'//\s*(\d+)\.\s*Cấu\s+hình\s+(?:chân\s+)?([A-P][A-Z0-9_]+)\s*:\s*(.+)$',
     lambda m: f"// {m.group(1)}. Configure pin {m.group(2)}: {translate_mode(m.group(3))}"),

    # LED controls
    (r'//\s*Bật\s+LED(?:\s+([A-P][A-Z0-9_]+))?(?:\s*\((.*?)\))?',
     lambda m: f"// Turn on LED" + (f" {m.group(1)}" if m.group(1) else "") + (f" ({translate_paren(m.group(2))})" if m.group(2) else "")),
    (r'//\s*Tắt\s+LED(?:\s+([A-P][A-Z0-9_]+))?(?:\s*\((.*?)\))?',
     lambda m: f"// Turn off LED" + (f" {m.group(1)}" if m.group(1) else "") + (f" ({translate_paren(m.group(2))})" if m.group(2) else "")),
    (r'//\s*Đảo\s+trạng\s+thái\s+LED(?:\s+([A-P][A-Z0-9_]+))?',
     lambda m: f"// Toggle LED state" + (f" {m.group(1)}" if m.group(1) else "")),

    # Waiting flags
    (r'//\s*Chờ\s+cờ\s+([A-Z0-9_]+)\s+(?:được\s+bật|hoàn\s+tất|sẵn\s+sàng)',
     lambda m: f"// Wait until {m.group(1)} flag is set"),
    (r'//\s*Chờ\s+([A-Z0-9_]+)\s+sẵn\s+sàng',
     lambda m: f"// Wait until {m.group(1)} is ready"),
    (r'//\s*Xóa\s+cờ\s+(?:ngắt\s+)?([A-Z0-9_]+)',
     lambda m: f"// Clear {m.group(1)} flag"),
]

def translate_mode(txt):
    txt = txt.replace("Chế độ", "Mode")
    txt = txt.replace("Tốc độ", "Speed")
    txt = txt.replace("kéo lên", "pull-up")
    txt = txt.replace("kéo xuống", "pull-down")
    txt = txt.replace("thả nổi", "floating")
    return txt

def translate_paren(txt):
    if not txt: return ""
    txt = txt.replace("Active-Low", "Active-Low")
    txt = txt.replace("kéo chân xuống mức 0", "pull pin LOW")
    txt = txt.replace("kéo chân lên mức 1", "set pin HIGH")
    txt = txt.replace("ghi mức 0", "write LOW")
    txt = txt.replace("ghi mức 1", "write HIGH")
    txt = txt.replace("mức 0", "LOW")
    txt = txt.replace("mức 1", "HIGH")
    return txt

# Common vocabulary dictionary for general words
WORD_MAP = [
    (r'\bCấp xung nhịp cho\b', 'Enable clock for'),
    (r'\bCấp xung nhịp\b', 'Enable clock'),
    (r'\bCấp xung clock cho\b', 'Enable clock for'),
    (r'\bCấp xung clock\b', 'Enable clock'),
    (r'\bCấp clock cho\b', 'Enable clock for'),
    (r'\bCấp clock\b', 'Enable clock'),
    (r'\bCấu hình chân\b', 'Configure pin'),
    (r'\bCấu hình\b', 'Configure'),
    (r'\bKhởi tạo\b', 'Initialize'),
    (r'\bKích hoạt\b', 'Enable'),
    (r'\bVô hiệu hóa\b', 'Disable'),
    (r'\bBật\b', 'Enable'),
    (r'\bTắt\b', 'Disable'),
    (r'\bXóa cờ\b', 'Clear flag'),
    (r'\bKiểm tra cờ\b', 'Check flag'),
    (r'\bKiểm tra\b', 'Check'),
    (r'\bChờ\b', 'Wait until'),
    (r'\bĐọc\b', 'Read'),
    (r'\bGhi\b', 'Write'),
    (r'\bGửi\b', 'Send'),
    (r'\bNhận\b', 'Receive'),
    (r'\bNạp lại\b', 'Reload'),
    (r'\bCho chó ăn\b', 'Feed watchdog'),
    (r'\bNuôi chó\b', 'Feed watchdog'),
    (r'\bNgắt\b', 'Interrupt'),
    (r'\bHàm xử lý ngắt\b', 'Interrupt handler'),
    (r'\bHàm ngắt\b', 'ISR'),
    (r'\bHệ số chia\b', 'Prescaler'),
    (r'\bGiá trị nạp lại\b', 'Reload value'),
    (r'\bThời gian lấy mẫu\b', 'Sampling time'),
    (r'\bĐộ rộng xung\b', 'Pulse width'),
    (r'\bChu kỳ\b', 'Period'),
    (r'\bTần số\b', 'Frequency'),
    (r'\bBộ đếm\b', 'Counter'),
    (r'\bChế độ\b', 'Mode'),
    (r'\bBộ nhớ\b', 'Memory'),
    (r'\bNgoại vi\b', 'Peripheral'),
    (r'\bThanh ghi\b', 'Register'),
    (r'\bCon trỏ\b', 'Pointer'),
    (r'\bĐịa chỉ\b', 'Address'),
    (r'\bMảng\b', 'Array'),
    (r'\bBộ đệm\b', 'Buffer'),
    (r'\bChuỗi\b', 'String'),
    (r'\bKý tự\b', 'Character'),
    (r'\bHoàn tất\b', 'complete'),
    (r'\bThành công\b', 'successful'),
    (r'\bThất bại\b', 'failed'),
    (r'\bMặc định\b', 'Default'),
    (r'\bTối đa\b', 'maximum'),
    (r'\bTối thiểu\b', 'minimum'),
    (r'\bBắt buộc\b', 'Mandatory'),
    (r'\bLưu ý\b', 'Note'),
    (r'\bCảnh báo\b', 'Warning'),
    (r'\bKhởi động lại\b', 'Restart'),
    (r'\bKhởi động\b', 'Startup'),
    (r'\bTreo máy\b', 'System hang'),
    (r'\bSự cố\b', 'Fault'),
    (r'\bLỗi\b', 'Error'),
    (r'\bTrạng thái\b', 'State'),
    (r'\bVòng lặp vô tận\b', 'Infinite loop'),
    (r'\bVòng lặp\b', 'Loop'),
    (r'\bNút nhấn\b', 'Button'),
    (r'\bNút bấm\b', 'Button'),
    (r'\bPhím\b', 'Key'),
    (r'\bChống rung\b', 'Debounce'),
    (r'\bĐộ trễ\b', 'Delay'),
    (r'\bThời gian trễ\b', 'Delay time'),
    (r'\bBiến trở\b', 'Potentiometer'),
    (r'\bCảm biến\b', 'Sensor'),
    (r'\bNhiệt độ\b', 'Temperature'),
    (r'\bĐiện áp\b', 'Voltage'),
    (r'\bDòng điện\b', 'Current'),
    (r'\bCông suất\b', 'Power'),
    (r'\bĐộng cơ\b', 'Motor'),
]

def translate_comment(c_text):
    c_clean = c_text.strip()
    # Check exact match
    if c_clean in EXACT_MAP:
        return EXACT_MAP[c_clean]
    
    # Check regex rules
    for pattern, repl in REGEX_RULES:
        if re.search(pattern, '// ' + c_clean, re.IGNORECASE):
            res = re.sub(pattern, repl, '// ' + c_clean, flags=re.IGNORECASE)
            return res.replace('// ', '').strip()

    # Fallback: Apply word replacements
    res = c_clean
    for pat, rep in WORD_MAP:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    
    # Clean up any residual Vietnamese tones if words were replaced
    return res

print("Translation module ready.")
