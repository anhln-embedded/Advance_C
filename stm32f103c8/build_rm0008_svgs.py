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
    light = re.sub(r'@media\s*\(prefers-color-scheme:\s*dark\)\s*\{[\s\S]*?\}\s*\}', '', content)
    light = light.replace('--canvas-bg: #f8fafc;', '--canvas-bg: #ffffff;')
    
    dark_vars_match = re.search(r'@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{([\s\S]*?)\}\s*\}', content)
    if dark_vars_match:
        dark_vars = dark_vars_match.group(1).strip()
        dark = re.sub(r':root\s*\{[\s\S]*?\}', ':root {\n        ' + dark_vars + '\n      }', content)
        dark = re.sub(r'@media\s*\(prefers-color-scheme:\s*dark\)\s*\{[\s\S]*?\}\s*\}', '', dark)
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
    print(f"Generated RM0008 SVG: {filename}")

COMMON_STYLES = """
    <style>
      :root {
        --canvas-bg: #f8fafc;
        --canvas-border: #cbd5e1;
        --card-bg: #ffffff;
        --card-border: #94a3b8;
        --title-color: #0f172a;
        --subtitle-color: #475569;
        --text-primary: #0f172a;
        --text-muted: #64748b;
        --st-blue: #00205b;
        --st-cyan: #00a3e0;
        --accent-blue: #0284c7;
        --accent-green: #059669;
        --accent-amber: #d97706;
        --accent-red: #dc2626;
        --accent-purple: #7c3aed;
        --wire-line: #334155;
        --bus-line: #0284c7;
        --vdd-color: #dc2626;
        --vss-color: #16a34a;
      }
      @media (prefers-color-scheme: dark) {
        :root {
          --canvas-bg: #0b1120;
          --canvas-border: #1e293b;
          --card-bg: #131d31;
          --card-border: #334155;
          --title-color: #f8fafc;
          --subtitle-color: #94a3b8;
          --text-primary: #f1f5f9;
          --text-muted: #94a3b8;
          --st-blue: #38bdf8;
          --st-cyan: #38bdf8;
          --accent-blue: #38bdf8;
          --accent-green: #34d399;
          --accent-amber: #fbbf24;
          --accent-red: #f87171;
          --accent-purple: #c084fc;
          --wire-line: #94a3b8;
          --bus-line: #60a5fa;
          --vdd-color: #f87171;
          --vss-color: #4ade80;
        }
      }
      text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
      .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
    </style>
"""

