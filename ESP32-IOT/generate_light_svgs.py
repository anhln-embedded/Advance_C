import os

# Paths to update
dirs = [
    r"F:\Advance_C\ESP32-IOT\images",
    r"F:\embedded-lab-web\public\images",
    r"F:\embedded-lab-web\public\images\esp32"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

def save_svg(filename, content):
    for d in dirs:
        p = os.path.join(d, filename)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content.strip())
    print(f"Updated light SVG: {filename}")

# ==============================================================================
# 1. Bai 01: Pinout (LIGHT THEME)
# ==============================================================================
svg_pinout = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 640" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <defs>
    <filter id="lightShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Outer Border -->
  <rect x="10" y="10" width="900" height="620" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>

  <!-- Title -->
  <text x="460" y="45" text-anchor="middle" fill="#0f172a" font-size="22" font-weight="800">SƠ ĐỒ BẢN ĐỒ CHÂN (PINOUT) ESP32 DEVKIT V1</text>
  <text x="460" y="70" text-anchor="middle" fill="#64748b" font-size="13" font-weight="600">Tensilica Xtensa Dual-Core 32-bit LX6 - 30 Chân Tiêu Chuẩn</text>

  <!-- Legend -->
  <g transform="translate(130, 92)">
    <rect x="0" y="0" width="14" height="14" fill="#dc2626" rx="3"/>
    <text x="20" y="12" fill="#334155" font-size="12" font-weight="600">Power (3V3, GND, VIN)</text>
    <rect x="180" y="0" width="14" height="14" fill="#16a34a" rx="3"/>
    <text x="200" y="12" fill="#334155" font-size="12" font-weight="600">GPIO Thông Thường</text>
    <rect x="360" y="0" width="14" height="14" fill="#ea580c" rx="3"/>
    <text x="380" y="12" fill="#334155" font-size="12" font-weight="600">ADC1 (An Toàn)</text>
    <rect x="520" y="0" width="14" height="14" fill="#e11d48" rx="3"/>
    <text x="540" y="12" fill="#334155" font-size="12" font-weight="600">Input Only (34-39)</text>
  </g>

  <!-- ESP32 Board Representation -->
  <rect x="360" y="130" width="200" height="470" rx="12" fill="#1e293b" stroke="#0f172a" stroke-width="3" filter="url(#lightShadow)"/>
  
  <!-- Wi-Fi Antenna -->
  <rect x="395" y="135" width="130" height="45" rx="4" fill="#334155" stroke="#475569"/>
  <path d="M 410 155 L 430 145 L 450 155 L 470 145 L 490 155 L 510 145" fill="none" stroke="#fbbf24" stroke-width="2"/>
  <text x="460" y="172" text-anchor="middle" fill="#fbbf24" font-size="10" font-weight="bold">ANTENNA WI-FI / BLE</text>

  <!-- Metal Shield (SoC) -->
  <rect x="390" y="195" width="140" height="140" rx="8" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <text x="460" y="260" text-anchor="middle" fill="#ffffff" font-size="15" font-weight="bold">ESP-WROOM-32</text>
  <text x="460" y="280" text-anchor="middle" fill="#94a3b8" font-size="11">Espressif Systems</text>

  <!-- Micro USB Port -->
  <rect x="430" y="565" width="60" height="30" rx="4" fill="#64748b"/>
  <text x="460" y="584" text-anchor="middle" fill="#ffffff" font-size="10" font-weight="bold">USB</text>

  <!-- Buttons -->
  <rect x="375" y="545" width="26" height="26" rx="4" fill="#9333ea"/>
  <text x="388" y="562" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="bold">EN</text>
  <rect x="519" y="545" width="26" height="26" rx="4" fill="#d97706"/>
  <text x="532" y="562" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="bold">BOOT</text>

  <!-- LEFT PINS (15 Pins) -->
  <g font-size="11" font-weight="bold">
    <!-- Pin 1: 3V3 -->
    <rect x="330" y="195" width="30" height="16" fill="#dc2626" rx="3"/>
    <text x="320" y="208" text-anchor="end" fill="#dc2626">3.3V (Nguồn ra)</text>
    <!-- Pin 2: EN -->
    <rect x="330" y="220" width="30" height="16" fill="#9333ea" rx="3"/>
    <text x="320" y="233" text-anchor="end" fill="#9333ea">EN (Reset Chip)</text>
    <!-- Pin 3: VP / GPIO 36 -->
    <rect x="330" y="245" width="30" height="16" fill="#e11d48" rx="3"/>
    <text x="320" y="258" text-anchor="end" fill="#be123c">GPIO 36 (VP / ADC1_CH0 - In Only)</text>
    <!-- Pin 4: VN / GPIO 39 -->
    <rect x="330" y="270" width="30" height="16" fill="#e11d48" rx="3"/>
    <text x="320" y="283" text-anchor="end" fill="#be123c">GPIO 39 (VN / ADC1_CH3 - In Only)</text>
    <!-- Pin 5: GPIO 34 -->
    <rect x="330" y="295" width="30" height="16" fill="#e11d48" rx="3"/>
    <text x="320" y="308" text-anchor="end" fill="#be123c">GPIO 34 (ADC1_CH6 - In Only)</text>
    <!-- Pin 6: GPIO 35 -->
    <rect x="330" y="320" width="30" height="16" fill="#e11d48" rx="3"/>
    <text x="320" y="333" text-anchor="end" fill="#be123c">GPIO 35 (ADC1_CH7 - In Only)</text>
    <!-- Pin 7: GPIO 32 -->
    <rect x="330" y="345" width="30" height="16" fill="#ea580c" rx="3"/>
    <text x="320" y="358" text-anchor="end" fill="#ea580c">GPIO 32 (ADC1_CH4 / Touch 9)</text>
    <!-- Pin 8: GPIO 33 -->
    <rect x="330" y="370" width="30" height="16" fill="#ea580c" rx="3"/>
    <text x="320" y="383" text-anchor="end" fill="#ea580c">GPIO 33 (ADC1_CH5 / Touch 8)</text>
    <!-- Pin 9: GPIO 25 -->
    <rect x="330" y="395" width="30" height="16" fill="#0284c7" rx="3"/>
    <text x="320" y="408" text-anchor="end" fill="#0369a1">GPIO 25 (DAC1 / ADC2_CH8)</text>
    <!-- Pin 10: GPIO 26 -->
    <rect x="330" y="420" width="30" height="16" fill="#0284c7" rx="3"/>
    <text x="320" y="433" text-anchor="end" fill="#0369a1">GPIO 26 (DAC2 / ADC2_CH9)</text>
    <!-- Pin 11: GPIO 27 -->
    <rect x="330" y="445" width="30" height="16" fill="#16a34a" rx="3"/>
    <text x="320" y="458" text-anchor="end" fill="#15803d">GPIO 27 (Touch 7)</text>
    <!-- Pin 12: GPIO 14 -->
    <rect x="330" y="470" width="30" height="16" fill="#16a34a" rx="3"/>
    <text x="320" y="483" text-anchor="end" fill="#15803d">GPIO 14 (HSPI_CLK)</text>
    <!-- Pin 13: GPIO 12 -->
    <rect x="330" y="495" width="30" height="16" fill="#16a34a" rx="3"/>
    <text x="320" y="508" text-anchor="end" fill="#15803d">GPIO 12 (HSPI_MISO)</text>
    <!-- Pin 14: GND -->
    <rect x="330" y="520" width="30" height="16" fill="#475569" rx="3"/>
    <text x="320" y="533" text-anchor="end" fill="#334155">GND (Mass 0V)</text>
    <!-- Pin 15: VIN -->
    <rect x="330" y="545" width="30" height="16" fill="#dc2626" rx="3"/>
    <text x="320" y="558" text-anchor="end" fill="#dc2626">VIN (Nguồn vào 5V)</text>
  </g>

  <!-- RIGHT PINS (15 Pins) -->
  <g font-size="11" font-weight="bold">
    <!-- Pin 1: GPIO 23 -->
    <rect x="560" y="195" width="30" height="16" fill="#16a34a" rx="3"/>
    <text x="600" y="208" fill="#15803d">GPIO 23 (VSPI_MOSI)</text>
    <!-- Pin 2: GPIO 22 -->
    <rect x="560" y="220" width="30" height="16" fill="#0891b2" rx="3"/>
    <text x="600" y="233" fill="#0e7490">GPIO 22 (I2C_SCL)</text>
    <!-- Pin 3: TX0 (GPIO 1) -->
    <rect x="560" y="245" width="30" height="16" fill="#2563eb" rx="3"/>
    <text x="600" y="258" fill="#1d4ed8">TX0 / GPIO 1 (Console TX)</text>
    <!-- Pin 4: RX0 (GPIO 3) -->
    <rect x="560" y="270" width="30" height="16" fill="#2563eb" rx="3"/>
    <text x="600" y="283" fill="#1d4ed8">RX0 / GPIO 3 (Console RX)</text>
    <!-- Pin 5: GPIO 21 -->
    <rect x="560" y="295" width="30" height="16" fill="#0891b2" rx="3"/>
    <text x="600" y="308" fill="#0e7490">GPIO 21 (I2C_SDA)</text>
    <!-- Pin 6: GPIO 19 -->
    <rect x="560" y="320" width="30" height="16" fill="#16a34a" rx="3"/>
    <text x="600" y="333" fill="#15803d">GPIO 19 (VSPI_MISO)</text>
    <!-- Pin 7: GPIO 18 -->
    <rect x="560" y="345" width="30" height="16" fill="#16a34a" rx="3"/>
    <text x="600" y="358" fill="#15803d">GPIO 18 (VSPI_SCK / PWM)</text>
    <!-- Pin 8: GPIO 5 -->
    <rect x="560" y="370" width="30" height="16" fill="#16a34a" rx="3"/>
    <text x="600" y="383" fill="#15803d">GPIO 5 (VSPI_CS)</text>
    <!-- Pin 9: GPIO 17 -->
    <rect x="560" y="395" width="30" height="16" fill="#2563eb" rx="3"/>
    <text x="600" y="408" fill="#1d4ed8">TX2 / GPIO 17 (UART2_TX)</text>
    <!-- Pin 10: GPIO 16 -->
    <rect x="560" y="420" width="30" height="16" fill="#2563eb" rx="3"/>
    <text x="600" y="433" fill="#1d4ed8">RX2 / GPIO 16 (UART2_RX)</text>
    <!-- Pin 11: GPIO 4 -->
    <rect x="560" y="445" width="30" height="16" fill="#16a34a" rx="3"/>
    <text x="600" y="458" fill="#15803d">GPIO 4 (Touch 0)</text>
    <!-- Pin 12: GPIO 2 -->
    <rect x="560" y="470" width="30" height="16" fill="#2563eb" rx="3"/>
    <text x="600" y="483" fill="#1d4ed8">GPIO 2 (LED Onboard)</text>
    <!-- Pin 13: GPIO 15 -->
    <rect x="560" y="495" width="30" height="16" fill="#16a34a" rx="3"/>
    <text x="600" y="508" fill="#15803d">GPIO 15 (HSPI_CS)</text>
    <!-- Pin 14: GND -->
    <rect x="560" y="520" width="30" height="16" fill="#475569" rx="3"/>
    <text x="600" y="533" fill="#334155">GND (Mass 0V)</text>
    <!-- Pin 15: 3V3 -->
    <rect x="560" y="545" width="30" height="16" fill="#dc2626" rx="3"/>
    <text x="600" y="558" fill="#dc2626">3.3V (Nguồn ra)</text>
  </g>
