import os
import re

dirs = [
    r"F:\Advance_C\stm32f103c8\images",
    r"F:\embedded-lab-web\public\images\stm32f103",
    r"F:\embedded-lab-web\public\images"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

def split_light_dark(content):
    # Tạo bản light: bỏ media query, đổi canvas-bg sang trắng tinh #ffffff
    light = re.sub(r'@media\s*\(prefers-color-scheme:\s*dark\)\s*\{[\s\S]*?\}\s*\}', '', content)
    light = light.replace('--canvas-bg: #f8fafc;', '--canvas-bg: #ffffff;')
    light = light.replace(' - Hỗ trợ Giao diện Sáng / Tối', '')
    
    # Tạo bản dark: trích xuất biến trong media query gán vào :root
    dark_vars_match = re.search(r'@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{([\s\S]*?)\}\s*\}', content)
    if dark_vars_match:
        dark_vars = dark_vars_match.group(1).strip()
        dark = re.sub(r':root\s*\{[\s\S]*?\}', ':root {\n        ' + dark_vars + '\n      }', content)
        dark = re.sub(r'@media\s*\(prefers-color-scheme:\s*dark\)\s*\{[\s\S]*?\}\s*\}', '', dark)
        dark = dark.replace(' - Hỗ trợ Giao diện Sáng / Tối', '')
    else:
        dark = content

    return light.strip(), dark.strip()

def save_svg(filename, content):
    light_content, dark_content = split_light_dark(content)
    base_name, ext = os.path.splitext(filename)
    
    files_to_save = [
        (filename, light_content),
        (f"{base_name}_light{ext}", light_content),
        (f"{base_name}_dark{ext}", dark_content)
    ]
    
    for fname, cnt in files_to_save:
        for d in dirs:
            p = os.path.join(d, fname)
            with open(p, "w", encoding="utf-8") as f:
                f.write(cnt)
        print(f"Saved SVG: {fname}")

# ==============================================================================
# 1. SƠ ĐỒ PINOUT BLUE PILL STM32F103C8T6 (HỖ TRỢ DARK & LIGHT MODE)
# ==============================================================================
svg_pinout = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1060 920" width="100%" height="100%" style="font-family: 'Segoe UI', Arial, -apple-system, sans-serif;">
  <defs>
    <style>
      :root {
        --canvas-bg: #f8fafc;
        --canvas-border: #e2e8f0;
        --card-bg: #ffffff;
        --title-color: #0f172a;
        --subtitle-color: #475569;
        --board-pcb: #1e3a8a;
        --board-border: #172554;
        --chip-body: #0f172a;
        --chip-border: #334155;
        --chip-text: #e2e8f0;
        --pin-silver: #cbd5e1;
        --pin-stroke: #64748b;
        --label-box-bg: #ffffff;
        --label-border: #cbd5e1;
        --text-primary: #1e293b;
        --text-muted: #64748b;
        --wire-line: #94a3b8;
      }

      @media (prefers-color-scheme: dark) {
        :root {
          --canvas-bg: #0b0f19;
          --canvas-border: #1e293b;
          --card-bg: #111827;
          --title-color: #f8fafc;
          --subtitle-color: #94a3b8;
          --board-pcb: #172554;
          --board-border: #1e3a8a;
          --chip-body: #030712;
          --chip-border: #1e293b;
          --chip-text: #f1f5f9;
          --pin-silver: #475569;
          --pin-stroke: #334155;
          --label-box-bg: #1e293b;
          --label-border: #334155;
          --text-primary: #f8fafc;
          --text-muted: #94a3b8;
          --wire-line: #475569;
        }
      }

      .canvas-bg { fill: var(--canvas-bg); stroke: var(--canvas-border); }
      .title-text { fill: var(--title-color); font-weight: 800; font-size: 24px; text-anchor: middle; }
      .subtitle-text { fill: var(--subtitle-color); font-weight: 600; font-size: 13px; text-anchor: middle; }
      .pcb { fill: var(--board-pcb); stroke: var(--board-border); stroke-width: 3; rx: 14; }
      .mcu { fill: var(--chip-body); stroke: var(--chip-border); stroke-width: 2; rx: 8; }
      .mcu-label { fill: var(--chip-text); font-weight: 700; text-anchor: middle; }
      .pin-box { fill: var(--label-box-bg); stroke: var(--label-border); stroke-width: 1.5; rx: 5; }
      .pin-txt { fill: var(--text-primary); font-size: 11px; font-weight: 700; font-family: monospace; }
      .pin-desc { fill: var(--text-muted); font-size: 10px; font-weight: 600; }
      .wire { stroke: var(--wire-line); stroke-width: 1.5; fill: none; }
      .hdr-pin { fill: var(--pin-silver); stroke: var(--pin-stroke); stroke-width: 1.5; rx: 2; }
    </style>
    <filter id="dropShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- Outer Canvas -->
  <rect x="10" y="10" width="1040" height="900" class="canvas-bg" rx="16" stroke-width="2"/>

  <!-- Title & Subtitle -->
  <text x="530" y="48" class="title-text">SƠ ĐỒ BẢN ĐỒ CHÂN (PINOUT) STM32F103C8T6 BLUE PILL</text>
  <text x="530" y="73" class="subtitle-text">Lõi ARM Cortex-M3 32-bit (72MHz, 64KB Flash, 20KB SRAM) - Hỗ trợ Giao diện Sáng / Tối</text>

  <!-- Legend -->
  <g transform="translate(130, 92)" font-size="11" font-weight="700">
    <rect x="0" y="0" width="14" height="14" fill="#ef4444" rx="3"/>
    <text x="20" y="12" fill="#ef4444">Nguồn (3.3V, 5V, VBAT)</text>

    <rect x="200" y="0" width="14" height="14" fill="#64748b" rx="3"/>
    <text x="220" y="12" class="pin-desc">GND (Mass)</text>

    <rect x="330" y="0" width="14" height="14" fill="#10b981" rx="3"/>
    <text x="350" y="12" fill="#10b981">GPIO thường (3.3V)</text>

    <rect x="500" y="0" width="14" height="14" fill="#06b6d4" rx="3"/>
    <text x="520" y="12" fill="#06b6d4">5V-Tolerant (Chịu 5V)</text>

    <rect x="680" y="0" width="14" height="14" fill="#f59e0b" rx="3"/>
    <text x="700" y="12" fill="#f59e0b">Analog / ADC</text>
  </g>

  <!-- BLUE PILL BOARD (CENTER: X=390, Y=130, W=280, H=740) -->
  <g filter="url(#dropShadow)">
    <rect x="390" y="130" width="280" height="740" class="pcb"/>

    <!-- Micro-USB Port (Top) -->
    <rect x="495" y="118" width="70" height="36" rx="4" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
    <rect x="510" y="112" width="40" height="10" rx="2" fill="#64748b"/>
    <text x="530" y="142" font-size="9" font-weight="800" fill="#0f172a" text-anchor="middle">USB</text>

    <!-- Reset Button -->
    <rect x="430" y="170" width="34" height="34" rx="6" fill="#ef4444" stroke="#991b1b" stroke-width="2"/>
    <circle cx="447" cy="187" r="10" fill="#dc2626"/>
    <text x="447" y="191" font-size="8" font-weight="900" fill="#ffffff" text-anchor="middle">RST</text>

    <!-- Boot Jumpers -->
    <rect x="580" y="165" width="56" height="42" rx="4" fill="#334155" stroke="#475569"/>
    <rect x="585" y="170" width="20" height="14" rx="2" fill="#eab308"/>
    <rect x="610" y="170" width="20" height="14" rx="2" fill="#eab308"/>
    <text x="595" y="198" font-size="8" font-weight="700" fill="#cbd5e1" text-anchor="middle">BT0</text>
    <text x="620" y="198" font-size="8" font-weight="700" fill="#cbd5e1" text-anchor="middle">BT1</text>

    <!-- Crystal 8MHz (HSE) -->
    <rect x="500" y="270" width="60" height="30" rx="8" fill="#cbd5e1" stroke="#94a3b8" stroke-width="2"/>
    <text x="530" y="289" font-size="9" font-weight="800" fill="#334155" text-anchor="middle">8.000 MHz</text>

    <!-- MCU STM32F103C8T6 (LQFP-48) -->
    <g transform="translate(460, 340)">
      <rect x="0" y="0" width="140" height="140" class="mcu"/>
      <circle cx="16" cy="16" r="4" fill="#64748b"/>
      <text x="70" y="55" class="mcu-label" font-size="13">ARM Cortex-M3</text>
      <text x="70" y="75" class="mcu-label" font-size="14" fill="#38bdf8">STM32F103</text>
      <text x="70" y="93" class="mcu-label" font-size="12">C8T6</text>
      <text x="70" y="115" font-size="9" fill="#94a3b8" text-anchor="middle">STMicroelectronics</text>
    </g>

    <!-- LEDs: Power (Red) and PC13 (Green) -->
    <circle cx="435" cy="275" r="7" fill="#ef4444" stroke="#991b1b" stroke-width="1.5"/>
    <text x="435" y="297" font-size="8" font-weight="700" fill="#fca5a5" text-anchor="middle">PWR</text>

    <circle cx="435" cy="320" r="7" fill="#22c55e" stroke="#15803d" stroke-width="1.5"/>
    <text x="435" y="342" font-size="8" font-weight="700" fill="#86efac" text-anchor="middle">PC13</text>

    <!-- 32.768kHz RTC Crystal (LSE) -->
    <rect x="510" y="510" width="40" height="14" rx="4" fill="#94a3b8"/>
    <text x="530" y="521" font-size="7" font-weight="700" fill="#1e293b" text-anchor="middle">32.768K</text>

    <!-- SWD Header Pins (Bottom) -->
    <g transform="translate(470, 830)">
      <rect x="0" y="0" width="120" height="28" rx="4" fill="#0f172a" stroke="#475569"/>
      <circle cx="18" cy="14" r="5" class="hdr-pin"/>
      <circle cx="46" cy="14" r="5" class="hdr-pin"/>
      <circle cx="74" cy="14" r="5" class="hdr-pin"/>
      <circle cx="102" cy="14" r="5" class="hdr-pin"/>
      <text x="18" y="38" font-size="8" font-weight="700" fill="#ef4444" text-anchor="middle">3.3V</text>
      <text x="46" y="38" font-size="8" font-weight="700" fill="#38bdf8" text-anchor="middle">SWIO</text>
      <text x="74" y="38" font-size="8" font-weight="700" fill="#38bdf8" text-anchor="middle">SWCLK</text>
      <text x="102" y="38" font-size="8" font-weight="700" fill="#94a3b8" text-anchor="middle">GND</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- LEFT SIDE PINS (20 Pins): X=400 to Left Label Boxes                      -->
  <!-- ========================================================================= -->
  <!-- Helper python generated Left Pins -->
"""

left_pins = [
    ("PB12", "SPI2_NSS / I2C2_SMBA", "#06b6d4", "5V-Tol"),
    ("PB13", "SPI2_SCK / I2C2_SCL", "#06b6d4", "5V-Tol"),
    ("PB14", "SPI2_MISO / USART3_RTS", "#06b6d4", "5V-Tol"),
    ("PB15", "SPI2_MOSI", "#06b6d4", "5V-Tol"),
    ("PA8",  "USART1_CK / MCO / TIM1_CH1", "#06b6d4", "5V-Tol"),
    ("PA9",  "USART1_TX / TIM1_CH2", "#06b6d4", "5V-Tol"),
    ("PA10", "USART1_RX / TIM1_CH3", "#06b6d4", "5V-Tol"),
    ("PA11", "USB_DM / CAN_RX / TIM1_CH4", "#06b6d4", "5V-Tol"),
    ("PA12", "USB_DP / CAN_TX / TIM1_ETR", "#06b6d4", "5V-Tol"),
    ("PA15", "JTDI / SPI1_NSS", "#06b6d4", "5V-Tol"),
    ("PB3",  "JTDO / SPI1_SCK", "#06b6d4", "5V-Tol"),
    ("PB4",  "NJTRST / SPI1_MISO", "#06b6d4", "5V-Tol"),
    ("PB5",  "I2C1_SMBA / SPI1_MOSI", "#10b981", "3.3V"),
    ("PB6",  "I2C1_SCL / TIM4_CH1", "#06b6d4", "5V-Tol"),
    ("PB7",  "I2C1_SDA / TIM4_CH2", "#06b6d4", "5V-Tol"),
    ("PB8",  "TIM4_CH3 / CAN_RX (Remap)", "#06b6d4", "5V-Tol"),
    ("PB9",  "TIM4_CH4 / CAN_TX (Remap)", "#06b6d4", "5V-Tol"),
    ("5V",   "Nguồn 5V đầu vào (từ USB)", "#ef4444", "PWR"),
    ("GND",  "Mass chuẩn hệ thống", "#64748b", "GND"),
    ("3.3V", "Nguồn 3.3V đầu ra LDO (Tối đa 300mA)", "#ef4444", "PWR")
]

right_pins = [
    ("PB11", "I2C2_SDA / USART3_RX", "#06b6d4", "5V-Tol"),
    ("PB10", "I2C2_SCL / USART3_TX", "#06b6d4", "5V-Tol"),
    ("PB1",  "ADC12_IN9 / TIM3_CH4", "#f59e0b", "ADC/3V3"),
    ("PB0",  "ADC12_IN8 / TIM3_CH3", "#f59e0b", "ADC/3V3"),
    ("PA7",  "ADC12_IN7 / SPI1_MOSI / TIM3_CH2", "#f59e0b", "ADC/3V3"),
    ("PA6",  "ADC12_IN6 / SPI1_MISO / TIM3_CH1", "#f59e0b", "ADC/3V3"),
    ("PA5",  "ADC12_IN5 / SPI1_SCK", "#f59e0b", "ADC/3V3"),
    ("PA4",  "ADC12_IN4 / SPI1_NSS / USART2_CK", "#f59e0b", "ADC/3V3"),
    ("PA3",  "ADC12_IN3 / USART2_RX / TIM2_CH4", "#f59e0b", "ADC/3V3"),
    ("PA2",  "ADC12_IN2 / USART2_TX / TIM2_CH3", "#f59e0b", "ADC/3V3"),
    ("PA1",  "ADC12_IN1 / USART2_RTS / TIM2_CH2", "#f59e0b", "ADC/3V3"),
    ("PA0",  "ADC12_IN0 / WKUP / USART2_CTS", "#f59e0b", "ADC/3V3"),
    ("PC15", "OSC32_OUT / Chân I/O thường", "#10b981", "3.3V"),
    ("PC14", "OSC32_IN / Chân I/O thường", "#10b981", "3.3V"),
    ("PC13", "TAMPER-RTC / ĐÈN LED TÍCH HỢP (Active-Low)", "#22c55e", "LED ONBOARD"),
    ("VBAT", "Nguồn cấp Pin 3V nuôi RTC khi mất điện", "#ef4444", "PWR"),
    ("3.3V", "Nguồn 3.3V đầu ra", "#ef4444", "PWR"),
    ("GND",  "Mass chuẩn hệ thống", "#64748b", "GND"),
    ("GND",  "Mass chuẩn hệ thống", "#64748b", "GND"),
    ("3.3V", "Nguồn 3.3V đầu ra", "#ef4444", "PWR")
]

start_y = 160
step_y = 33

svg_left_elements = []
for idx, (pname, pdesc, color, tag) in enumerate(left_pins):
    y = start_y + idx * step_y
    # Header pin on board
    svg_left_elements.append(f'<circle cx="410" cy="{y+10}" r="4" class="hdr-pin"/>')
    # Wire
    svg_left_elements.append(f'<line x1="404" y1="{y+10}" x2="350" y2="{y+10}" class="wire"/>')
    # Label Box
    svg_left_elements.append(f'''<g transform="translate(30, {y})">
      <rect x="0" y="0" width="315" height="23" class="pin-box"/>
      <rect x="250" y="2" width="60" height="19" rx="3" fill="{color}" opacity="0.2"/>
      <text x="280" y="15" fill="{color}" font-size="9" font-weight="800" text-anchor="middle">{pname}</text>
      <text x="240" y="15" text-anchor="end" class="pin-desc">{pdesc}</text>
    </g>''')

svg_right_elements = []
for idx, (pname, pdesc, color, tag) in enumerate(right_pins):
    y = start_y + idx * step_y
    # Header pin on board
    svg_right_elements.append(f'<circle cx="650" cy="{y+10}" r="4" class="hdr-pin"/>')
    # Wire
    svg_right_elements.append(f'<line x1="656" y1="{y+10}" x2="710" y2="{y+10}" class="wire"/>')
    # Label Box
    is_special = (pname == "PC13")
    box_border = f'stroke="#22c55e" stroke-width="2"' if is_special else 'class="pin-box"'
    svg_right_elements.append(f'''<g transform="translate(715, {y})">
      <rect x="0" y="0" width="315" height="23" {box_border} rx="5" fill="var(--label-box-bg)"/>
      <rect x="5" y="2" width="60" height="19" rx="3" fill="{color}" opacity="0.2"/>
      <text x="35" y="15" fill="{color}" font-size="9" font-weight="800" text-anchor="middle">{pname}</text>
      <text x="75" y="15" class="pin-desc">{pdesc}</text>
    </g>''')

svg_pinout += "\n".join(svg_left_elements)
svg_pinout += "\n".join(svg_right_elements)
svg_pinout += "\n</svg>"

save_svg("bai01_stm32f103_bluepill_pinout.svg", svg_pinout)

# ==============================================================================
# 2. SƠ ĐỒ KẾT NỐI ST-LINK V2 VỚI BLUE PILL & MẠCH NGUYÊN LÝ LED PC13
# ==============================================================================
svg_stlink_schematic = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" width="100%" height="100%" style="font-family: 'Segoe UI', Arial, -apple-system, sans-serif;">
  <defs>
    <style>
      :root {
        --canvas-bg: #f8fafc;
        --canvas-border: #e2e8f0;
        --card-bg: #ffffff;
        --card-border: #cbd5e1;
        --title-color: #0f172a;
        --subtitle-color: #475569;
        --text-primary: #1e293b;
        --text-muted: #64748b;
        --panel-bg: #f1f5f9;
        --panel-border: #cbd5e1;
      }

      @media (prefers-color-scheme: dark) {
        :root {
          --canvas-bg: #0b0f19;
          --canvas-border: #1e293b;
          --card-bg: #111827;
          --card-border: #334155;
          --title-color: #f8fafc;
          --subtitle-color: #94a3b8;
          --text-primary: #f8fafc;
          --text-muted: #94a3b8;
          --panel-bg: #1e293b;
          --panel-border: #334155;
        }
      }

      .canvas-bg { fill: var(--canvas-bg); stroke: var(--canvas-border); }
      .card-box { fill: var(--card-bg); stroke: var(--card-border); stroke-width: 2; rx: 12; }
      .panel-box { fill: var(--panel-bg); stroke: var(--panel-border); stroke-width: 1.5; rx: 8; }
      .title-text { fill: var(--title-color); font-weight: 800; font-size: 19px; text-anchor: middle; }
      .subtitle-text { fill: var(--subtitle-color); font-weight: 600; font-size: 13px; text-anchor: middle; }
      .txt-p { fill: var(--text-primary); font-weight: 700; font-size: 13px; }
      .txt-m { fill: var(--text-muted); font-size: 12px; }
    </style>
    <filter id="shadowBox" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.15"/>
    </filter>
  </defs>

  <!-- Outer Canvas -->
  <rect x="10" y="10" width="940" height="540" class="canvas-bg" rx="16" stroke-width="2"/>

  <!-- Title -->
  <text x="480" y="45" class="title-text">SƠ ĐỒ NẠP CODE ST-LINK V2 &amp; MẠCH NGUYÊN LÝ LED PC13 (ACTIVE-LOW)</text>
  <text x="480" y="68" class="subtitle-text">Giao thức Serial Wire Debug (SWD) 4 Dây Chuẩn - Hỗ trợ Giao diện Sáng / Tối</text>

  <!-- LEFT SECTION: ST-LINK V2 to STM32 BLUE PILL (X=30, Y=95, W=465, H=430) -->
  <g transform="translate(30, 95)" filter="url(#shadowBox)">
    <rect x="0" y="0" width="465" height="430" class="card-box"/>
    <text x="232" y="32" class="title-text" font-size="15">1. Kết Nối Mạch Nạp ST-Link V2 (SWD Header)</text>

    <!-- ST-Link Body -->
    <rect x="30" y="70" width="110" height="280" rx="8" fill="#2563eb" stroke="#1d4ed8" stroke-width="2"/>
    <rect x="50" y="55" width="70" height="20" rx="3" fill="#94a3b8"/>
    <text x="85" y="69" font-size="9" font-weight="bold" fill="#0f172a" text-anchor="middle">USB PC</text>
    <text x="85" y="170" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle" transform="rotate(-90, 85, 170)">ST-LINK V2</text>

    <!-- ST-Link 4 Pins -->
    <circle cx="130" cy="120" r="5" fill="#ef4444"/>
    <circle cx="130" cy="170" r="5" fill="#06b6d4"/>
    <circle cx="130" cy="220" r="5" fill="#3b82f6"/>
    <circle cx="130" cy="270" r="5" fill="#64748b"/>

    <!-- Blue Pill Target -->
    <rect x="325" y="70" width="115" height="280" rx="8" fill="#1e3a8a" stroke="#172554" stroke-width="2"/>
    <text x="382" y="190" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle" transform="rotate(-90, 382, 190)">STM32 BLUE PILL</text>
    <circle cx="335" cy="120" r="5" fill="#ef4444"/>
    <circle cx="335" cy="170" r="5" fill="#06b6d4"/>
    <circle cx="335" cy="220" r="5" fill="#3b82f6"/>
    <circle cx="335" cy="270" r="5" fill="#64748b"/>

    <!-- Connecting Wires -->
    <!-- 3.3V Line -->
    <path d="M 130 120 L 335 120" stroke="#ef4444" stroke-width="3" fill="none"/>
    <rect x="195" y="108" width="76" height="22" rx="4" fill="#ef4444"/>
    <text x="233" y="123" font-size="11" font-weight="800" fill="#ffffff" text-anchor="middle">3.3V (VCC)</text>

    <!-- SWDIO Line -->
    <path d="M 130 170 L 335 170" stroke="#06b6d4" stroke-width="3" fill="none"/>
    <rect x="183" y="158" width="100" height="22" rx="4" fill="#06b6d4"/>
    <text x="233" y="173" font-size="11" font-weight="800" fill="#0f172a" text-anchor="middle">SWDIO (PA13)</text>

    <!-- SWCLK Line -->
    <path d="M 130 220 L 335 220" stroke="#3b82f6" stroke-width="3" fill="none"/>
    <rect x="183" y="208" width="100" height="22" rx="4" fill="#3b82f6"/>
    <text x="233" y="223" font-size="11" font-weight="800" fill="#ffffff" text-anchor="middle">SWCLK (PA14)</text>

    <!-- GND Line -->
    <path d="M 130 270 L 335 270" stroke="#64748b" stroke-width="3" fill="none"/>
    <rect x="195" y="258" width="76" height="22" rx="4" fill="#64748b"/>
    <text x="233" y="273" font-size="11" font-weight="800" fill="#ffffff" text-anchor="middle">GND (0V)</text>

    <text x="232" y="385" class="txt-m" text-anchor="middle">Lưu ý: Không cắm nhầm nguồn 5V vào chân 3.3V của chip!</text>
  </g>

  <!-- RIGHT SECTION: ACTIVE-LOW LED SCHEMATIC (X=515, Y=95, W=415, H=430) -->
  <g transform="translate(515, 95)" filter="url(#shadowBox)">
    <rect x="0" y="0" width="415" height="430" class="card-box"/>
    <text x="208" y="32" class="title-text" font-size="15">2. Sơ Đồ Mạch LED PC13 (Active-Low)</text>

    <!-- Schematic Box -->
    <g transform="translate(48, 65)">
      <!-- VCC 3.3V Rail -->
      <line x1="160" y1="20" x2="160" y2="60" stroke="#ef4444" stroke-width="3"/>
      <polygon points="160,10 150,25 170,25" fill="#ef4444"/>
      <text x="160" y="2" font-size="12" font-weight="900" fill="#ef4444" text-anchor="middle">+3.3V (VCC)</text>

      <!-- Resistor R = 510 Ohm -->
      <rect x="145" y="60" width="30" height="45" rx="3" fill="#f59e0b" stroke="#d97706" stroke-width="2"/>
      <text x="160" y="87" font-size="10" font-weight="bold" fill="#0f172a" text-anchor="middle">510Ω</text>
      <line x1="160" y1="105" x2="160" y2="135" stroke="var(--text-primary)" stroke-width="2.5"/>

      <!-- LED Green -->
      <!-- Triangle -->
      <polygon points="145,135 175,135 160,165" fill="#22c55e" stroke="#16a34a" stroke-width="2"/>
      <!-- Cathode Bar -->
      <line x1="145" y1="165" x2="175" y2="165" stroke="#16a34a" stroke-width="3"/>
      <!-- Photons Emission arrows -->
      <line x1="172" y1="140" x2="190" y2="130" stroke="#22c55e" stroke-width="2"/>
      <polygon points="190,130 183,135 186,140" fill="#22c55e"/>
      <line x1="175" y1="150" x2="193" y2="140" stroke="#22c55e" stroke-width="2"/>
      <polygon points="193,140 186,145 189,150" fill="#22c55e"/>
      <text x="212" y="152" font-size="11" font-weight="bold" fill="#22c55e">LED Xanh</text>

      <!-- Connection to PC13 -->
      <line x1="160" y1="165" x2="160" y2="215" stroke="var(--text-primary)" stroke-width="2.5"/>
      <rect x="110" y="215" width="100" height="30" rx="6" fill="#1e3a8a" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="160" y="235" font-size="12" font-weight="800" fill="#ffffff" text-anchor="middle">Chân PC13</text>
    </g>

    <!-- Logic Explanation Table -->
    <g transform="translate(20, 312)">
      <rect x="0" y="0" width="375" height="98" class="panel-box"/>
      
      <!-- Row 1: Low Level -> ON -->
      <g transform="translate(10, 10)">
        <rect x="0" y="0" width="355" height="24" rx="5" fill="#22c55e" fill-opacity="0.12" stroke="#22c55e" stroke-opacity="0.35"/>
        <text x="10" y="16" font-size="11.5" font-weight="700" fill="var(--text-primary)">• Mức 0 (0V):</text>
        <text x="96" y="16" font-size="11.5" font-weight="700" fill="#22c55e">Có dòng qua LED → BẬT SÁNG</text>
        <text x="345" y="16" font-size="10.5" font-weight="700" fill="#16a34a" text-anchor="end">ResetBits()</text>
      </g>

      <!-- Row 2: High Level -> OFF -->
      <g transform="translate(10, 38)">
        <rect x="0" y="0" width="355" height="24" rx="5" fill="#ef4444" fill-opacity="0.12" stroke="#ef4444" stroke-opacity="0.35"/>
        <text x="10" y="16" font-size="11.5" font-weight="700" fill="var(--text-primary)">• Mức 1 (3.3V):</text>
        <text x="96" y="16" font-size="11.5" font-weight="700" fill="#ef4444">Cân bằng áp 3.3V → TẮT</text>
        <text x="345" y="16" font-size="10.5" font-weight="700" fill="#dc2626" text-anchor="end">SetBits()</text>
      </g>

      <!-- Row 3: Bottom note -->
      <text x="187" y="84" font-size="10.5" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Cơ chế Active-Low: Kéo chân về 0V (Reset) để sáng đèn</text>
    </g>
  </g>
</svg>"""

save_svg("bai01_stlink_swd_connection.svg", svg_stlink_schematic)

# ==============================================================================
# 3. SƠ ĐỒ BẢN CHẤT LẬP TRÌNH MCU & MEMORY-MAPPED I/O (NGẮN GỌN CHO NGƯỜI MỚI BẮT ĐẦU)
# ==============================================================================
svg_memory_mapping = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" width="100%" height="100%" style="font-family: 'Segoe UI', Arial, -apple-system, sans-serif;">
  <defs>
    <style>
      :root {
        --canvas-bg: #f8fafc;
        --canvas-border: #e2e8f0;
        --card-bg: #ffffff;
        --card-border: #cbd5e1;
        --title-color: #0f172a;
        --subtitle-color: #475569;
        --text-primary: #1e293b;
        --text-muted: #64748b;
        --panel-bg: #f1f5f9;
        --panel-border: #cbd5e1;
      }

      @media (prefers-color-scheme: dark) {
        :root {
          --canvas-bg: #0b0f19;
          --canvas-border: #1e293b;
          --card-bg: #111827;
          --card-border: #334155;
          --title-color: #f8fafc;
          --subtitle-color: #94a3b8;
          --text-primary: #f8fafc;
          --text-muted: #94a3b8;
          --panel-bg: #1e293b;
          --panel-border: #334155;
        }
      }

      .canvas-bg { fill: var(--canvas-bg); stroke: var(--canvas-border); }
      .card-box { fill: var(--card-bg); stroke: var(--card-border); stroke-width: 1.5; rx: 12; }
      .title-text { fill: var(--title-color); font-weight: 800; font-size: 20px; text-anchor: middle; }
      .subtitle-text { fill: var(--subtitle-color); font-weight: 600; font-size: 13px; text-anchor: middle; }
      .step-title { font-weight: 800; font-size: 13px; text-anchor: middle; }
      .txt-p { fill: var(--text-primary); font-size: 12px; font-weight: 600; }
      .txt-bold { fill: var(--text-primary); font-size: 12.5px; font-weight: 800; }
      .txt-m { fill: var(--text-muted); font-size: 11px; }
      .txt-code { font-family: 'Consolas', 'Courier New', monospace; font-size: 11.5px; }
    </style>

    <filter id="shadowLight" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000000" flood-opacity="0.1"/>
    </filter>

    <marker id="arrowBlue" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#2563eb"/>
    </marker>
    <marker id="arrowGreen" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#059669"/>
    </marker>
  </defs>

  <!-- Canvas Background -->
  <rect x="10" y="10" width="940" height="460" class="canvas-bg" rx="16" stroke-width="2"/>

  <!-- Title Header -->
  <text x="480" y="44" class="title-text">BẢN CHẤT LẬP TRÌNH VI ĐIỀU KHIỂN QUA THANH GHI ODR</text>
  <text x="480" y="68" class="subtitle-text">Ghi bit vào ô nhớ GPIOC_ODR ➔ Thay đổi điện áp chân chip ➔ Bật / Tắt LED</text>

  <!-- ==================== BƯỚC 1: LỆNH CON TRỎ C ==================== -->
  <g transform="translate(40, 95)" filter="url(#shadowLight)">
    <rect x="0" y="0" width="250" height="285" class="card-box"/>
    <!-- Header -->
    <rect x="0" y="0" width="250" height="38" rx="12" fill="#2563eb"/>
    <text x="125" y="24" class="step-title" fill="#ffffff">1. BẠN VIẾT LỆNH C</text>

    <!-- Code Block -->
    <rect x="15" y="52" width="220" height="85" rx="6" fill="#0f172a"/>
    <text x="25" y="74" class="txt-code" fill="#94a3b8">// Bật LED (Mức 0):</text>
    <text x="25" y="94" class="txt-code" fill="#38bdf8">*REG_ODR &amp;= ~(1 &lt;&lt; 13);</text>
    <text x="25" y="114" class="txt-code" fill="#94a3b8">// Đảo trạng thái (Toggle):</text>
    <text x="25" y="128" class="txt-code" fill="#facc15">*REG_ODR ^= (1 &lt;&lt; 13);</text>

    <!-- Breakdown -->
    <rect x="15" y="150" width="220" height="118" rx="6" fill="var(--panel-bg)" stroke="var(--panel-border)" stroke-width="1"/>
    <text x="25" y="174" class="txt-bold" fill="#2563eb">• Địa chỉ:</text>
    <text x="85" y="174" class="txt-code" fill="var(--text-primary)">0x4001100C</text>
    
    <text x="25" y="202" class="txt-bold" fill="#d97706">• Dữ liệu:</text>
    <text x="85" y="202" class="txt-code" fill="var(--text-primary)">Bit 13 = 0 (BẬT)</text>
    
    <text x="25" y="234" class="txt-bold" fill="#059669">• Thao tác:</text>
    <text x="25" y="252" class="txt-p" fill="#059669">CPU ghi thẳng vào ODR</text>
  </g>

  <!-- ARROW 1 -> 2 -->
  <path d="M 300 235 L 345 235" stroke="#2563eb" stroke-width="3" fill="none" marker-end="url(#arrowBlue)"/>
  <text x="322" y="222" font-size="10" font-weight="800" fill="#2563eb" text-anchor="middle">GHI BIT</text>

  <!-- ==================== BƯỚC 2: THANH GHI ODR ==================== -->
  <g transform="translate(355, 95)" filter="url(#shadowLight)">
    <rect x="0" y="0" width="250" height="285" class="card-box"/>
    <!-- Header -->
    <rect x="0" y="0" width="250" height="38" rx="12" fill="#7c3aed"/>
    <text x="125" y="24" class="step-title" fill="#ffffff">2. THANH GHI GPIOC_ODR</text>

    <!-- Top info -->
    <rect x="15" y="52" width="220" height="58" rx="6" fill="var(--panel-bg)" stroke="var(--panel-border)" stroke-width="1"/>
    <text x="25" y="74" class="txt-bold" fill="#7c3aed">Output Data Register</text>
    <text x="25" y="94" class="txt-code" fill="var(--text-muted)">Địa chỉ: 0x4001 100C</text>

    <!-- Register Bits diagram -->
    <rect x="15" y="122" width="220" height="80" rx="6" fill="#fdf4ff" stroke="#c084fc" stroke-width="1.5"/>
    <text x="125" y="142" class="txt-bold" font-size="11" fill="#7c3aed" text-anchor="middle">ÁNH XẠ TỪNG BIT RA CHÂN</text>
    
    <!-- Bit boxes -->
    <g transform="translate(25, 152)">
      <rect x="0" y="0" width="35" height="26" rx="3" fill="var(--card-bg)" stroke="#cbd5e1"/>
      <text x="17" y="12" font-size="8" fill="var(--text-muted)" text-anchor="middle">Bit15</text>
      <text x="17" y="22" font-size="9" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">0</text>

      <rect x="40" y="0" width="35" height="26" rx="3" fill="var(--card-bg)" stroke="#cbd5e1"/>
      <text x="57" y="12" font-size="8" fill="var(--text-muted)" text-anchor="middle">Bit14</text>
      <text x="57" y="22" font-size="9" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">0</text>

      <!-- Highlight Bit 13 -->
      <rect x="80" y="0" width="45" height="26" rx="3" fill="#22c55e" stroke="#15803d" stroke-width="1.5"/>
      <text x="102" y="12" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="middle">Bit 13</text>
      <text x="102" y="22" font-size="10" font-weight="900" fill="#ffffff" text-anchor="middle">0</text>

      <rect x="130" y="0" width="35" height="26" rx="3" fill="var(--card-bg)" stroke="#cbd5e1"/>
      <text x="147" y="12" font-size="8" fill="var(--text-muted)" text-anchor="middle">...</text>
      <text x="147" y="22" font-size="9" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">...</text>

      <rect x="170" y="0" width="30" height="26" rx="3" fill="var(--card-bg)" stroke="#cbd5e1"/>
      <text x="185" y="12" font-size="8" fill="var(--text-muted)" text-anchor="middle">Bit0</text>
      <text x="185" y="22" font-size="9" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">0</text>
    </g>
    <text x="125" y="195" font-size="9.5" font-weight="bold" fill="#059669" text-anchor="middle">Bit 13 nối trực tiếp ra chân PC13</text>

    <!-- State note -->
    <rect x="15" y="214" width="220" height="54" rx="6" fill="var(--panel-bg)" stroke="var(--panel-border)" stroke-width="1"/>
    <text x="25" y="235" class="txt-bold" fill="#059669">• Bit 13 = 0 ➔ Chân PC13 = 0V</text>
    <text x="25" y="253" class="txt-m">• Bit 13 = 1 ➔ Chân PC13 = 3.3V</text>
  </g>

  <!-- ARROW 2 -> 3 -->
  <path d="M 615 235 L 660 235" stroke="#059669" stroke-width="3" fill="none" marker-end="url(#arrowGreen)"/>
  <text x="637" y="222" font-size="10" font-weight="800" fill="#059669" text-anchor="middle">XUẤT 0V</text>

  <!-- ==================== BƯỚC 3: THẾ GIỚI THỰC ==================== -->
  <g transform="translate(670, 95)" filter="url(#shadowLight)">
    <rect x="0" y="0" width="250" height="285" class="card-box"/>
    <!-- Header -->
    <rect x="0" y="0" width="250" height="38" rx="12" fill="#059669"/>
    <text x="125" y="24" class="step-title" fill="#ffffff">3. PHẦN CỨNG THỰC</text>

    <!-- Pin indicator -->
    <rect x="15" y="52" width="220" height="48" rx="6" fill="#1e293b"/>
    <text x="125" y="73" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">Chân chip: PC13</text>
    <text x="125" y="90" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">Điện áp: 0V (GND)</text>

    <!-- LED On Graphic -->
    <rect x="15" y="112" width="220" height="96" rx="6" fill="var(--panel-bg)" stroke="var(--panel-border)" stroke-width="1"/>
    <circle cx="125" cy="148" r="22" fill="#22c55e" filter="drop-shadow(0 0 8px #22c55e)"/>
    <circle cx="125" cy="148" r="14" fill="#bbf7d0"/>
    <text x="125" y="192" font-size="13" font-weight="900" fill="#15803d" text-anchor="middle">💡 LED BẬT SÁNG</text>

    <!-- Contrast note -->
    <rect x="15" y="220" width="220" height="48" rx="6" fill="var(--card-bg)" stroke="var(--card-border)"/>
    <text x="125" y="239" class="txt-bold" font-size="10.5" fill="#ef4444" text-anchor="middle">Nếu Bit 13 = 1 (3.3V):</text>
    <text x="125" y="255" class="txt-m" text-anchor="middle">Điện áp cân bằng ➔ LED TẮT</text>
  </g>

  <!-- ==================== FOOTER GHI CHÚ RÚT GỌN ==================== -->
  <g transform="translate(40, 395)" filter="url(#shadowLight)">
    <rect x="0" y="0" width="880" height="50" rx="8" fill="var(--card-bg)" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="440" y="31" class="txt-bold" font-size="12.5" fill="#0284c7" text-anchor="middle">
      💡 CỐT LÕI: Thanh ghi ODR chứa trạng thái chân chip. Đổi bit trong ODR = Đổi điện áp thực tế!
    </text>
  </g>

</svg>"""

save_svg("bai01_memory_mapping_cortex_m3.svg", svg_memory_mapping)
print("ALL SVGs successfully generated!")