# ==============================================================================
# 1. BÀI 02: STM32F103 GPIO STRUCTURE (ST RM0008 Figure 13 & 14)
# ==============================================================================
svg_gpio_rm0008 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 680" width="100%" height="100%">
{COMMON_STYLES}
  <!-- Canvas Background -->
  <rect width="1080" height="680" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Header & Official Reference -->
  <rect x="20" y="16" width="1040" height="60" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="40" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 9.1</text>
  <text x="40" y="62" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 13: Basic structure of a standard I/O port bit (Cấu trúc điện tử chân I/O GPIO STM32F103)</text>
  <rect x="910" y="28" width="130" height="34" rx="6" fill="#00205b"/>
  <text x="975" y="50" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left Side: Bus Interface & Registers Container -->
  <g transform="translate(30, 95)">
    <rect width="210" height="555" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="105" y="26" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">BUS INTERFACE</text>
    <text x="105" y="42" text-anchor="middle" font-size="11" font-weight="600" fill="var(--text-muted)">APB2 Peripheral Bus</text>

    <!-- Bit Set/Reset Register -->
    <g transform="translate(15, 60)">
      <rect width="180" height="50" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="90" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Bit Set / Reset Reg</text>
      <text x="90" y="38" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-blue)" class="mono">GPIOx_BSRR / BRR</text>
    </g>

    <!-- Write Signal -->
    <path d="M 105 110 L 105 135" stroke="var(--bus-line)" stroke-width="2" marker-end="url(#arrow-down)"/>

    <!-- Output Data Register -->
    <g transform="translate(15, 135)">
      <rect width="180" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="90" y="24" text-anchor="middle" font-size="12" font-weight="700" fill="var(--title-color)">Output Data Register</text>
      <text x="90" y="42" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-blue)" class="mono">GPIOx_ODR</text>
    </g>

    <!-- Read ODR feedback -->
    <g transform="translate(15, 215)">
      <rect width="180" height="35" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="90" y="22" text-anchor="middle" font-size="11" font-weight="600" fill="var(--text-primary)">Read GPIOx_ODR</text>
    </g>

    <!-- Alternate Function Output -->
    <g transform="translate(15, 275)">
      <rect width="180" height="50" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="90" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-purple)">Alternate Function Out</text>
      <text x="90" y="38" text-anchor="middle" font-size="10" fill="var(--text-muted)">(USART_TX, SPI_SCK...)</text>
    </g>

    <!-- Input Data Register -->
    <g transform="translate(15, 360)">
      <rect width="180" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="90" y="24" text-anchor="middle" font-size="12" font-weight="700" fill="var(--title-color)">Input Data Register</text>
      <text x="90" y="42" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-green)" class="mono">GPIOx_IDR</text>
    </g>

    <!-- Alternate Function Input -->
    <g transform="translate(15, 440)">
      <rect width="180" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="90" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-purple)">Alternate Function In</text>
      <text x="90" y="35" text-anchor="middle" font-size="10" fill="var(--text-muted)">(USART_RX, EXTI, TIM)</text>
    </g>

    <!-- Analog In/Out -->
    <g transform="translate(15, 500)">
      <rect width="180" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="90" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-amber)">Analog In/Out (ADC/DAC)</text>
    </g>
  </g>

  <!-- Center Section: Output Control Logic & MOSFET Drivers -->
  <g transform="translate(270, 95)">
    <!-- Output Control Block -->
    <rect x="0" y="115" width="160" height="135" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="80" y="140" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-blue)">OUTPUT CONTROL</text>
    <text x="80" y="160" text-anchor="middle" font-size="10" font-weight="600" fill="var(--text-muted)">Push-Pull / Open-Drain</text>
    <text x="80" y="180" text-anchor="middle" font-size="10" fill="var(--text-muted)">Control Logic</text>
    <line x1="15" y1="195" x2="145" y2="195" stroke="var(--card-border)"/>
    <text x="80" y="215" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">CNF[1:0] / MODE[1:0]</text>
    <text x="80" y="235" text-anchor="middle" font-size="9" fill="var(--text-muted)">(Tốc độ 2/10/50MHz)</text>

    <!-- Output Lines to MOSFETs -->
    <path d="M 160 145 L 230 145" stroke="var(--wire-line)" stroke-width="2"/>
    <text x="180" y="138" font-size="10" font-weight="600" fill="var(--text-muted)">Gate P</text>

    <path d="M 160 215 L 230 215" stroke="var(--wire-line)" stroke-width="2"/>
    <text x="180" y="230" font-size="10" font-weight="600" fill="var(--text-muted)">Gate N</text>

    <!-- P-MOS Transistor Box -->
    <g transform="translate(230, 115)">
      <rect width="110" height="60" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <!-- P-MOS symbol representation -->
      <circle cx="28" cy="30" r="4" fill="none" stroke="var(--accent-red)" stroke-width="1.5"/>
      <text x="65" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-red)">P-MOS</text>
      <text x="65" y="44" text-anchor="middle" font-size="9" font-weight="600" fill="var(--text-muted)">Pull-up (VDD)</text>
    </g>

    <!-- VDD Power Rail to P-MOS -->
    <line x1="285" y1="60" x2="285" y2="115" stroke="var(--vdd-color)" stroke-width="2.5"/>
    <polygon points="280,60 290,60 285,50" fill="var(--vdd-color)"/>
    <text x="285" y="42" text-anchor="middle" font-size="11" font-weight="800" fill="var(--vdd-color)">VDD (3.3V)</text>

    <!-- N-MOS Transistor Box -->
    <g transform="translate(230, 185)">
      <rect width="110" height="60" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <text x="55" y="28" text-anchor="middle" font-size="12" font-weight="800" fill="var(--vss-color)">N-MOS</text>
      <text x="55" y="46" text-anchor="middle" font-size="9" font-weight="600" fill="var(--text-muted)">Pull-down (VSS)</text>
    </g>

    <!-- VSS (GND) to N-MOS -->
    <line x1="285" y1="245" x2="285" y2="285" stroke="var(--vss-color)" stroke-width="2.5"/>
    <!-- Ground symbol -->
    <line x1="270" y1="285" x2="300" y2="285" stroke="var(--vss-color)" stroke-width="2.5"/>
    <line x1="275" y1="290" x2="295" y2="290" stroke="var(--vss-color)" stroke-width="2"/>
    <line x1="280" y1="295" x2="290" y2="295" stroke="var(--vss-color)" stroke-width="1.5"/>
    <text x="285" y="310" text-anchor="middle" font-size="11" font-weight="800" fill="var(--vss-color)">VSS (GND)</text>

    <!-- Junction of P-MOS and N-MOS outputs -->
    <path d="M 340 145 L 375 145 L 375 215 L 340 215" stroke="var(--wire-line)" stroke-width="2"/>
    <circle cx="375" cy="180" r="4" fill="var(--title-color)"/>
  </g>

  <!-- Upper Center: Pull-up and Pull-down Resistors (RM0008) -->
  <g transform="translate(450, 95)">
    <!-- VDD Rail for Pull-Up -->
    <line x1="70" y1="30" x2="70" y2="60" stroke="var(--vdd-color)" stroke-width="2"/>
    <polygon points="65,30 75,30 70,20" fill="var(--vdd-color)"/>
    <text x="70" y="15" text-anchor="middle" font-size="11" font-weight="800" fill="var(--vdd-color)">VDD</text>

    <!-- Pull-Up Resistor & Switch Box -->
    <rect x="10" y="60" width="120" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="70" y="82" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">R_PU ~40kΩ</text>
    <text x="70" y="98" text-anchor="middle" font-size="10" fill="var(--accent-blue)">[P-MOS Switch]</text>
    <text x="70" y="114" text-anchor="middle" font-size="9" fill="var(--text-muted)">(Control: ODR=1)</text>

    <!-- Connect to PAD line -->
    <line x1="70" y1="125" x2="70" y2="275" stroke="var(--wire-line)" stroke-width="2"/>
    <circle cx="70" cy="275" r="4" fill="var(--title-color)"/>

    <!-- Pull-Down Resistor & Switch Box -->
    <rect x="10" y="325" width="120" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="70" y="347" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">R_PD ~40kΩ</text>
    <text x="70" y="363" text-anchor="middle" font-size="10" fill="var(--accent-green)">[N-MOS Switch]</text>
    <text x="70" y="379" text-anchor="middle" font-size="9" fill="var(--text-muted)">(Control: ODR=0)</text>

    <line x1="70" y1="275" x2="70" y2="325" stroke="var(--wire-line)" stroke-width="2"/>
    <line x1="70" y1="390" x2="70" y2="420" stroke="var(--vss-color)" stroke-width="2"/>
    <!-- Ground symbol -->
    <line x1="55" y1="420" x2="85" y2="420" stroke="var(--vss-color)" stroke-width="2"/>
    <line x1="60" y1="425" x2="80" y2="425" stroke="var(--vss-color)" stroke-width="1.5"/>
    <line x1="65" y1="430" x2="75" y2="430" stroke="var(--vss-color)" stroke-width="1"/>
    <text x="70" y="445" text-anchor="middle" font-size="10" font-weight="700" fill="var(--vss-color)">VSS</text>
  </g>

  <!-- Input Path: Schmitt Trigger (RM0008) -->
  <g transform="translate(390, 440)">
    <!-- Line from PAD to Schmitt Trigger -->
    <path d="M 130 -70 L 60 -70 L 60 40 L 90 40" stroke="var(--wire-line)" stroke-width="2"/>
    <circle cx="130" cy="-70" r="4" fill="var(--title-color)"/>

    <!-- Schmitt Trigger Symbol Box -->
    <rect x="90" y="10" width="130" height="60" rx="6" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="155" y="32" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-green)">SCHMITT TRIGGER</text>
    <!-- Hysteresis symbol -->
    <path d="M 140 50 L 155 50 L 155 42 L 170 42" stroke="var(--accent-green)" stroke-width="2" fill="none"/>
    <text x="155" y="62" text-anchor="middle" font-size="9" fill="var(--text-muted)">Hysteresis ~200mV</text>

    <!-- Output from Schmitt Trigger back to IDR and Alternate Function Input -->
    <path d="M 90 40 L -145 40 L -145 15" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow-left)"/>
    <path d="M -145 40 L -145 95" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow-left)"/>
  </g>

  <!-- Protection Diodes & I/O Pin (Right Side) -->
  <g transform="translate(680, 95)">
    <!-- Main I/O Net Bus Line -->
    <line x1="-35" y1="275" x2="160" y2="275" stroke="var(--wire-line)" stroke-width="3"/>

    <!-- Protection Diode to VDD (D1) -->
    <line x1="60" y1="275" x2="60" y2="150" stroke="var(--wire-line)" stroke-width="2"/>
    <circle cx="60" cy="275" r="4" fill="var(--title-color)"/>
    
    <!-- Diode symbol pointing UP to VDD -->
    <polygon points="50,180 70,180 60,160" fill="var(--accent-red)" stroke="var(--accent-red)" stroke-width="1.5"/>
    <line x1="50" y1="160" x2="70" y2="160" stroke="var(--accent-red)" stroke-width="2"/>
    <line x1="60" y1="160" x2="60" y2="120" stroke="var(--vdd-color)" stroke-width="2"/>
    <polygon points="55,120 65,120 60,110" fill="var(--vdd-color)"/>
    <text x="60" y="100" text-anchor="middle" font-size="11" font-weight="800" fill="var(--vdd-color)">VDD (3.3V)</text>
    <text x="95" y="172" font-size="10" font-weight="700" fill="var(--text-muted)">D1 (ESD)</text>

    <!-- Protection Diode to VSS (D2) -->
    <line x1="60" y1="275" x2="60" y2="380" stroke="var(--wire-line)" stroke-width="2"/>
    <!-- Diode symbol pointing UP from VSS -->
    <polygon points="50,350 70,350 60,330" fill="var(--accent-green)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <line x1="50" y1="330" x2="70" y2="330" stroke="var(--accent-green)" stroke-width="2"/>
    <line x1="60" y1="350" x2="60" y2="400" stroke="var(--vss-color)" stroke-width="2"/>
    <!-- Ground symbol -->
    <line x1="45" y1="400" x2="75" y2="400" stroke="var(--vss-color)" stroke-width="2"/>
    <line x1="50" y1="405" x2="70" y2="405" stroke="var(--vss-color)" stroke-width="1.5"/>
    <line x1="55" y1="410" x2="65" y2="410" stroke="var(--vss-color)" stroke-width="1"/>
    <text x="60" y="425" text-anchor="middle" font-size="10" font-weight="700" fill="var(--vss-color)">VSS (GND)</text>
    <text x="95" y="342" font-size="10" font-weight="700" fill="var(--text-muted)">D2 (ESD)</text>

    <!-- 5V-Tolerant (FT) Note -->
    <rect x="15" y="210" width="140" height="35" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-dasharray="3,3"/>
    <text x="85" y="225" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-amber)">Nếu là chân 5V-Tolerant (FT):</text>
    <text x="85" y="238" text-anchor="middle" font-size="8" fill="var(--text-muted)">Không có D1 nối VDD 3.3V</text>

    <!-- Physical I/O PAD (External Pin) -->
    <g transform="translate(160, 240)">
      <rect width="140" height="70" rx="8" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
      <text x="70" y="30" text-anchor="middle" font-size="16" font-weight="900" fill="#ffffff">I/O PIN (PAD)</text>
      <text x="70" y="50" text-anchor="middle" font-size="11" font-weight="600" fill="#e0f2fe">Chân vật lý bên ngoài</text>
      <text x="70" y="62" text-anchor="middle" font-size="9" fill="#bae6fd">(PA0..PA15, PB0..PB15...)</text>
    </g>
  </g>

  <!-- Connect Driver to Main Net -->
  <path d="M 645 275 L 645 275" stroke="var(--wire-line)" stroke-width="2"/>

  <!-- Markers -->
  <defs>
    <marker id="arrow-down" viewBox="0 0 10 10" refX="5" refY="6" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 5 8 L 10 0 z" fill="var(--bus-line)"/>
    </marker>
    <marker id="arrow-left" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 8 0 L 0 5 L 8 10 z" fill="var(--wire-line)"/>
    </marker>
  </defs>