</svg>
"""
save_svg("bai01_esp32_pinout.svg", svg_pinout)

# ==============================================================================
# 2. Bai 01: Wokwi Interface Guide (LIGHT THEME)
# ==============================================================================
svg_wokwi = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 490" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <!-- Container Card -->
  <rect x="10" y="10" width="840" height="470" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>

  <text x="430" y="42" text-anchor="middle" fill="#0f172a" font-size="20" font-weight="800">HƯỚNG DẪN GIAO DIỆN MÔ PHỎNG WOKWI ESP32</text>
  <text x="430" y="65" text-anchor="middle" fill="#0284c7" font-size="12" font-weight="600">https://wokwi.com/projects/new/esp32</text>

  <!-- Top Toolbar -->
  <rect x="30" y="85" width="800" height="42" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="45" y="93" width="85" height="26" rx="6" fill="#16a34a"/>
  <text x="87" y="110" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="bold">► Start</text>
  <rect x="140" y="93" width="95" height="26" rx="6" fill="#2563eb"/>
  <text x="187" y="110" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="bold">+ Add Part</text>
  <rect x="245" y="93" width="70" height="26" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="280" y="110" text-anchor="middle" fill="#334155" font-size="11" font-weight="600">Restart</text>
  <text x="810" y="111" text-anchor="end" fill="#ea580c" font-size="12" font-weight="bold">ESP32 DevKit V4</text>

  <!-- Left: Code Editor -->
  <rect x="30" y="140" width="385" height="240" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="30" y="140" width="385" height="32" rx="8" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="45" y="161" fill="#2563eb" font-size="12" font-weight="bold">sketch.ino</text>
  <text x="135" y="161" fill="#64748b" font-size="12">diagram.json</text>
  <text x="235" y="161" fill="#64748b" font-size="12">libraries.txt</text>

  <text x="45" y="195" fill="#7c3aed" font-size="11" font-weight="600">#define LED_PIN 2</text>
  <text x="45" y="215" fill="#0f172a" font-size="11" font-weight="600">void setup() {</text>
  <text x="65" y="235" fill="#2563eb" font-size="11">Serial.begin(115200);</text>
  <text x="65" y="255" fill="#16a34a" font-size="11">pinMode(LED_PIN, OUTPUT);</text>
  <text x="45" y="275" fill="#0f172a" font-size="11" font-weight="600">}</text>
  <text x="45" y="295" fill="#0f172a" font-size="11" font-weight="600">void loop() { ... }</text>

  <!-- Right: Simulation Board Area -->
  <rect x="435" y="140" width="395" height="240" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="632" y="165" text-anchor="middle" fill="#0f172a" font-size="12" font-weight="bold">KHÔNG GIAN LẮP RÁP MẠCH ĐIỆN TỬ</text>
  
  <!-- Mini ESP32 -->
  <rect x="470" y="185" width="105" height="175" rx="6" fill="#1e293b" stroke="#0f172a"/>
  <text x="522" y="270" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="bold">ESP32</text>
  
  <!-- LED & Resistor -->
  <circle cx="670" cy="225" r="15" fill="#ef4444" stroke="#dc2626" stroke-width="2"/>
  <text x="670" y="229" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="bold">LED</text>
  <rect x="655" y="260" width="30" height="12" fill="#d97706" rx="2"/>
  <text x="670" y="288" text-anchor="middle" fill="#475569" font-size="10" font-weight="bold">220Ω</text>

  <!-- Wires -->
  <path d="M 575 215 Q 620 215 655 225" fill="none" stroke="#16a34a" stroke-width="2.5"/>
  <path d="M 670 240 L 670 260" fill="none" stroke="#ef4444" stroke-width="2.5"/>
  <path d="M 670 272 Q 670 330 575 340" fill="none" stroke="#475569" stroke-width="2.5"/>

  <!-- Bottom: Serial Monitor -->
  <rect x="30" y="395" width="800" height="70" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="45" y="415" fill="#475569" font-size="11" font-weight="bold">SERIAL MONITOR (115200 BAUD)</text>
  <text x="45" y="435" fill="#16a34a" font-size="11" font-weight="600">[SYSTEM] ESP32 Ready! Ket noi thanh cong!</text>
  <text x="45" y="452" fill="#0f172a" font-size="11">[LOG] LED: BAT (HIGH - 3.3V)</text>
</svg>
"""
save_svg("bai01_wokwi_interface.svg", svg_wokwi)

# ==============================================================================
# 3. Bai 02: Pull-up vs Pull-down Resistor (LIGHT THEME)
# ==============================================================================
svg_pullup = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 390" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="800" height="370" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="410" y="42" text-anchor="middle" fill="#0f172a" font-size="20" font-weight="800">NGUYÊN LÝ ĐIỆN TRỞ KÉO PULL-UP VÀ PULL-DOWN</text>

  <!-- Left: Pull-up Circuit -->
  <g transform="translate(60, 65)">
    <rect x="0" y="0" width="320" height="290" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="160" y="30" text-anchor="middle" fill="#16a34a" font-size="15" font-weight="bold">MẠCH PULL-UP (KÉO LÊN 3.3V)</text>
    
    <!-- 3.3V Rail -->
    <line x1="90" y1="60" x2="150" y2="60" stroke="#dc2626" stroke-width="3"/>
    <text x="120" y="52" text-anchor="middle" fill="#dc2626" font-size="12" font-weight="bold">VCC 3.3V</text>

    <!-- Resistor R -->
    <line x1="120" y1="60" x2="120" y2="85" stroke="#334155" stroke-width="2"/>
    <rect x="110" y="85" width="20" height="40" fill="#fed7aa" stroke="#ea580c" stroke-width="1.5" rx="2"/>
    <text x="145" y="110" fill="#ea580c" font-size="11" font-weight="bold">R (10kΩ)</text>
    <line x1="120" y1="125" x2="120" y2="150" stroke="#334155" stroke-width="2"/>

    <!-- Junction Node to GPIO -->
    <circle cx="120" cy="150" r="4" fill="#2563eb"/>
    <line x1="120" y1="150" x2="230" y2="150" stroke="#2563eb" stroke-width="3"/>
    <text x="235" y="154" fill="#2563eb" font-size="12" font-weight="bold">GPIO ESP32</text>

    <!-- Switch to GND -->
    <line x1="120" y1="150" x2="120" y2="180" stroke="#334155" stroke-width="2"/>
    <circle cx="120" cy="180" r="3" fill="#334155"/>
    <line x1="120" y1="180" x2="135" y2="205" stroke="#334155" stroke-width="2"/>
    <circle cx="120" cy="210" r="3" fill="#334155"/>
    <text x="155" y="200" fill="#475569" font-size="11" font-weight="600">Nút nhấn</text>
    
    <line x1="120" y1="210" x2="120" y2="235" stroke="#475569" stroke-width="2"/>
    <line x1="100" y1="235" x2="140" y2="235" stroke="#475569" stroke-width="3"/>
    <text x="120" y="255" text-anchor="middle" fill="#475569" font-size="11" font-weight="bold">GND (0V)</text>

    <text x="20" y="275" fill="#0f172a" font-size="11" font-weight="600">Thả nút: GPIO = HIGH (1) | Bấm: GPIO = LOW (0)</text>
  </g>

  <!-- Right: Pull-down Circuit -->
  <g transform="translate(440, 65)">
    <rect x="0" y="0" width="320" height="290" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="160" y="30" text-anchor="middle" fill="#d97706" font-size="15" font-weight="bold">MẠCH PULL-DOWN (KÉO XUỐNG 0V)</text>

    <!-- 3.3V Rail -->
    <line x1="90" y1="60" x2="150" y2="60" stroke="#dc2626" stroke-width="3"/>
    <text x="120" y="52" text-anchor="middle" fill="#dc2626" font-size="12" font-weight="bold">VCC 3.3V</text>

    <!-- Switch -->
    <line x1="120" y1="60" x2="120" y2="85" stroke="#334155" stroke-width="2"/>
    <circle cx="120" cy="85" r="3" fill="#334155"/>
    <line x1="120" y1="85" x2="135" y2="110" stroke="#334155" stroke-width="2"/>
    <circle cx="120" cy="115" r="3" fill="#334155"/>
    <text x="155" y="105" fill="#475569" font-size="11" font-weight="600">Nút nhấn</text>

    <line x1="120" y1="115" x2="120" y2="150" stroke="#334155" stroke-width="2"/>

    <!-- Junction Node to GPIO -->
    <circle cx="120" cy="150" r="4" fill="#2563eb"/>
    <line x1="120" y1="150" x2="230" y2="150" stroke="#2563eb" stroke-width="3"/>
    <text x="235" y="154" fill="#2563eb" font-size="12" font-weight="bold">GPIO ESP32</text>

    <!-- Resistor R to GND -->
    <rect x="110" y="165" width="20" height="40" fill="#fed7aa" stroke="#ea580c" stroke-width="1.5" rx="2"/>
    <line x1="120" y1="150" x2="120" y2="165" stroke="#334155" stroke-width="2"/>
    <text x="145" y="190" fill="#ea580c" font-size="11" font-weight="bold">R (10kΩ)</text>
    <line x1="120" y1="205" x2="120" y2="235" stroke="#475569" stroke-width="2"/>
    <line x1="100" y1="235" x2="140" y2="235" stroke="#475569" stroke-width="3"/>
    <text x="120" y="255" text-anchor="middle" fill="#475569" font-size="11" font-weight="bold">GND (0V)</text>

    <text x="20" y="275" fill="#0f172a" font-size="11" font-weight="600">Thả nút: GPIO = LOW (0) | Bấm: GPIO = HIGH (1)</text>
  </g>
</svg>
"""
save_svg("bai02_gpio_pullup_pulldown.svg", svg_pullup)

# ==============================================================================
# 4. Bai 03: Interrupt Flow (LIGHT THEME)
# ==============================================================================
svg_intr_flow = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 320" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="820" height="300" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="420" y="38" text-anchor="middle" fill="#0f172a" font-size="18" font-weight="800">SƠ ĐỒ LUỒNG THỰC THI NGẮT PHẦN CỨNG (INTERRUPT FLOW)</text>
  
  <!-- Main Execution Stream -->
  <g transform="translate(60, 60)">
    <rect x="0" y="0" width="220" height="210" rx="10" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
    <text x="110" y="30" text-anchor="middle" fill="#2563eb" font-size="14" font-weight="bold">CHƯƠNG TRÌNH CHÍNH (loop)</text>
    
    <rect x="20" y="50" width="180" height="35" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="110" y="72" text-anchor="middle" fill="#334155" font-size="11">Đang đọc cảm biến...</text>

    <rect x="20" y="98" width="180" height="35" rx="6" fill="#fef3c7" stroke="#f59e0b"/>
    <text x="110" y="120" text-anchor="middle" fill="#b45309" font-size="11" font-weight="bold">Chạy delay(2000)...</text>

    <rect x="20" y="145" width="180" height="35" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="110" y="167" text-anchor="middle" fill="#334155" font-size="11">Gửi dữ liệu Wi-Fi...</text>
  </g>

  <!-- Hardware Event -->
  <g transform="translate(330, 105)">
    <circle cx="45" cy="45" r="40" fill="#fee2e2" stroke="#ef4444" stroke-width="2.5"/>
    <text x="45" y="40" text-anchor="middle" fill="#b91c1c" font-size="11" font-weight="bold">NGẮT NGOÀI</text>
    <text x="45" y="55" text-anchor="middle" fill="#b91c1c" font-size="9" font-weight="bold">(Bấm nút)</text>

    <line x1="-35" y1="15" x2="0" y2="35" stroke="#ef4444" stroke-width="2.5"/>
    <polygon points="5,38 -8,31 -4,42" fill="#ef4444"/>
  </g>

  <!-- ISR Area -->
  <g transform="translate(480, 60)">
    <rect x="0" y="0" width="300" height="210" rx="10" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
    <text x="150" y="30" text-anchor="middle" fill="#16a34a" font-size="14" font-weight="bold">TRÌNH PHỤC VỤ NGẮT (ISR)</text>
    <text x="150" y="48" text-anchor="middle" fill="#d97706" font-size="10" font-weight="bold">Khai báo IRAM_ATTR (Chạy trên RAM nội)</text>

    <rect x="20" y="65" width="260" height="32" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="150" y="85" text-anchor="middle" fill="#334155" font-size="10">1. Lưu ngữ cảnh thanh ghi CPU</text>

    <rect x="20" y="108" width="260" height="34" rx="6" fill="#dcfce7" stroke="#16a34a"/>
    <text x="150" y="129" text-anchor="middle" fill="#15803d" font-size="11" font-weight="bold">2. Bật cờ buttonTriggered = true;</text>

    <rect x="20" y="152" width="260" height="32" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="150" y="172" text-anchor="middle" fill="#334155" font-size="10">3. Khôi phục CPU &amp; Quay lại loop</text>
  </g>

  <!-- Return Arrow -->
  <path d="M 480 220 Q 380 265 290 220" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-dasharray="4"/>
  <polygon points="285,217 298,216 293,226" fill="#16a34a"/>
  <text x="385" y="270" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="bold">Tự động quay lại tiếp tục lệnh cũ</text>
</svg>
"""
save_svg("bai03_interrupt_flow.svg", svg_intr_flow)

# ==============================================================================
# 5. Bai 03: Bouncing vs Debounce (LIGHT THEME)
# ==============================================================================
svg_bounce = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 350" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="820" height="330" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="420" y="38" text-anchor="middle" fill="#0f172a" font-size="18" font-weight="800">HIỆN TƯỢNG RUNG PHÍM (BOUNCING) VÀ LỌC XUNG DEBOUNCE</text>

  <!-- Top Graph: Bouncing Signal -->
  <g transform="translate(60, 55)">
    <text x="0" y="20" fill="#dc2626" font-size="13" font-weight="bold">1. Tín hiệu thô trực tiếp từ nút nhấn cơ khí (Bị rung 5 - 20ms):</text>
    <line x1="40" y1="40" x2="40" y2="110" stroke="#cbd5e1" stroke-width="2"/>
    <line x1="40" y1="110" x2="730" y2="110" stroke="#cbd5e1" stroke-width="2"/>
    <text x="15" y="55" fill="#64748b" font-size="10" font-weight="bold">3.3V</text>
    <text x="20" y="115" fill="#64748b" font-size="10" font-weight="bold">0V</text>

    <!-- Waveform with bouncing -->
    <path d="M 40 50 L 180 50 L 185 110 L 190 60 L 195 110 L 200 50 L 205 110 L 210 70 L 220 110 L 520 110 L 525 50 L 530 90 L 535 50 L 730 50" fill="none" stroke="#dc2626" stroke-width="2.5"/>
    
    <!-- Zone highlight -->
    <rect x="180" y="40" width="45" height="70" fill="#fee2e2" opacity="0.6"/>
    <text x="202" y="130" text-anchor="middle" fill="#dc2626" font-size="10" font-weight="bold">Rung tiếp điểm (~15ms)</text>
    <text x="370" y="90" text-anchor="middle" fill="#475569" font-size="11" font-weight="600">Thời gian ngón tay giữ nút bấm</text>
  </g>

  <!-- Bottom Graph: Clean Debounced Signal -->
  <g transform="translate(60, 200)">
    <text x="0" y="20" fill="#16a34a" font-size="13" font-weight="bold">2. Tín hiệu logic sạch sau khi xử lý phần mềm Debounce (millis):</text>
    <line x1="40" y1="40" x2="40" y2="110" stroke="#cbd5e1" stroke-width="2"/>
    <line x1="40" y1="110" x2="730" y2="110" stroke="#cbd5e1" stroke-width="2"/>
    <text x="15" y="55" fill="#64748b" font-size="10" font-weight="bold">3.3V</text>
    <text x="20" y="115" fill="#64748b" font-size="10" font-weight="bold">0V</text>

    <!-- Clean Waveform -->
    <path d="M 40 50 L 185 50 L 185 110 L 535 110 L 535 50 L 730 50" fill="none" stroke="#16a34a" stroke-width="3"/>
    
    <!-- Interrupt trigger mark -->
    <circle cx="185" cy="110" r="5" fill="#ea580c"/>
    <line x1="185" y1="20" x2="185" y2="110" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4"/>
    <text x="195" y="30" fill="#ea580c" font-size="11" font-weight="bold">Chỉ kích hoạt ngắt đúng 1 lần!</text>
  </g>
</svg>
"""
save_svg("bai03_bouncing_debounce.svg", svg_bounce)

# ==============================================================================
# 6. Bai 04: PWM Duty Cycle (LIGHT THEME)
# ==============================================================================
svg_pwm = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 370" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="800" height="350" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="410" y="38" text-anchor="middle" fill="#0f172a" font-size="18" font-weight="800">ĐIỀU CHẾ ĐỘ RỘNG XUNG PWM (DUTY CYCLE VÀ ĐIỆN ÁP TRUNG BÌNH)</text>

  <!-- 25% Duty Cycle -->
  <g transform="translate(60, 60)">
    <text x="0" y="15" fill="#0f172a" font-size="12" font-weight="bold">25% Duty Cycle (Điện áp TB = 0.82V -> LED sáng mờ):</text>
    <path d="M 0 55 L 40 55 L 40 25 L 75 25 L 75 55 L 180 55 L 180 25 L 215 25 L 215 55 L 320 55 L 320 25 L 355 25 L 355 55 L 460 55" fill="none" stroke="#ef4444" stroke-width="2.5"/>
    <line x1="0" y1="47" x2="460" y2="47" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4"/>
    <text x="480" y="50" fill="#ea580c" font-size="11" font-weight="bold">V_avg ~ 0.82V</text>
  </g>

  <!-- 50% Duty Cycle -->
  <g transform="translate(60, 150)">
    <text x="0" y="15" fill="#0f172a" font-size="12" font-weight="bold">50% Duty Cycle (Điện áp TB = 1.65V -> LED sáng vừa):</text>
    <path d="M 0 55 L 40 55 L 40 25 L 110 25 L 110 55 L 180 55 L 180 25 L 250 25 L 250 55 L 320 55 L 320 25 L 390 25 L 390 55 L 460 55" fill="none" stroke="#2563eb" stroke-width="2.5"/>
    <line x1="0" y1="40" x2="460" y2="40" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4"/>
    <text x="480" y="44" fill="#ea580c" font-size="11" font-weight="bold">V_avg ~ 1.65V</text>
  </g>

  <!-- 75% Duty Cycle -->
  <g transform="translate(60, 240)">
    <text x="0" y="15" fill="#0f172a" font-size="12" font-weight="bold">75% Duty Cycle (Điện áp TB = 2.47V -> LED sáng mạnh):</text>
    <path d="M 0 55 L 40 55 L 40 25 L 145 25 L 145 55 L 180 55 L 180 25 L 285 25 L 285 55 L 320 55 L 320 25 L 425 25 L 425 55 L 460 55" fill="none" stroke="#16a34a" stroke-width="2.5"/>
    <line x1="0" y1="32" x2="460" y2="32" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4"/>
    <text x="480" y="36" fill="#ea580c" font-size="11" font-weight="bold">V_avg ~ 2.47V</text>
  </g>

  <text x="410" y="340" text-anchor="middle" fill="#475569" font-size="11" font-weight="600">Công thức: Điện áp trung bình = 3.3V * (Duty Cycle / 100%)</text>
</svg>
"""
save_svg("bai04_pwm_duty_cycle.svg", svg_pwm)