</svg>"""

save_svg("bai02_gpio_structure.svg", svg_gpio_rm0008)

# ==============================================================================
# 2. BÀI 03: CLOCK TREE (ST RM0008 Figure 8: Clock tree)
# ==============================================================================
svg_clock_tree_rm0008 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 680" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="1100" height="680" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Header -->
  <rect x="20" y="16" width="1060" height="60" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="40" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 6.2</text>
  <text x="40" y="62" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 8: Clock tree (Sơ đồ cây xung nhịp và phân phối tần số STM32F103)</text>
  <rect x="930" y="28" width="130" height="34" rx="6" fill="#00205b"/>
  <text x="995" y="50" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left: Clock Sources -->
  <g transform="translate(30, 95)">
    <rect width="210" height="555" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="105" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">CLOCK SOURCES</text>
    <text x="105" y="44" text-anchor="middle" font-size="11" fill="var(--text-muted)">(Nguồn dao động)</text>

    <!-- HSE External 8MHz Crystal -->
    <g transform="translate(15, 60)">
      <rect width="180" height="70" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="90" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-blue)">HSE OSCILLATOR</text>
      <text x="90" y="42" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Thạch anh 4 - 16MHz</text>
      <text x="90" y="58" text-anchor="middle" font-size="10" fill="var(--text-muted)">(Blue Pill: 8.000MHz)</text>
    </g>

    <!-- HSI Internal 8MHz RC -->
    <g transform="translate(15, 145)">
      <rect width="180" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
      <text x="90" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-green)">HSI RC OSCILLATOR</text>
      <text x="90" y="42" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Xung nội 8MHz</text>
      <text x="90" y="56" text-anchor="middle" font-size="10" fill="var(--text-muted)">(Khởi động mặc định)</text>
    </g>

    <!-- LSI Internal 40kHz RC -->
    <g transform="translate(15, 225)">
      <rect width="180" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="90" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-amber)">LSI RC OSCILLATOR</text>
      <text x="90" y="42" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Xung thấp nội ~40kHz</text>
      <text x="90" y="56" text-anchor="middle" font-size="10" fill="var(--text-muted)">(Cấp riêng cho IWDG)</text>
    </g>

    <!-- LSE External 32.768kHz Crystal -->
    <g transform="translate(15, 305)">
      <rect width="180" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="90" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-purple)">LSE OSCILLATOR</text>
      <text x="90" y="42" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Thạch anh 32.768kHz</text>
      <text x="90" y="56" text-anchor="middle" font-size="10" fill="var(--text-muted)">(Cấp cho khối RTC)</text>
    </g>

    <!-- MCO Pin output -->
    <g transform="translate(15, 420)">
      <rect width="180" height="100" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="90" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">MCO Pin (PA8)</text>
      <text x="90" y="46" text-anchor="middle" font-size="10" fill="var(--text-muted)">Microcontroller Clock Out</text>
      <text x="90" y="66" text-anchor="middle" font-size="10" fill="var(--accent-blue)">Xuất SYSCLK, HSI, HSE</text>
      <text x="90" y="82" text-anchor="middle" font-size="9" fill="var(--text-muted)">Đo kiểm tần số thực tế</text>
    </g>
  </g>

  <!-- Center Section: PLL Multiplier & SW MUX -->
  <g transform="translate(270, 95)">
    <!-- PLL Block -->
    <rect x="0" y="60" width="220" height="150" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="110" y="30" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-blue)">PHASE-LOCKED LOOP (PLL)</text>
    
    <rect x="15" y="45" width="190" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="110" y="68" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">PLL Source MUX (HSE / HSI/2)</text>

    <rect x="15" y="95" width="190" height="45" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="110" y="116" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-blue)">PLLMUL: ×2 → ×16</text>
    <text x="110" y="132" text-anchor="middle" font-size="10" fill="var(--text-muted)">8MHz × 9 = 72MHz</text>

    <!-- System Clock Switch (SW MUX) -->
    <rect x="0" y="250" width="220" height="130" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="110" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-green)">SYSCLK SELECTOR (SW)</text>
    
    <text x="25" y="55" font-size="11" font-weight="600" fill="var(--text-primary)">SW = 00: HSI (8MHz)</text>
    <text x="25" y="78" font-size="11" font-weight="600" fill="var(--text-primary)">SW = 01: HSE (8MHz)</text>
    <text x="25" y="101" font-size="11" font-weight="800" fill="var(--accent-blue)">SW = 10: PLLCLK (72MHz)</text>

    <text x="110" y="122" text-anchor="middle" font-size="9" fill="var(--text-muted)">Cờ báo chuyển đổi: SWS[1:0]</text>
  </g>

  <!-- Right Section: Prescalers & Peripheral Domains (AHB, APB1, APB2) -->
  <g transform="translate(520, 95)">
    <!-- AHB Prescaler -->
    <rect x="0" y="60" width="530" height="90" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="20" y="28" font-size="13" font-weight="800" fill="var(--accent-blue)">AHB PRESCALER (/1, /2 ... /512) → HCLK = 72MHz Tối Đa</text>
    <text x="20" y="48" font-size="11" fill="var(--text-muted)">Cấp xung cho lõi ARM Cortex-M3, Bộ điều khiển DMA1/DMA2, SRAM và Flash Memory</text>
    
    <g transform="translate(20, 55)">
      <rect width="150" height="25" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="75" y="17" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">SysTick Timer (HCLK/8)</text>

      <rect x="160" width="150" height="25" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="235" y="17" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">Flash Access 2 Wait States</text>

      <rect x="320" width="170" height="25" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="405" y="17" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">FCLK Cortex Free Running</text>
    </g>

    <!-- APB2 Prescaler (High Speed Domain) -->
    <rect x="0" y="175" width="530" height="145" rx="8" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="20" y="28" font-size="13" font-weight="800" fill="var(--accent-purple)">APB2 PRESCALER (/1, /2, /4...) → PCLK2 = 72MHz Tối Đa</text>
    <text x="20" y="48" font-size="11" fill="var(--text-muted)">Miền ngoại vi tốc độ cao: GPIOA..GPIOG, ADC1, ADC2, TIM1, USART1, SPI1</text>

    <!-- ADC Prescaler inside APB2 -->
    <g transform="translate(20, 60)">
      <rect width="490" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="20" y="25" font-size="11" font-weight="800" fill="var(--accent-amber)">ADC PRESCALER (/2, /4, /6, /8):</text>
      <text x="190" y="25" font-size="11" font-weight="700" fill="var(--title-color)">ADCCLK = 72MHz / 6 = 12MHz (Giới hạn tối đa 14MHz!)</text>
    </g>

    <text x="20" y="125" font-size="10" fill="var(--text-muted)">TIM1 Multiplier: Nếu APB2 prescaler = 1 → TIM1CLK = 72MHz</text>

    <!-- APB1 Prescaler (Low Speed Domain) -->
    <rect x="0" y="345" width="530" height="140" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="20" y="28" font-size="13" font-weight="800" fill="var(--accent-green)">APB1 PRESCALER (/2) → PCLK1 = 36MHz Tối Đa (BẮT BUỘC CHIA 2!)</text>
    <text x="20" y="48" font-size="11" fill="var(--text-muted)">Miền ngoại vi tốc độ thấp: TIM2, TIM3, TIM4, USART2, USART3, SPI2, I2C1, I2C2, CAN, WWDG</text>

    <!-- Timer Multiplier Logic -->
    <g transform="translate(20, 60)">
      <rect width="490" height="35" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
      <text x="20" y="22" font-size="11" font-weight="700" fill="var(--accent-green)">Timer Multiplier ×2:</text>
      <text x="140" y="22" font-size="11" font-weight="600" fill="var(--title-color)">Khi APB1 chia 2 (PCLK1=36MHz) → TIMx_CLK tự động nhân 2 = 72MHz!</text>
    </g>

    <text x="20" y="120" font-size="10" fill="var(--text-muted)">USB Prescaler: PLLCLK 72MHz / 1.5 = 48MHz (Chuẩn tốc độ USB 2.0 Full Speed 12Mbps)</text>
  </g>

  <!-- Connecting Bus Arrows -->
  <path d="M 220 200 L 270 200" stroke="var(--bus-line)" stroke-width="2.5"/>
  <path d="M 490 200 L 520 200" stroke="var(--bus-line)" stroke-width="2.5"/>
  <path d="M 490 105 L 520 105" stroke="var(--bus-line)" stroke-width="2.5"/>
  <path d="M 505 105 L 505 400 L 520 400" stroke="var(--bus-line)" stroke-width="2.5"/>
</svg>"""

save_svg("bai03_clock_tree.svg", svg_clock_tree_rm0008)

print("SUCCESS: ALL CORE RM0008 SCHEMATICS BUILT!")