# ==============================================================================
# 7. Bai 04: Servo Waveform (LIGHT THEME)
# ==============================================================================
svg_servo = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 350" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="820" height="330" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="420" y="38" text-anchor="middle" fill="#0f172a" font-size="18" font-weight="800">ĐIỀU KHIỂN GÓC QUAY ĐỘNG CƠ SERVO SG90 BẰNG ĐỘ RỘNG XUNG (50Hz)</text>

  <!-- 0 Degrees -->
  <g transform="translate(60, 60)">
    <text x="0" y="20" fill="#dc2626" font-size="13" font-weight="bold">Góc 0°: Xung High 0.5ms (500us)</text>
    <path d="M 0 50 L 30 50 L 30 25 L 50 25 L 50 50 L 450 50 L 450 25 L 470 25 L 470 50 L 520 50" fill="none" stroke="#dc2626" stroke-width="2.5"/>
    <rect x="30" y="25" width="20" height="25" fill="#fee2e2"/>
    <text x="40" y="18" text-anchor="middle" fill="#dc2626" font-size="10" font-weight="bold">0.5ms</text>
    <text x="540" y="45" fill="#334155" font-size="11" font-weight="600">Quay hết về bên TRÁI</text>
  </g>

  <!-- 90 Degrees -->
  <g transform="translate(60, 145)">
    <text x="0" y="20" fill="#d97706" font-size="13" font-weight="bold">Góc 90°: Xung High 1.5ms (1500us)</text>
    <path d="M 0 50 L 30 50 L 30 25 L 90 25 L 90 50 L 450 50 L 450 25 L 510 25 L 510 50 L 520 50" fill="none" stroke="#d97706" stroke-width="2.5"/>
    <rect x="30" y="25" width="60" height="25" fill="#fef3c7"/>
    <text x="60" y="18" text-anchor="middle" fill="#d97706" font-size="10" font-weight="bold">1.5ms</text>
    <text x="540" y="45" fill="#334155" font-size="11" font-weight="600">Vị trí CHÍNH GIỮA</text>
  </g>

  <!-- 180 Degrees -->
  <g transform="translate(60, 230)">
    <text x="0" y="20" fill="#16a34a" font-size="13" font-weight="bold">Góc 180°: Xung High 2.5ms (2500us)</text>
    <path d="M 0 50 L 30 50 L 30 25 L 130 25 L 130 50 L 450 50 L 450 25 L 550 25 L 550 50 L 520 50" fill="none" stroke="#16a34a" stroke-width="2.5"/>
    <rect x="30" y="25" width="100" height="25" fill="#dcfce7"/>
    <text x="80" y="18" text-anchor="middle" fill="#16a34a" font-size="10" font-weight="bold">2.5ms</text>
    <text x="540" y="45" fill="#334155" font-size="11" font-weight="600">Quay hết về bên PHẢI</text>
  </g>

  <text x="420" y="325" text-anchor="middle" fill="#475569" font-size="11" font-weight="600">Chu kỳ lặp lại T = 20ms (Tần số chuẩn 50Hz của Servo)</text>
</svg>
"""
save_svg("bai04_servo_waveform.svg", svg_servo)

# ==============================================================================
# 8. Bai 05: ADC Sampling (LIGHT THEME)
# ==============================================================================
svg_adc = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 330" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="820" height="310" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="420" y="38" text-anchor="middle" fill="#0f172a" font-size="18" font-weight="800">CHUYỂN ĐỔI TƯƠNG TỰ - SỐ (ADC 12-BIT TRÊN ESP32)</text>

  <!-- Continuous Analog Signal -->
  <g transform="translate(50, 60)">
    <rect x="0" y="0" width="220" height="200" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
    <text x="110" y="30" text-anchor="middle" fill="#ea580c" font-size="13" font-weight="bold">ĐIỆN ÁP VÀO (ANALOG)</text>
    <text x="110" y="50" text-anchor="middle" fill="#64748b" font-size="11">Từ 0V đến 3.3V</text>

    <path d="M 20 160 Q 60 40 110 100 T 200 60" fill="none" stroke="#ea580c" stroke-width="3"/>
    <text x="110" y="180" text-anchor="middle" fill="#334155" font-size="11" font-weight="600">Tín hiệu biến thiên liên tục</text>
  </g>

  <!-- ADC Block -->
  <g transform="translate(310, 90)">
    <rect x="0" y="0" width="200" height="140" rx="10" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
    <text x="100" y="35" text-anchor="middle" fill="#2563eb" font-size="16" font-weight="bold">SAR ADC 12-BIT</text>
    <text x="100" y="60" text-anchor="middle" fill="#0f172a" font-size="11" font-weight="bold">2^12 = 4096 Mức lượng tử</text>
    <text x="100" y="85" text-anchor="middle" fill="#d97706" font-size="11" font-weight="bold">Khối ADC1 (An Toàn)</text>
    <text x="100" y="110" text-anchor="middle" fill="#16a34a" font-size="10" font-weight="bold">analogRead(pin)</text>
  </g>

  <!-- Converted Digital Output -->
  <g transform="translate(550, 60)">
    <rect x="0" y="0" width="230" height="200" rx="10" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
    <text x="115" y="30" text-anchor="middle" fill="#16a34a" font-size="13" font-weight="bold">GIÁ TRỊ SỐ (DIGITAL)</text>
    <text x="115" y="50" text-anchor="middle" fill="#64748b" font-size="11">Số nguyên từ 0 đến 4095</text>

    <!-- Discrete levels -->
    <line x1="30" y1="160" x2="60" y2="160" stroke="#16a34a" stroke-width="2.5"/>
    <line x1="60" y1="160" x2="60" y2="120" stroke="#16a34a" stroke-width="2.5"/>
    <line x1="60" y1="120" x2="110" y2="120" stroke="#16a34a" stroke-width="2.5"/>
    <line x1="110" y1="120" x2="110" y2="80" stroke="#16a34a" stroke-width="2.5"/>
    <line x1="110" y1="80" x2="160" y2="80" stroke="#16a34a" stroke-width="2.5"/>
    <line x1="160" y1="80" x2="160" y2="50" stroke="#16a34a" stroke-width="2.5"/>
    <line x1="160" y1="50" x2="200" y2="50" stroke="#16a34a" stroke-width="2.5"/>

    <text x="115" y="180" text-anchor="middle" fill="#334155" font-size="11" font-weight="600">Dữ liệu số rời rạc cho CPU</text>
  </g>

  <text x="420" y="295" text-anchor="middle" fill="#475569" font-size="12" font-weight="600">Công thức: Điện áp = (Giá trị ADC / 4095) * 3.3V</text>
</svg>
"""
save_svg("bai05_adc_sampling.svg", svg_adc)

# ==============================================================================
# 9. Bai 06: UART Frame (LIGHT THEME)
# ==============================================================================
svg_uart = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 330" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="840" height="310" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="430" y="42" text-anchor="middle" fill="#0f172a" font-size="20" font-weight="800">CẤU TRÚC GÓI DỮ LIỆU NỐI TIẾP UART (FRAME FORMAT)</text>
  
  <g transform="translate(50, 75)">
    <!-- Idle High Line -->
    <line x1="0" y1="50" x2="50" y2="50" stroke="#475569" stroke-width="3"/>
    <text x="25" y="38" text-anchor="middle" fill="#475569" font-size="11" font-weight="bold">IDLE (1)</text>

    <!-- Start Bit (0) -->
    <rect x="50" y="50" width="60" height="70" fill="#fee2e2" stroke="#dc2626" stroke-width="2" rx="2"/>
    <text x="80" y="90" text-anchor="middle" fill="#dc2626" font-size="12" font-weight="bold">START</text>
    <text x="80" y="105" text-anchor="middle" fill="#dc2626" font-size="10">(Bit 0)</text>

    <!-- 8 Data Bits -->
    <g fill="#dcfce7" stroke="#16a34a" stroke-width="1.5">
      <rect x="110" y="50" width="55" height="70" rx="2"/>
      <rect x="165" y="50" width="55" height="70" rx="2"/>
      <rect x="220" y="50" width="55" height="70" rx="2"/>
      <rect x="275" y="50" width="55" height="70" rx="2"/>
      <rect x="330" y="50" width="55" height="70" rx="2"/>
      <rect x="385" y="50" width="55" height="70" rx="2"/>
      <rect x="440" y="50" width="55" height="70" rx="2"/>
      <rect x="495" y="50" width="55" height="70" rx="2"/>
    </g>
    <g fill="#15803d" font-size="12" font-weight="bold" text-anchor="middle">
      <text x="137" y="85">D0</text>
      <text x="137" y="105" font-size="9">(LSB)</text>
      <text x="192" y="90">D1</text>
      <text x="247" y="90">D2</text>
      <text x="302" y="90">D3</text>
      <text x="357" y="90">D4</text>
      <text x="412" y="90">D5</text>
      <text x="467" y="90">D6</text>
      <text x="522" y="85">D7</text>
      <text x="522" y="105" font-size="9">(MSB)</text>
    </g>

    <!-- Parity Bit -->
    <rect x="550" y="50" width="65" height="70" fill="#fef3c7" stroke="#d97706" stroke-width="1.5" rx="2"/>
    <text x="582" y="85" text-anchor="middle" fill="#b45309" font-size="11" font-weight="bold">PARITY</text>
    <text x="582" y="105" text-anchor="middle" fill="#b45309" font-size="9">(Tùy chọn)</text>

    <!-- Stop Bit (1) -->
    <rect x="615" y="50" width="65" height="70" fill="#dbeafe" stroke="#2563eb" stroke-width="2" rx="2"/>
    <text x="647" y="85" text-anchor="middle" fill="#1d4ed8" font-size="12" font-weight="bold">STOP</text>
    <text x="647" y="105" text-anchor="middle" fill="#1d4ed8" font-size="10">(Bit 1)</text>

    <!-- Return to Idle -->
    <line x1="680" y1="50" x2="740" y2="50" stroke="#475569" stroke-width="3"/>
    <text x="710" y="38" text-anchor="middle" fill="#475569" font-size="11" font-weight="bold">IDLE (1)</text>

    <!-- Bracket for Data Bits -->
    <path d="M 110 135 L 110 145 L 325 145 L 325 155 L 335 155 L 335 145 L 550 145 L 550 135" fill="none" stroke="#16a34a" stroke-width="2"/>
    <text x="330" y="175" text-anchor="middle" fill="#15803d" font-size="12" font-weight="bold">8 BITS DỮ LIỆU (1 BYTE - KÝ TỰ MÃ ASCII)</text>
  </g>

  <text x="430" y="285" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Cấu hình tiêu chuẩn: 115200 Baudrate - 8 Data Bits - No Parity - 1 Stop Bit (115200 8-N-1)</text>
</svg>
"""
save_svg("bai06_uart_frame.svg", svg_uart)

# ==============================================================================
# 10. Bai 07: I2C Bus Topology (LIGHT THEME)
# ==============================================================================
svg_i2c = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 370" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="840" height="350" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="430" y="42" text-anchor="middle" fill="#0f172a" font-size="20" font-weight="800">KIẾN TRÚC ĐƯỜNG BUS GIAO TIẾP I2C (2 DÂY ĐỒNG BỘ)</text>

  <!-- Master (ESP32) -->
  <rect x="50" y="100" width="150" height="180" rx="10" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
  <text x="125" y="130" text-anchor="middle" fill="#2563eb" font-size="15" font-weight="bold">ESP32 (MASTER)</text>
  <text x="125" y="150" text-anchor="middle" fill="#64748b" font-size="11">Khởi tạo xung Clock</text>
  
  <text x="180" y="195" fill="#d97706" font-size="12" font-weight="bold">SCL (22)</text>
  <text x="180" y="245" fill="#0284c7" font-size="12" font-weight="bold">SDA (21)</text>

  <!-- SCL Bus -->
  <line x1="200" y1="190" x2="790" y2="190" stroke="#d97706" stroke-width="3"/>
  <text x="240" y="180" fill="#d97706" font-size="11" font-weight="bold">Đường SCL (Serial Clock)</text>

  <!-- SDA Bus -->
  <line x1="200" y1="240" x2="790" y2="240" stroke="#0284c7" stroke-width="3"/>
  <text x="240" y="260" fill="#0284c7" font-size="11" font-weight="bold">Đường SDA (Serial Data 2 chiều)</text>

  <!-- Pull-up resistors -->
  <rect x="280" y="80" width="15" height="35" fill="#fed7aa" stroke="#ea580c" stroke-width="1.5" rx="2"/>
  <line x1="287" y1="65" x2="287" y2="80" stroke="#dc2626" stroke-width="2"/>
  <line x1="287" y1="115" x2="287" y2="190" stroke="#d97706" stroke-width="2"/>
  <circle cx="287" cy="190" r="3" fill="#d97706"/>

  <rect x="330" y="80" width="15" height="35" fill="#fed7aa" stroke="#ea580c" stroke-width="1.5" rx="2"/>
  <line x1="337" y1="65" x2="337" y2="80" stroke="#dc2626" stroke-width="2"/>
  <line x1="337" y1="115" x2="337" y2="240" stroke="#0284c7" stroke-width="2"/>
  <circle cx="337" cy="240" r="3" fill="#0284c7"/>

  <line x1="260" y1="65" x2="360" y2="65" stroke="#dc2626" stroke-width="2"/>
  <text x="310" y="55" text-anchor="middle" fill="#dc2626" font-size="11" font-weight="bold">Trở kéo Pull-up 4.7kΩ lên 3.3V</text>

  <!-- Slave 1: LCD 1602 -->
  <rect x="430" y="110" width="160" height="170" rx="10" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
  <text x="510" y="140" text-anchor="middle" fill="#16a34a" font-size="14" font-weight="bold">LCD 1602 I2C</text>
  <text x="510" y="160" text-anchor="middle" fill="#ea580c" font-size="12" font-weight="bold">Địa chỉ: 0x27</text>
  <line x1="460" y1="190" x2="460" y2="200" stroke="#d97706" stroke-width="2"/>
  <circle cx="460" cy="190" r="3" fill="#d97706"/>
  <line x1="490" y1="240" x2="490" y2="200" stroke="#0284c7" stroke-width="2"/>
  <circle cx="490" cy="240" r="3" fill="#0284c7"/>

  <!-- Slave 2: OLED SSD1306 -->
  <rect x="640" y="110" width="160" height="170" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2"/>
  <text x="720" y="140" text-anchor="middle" fill="#7c3aed" font-size="14" font-weight="bold">OLED SSD1306</text>
  <text x="720" y="160" text-anchor="middle" fill="#ea580c" font-size="12" font-weight="bold">Địa chỉ: 0x3C</text>
  <line x1="670" y1="190" x2="670" y2="200" stroke="#d97706" stroke-width="2"/>
  <circle cx="670" cy="190" r="3" fill="#d97706"/>
  <line x1="700" y1="240" x2="700" y2="200" stroke="#0284c7" stroke-width="2"/>
  <circle cx="700" cy="240" r="3" fill="#0284c7"/>

  <text x="430" y="325" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Các thiết bị mắc song song trên cùng 2 dây tín hiệu và phân biệt nhau bằng Địa chỉ vật lý 7-bit</text>
</svg>
"""
save_svg("bai07_i2c_bus_topology.svg", svg_i2c)

# ==============================================================================
# 11. Bai 08: Ultrasonic Sensor Timing (LIGHT THEME)
# ==============================================================================
svg_ultrasonic = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 330" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="820" height="310" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="420" y="38" text-anchor="middle" fill="#0f172a" font-size="18" font-weight="800">GIẢN ĐỒ THỜI GIAN ĐO KHOẢNG CÁCH CẢM BIẾN SIÊU ÂM HC-SR04</text>

  <!-- Trigger Pulse -->
  <g transform="translate(60, 60)">
    <text x="0" y="20" fill="#ea580c" font-size="12" font-weight="bold">1. Chân TRIG (Phát xung kích từ ESP32):</text>
    <path d="M 0 50 L 40 50 L 40 25 L 70 25 L 70 50 L 520 50" fill="none" stroke="#ea580c" stroke-width="2.5"/>
    <rect x="40" y="25" width="30" height="25" fill="#ffedd5"/>
    <text x="55" y="18" text-anchor="middle" fill="#ea580c" font-size="10" font-weight="bold">Xung 10us</text>
  </g>

  <!-- Ultrasonic Burst 40kHz -->
  <g transform="translate(60, 135)">
    <text x="0" y="20" fill="#2563eb" font-size="12" font-weight="bold">2. Cảm biến tự động phát ra 8 chu kỳ sóng siêu âm 40 kHz:</text>
    <path d="M 0 50 L 80 50 L 85 30 L 90 70 L 95 30 L 100 70 L 105 30 L 110 70 L 115 30 L 120 70 L 125 50 L 520 50" fill="none" stroke="#2563eb" stroke-width="2.5"/>
    <text x="145" y="45" fill="#2563eb" font-size="11" font-weight="bold">8 xung 40kHz truyền trong không khí</text>
  </g>

  <!-- Echo Pulse -->
  <g transform="translate(60, 210)">
    <text x="0" y="20" fill="#16a34a" font-size="12" font-weight="bold">3. Chân ECHO (ESP32 đo thời gian xung phản hồi mức High):</text>
    <path d="M 0 50 L 125 50 L 125 25 L 390 25 L 390 50 L 520 50" fill="none" stroke="#16a34a" stroke-width="2.5"/>
    <rect x="125" y="25" width="265" height="25" fill="#dcfce7"/>
    <text x="257" y="18" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="bold">Thời gian Echo (t)</text>
  </g>

  <text x="420" y="305" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Công thức tính khoảng cách: d (cm) = [Thời gian Echo (us) * 0.034] / 2 = Thời gian / 58</text>
</svg>
"""
save_svg("bai08_ultrasonic_timing.svg", svg_ultrasonic)

# ==============================================================================
# 12. Bai 09: FreeRTOS Dual Core (LIGHT THEME)
# ==============================================================================
svg_freertos = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 390" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="840" height="370" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="430" y="42" text-anchor="middle" fill="#0f172a" font-size="20" font-weight="800">KIẾN TRÚC ĐA TÁC VỤ FREERTOS TRÊN 2 NHÂN (DUAL-CORE) ESP32</text>

  <!-- Core 0 -->
  <g transform="translate(60, 70)">
    <rect x="0" y="0" width="345" height="265" rx="12" fill="#ffffff" stroke="#ef4444" stroke-width="2"/>
    <text x="172" y="30" text-anchor="middle" fill="#dc2626" font-size="16" font-weight="bold">CPU CORE 0 (PRO_CPU)</text>
    <text x="172" y="50" text-anchor="middle" fill="#64748b" font-size="11">Xử lý giao thức nền &amp; Mạng không dây</text>

    <!-- Task A -->
    <rect x="25" y="70" width="295" height="50" rx="8" fill="#f5f3ff" stroke="#7c3aed"/>
    <text x="40" y="92" fill="#7c3aed" font-size="12" font-weight="bold">Wi-Fi &amp; TCP/IP Stack Task</text>
    <text x="40" y="110" fill="#475569" font-size="10">Duy trì kết nối mạng ngầm của Espressif</text>

    <!-- Task B -->
    <rect x="25" y="130" width="295" height="50" rx="8" fill="#eff6ff" stroke="#2563eb"/>
    <text x="40" y="152" fill="#1d4ed8" font-size="12" font-weight="bold">Task_Network (User Created)</text>
    <text x="40" y="170" fill="#475569" font-size="10">Truyền nhận gói tin MQTT / HTTP Client</text>

    <text x="172" y="230" text-anchor="middle" fill="#16a34a" font-size="12" font-weight="bold">Hoạt động độc lập không gây nghẽn Core 1</text>
  </g>

  <!-- Core 1 -->
  <g transform="translate(455, 70)">
    <rect x="0" y="0" width="345" height="265" rx="12" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
    <text x="172" y="30" text-anchor="middle" fill="#16a34a" font-size="16" font-weight="bold">CPU CORE 1 (APP_CPU)</text>
    <text x="172" y="50" text-anchor="middle" fill="#64748b" font-size="11">Nơi chạy các tác vụ ứng dụng người dùng</text>

    <!-- Task C -->
    <rect x="25" y="70" width="295" height="50" rx="8" fill="#fff7ed" stroke="#ea580c"/>
    <text x="40" y="92" fill="#ea580c" font-size="12" font-weight="bold">Task_SensorRead (Mỗi 1s)</text>
    <text x="40" y="110" fill="#475569" font-size="10">Đọc cảm biến DHT22, siêu âm, ADC</text>

    <!-- Task D -->
    <rect x="25" y="130" width="295" height="50" rx="8" fill="#fefce8" stroke="#ca8a04"/>
    <text x="40" y="152" fill="#a16207" font-size="12" font-weight="bold">Task_DisplayLCD &amp; Actuators</text>
    <text x="40" y="170" fill="#475569" font-size="10">Cập nhật màn hình I2C &amp; Xoay Servo</text>

    <text x="172" y="230" text-anchor="middle" fill="#d97706" font-size="12" font-weight="bold">Mặc định hàm setup() và loop() chạy tại đây</text>
  </g>

  <text x="430" y="360" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Bộ lập lịch FreeRTOS tự động điều phối thời gian thực với độ trễ thấp</text>
</svg>
"""
save_svg("bai09_freertos_dualcore.svg", svg_freertos)

# ==============================================================================
# 13. Bai 10: Queue & Mutex Model (LIGHT THEME)
# ==============================================================================
svg_queue = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 350" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="840" height="330" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="430" y="42" text-anchor="middle" fill="#0f172a" font-size="20" font-weight="800">MÔ HÌNH HÀNG ĐỢI (QUEUE) VÀ KHÓA MUTEX TRONG FREERTOS</text>

  <!-- Producer Task -->
  <rect x="40" y="90" width="180" height="130" rx="10" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
  <text x="130" y="125" text-anchor="middle" fill="#16a34a" font-size="14" font-weight="bold">TASK PRODUCER</text>
  <text x="130" y="145" text-anchor="middle" fill="#334155" font-size="11">(Đo cảm biến)</text>
  <text x="130" y="175" text-anchor="middle" fill="#ea580c" font-size="12" font-weight="bold">xQueueSend()</text>

  <!-- Arrow to Queue -->
  <line x1="220" y1="150" x2="290" y2="150" stroke="#ea580c" stroke-width="3"/>
  <polygon points="295,150 285,145 285,155" fill="#ea580c"/>

  <!-- Queue FIFO -->
  <g transform="translate(300, 110)">
    <rect x="0" y="0" width="270" height="80" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
    <text x="135" y="25" text-anchor="middle" fill="#2563eb" font-size="13" font-weight="bold">FREERTOS QUEUE (HÀNG ĐỢI FIFO)</text>
    
    <!-- Slots -->
    <rect x="20" y="35" width="60" height="35" fill="#f1f5f9" stroke="#cbd5e1" rx="4"/>
    <text x="50" y="57" text-anchor="middle" fill="#15803d" font-size="11" font-weight="bold">Gói #3</text>
    <rect x="100" y="35" width="60" height="35" fill="#f1f5f9" stroke="#cbd5e1" rx="4"/>
    <text x="130" y="57" text-anchor="middle" fill="#15803d" font-size="11" font-weight="bold">Gói #2</text>
    <rect x="180" y="35" width="60" height="35" fill="#f1f5f9" stroke="#cbd5e1" rx="4"/>
    <text x="210" y="57" text-anchor="middle" fill="#15803d" font-size="11" font-weight="bold">Gói #1 (Đầu)</text>
  </g>

  <!-- Arrow from Queue -->
  <line x1="570" y1="150" x2="640" y2="150" stroke="#16a34a" stroke-width="3"/>
  <polygon points="645,150 635,145 635,155" fill="#16a34a"/>

  <!-- Consumer Task -->
  <rect x="650" y="90" width="170" height="130" rx="10" fill="#ffffff" stroke="#ca8a04" stroke-width="2"/>
  <text x="735" y="125" text-anchor="middle" fill="#a16207" font-size="14" font-weight="bold">TASK CONSUMER</text>
  <text x="735" y="145" text-anchor="middle" fill="#334155" font-size="11">(Hiển thị ra LCD)</text>
  <text x="735" y="175" text-anchor="middle" fill="#16a34a" font-size="12" font-weight="bold">xQueueReceive()</text>

  <!-- Mutex Lock Area -->
  <rect x="250" y="245" width="370" height="70" rx="10" fill="#ffffff" stroke="#ef4444" stroke-width="1.5"/>
  <text x="435" y="270" text-anchor="middle" fill="#dc2626" font-size="13" font-weight="bold">MUTEX (Ổ KHÓA BẢO VỆ TÀI NGUYÊN DÙNG CHUNG)</text>
  <text x="435" y="292" text-anchor="middle" fill="#475569" font-size="11" font-weight="600">Bảo vệ cổng Serial / Bus I2C không bị in chồng chéo dữ liệu giữa các Task</text>
</svg>
"""
save_svg("bai10_queue_mutex_model.svg", svg_queue)

# ==============================================================================
# 14. Bai 11: Flash Memory Map (LIGHT THEME)
# ==============================================================================
svg_flash = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 310" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="820" height="290" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="420" y="40" text-anchor="middle" fill="#0f172a" font-size="18" font-weight="800">BẢN ĐỒ PHÂN VÙNG BỘ NHỚ FLASH TRÊN ESP32 (4MB FLASH MAP)</text>

  <!-- 4MB Flash Block -->
  <g transform="translate(50, 70)">
    <rect x="0" y="0" width="730" height="120" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>

    <!-- Bootloader -->
    <rect x="10" y="15" width="85" height="90" rx="6" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
    <text x="52" y="60" text-anchor="middle" fill="#b91c1c" font-size="12" font-weight="bold">Bootloader</text>
    <text x="52" y="80" text-anchor="middle" fill="#b91c1c" font-size="10">0x1000</text>

    <!-- Partition Table -->
    <rect x="105" y="15" width="80" height="90" rx="6" fill="#ffedd5" stroke="#f97316" stroke-width="1.5"/>
    <text x="145" y="55" text-anchor="middle" fill="#c2410c" font-size="11" font-weight="bold">Partition</text>
    <text x="145" y="70" text-anchor="middle" fill="#c2410c" font-size="11" font-weight="bold">Table</text>
    <text x="145" y="88" text-anchor="middle" fill="#c2410c" font-size="9">0x8000</text>

    <!-- NVS (Preferences) -->
    <rect x="195" y="15" width="95" height="90" rx="6" fill="#fef3c7" stroke="#eab308" stroke-width="1.5"/>
    <text x="242" y="55" text-anchor="middle" fill="#a16207" font-size="12" font-weight="bold">NVS (Flash)</text>
    <text x="242" y="72" text-anchor="middle" fill="#a16207" font-size="10">Preferences</text>
    <text x="242" y="88" text-anchor="middle" fill="#a16207" font-size="10">20KB</text>

    <!-- App 0 (Firmware) -->
    <rect x="300" y="15" width="230" height="90" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
    <text x="415" y="55" text-anchor="middle" fill="#15803d" font-size="13" font-weight="bold">ỨNG DỤNG CHÍNH (app0)</text>
    <text x="415" y="75" text-anchor="middle" fill="#15803d" font-size="10">Code Arduino / FreeRTOS (~1.3MB)</text>

    <!-- LittleFS File System -->
    <rect x="540" y="15" width="180" height="90" rx="6" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
    <text x="630" y="55" text-anchor="middle" fill="#1d4ed8" font-size="13" font-weight="bold">LittleFS (Tệp Tin)</text>
    <text x="630" y="75" text-anchor="middle" fill="#1d4ed8" font-size="10">Chứa HTML, CSS, JSON (~1.5MB)</text>
  </g>

  <text x="420" y="240" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Dữ liệu ghi vào vùng NVS (Preferences) hoặc LittleFS được lưu trữ vĩnh viễn kể cả khi mất điện</text>
</svg>
"""
save_svg("bai11_flash_memory_map.svg", svg_flash)

# ==============================================================================
# 15. Bai 12: Wi-Fi Modes (LIGHT THEME)
# ==============================================================================
svg_wifi_modes = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 330" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="820" height="310" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="420" y="38" text-anchor="middle" fill="#0f172a" font-size="18" font-weight="800">SO SÁNH 2 CHẾ ĐỘ WI-FI TRÊN ESP32: STATION VÀ ACCESS POINT</text>

  <!-- Left: Station Mode -->
  <g transform="translate(55, 60)">
    <rect x="0" y="0" width="340" height="230" rx="12" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
    <text x="170" y="30" text-anchor="middle" fill="#16a34a" font-size="14" font-weight="bold">1. CHẾ ĐỘ STATION (WIFI_STA)</text>
    <text x="170" y="50" text-anchor="middle" fill="#64748b" font-size="11">ESP32 kết nối vào Router Wi-Fi có sẵn</text>

    <!-- Router -->
    <rect x="25" y="80" width="105" height="75" rx="8" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="77" y="112" text-anchor="middle" fill="#ea580c" font-size="12" font-weight="bold">ROUTER</text>
    <text x="77" y="128" text-anchor="middle" fill="#64748b" font-size="10">Gia đình / Cty</text>

    <!-- Waves -->
    <path d="M 140 115 Q 170 95 200 115" fill="none" stroke="#16a34a" stroke-width="2.5"/>
    <text x="170" y="90" text-anchor="middle" fill="#16a34a" font-size="10" font-weight="bold">Sóng Wi-Fi</text>

    <!-- ESP32 -->
    <rect x="210" y="80" width="105" height="75" rx="8" fill="#1e293b"/>
    <text x="262" y="112" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="bold">ESP32</text>
    <text x="262" y="128" text-anchor="middle" fill="#94a3b8" font-size="10">Client nhận IP</text>

    <text x="170" y="190" text-anchor="middle" fill="#334155" font-size="11" font-weight="600">Mục đích: Ra Internet gửi MQTT / HTTP</text>
  </g>

  <!-- Right: SoftAP Mode -->
  <g transform="translate(445, 60)">
    <rect x="0" y="0" width="340" height="230" rx="12" fill="#ffffff" stroke="#d97706" stroke-width="2"/>
    <text x="170" y="30" text-anchor="middle" fill="#d97706" font-size="14" font-weight="bold">2. CHẾ ĐỘ SOFTAP (WIFI_AP)</text>
    <text x="170" y="50" text-anchor="middle" fill="#64748b" font-size="11">ESP32 tự phát sóng Wi-Fi cho điện thoại kết nối</text>

    <!-- ESP32 AP -->
    <rect x="25" y="80" width="105" height="75" rx="8" fill="#1e293b"/>
    <text x="77" y="112" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="bold">ESP32</text>
    <text x="77" y="128" text-anchor="middle" fill="#f59e0b" font-size="10" font-weight="bold">Phát Wi-Fi</text>

    <!-- Waves -->
    <path d="M 140 115 Q 170 95 200 115" fill="none" stroke="#d97706" stroke-width="2.5"/>
    <text x="170" y="90" text-anchor="middle" fill="#d97706" font-size="10" font-weight="bold">Tự phát SSID</text>

    <!-- Smartphone -->
    <rect x="210" y="80" width="105" height="75" rx="8" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="262" y="112" text-anchor="middle" fill="#7c3aed" font-size="12" font-weight="bold">ĐIỆN THOẠI</text>
    <text x="262" y="128" text-anchor="middle" fill="#64748b" font-size="10">Bắt sóng cấu hình</text>

    <text x="170" y="190" text-anchor="middle" fill="#334155" font-size="11" font-weight="600">Mục đích: Cài đặt thiết bị khi chưa có mạng</text>
  </g>
</svg>
"""
save_svg("bai12_wifi_modes.svg", svg_wifi_modes)

# ==============================================================================
# 16. Bai 13: Web Server Architecture (LIGHT THEME)
# ==============================================================================
svg_web = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 350" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="840" height="330" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="430" y="42" text-anchor="middle" fill="#0f172a" font-size="20" font-weight="800">KIẾN TRÚC MÁY CHỦ WEB (WEB SERVER) TRÊN ESP32</text>

  <!-- Client: Smartphone/PC -->
  <rect x="40" y="80" width="200" height="210" rx="12" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
  <text x="140" y="115" text-anchor="middle" fill="#2563eb" font-size="15" font-weight="bold">TRÌNH DUYỆT WEB</text>
  <text x="140" y="135" text-anchor="middle" fill="#64748b" font-size="11">(Chrome trên Điện Thoại / PC)</text>
  
  <rect x="60" y="160" width="160" height="40" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="140" y="185" text-anchor="middle" fill="#15803d" font-size="12" font-weight="bold">http://192.168.1.15</text>
  <text x="140" y="240" text-anchor="middle" fill="#0f172a" font-size="12" font-weight="600">Bấm nút "BẬT ĐÈN"</text>

  <!-- Requests & Responses -->
  <g transform="translate(250, 115)">
    <line x1="0" y1="30" x2="165" y2="30" stroke="#ea580c" stroke-width="3"/>
    <polygon points="170,30 160,25 160,35" fill="#ea580c"/>
    <text x="85" y="20" text-anchor="middle" fill="#ea580c" font-size="11" font-weight="bold">HTTP GET /led/on</text>

    <line x1="170" y1="90" x2="5" y2="90" stroke="#16a34a" stroke-width="3"/>
    <polygon points="0,90 10,85 10,95" fill="#16a34a"/>
    <text x="85" y="115" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="bold">HTTP 200 OK (HTML/CSS)</text>
  </g>

  <!-- Server: ESP32 -->
  <rect x="435" y="80" width="380" height="210" rx="12" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
  <text x="625" y="115" text-anchor="middle" fill="#16a34a" font-size="15" font-weight="bold">ESP32 WEB SERVER (PORT 80)</text>
  <text x="625" y="135" text-anchor="middle" fill="#64748b" font-size="11">Thư viện WebServer.h</text>

  <rect x="460" y="150" width="160" height="50" rx="6" fill="#fff7ed" stroke="#ea580c"/>
  <text x="540" y="172" text-anchor="middle" fill="#ea580c" font-size="11" font-weight="bold">server.on("/led/on")</text>
  <text x="540" y="188" text-anchor="middle" fill="#15803d" font-size="10" font-weight="bold">digitalWrite(2, HIGH)</text>

  <rect x="635" y="150" width="160" height="50" rx="6" fill="#eff6ff" stroke="#2563eb"/>
  <text x="715" y="172" text-anchor="middle" fill="#1d4ed8" font-size="11" font-weight="bold">Trang HTML / CSS</text>
  <text x="715" y="188" text-anchor="middle" fill="#334155" font-size="10">Giao diện điều khiển</text>

  <text x="625" y="255" text-anchor="middle" fill="#dc2626" font-size="12" font-weight="bold">-> Chân GPIO 2 xuất điện áp làm đèn LED SÁNG</text>
</svg>
"""
save_svg("bai13_webserver_flow.svg", svg_web)

# ==============================================================================
# 17. Bai 14: HTTP Client ThingSpeak (LIGHT THEME)
# ==============================================================================
svg_thingspeak = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 310" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="820" height="290" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="420" y="38" text-anchor="middle" fill="#0f172a" font-size="18" font-weight="800">LUỒNG DỮ LIỆU ĐẨY THÔNG SỐ CẢM BIẾN LÊN THINGSPEAK CLOUD</text>

  <!-- ESP32 Client -->
  <rect x="50" y="80" width="190" height="160" rx="12" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
  <text x="145" y="115" text-anchor="middle" fill="#16a34a" font-size="15" font-weight="bold">ESP32 CLIENT</text>
  <text x="145" y="135" text-anchor="middle" fill="#334155" font-size="11">Đo nhiệt độ: 28.5°C</text>
  <text x="145" y="155" text-anchor="middle" fill="#334155" font-size="11">Đo độ ẩm: 65%</text>
  <rect x="70" y="175" width="150" height="35" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="145" y="197" text-anchor="middle" fill="#ea580c" font-size="11" font-weight="bold">HTTPClient.h</text>

  <!-- Arrow HTTP GET -->
  <g transform="translate(250, 115)">
    <line x1="0" y1="30" x2="280" y2="30" stroke="#ea580c" stroke-width="3"/>
    <polygon points="285,30 275,25 275,35" fill="#ea580c"/>
    <text x="140" y="20" text-anchor="middle" fill="#ea580c" font-size="11" font-weight="bold">HTTP GET /update?api_key=XXX&amp;field1=28.5&amp;field2=65</text>
    <text x="140" y="60" text-anchor="middle" fill="#64748b" font-size="10">Gửi qua Internet định kỳ mỗi 20 giây</text>
  </g>

  <!-- ThingSpeak Cloud -->
  <rect x="550" y="80" width="240" height="160" rx="12" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
  <text x="670" y="115" text-anchor="middle" fill="#2563eb" font-size="15" font-weight="bold">THINGSPEAK CLOUD</text>
  <text x="670" y="135" text-anchor="middle" fill="#64748b" font-size="11">(Nền tảng IoT của MathWorks)</text>

  <rect x="575" y="155" width="190" height="55" rx="6" fill="#eff6ff" stroke="#93c5fd"/>
  <text x="670" y="178" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="bold">Vẽ đồ thị trực quan</text>
  <text x="670" y="196" text-anchor="middle" fill="#334155" font-size="10">Lưu trữ database lịch sử</text>

  <text x="420" y="275" text-anchor="middle" fill="#334155" font-size="12" font-weight="600">Người dùng có thể xem biểu đồ trực tiếp từ bất kỳ trình duyệt nào trên thế giới</text>
</svg>
"""
save_svg("bai14_http_thingspeak.svg", svg_thingspeak)

# ==============================================================================
# 18. Bai 15: MQTT Pub/Sub (LIGHT THEME)
# ==============================================================================
svg_mqtt = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 370" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="840" height="350" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="430" y="42" text-anchor="middle" fill="#0f172a" font-size="20" font-weight="800">KIẾN TRÚC GIAO THỨC IOT MQTT (PUBLISH / SUBSCRIBE)</text>

  <!-- ESP32 Device -->
  <rect x="40" y="90" width="200" height="210" rx="12" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
  <text x="140" y="125" text-anchor="middle" fill="#16a34a" font-size="15" font-weight="bold">THIẾT BỊ ESP32</text>
  <text x="140" y="145" text-anchor="middle" fill="#64748b" font-size="11">(Publisher &amp; Subscriber)</text>
  
  <rect x="55" y="165" width="170" height="42" rx="6" fill="#fff7ed" stroke="#ea580c"/>
  <text x="140" y="191" text-anchor="middle" fill="#ea580c" font-size="11" font-weight="bold">Cảm biến DHT22</text>
  
  <rect x="55" y="225" width="170" height="42" rx="6" fill="#eff6ff" stroke="#2563eb"/>
  <text x="140" y="251" text-anchor="middle" fill="#1d4ed8" font-size="11" font-weight="bold">Đèn LED &amp; Cửa Servo</text>

  <!-- Central MQTT Broker -->
  <rect x="330" y="80" width="200" height="230" rx="14" fill="#ffffff" stroke="#ea580c" stroke-width="3"/>
  <text x="430" y="115" text-anchor="middle" fill="#ea580c" font-size="16" font-weight="bold">MQTT BROKER</text>
  <text x="430" y="135" text-anchor="middle" fill="#64748b" font-size="11">(Máy Chủ Trung Gian)</text>
  <text x="430" y="160" text-anchor="middle" fill="#2563eb" font-size="12" font-weight="bold">broker.hivemq.com</text>
  <text x="430" y="180" text-anchor="middle" fill="#2563eb" font-size="12">Cổng: 1883</text>

  <rect x="345" y="210" width="170" height="65" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="430" y="235" text-anchor="middle" fill="#16a34a" font-size="11" font-weight="bold">Điều phối bản tin</text>
  <text x="430" y="255" text-anchor="middle" fill="#0f172a" font-size="10" font-weight="bold">Độ trễ cực thấp &lt; 50ms</text>

  <!-- Client: Mobile App -->
  <rect x="620" y="90" width="200" height="210" rx="12" fill="#ffffff" stroke="#7c3aed" stroke-width="2"/>
  <text x="720" y="125" text-anchor="middle" fill="#7c3aed" font-size="15" font-weight="bold">APP ĐIỆN THOẠI</text>
  <text x="720" y="145" text-anchor="middle" fill="#64748b" font-size="11">(MQTT Dashboard)</text>
  
  <rect x="635" y="165" width="170" height="42" rx="6" fill="#f0fdf4" stroke="#16a34a"/>
  <text x="720" y="191" text-anchor="middle" fill="#15803d" font-size="11" font-weight="bold">Xem đồ thị nhiệt độ</text>

  <rect x="635" y="225" width="170" height="42" rx="6" fill="#fef2f2" stroke="#dc2626"/>
  <text x="720" y="251" text-anchor="middle" fill="#b91c1c" font-size="11" font-weight="bold">Bấm nút Mở cửa / Bật đèn</text>

  <!-- Telemetry Line -->
  <line x1="240" y1="185" x2="330" y2="185" stroke="#ea580c" stroke-width="2.5"/>
  <line x1="530" y1="185" x2="620" y2="185" stroke="#ea580c" stroke-width="2.5"/>
  <text x="285" y="177" fill="#ea580c" font-size="10" font-weight="bold">PUB Temp</text>
  <text x="575" y="177" fill="#ea580c" font-size="10" font-weight="bold">SUB Temp</text>

  <!-- Control Line -->
  <line x1="620" y1="245" x2="530" y2="245" stroke="#dc2626" stroke-width="2.5"/>
  <line x1="330" y1="245" x2="240" y2="245" stroke="#dc2626" stroke-width="2.5"/>
  <text x="565" y="237" fill="#dc2626" font-size="10" font-weight="bold">PUB "OPEN"</text>
  <text x="275" y="237" fill="#dc2626" font-size="10" font-weight="bold">SUB "OPEN"</text>
</svg>
"""
save_svg("bai15_mqtt_pubsub.svg", svg_mqtt)

# ==============================================================================
# 19. Bai 16: Smart Home Architecture (LIGHT THEME)
# ==============================================================================
svg_capstone = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 460" width="100%" height="100%" style="background:#ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="900" height="440" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  <text x="460" y="42" text-anchor="middle" fill="#0f172a" font-size="22" font-weight="800">SƠ ĐỒ KHỐI TỔNG THỂ HỆ THỐNG SMART HOME IOT ĐA NHIỆM</text>

  <!-- Central Microcontroller: ESP32 -->
  <rect x="340" y="80" width="240" height="260" rx="14" fill="#ffffff" stroke="#2563eb" stroke-width="3"/>
  <text x="460" y="115" text-anchor="middle" fill="#1d4ed8" font-size="18" font-weight="bold">ESP32 DUAL-CORE</text>
  <text x="460" y="135" text-anchor="middle" fill="#64748b" font-size="12">Tensilica Xtensa LX6 (240MHz)</text>

  <rect x="360" y="150" width="200" height="40" rx="6" fill="#fee2e2" stroke="#ef4444"/>
  <text x="460" y="175" text-anchor="middle" fill="#b91c1c" font-size="11" font-weight="bold">Core 0: Wi-Fi &amp; MQTT Cloud</text>

  <rect x="360" y="200" width="200" height="40" rx="6" fill="#dcfce7" stroke="#16a34a"/>
  <text x="460" y="225" text-anchor="middle" fill="#15803d" font-size="11" font-weight="bold">Core 1: Sensor, Actuator, LCD</text>

  <rect x="360" y="250" width="200" height="40" rx="6" fill="#f3e8ff" stroke="#9333ea"/>
  <text x="460" y="275" text-anchor="middle" fill="#7e22ce" font-size="11" font-weight="bold">FreeRTOS: Queue &amp; Mutex</text>

  <!-- LEFT: SENSORS (INPUTS) -->
  <!-- DHT22 -->
  <rect x="40" y="80" width="190" height="60" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
  <text x="135" y="105" text-anchor="middle" fill="#16a34a" font-size="13" font-weight="bold">CẢM BIẾN DHT22</text>
  <text x="135" y="125" text-anchor="middle" fill="#334155" font-size="11">Nhiệt độ &amp; Độ ẩm (GPIO 15)</text>
  <line x1="230" y1="110" x2="340" y2="150" stroke="#16a34a" stroke-width="2.5"/>

  <!-- LDR Sensor -->
  <rect x="40" y="160" width="190" height="60" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
  <text x="135" y="185" text-anchor="middle" fill="#ea580c" font-size="13" font-weight="bold">QUANG TRỞ (LDR)</text>
  <text x="135" y="205" text-anchor="middle" fill="#334155" font-size="11">Cường độ sáng (ADC 34)</text>
  <line x1="230" y1="190" x2="340" y2="190" stroke="#ea580c" stroke-width="2.5"/>

  <!-- SOS Button -->
  <rect x="40" y="240" width="190" height="60" rx="8" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
  <text x="135" y="265" text-anchor="middle" fill="#dc2626" font-size="13" font-weight="bold">NÚT BẤM KHẨN CẤP</text>
  <text x="135" y="285" text-anchor="middle" fill="#334155" font-size="11">Ngắt ngoài GPIO 4 (IRAM)</text>
  <line x1="230" y1="270" x2="340" y2="230" stroke="#dc2626" stroke-width="2.5"/>

  <!-- RIGHT: ACTUATORS & DISPLAY (OUTPUTS) -->
  <!-- LCD 1602 -->
  <rect x="690" y="80" width="190" height="60" rx="8" fill="#ffffff" stroke="#d97706" stroke-width="2"/>
  <text x="785" y="105" text-anchor="middle" fill="#d97706" font-size="13" font-weight="bold">MÀN HÌNH LCD 1602</text>
  <text x="785" y="125" text-anchor="middle" fill="#334155" font-size="11">Giao tiếp I2C (SDA 21, SCL 22)</text>
  <line x1="580" y1="150" x2="690" y2="110" stroke="#d97706" stroke-width="2.5"/>

  <!-- Servo Door -->
  <rect x="690" y="160" width="190" height="60" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
  <text x="785" y="185" text-anchor="middle" fill="#2563eb" font-size="13" font-weight="bold">CỬA TỰ ĐỘNG SERVO</text>
  <text x="785" y="205" text-anchor="middle" fill="#334155" font-size="11">PWM 50Hz (GPIO 18)</text>
  <line x1="580" y1="190" x2="690" y2="190" stroke="#2563eb" stroke-width="2.5"/>

  <!-- Smart Light -->
  <rect x="690" y="240" width="190" height="60" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="2"/>
  <text x="785" y="265" text-anchor="middle" fill="#7c3aed" font-size="13" font-weight="bold">ĐÈN CHIẾU SÁNG</text>
  <text x="785" y="285" text-anchor="middle" fill="#334155" font-size="11">Output GPIO 2 (LED)</text>
  <line x1="580" y1="230" x2="690" y2="270" stroke="#7c3aed" stroke-width="2.5"/>

  <!-- BOTTOM: CLOUD IOT -->
  <rect x="260" y="375" width="400" height="60" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
  <text x="460" y="400" text-anchor="middle" fill="#ea580c" font-size="14" font-weight="bold">CLOUD IOT &amp; APP DI ĐỘNG</text>
  <text x="460" y="420" text-anchor="middle" fill="#475569" font-size="11">Wi-Fi 802.11 b/g/n + Giao thức MQTT (broker.hivemq.com)</text>
  <line x1="460" y1="340" x2="460" y2="375" stroke="#ea580c" stroke-width="3"/>
</svg>
"""
save_svg("bai16_smarthome_architecture.svg", svg_capstone)
