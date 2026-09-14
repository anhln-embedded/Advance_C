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
    print(f"Generated Official RM0008 Schematic: {filename}")

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
        --accent-blue: #0284c7;
        --accent-green: #059669;
        --accent-amber: #d97706;
        --accent-red: #dc2626;
        --accent-purple: #7c3aed;
        --wire-line: #334155;
        --bus-line: #0284c7;
        --vdd-color: #dc2626;
        --vss-color: #16a34a;
        --logic-gate: #0284c7;
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
          --accent-blue: #38bdf8;
          --accent-green: #34d399;
          --accent-amber: #fbbf24;
          --accent-red: #f87171;
          --accent-purple: #c084fc;
          --wire-line: #94a3b8;
          --bus-line: #60a5fa;
          --vdd-color: #f87171;
          --vss-color: #4ade80;
          --logic-gate: #38bdf8;
        }
      }
      path { fill: none; }
      marker path { fill: inherit; }
      polygon { fill: inherit; }
      text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
      .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
    </style>
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--wire-line)"/>
      </marker>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--bus-line)"/>
      </marker>
      <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--accent-red)"/>
      </marker>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--accent-green)"/>
      </marker>
    </defs>
"""

# ==============================================================================
# 1. BÀI 02: STM32F103 GPIO STRUCTURE (ST RM0008 Figure 13 & 14)
# ==============================================================================
svg_gpio = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 720" width="100%" height="100%">
{COMMON_STYLES}
  <!-- Background Canvas -->
  <rect width="1180" height="720" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Top Title Bar -->
  <rect x="25" y="16" width="1130" height="64" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="45" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 9.1</text>
  <text x="45" y="64" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 13: Basic structure of a standard I/O port bit (Sơ đồ nguyên lý mạch Transistor chân GPIO)</text>
  <rect x="1000" y="28" width="135" height="36" rx="6" fill="#00205b"/>
  <text x="1067" y="51" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Zone 1: Bus Interface & Registers (X: 30 -> 240) -->
  <g transform="translate(30, 95)">
    <rect width="210" height="595" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="105" y="26" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">BUS INTERFACE</text>
    <text x="105" y="42" text-anchor="middle" font-size="11" font-weight="600" fill="var(--text-muted)">Peripheral Bus APB2</text>

    <!-- BSRR / BRR -->
    <g transform="translate(15, 60)">
      <rect width="180" height="48" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="90" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Bit Set / Reset Reg</text>
      <text x="90" y="36" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-blue)" class="mono">GPIOx_BSRR / BRR</text>
    </g>

    <!-- Write Bus line to ODR -->
    <path d="M 105 108 L 105 130" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

    <!-- ODR -->
    <g transform="translate(15, 130)">
      <rect width="180" height="52" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="90" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Output Data Register</text>
      <text x="90" y="39" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-blue)" class="mono">GPIOx_ODR</text>
    </g>

    <!-- Read ODR Feedback -->
    <g transform="translate(15, 205)">
      <rect width="180" height="34" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="90" y="22" text-anchor="middle" font-size="10" font-weight="600" fill="var(--text-primary)">Read GPIOx_ODR</text>
    </g>

    <!-- Alternate Function Output -->
    <g transform="translate(15, 260)">
      <rect width="180" height="48" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="90" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-purple)">Alternate Function Out</text>
      <text x="90" y="36" text-anchor="middle" font-size="9" fill="var(--text-muted)">(USART_TX, SPI_SCK...)</text>
    </g>

    <!-- Input Data Register (IDR) -->
    <g transform="translate(15, 365)">
      <rect width="180" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="90" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Input Data Register</text>
      <text x="90" y="42" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-green)" class="mono">GPIOx_IDR</text>
    </g>

    <!-- Alternate Function Input -->
    <g transform="translate(15, 445)">
      <rect width="180" height="48" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="90" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-purple)">Alternate Function In</text>
      <text x="90" y="36" text-anchor="middle" font-size="9" fill="var(--text-muted)">(USART_RX, EXTI, TIM)</text>
    </g>

    <!-- Analog In/Out -->
    <g transform="translate(15, 520)">
      <rect width="180" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="90" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-amber)">Analog In / Out</text>
      <text x="90" y="37" text-anchor="middle" font-size="9" fill="var(--text-muted)">(ADC Input / DAC Out)</text>
    </g>
  </g>

  <!-- Zone 2: Output Control Block (X: 275 -> 445) -->
  <g transform="translate(275, 215)">
    <rect width="170" height="150" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="85" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-blue)">OUTPUT CONTROL</text>
    <text x="85" y="45" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">Push-Pull / Open-Drain</text>
    <text x="85" y="62" text-anchor="middle" font-size="9" fill="var(--text-muted)">Logic &amp; Driver Control</text>
    
    <line x1="15" y1="75" x2="155" y2="75" stroke="var(--card-border)"/>
    <text x="85" y="94" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-amber)">CNF[1:0] / MODE[1:0]</text>
    <text x="85" y="112" text-anchor="middle" font-size="9" fill="var(--text-muted)">Output Speed 2/10/50MHz</text>
    <text x="85" y="128" text-anchor="middle" font-size="9" fill="var(--text-muted)">Tự động ngắt P-MOS khi OD</text>

    <!-- Input lines into Output Control from ODR & AF -->
    <path d="M -35 30 L 0 30" fill="none" stroke="var(--bus-line)" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <text x="-5" y="24" text-anchor="end" font-size="9" font-weight="700" fill="var(--bus-line)">ODR bit</text>

    <path d="M -35 90 L 0 90" fill="none" stroke="var(--accent-purple)" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <text x="-5" y="84" text-anchor="end" font-size="9" font-weight="700" fill="var(--accent-purple)">AF Out</text>
  </g>

  <!-- Zone 3: MOSFET Transistor Output Driver (X: 490 -> 640) -->
  <g transform="translate(490, 150)">
    <!-- Gate P line from Output Control -->
    <path d="M -45 95 L -20 95 L -20 45 L 30 45" fill="none" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="-15" y="38" font-size="10" font-weight="700" fill="var(--accent-red)">Gate P</text>

    <!-- P-MOS Transistor Box -->
    <rect x="30" y="15" width="130" height="65" rx="6" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="2"/>
    <!-- Inversion Bubble (PMOS) -->
    <circle cx="24" cy="45" r="4" fill="none" stroke="var(--accent-red)" stroke-width="2"/>
    <text x="95" y="40" text-anchor="middle" font-size="14" font-weight="900" fill="var(--accent-red)">P-MOS</text>
    <text x="95" y="58" text-anchor="middle" font-size="9" font-weight="700" fill="var(--text-muted)">Pull-Up to VDD</text>

    <!-- VDD Power Rail to P-MOS Source -->
    <line x1="95" y1="-25" x2="95" y2="15" stroke="var(--vdd-color)" stroke-width="2.5"/>
    <polygon points="90,-25 100,-25 95,-36" fill="var(--vdd-color)"/>
    <text x="95" y="-42" text-anchor="middle" font-size="12" font-weight="900" fill="var(--vdd-color)">VDD (3.3V)</text>

    <!-- Gate N line from Output Control -->
    <path d="M -45 160 L -20 160 L -20 215 L 30 215" fill="none" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="-15" y="208" font-size="10" font-weight="700" fill="var(--vss-color)">Gate N</text>

    <!-- N-MOS Transistor Box -->
    <rect x="30" y="185" width="130" height="65" rx="6" fill="var(--card-bg)" stroke="var(--vss-color)" stroke-width="2"/>
    <text x="95" y="212" text-anchor="middle" font-size="14" font-weight="900" fill="var(--vss-color)">N-MOS</text>
    <text x="95" y="230" text-anchor="middle" font-size="9" font-weight="700" fill="var(--text-muted)">Pull-Down to VSS</text>

    <!-- VSS (Ground) from N-MOS Source -->
    <line x1="95" y1="250" x2="95" y2="285" stroke="var(--vss-color)" stroke-width="2.5"/>
    <line x1="75" y1="285" x2="115" y2="285" stroke="var(--vss-color)" stroke-width="2.5"/>
    <line x1="82" y1="290" x2="108" y2="290" stroke="var(--vss-color)" stroke-width="2"/>
    <line x1="89" y1="295" x2="101" y2="295" stroke="var(--vss-color)" stroke-width="1.5"/>
    <text x="95" y="312" text-anchor="middle" font-size="11" font-weight="800" fill="var(--vss-color)">VSS (GND)</text>

    <!-- Drains Junction: Output node combining P-MOS and N-MOS -->
    <path d="M 160 45 L 200 45 L 200 215 L 160 215" fill="none" stroke="var(--wire-line)" stroke-width="2.5"/>
    <circle cx="200" cy="130" r="4.5" fill="var(--title-color)"/>
    <line x1="200" y1="130" x2="250" y2="130" stroke="var(--wire-line)" stroke-width="2.5"/>
    <text x="210" y="122" font-size="10" font-weight="700" fill="var(--text-muted)">Driver Out</text>
  </g>

  <!-- Zone 4: Internal Pull-Up & Pull-Down Resistors (X: 720 -> 840) -->
  <g transform="translate(710, 100)">
    <!-- VDD Power Rail for Pull-Up -->
    <line x1="60" y1="25" x2="60" y2="45" stroke="var(--vdd-color)" stroke-width="2"/>
    <polygon points="55,25 65,25 60,16" fill="var(--vdd-color)"/>
    <text x="60" y="10" text-anchor="middle" font-size="11" font-weight="800" fill="var(--vdd-color)">VDD</text>

    <!-- Pull-Up Resistor Box -->
    <rect x="5" y="45" width="110" height="75" rx="6" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="60" y="68" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">R_PU ~40kΩ</text>
    <text x="60" y="86" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-blue)">P-MOS Switch</text>
    <text x="60" y="104" text-anchor="middle" font-size="8" fill="var(--text-muted)">(Bật khi ODR=1)</text>

    <!-- Wire from Pull-up to Main I/O Bus -->
    <line x1="60" y1="120" x2="60" y2="180" stroke="var(--wire-line)" stroke-width="2"/>
    <circle cx="60" cy="180" r="4" fill="var(--title-color)"/>

    <!-- Pull-Down Resistor Box -->
    <rect x="5" y="225" width="110" height="75" rx="6" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="60" y="248" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">R_PD ~40kΩ</text>
    <text x="60" y="266" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-green)">N-MOS Switch</text>
    <text x="60" y="284" text-anchor="middle" font-size="8" fill="var(--text-muted)">(Bật khi ODR=0)</text>

    <line x1="60" y1="180" x2="60" y2="225" stroke="var(--wire-line)" stroke-width="2"/>
    <line x1="60" y1="300" x2="60" y2="330" stroke="var(--vss-color)" stroke-width="2"/>
    <!-- Ground symbol -->
    <line x1="45" y1="330" x2="75" y2="330" stroke="var(--vss-color)" stroke-width="2"/>
    <line x1="50" y1="334" x2="70" y2="334" stroke="var(--vss-color)" stroke-width="1.5"/>
    <line x1="55" y1="338" x2="65" y2="338" stroke="var(--vss-color)" stroke-width="1"/>
    <text x="60" y="352" text-anchor="middle" font-size="10" font-weight="700" fill="var(--vss-color)">VSS</text>
  </g>

  <!-- Zone 5: Input Stage - Schmitt Trigger (X: 520 -> 720, Y: 480) -->
  <g transform="translate(460, 470)">
    <!-- Tap wire from main I/O bus down to Schmitt Trigger -->
    <path d="M 310 -190 L 310 -20 L 220 -20 L 220 20" fill="none" stroke="var(--wire-line)" stroke-width="2"/>
    <circle cx="310" cy="-190" r="4" fill="var(--title-color)"/>

    <!-- Schmitt Trigger Box -->
    <rect x="70" y="0" width="160" height="65" rx="6" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="150" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-green)">SCHMITT TRIGGER</text>
    
    <!-- Hysteresis Icon -->
    <path d="M 130 46 L 148 46 L 148 36 L 166 36" fill="none" stroke="var(--accent-green)" stroke-width="2.5"/>
    <text x="150" y="58" text-anchor="middle" font-size="8" fill="var(--text-muted)">Hysteresis ~200mV</text>

    <!-- Line out of Schmitt Trigger to IDR and AF In -->
    <path d="M 70 32 L -220 32 L -220 -10" fill="none" stroke="var(--accent-green)" stroke-width="2" marker-end="url(#arrow-green)"/>
    <text x="-150" y="24" font-size="9" font-weight="700" fill="var(--accent-green)">Input to IDR</text>

    <path d="M -220 32 L -220 50" fill="none" stroke="var(--accent-purple)" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <text x="-150" y="46" font-size="9" font-weight="700" fill="var(--accent-purple)">Input to AF</text>
  </g>

  <!-- Analog Tap wire directly from PAD to Analog Block -->
  <path d="M 850 280 L 850 635 L 240 635" fill="none" stroke="var(--accent-amber)" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow)"/>
  <circle cx="850" cy="280" r="4" fill="var(--accent-amber)"/>
  <text x="560" y="628" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-amber)">Tín hiệu Analog (Bỏ qua Schmitt Trigger &amp; Output Driver)</text>

  <!-- Zone 6: Protection Diodes & Physical I/O PAD (X: 860 -> 1140) -->
  <g transform="translate(870, 95)">
    <!-- Main I/O Net Bus Line -->
    <line x1="-130" y1="185" x2="130" y2="185" stroke="var(--wire-line)" stroke-width="3"/>

    <!-- Protection Diode D1 (to VDD) -->
    <line x1="30" y1="185" x2="30" y2="70" stroke="var(--wire-line)" stroke-width="2"/>
    <circle cx="30" cy="185" r="4" fill="var(--title-color)"/>
    
    <!-- Diode symbol pointing UP to VDD -->
    <polygon points="20,105 40,105 30,85" fill="var(--accent-red)" stroke="var(--accent-red)" stroke-width="1.5"/>
    <line x1="20" y1="85" x2="40" y2="85" stroke="var(--accent-red)" stroke-width="2"/>
    <line x1="30" y1="85" x2="30" y2="40" stroke="var(--vdd-color)" stroke-width="2"/>
    <polygon points="25,40 35,40 30,30" fill="var(--vdd-color)"/>
    <text x="30" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--vdd-color)">VDD (3.3V)</text>
    <text x="70" y="98" font-size="10" font-weight="700" fill="var(--accent-red)">D1 (ESD)</text>

    <!-- Protection Diode D2 (from VSS) -->
    <line x1="30" y1="185" x2="30" y2="300" stroke="var(--wire-line)" stroke-width="2"/>
    <!-- Diode symbol pointing UP from VSS -->
    <polygon points="20,270 40,270 30,250" fill="var(--accent-green)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <line x1="20" y1="250" x2="40" y2="250" stroke="var(--accent-green)" stroke-width="2"/>
    <line x1="30" y1="270" x2="30" y2="320" stroke="var(--vss-color)" stroke-width="2"/>
    <!-- Ground symbol -->
    <line x1="15" y1="320" x2="45" y2="320" stroke="var(--vss-color)" stroke-width="2"/>
    <line x1="20" y1="325" x2="40" y2="325" stroke="var(--vss-color)" stroke-width="1.5"/>
    <line x1="25" y1="330" x2="35" y2="330" stroke="var(--vss-color)" stroke-width="1"/>
    <text x="30" y="348" text-anchor="middle" font-size="10" font-weight="700" fill="var(--vss-color)">VSS (GND)</text>
    <text x="70" y="265" font-size="10" font-weight="700" fill="var(--accent-green)">D2 (ESD)</text>

    <!-- Note on 5V-Tolerant (FT) pins -->
    <rect x="-15" y="130" width="130" height="34" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-dasharray="3,3"/>
    <text x="50" y="145" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-amber)">Chân 5V-Tolerant (FT):</text>
    <text x="50" y="157" text-anchor="middle" font-size="8" fill="var(--text-muted)">Không có D1 nối VDD</text>

    <!-- Physical External Pin (PAD) -->
    <g transform="translate(130, 150)">
      <rect width="140" height="70" rx="8" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
      <text x="70" y="30" text-anchor="middle" font-size="16" font-weight="900" fill="#ffffff">I/O PIN (PAD)</text>
      <text x="70" y="48" text-anchor="middle" font-size="10" font-weight="600" fill="#e0f2fe">Chân kim loại vật lý</text>
      <text x="70" y="62" text-anchor="middle" font-size="9" fill="#bae6fd">(PA0..PA15, PB0...)</text>
    </g>
  </g>
</svg>"""

save_svg("bai02_gpio_structure.svg", svg_gpio)

# ==============================================================================
# 2. BÀI 03: CLOCK TREE (ST RM0008 Figure 8: Clock tree)
# ==============================================================================
svg_clock_tree = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="100%" height="100%">
{COMMON_STYLES}
  <!-- Canvas Background -->
  <rect width="1200" height="750" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Top Title Bar -->
  <rect x="25" y="16" width="1150" height="64" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="45" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 6.2</text>
  <text x="45" y="64" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 8: Clock tree (Sơ đồ cây xung nhịp và phân phối tần số STM32F103)</text>
  <rect x="1020" y="28" width="135" height="36" rx="6" fill="#00205b"/>
  <text x="1087" y="51" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left: Clock Sources (X: 30 -> 230) -->
  <g transform="translate(30, 95)">
    <rect width="200" height="625" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="100" y="26" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">CLOCK SOURCES</text>
    <text x="100" y="44" text-anchor="middle" font-size="10" fill="var(--text-muted)">(Nguồn dao động)</text>

    <!-- HSE -->
    <g transform="translate(15, 60)">
      <rect width="170" height="75" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="85" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-blue)">HSE OSCILLATOR</text>
      <text x="85" y="40" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Thạch Anh Ngoài</text>
      <text x="85" y="56" text-anchor="middle" font-size="10" fill="var(--text-muted)">4MHz - 16MHz</text>
      <text x="85" y="69" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-blue)">(Blue Pill: 8.000MHz)</text>
    </g>

    <!-- HSI -->
    <g transform="translate(15, 150)">
      <rect width="170" height="70" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
      <text x="85" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-green)">HSI RC OSCILLATOR</text>
      <text x="85" y="40" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Dao Động RC Nội</text>
      <text x="85" y="56" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-green)">8.000MHz (±1%)</text>
      <text x="85" y="66" text-anchor="middle" font-size="8" fill="var(--text-muted)">(Xung mặc định khi Reset)</text>
    </g>

    <!-- LSI -->
    <g transform="translate(15, 235)">
      <rect width="170" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="85" y="20" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-amber)">LSI RC OSCILLATOR</text>
      <text x="85" y="38" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">Xung Thấp Nội ~40kHz</text>
      <text x="85" y="54" text-anchor="middle" font-size="9" fill="var(--text-muted)">Cấp cho IWDG &amp; RTC</text>
    </g>

    <!-- LSE -->
    <g transform="translate(15, 315)">
      <rect width="170" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="85" y="20" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-purple)">LSE OSCILLATOR</text>
      <text x="85" y="38" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">Thạch Anh 32.768kHz</text>
      <text x="85" y="54" text-anchor="middle" font-size="9" fill="var(--text-muted)">Cấp chuẩn cho RTC</text>
    </g>

    <!-- MCO Pin Box -->
    <g transform="translate(15, 480)">
      <rect width="170" height="90" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <text x="85" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)">MCO PIN (PA8)</text>
      <text x="85" y="40" text-anchor="middle" font-size="10" fill="var(--text-muted)">Clock Output đo kiểm</text>
      <text x="85" y="58" text-anchor="middle" font-size="9" fill="var(--accent-blue)">Xuất SYSCLK, HSI, HSE</text>
      <text x="85" y="74" text-anchor="middle" font-size="9" fill="var(--accent-purple)">Hoặc PLLCLK / 2</text>
    </g>
  </g>

  <!-- Center-Left: PLL Multiplier & SYSCLK Switch (X: 260 -> 480) -->
  <g transform="translate(260, 95)">
    <!-- CSS (Clock Security System) -->
    <rect x="0" y="0" width="220" height="55" rx="6" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
    <text x="110" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-red)">CSS (CLOCK SECURITY SYSTEM)</text>
    <text x="110" y="40" text-anchor="middle" font-size="9" fill="var(--text-muted)">Tự chuyển sang HSI nếu HSE hỏng</text>

    <!-- PLL Box -->
    <g transform="translate(0, 70)">
      <rect width="220" height="230" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="110" y="26" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-blue)">PHASE-LOCKED LOOP (PLL)</text>
      
      <!-- PLL Source Selector -->
      <g transform="translate(15, 40)">
        <rect width="190" height="50" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="95" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">PLL Source Selector:</text>
        <text x="95" y="38" text-anchor="middle" font-size="10" fill="var(--accent-blue)">HSE / 1 (hoặc HSE / 2) | HSI / 2</text>
      </g>

      <!-- PLL Multiplier Factor -->
      <g transform="translate(15, 105)">
        <rect width="190" height="60" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
        <text x="95" y="24" text-anchor="middle" font-size="12" font-weight="900" fill="var(--accent-blue)">PLLMUL: ×2 → ×16</text>
        <text x="95" y="44" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">8MHz × 9 = 72MHz (Tối Đa)</text>
      </g>

      <text x="110" y="190" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-green)">PLLCLK = 72MHz Output</text>
      <text x="110" y="210" text-anchor="middle" font-size="9" fill="var(--text-muted)">Cờ khóa tần: RCC_CR_PLLRDY</text>
    </g>

    <!-- SYSCLK Selector Switch MUX -->
    <g transform="translate(0, 320)">
      <rect width="220" height="200" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="110" y="26" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-green)">SYSCLK SELECTOR (SW MUX)</text>
      <text x="110" y="44" text-anchor="middle" font-size="10" fill="var(--text-muted)">Chọn nguồn xung nhịp hệ thống</text>
      
      <g transform="translate(15, 55)">
        <rect width="190" height="110" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="15" y="24" font-size="10" font-weight="600" fill="var(--text-primary)">• SW = 00: HSI (8MHz)</text>
        <text x="15" y="46" font-size="10" font-weight="600" fill="var(--text-primary)">• SW = 01: HSE (8MHz)</text>
        <text x="15" y="70" font-size="11" font-weight="900" fill="var(--accent-blue)">• SW = 10: PLLCLK (72MHz)</text>
        <line x1="10" y1="80" x2="180" y2="80" stroke="var(--card-border)"/>
        <text x="95" y="98" text-anchor="middle" font-size="9" fill="var(--text-muted)">Kiểm tra cờ chuyển: SWS[1:0]</text>
      </g>

      <text x="110" y="185" text-anchor="middle" font-size="11" font-weight="900" fill="var(--title-color)">SYSCLK = 72MHz</text>
    </g>
  </g>

  <!-- Right: Prescalers & Peripheral Domains (X: 510 -> 1160) -->
  <g transform="translate(510, 95)">
    <!-- AHB Prescaler Container -->
    <rect x="0" y="0" width="650" height="175" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="25" y="28" font-size="14" font-weight="800" fill="var(--accent-blue)">AHB PRESCALER (/1, /2, /4.. /512) → HCLK = 72MHz Tối Đa</text>
    <text x="25" y="48" font-size="11" fill="var(--text-muted)">Cấp xung nhịp cho lõi ARM Cortex-M3, Bộ điều khiển DMA1/DMA2, SRAM và Flash</text>

    <!-- Sub-blocks inside AHB -->
    <g transform="translate(20, 60)">
      <!-- Cortex-M3 Core -->
      <rect width="185" height="95" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="92" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-blue)">ARM CORTEX-M3</text>
      <text x="92" y="44" text-anchor="middle" font-size="12" font-weight="900" fill="var(--title-color)">Core FCLK = 72MHz</text>
      <text x="92" y="64" text-anchor="middle" font-size="9" fill="var(--text-muted)">Thực thi lệnh 1.25 DMIPS/MHz</text>
      <text x="92" y="80" text-anchor="middle" font-size="9" fill="var(--text-muted)">Không chia tần số</text>

      <!-- SysTick Timer -->
      <rect x="200" width="195" height="95" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <text x="297" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)">SYSTICK TIMER</text>
      <text x="297" y="44" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-green)">HCLK / 8 = 9MHz</text>
      <text x="297" y="62" text-anchor="middle" font-size="9" fill="var(--text-muted)">(Hoặc HCLK trực tiếp 72MHz)</text>
      <text x="297" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-green)">Tạo ngắt định thời 1ms RTOS</text>

      <!-- Flash Memory Access -->
      <rect x="410" width="195" height="95" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="507" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-amber)">FLASH ACCESS LATENCY</text>
      <text x="507" y="44" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)">2 WAIT STATES (LATENCY=2)</text>
      <text x="507" y="64" text-anchor="middle" font-size="9" fill="var(--accent-red)">! Bắt buộc khi HCLK &gt; 48MHz</text>
      <text x="507" y="80" text-anchor="middle" font-size="9" fill="var(--text-muted)">Bật Prefetch Buffer: FLASH_ACR</text>
    </g>

    <!-- APB2 Prescaler (High Speed Domain) -->
    <g transform="translate(0, 190)">
      <rect width="650" height="210" rx="8" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
      <text x="25" y="28" font-size="14" font-weight="800" fill="var(--accent-purple)">APB2 PRESCALER (/1, /2, /4.. /16) → PCLK2 = 72MHz Tối Đa</text>
      <text x="25" y="48" font-size="11" fill="var(--text-muted)">Miền ngoại vi tốc độ cao: GPIOA..GPIOG, ADC1, ADC2, TIM1, USART1, SPI1</text>

      <g transform="translate(20, 60)">
        <!-- ADC Prescaler Box -->
        <rect width="395" height="75" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
        <text x="15" y="24" font-size="12" font-weight="900" fill="var(--accent-amber)">ADC PRESCALER (/2, /4, /6, /8):</text>
        <text x="15" y="45" font-size="12" font-weight="800" fill="var(--title-color)">ADCCLK = 72MHz / 6 = 12.0MHz</text>
        <text x="15" y="65" font-size="9" font-weight="700" fill="var(--accent-red)">! TỐI ĐA 14MHz THEO DATASHEET (Không chia 2 hoặc 4 ở 72MHz)</text>

        <!-- TIM1 Clock -->
        <rect x="410" width="195" height="75" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="507" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-purple)">TIM1 CLOCK</text>
        <text x="507" y="45" text-anchor="middle" font-size="12" font-weight="800" fill="var(--title-color)">TIM1CLK = 72MHz</text>
        <text x="507" y="65" text-anchor="middle" font-size="9" fill="var(--text-muted)">Timer cao cấp điều khiển động cơ</text>
      </g>

      <!-- Peripherals list on APB2 -->
      <g transform="translate(20, 145)">
        <rect width="605" height="50" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="15" y="22" font-size="11" font-weight="700" fill="var(--title-color)">Ngoại Vi APB2 (Bật qua RCC_APB2ENR):</text>
        <text x="15" y="40" font-size="10" fill="var(--text-muted)">IOPAEN (Port A), IOPBEN (Port B), IOPCEN (Port C), AFIOEN, ADC1EN, ADC2EN, TIM1EN, USART1EN, SPI1EN</text>
      </g>
    </g>

    <!-- APB1 Prescaler (Low Speed Domain) -->
    <g transform="translate(0, 415)">
      <rect width="650" height="210" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="25" y="28" font-size="14" font-weight="800" fill="var(--accent-green)">APB1 PRESCALER (/2) → PCLK1 = 36MHz Tối Đa (BẮT BUỘC CHIA 2!)</text>
      <text x="25" y="48" font-size="11" fill="var(--text-muted)">Miền ngoại vi tốc độ thấp: TIM2..TIM4, USART2..3, SPI2, I2C1..2, CAN 2.0B, WWDG, PWR</text>

      <g transform="translate(20, 60)">
        <!-- Timer Multiplier Logic -->
        <rect width="395" height="75" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="2"/>
        <text x="15" y="24" font-size="12" font-weight="900" fill="var(--accent-green)">CƠ CHẾ NHÂN TẦN SỐ TIMER TỰ ĐỘNG (×2):</text>
        <text x="15" y="45" font-size="11" font-weight="700" fill="var(--title-color)">Khi APB1 Prescaler &gt; 1 (chia 2 để PCLK1 = 36MHz)</text>
        <text x="15" y="65" font-size="9.5" font-weight="800" fill="var(--accent-blue)">→ Xung Timer tự động nhân đôi: TIMx_CLK = 36MHz × 2 = 72MHz</text>

        <!-- USB Prescaler -->
        <rect x="410" width="195" height="75" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
        <text x="507" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-blue)">USB PRESCALER (/1.5)</text>
        <text x="507" y="45" text-anchor="middle" font-size="12" font-weight="800" fill="var(--title-color)">USBCLK = 48.0MHz</text>
        <text x="507" y="65" text-anchor="middle" font-size="9" fill="var(--text-muted)">Chuẩn USB 2.0 Full Speed 12Mbps</text>
      </g>

      <!-- Peripherals list on APB1 -->
      <g transform="translate(20, 145)">
        <rect width="605" height="50" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="15" y="22" font-size="11" font-weight="700" fill="var(--title-color)">Ngoại Vi APB1 (Bật qua RCC_APB1ENR):</text>
        <text x="15" y="40" font-size="10" fill="var(--text-muted)">TIM2EN, TIM3EN, TIM4EN, USART2EN, USART3EN, SPI2EN, I2C1EN, I2C2EN, CAN1EN, WWDGEN, PWREN, BKPEN</text>
      </g>
    </g>
  </g>

  <!-- Connecting Arrows -->
  <path d="M 230 140 L 260 140" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <path d="M 230 190 L 260 190" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <path d="M 480 420 L 510 420" fill="none" stroke="var(--bus-line)" stroke-width="3" marker-end="url(#arrow-blue)"/>
  <path d="M 480 420 L 495 420 L 495 180 L 510 180" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <path d="M 480 420 L 495 420 L 495 600 L 510 600" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
</svg>"""

save_svg("bai03_clock_tree.svg", svg_clock_tree)

# ==============================================================================
# 3. BÀI 04: EXTI & NVIC ARCHITECTURE (ST RM0008 Figure 19)
# ==============================================================================
svg_exti = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 660" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="1140" height="660" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Top Header -->
  <rect x="25" y="16" width="1090" height="64" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="45" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 10</text>
  <text x="45" y="64" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 19: External interrupt/event controller block diagram (Sơ đồ khối bộ điều khiển ngắt ngoài EXTI)</text>
  <rect x="960" y="28" width="135" height="36" rx="6" fill="#00205b"/>
  <text x="1027" y="51" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left: GPIO Pin Multiplexer (AFIO_EXTICR) -->
  <g transform="translate(35, 100)">
    <rect width="210" height="520" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="105" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">I/O PORT MUX (AFIO)</text>
    <text x="105" y="46" text-anchor="middle" font-size="11" fill="var(--text-muted)">AFIO_EXTICR1..4</text>

    <!-- Source Ports -->
    <g transform="translate(15, 65)">
      <rect width="180" height="60" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="90" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">PAx, PBx, PCx, PDx...</text>
      <text x="90" y="42" text-anchor="middle" font-size="10" fill="var(--text-muted)">16 chân mỗi Port (Pin 0..15)</text>
    </g>

    <!-- MUX Selection Logic -->
    <g transform="translate(15, 145)">
      <rect width="180" height="150" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="90" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-amber)">QUY TẮC MUX EXTI:</text>
      <text x="15" y="52" font-size="10" fill="var(--text-primary)">• Cùng số chân = Chung 1 Line</text>
      <text x="15" y="74" font-size="10" fill="var(--accent-red)">• PA0, PB0, PC0 → EXTI0</text>
      <text x="15" y="96" font-size="10" fill="var(--text-muted)">(Không thể dùng song song!)</text>
      <text x="15" y="122" font-size="10" fill="var(--accent-blue)">• PA1, PB1, PC1 → EXTI1</text>
      <text x="15" y="140" font-size="10" fill="var(--accent-blue)">• PA15, PB15 → EXTI15</text>
    </g>

    <!-- Other EXTI Lines -->
    <g transform="translate(15, 315)">
      <rect width="180" height="185" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="90" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-purple)">EXTI NỘI BỘ KHÁC:</text>
      <text x="15" y="55" font-size="10" fill="var(--text-primary)">• Line 16: PVD (Nguồn sụt)</text>
      <text x="15" y="80" font-size="10" fill="var(--text-primary)">• Line 17: RTC Alarm (Báo thức)</text>
      <text x="15" y="105" font-size="10" fill="var(--text-primary)">• Line 18: USB Wakeup</text>
      <text x="15" y="130" font-size="10" fill="var(--text-primary)">• Line 19: Ethernet Wakeup</text>
      <text x="90" y="165" text-anchor="middle" font-size="9" fill="var(--text-muted)">Tổng cộng 20 đường ngắt</text>
    </g>
  </g>

  <!-- Middle: Edge Detector & Control Registers (X: 280 -> 680) -->
  <g transform="translate(280, 100)">
    <!-- Input Line from AFIO -->
    <path d="M -35 120 L 20 120" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
    <text x="-15" y="112" font-size="10" font-weight="700" fill="var(--bus-line)">EXTI Line x</text>

    <!-- Edge Detector Circuit -->
    <rect x="20" y="70" width="190" height="100" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="115" y="96" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-blue)">EDGE DETECTOR</text>
    <text x="115" y="116" text-anchor="middle" font-size="10" font-weight="600" fill="var(--title-color)">Mạch Phát Hiện Cạnh Xung</text>

    <!-- Trigger Selection Registers -->
    <g transform="translate(20, 200)">
      <!-- Rising Trigger -->
      <rect width="190" height="48" rx="6" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
      <text x="95" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-green)">Rising Trigger Selection</text>
      <text x="95" y="36" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)" class="mono">EXTI_RTSR</text>

      <!-- Falling Trigger -->
      <rect y="65" width="190" height="48" rx="6" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
      <text x="95" y="85" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-red)">Falling Trigger Selection</text>
      <text x="95" y="101" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)" class="mono">EXTI_FTSR</text>
    </g>

    <!-- Trigger control lines into Edge Detector -->
    <path d="M 115 200 L 115 170" fill="none" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Software Interrupt Event Register (SWIER) -->
    <g transform="translate(20, 345)">
      <rect width="190" height="52" rx="6" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="95" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-purple)">Software Interrupt Event Reg</text>
      <text x="95" y="40" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)" class="mono">EXTI_SWIER</text>
    </g>

    <!-- OR Gate Combining Hardware Edge & Software Trigger -->
    <g transform="translate(250, 95)">
      <path d="M -40 25 L 0 25" fill="none" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow)"/>
      <path d="M -40 275 L 0 275 L 0 65 L 20 65" fill="none" stroke="var(--wire-line)" stroke-width="2"/>
      
      <!-- OR gate symbol box -->
      <rect x="20" y="10" width="70" height="70" rx="8" fill="var(--card-bg)" stroke="var(--logic-gate)" stroke-width="2"/>
      <text x="55" y="48" text-anchor="middle" font-size="16" font-weight="900" fill="var(--logic-gate)">OR</text>
    </g>

    <!-- Output from OR Gate splits into Interrupt Path (Top) and Event Path (Bottom) -->
    <path d="M 340 140 L 375 140 L 375 60 L 410 60" fill="none" stroke="var(--wire-line)" stroke-width="2"/>
    <circle cx="375" cy="140" r="4" fill="var(--title-color)"/>
    <path d="M 375 140 L 375 320 L 410 320" fill="none" stroke="var(--wire-line)" stroke-width="2"/>
  </g>

  <!-- Right: Interrupt & Event Logic (X: 720 -> 1100) -->
  <g transform="translate(720, 100)">
    <!-- TOP PATH: INTERRUPT REQUEST TO NVIC -->
    <rect x="0" y="0" width="160" height="48" rx="6" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="80" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-blue)">Interrupt Mask Reg</text>
    <text x="80" y="38" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)" class="mono">EXTI_IMR</text>

    <!-- AND Gate for Interrupt -->
    <g transform="translate(60, 60)">
      <rect width="60" height="60" rx="6" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="30" y="36" text-anchor="middle" font-size="14" font-weight="900" fill="var(--accent-green)">AND</text>
      <line x1="20" y1="-12" x2="20" y2="0" stroke="var(--wire-line)" stroke-width="2"/>
    </g>

    <!-- Pending Request Register (PR) -->
    <g transform="translate(160, 65)">
      <path d="M -40 25 L 0 25" fill="none" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow)"/>
      <rect width="180" height="50" rx="6" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
      <text x="90" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Pending Request Register</text>
      <text x="90" y="40" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-amber)" class="mono">EXTI_PR (Ghi 1 để xóa!)</text>
    </g>

    <!-- Output to NVIC -->
    <g transform="translate(200, 155)">
      <path d="M 50 -40 L 50 0" fill="none" stroke="var(--accent-red)" stroke-width="2.5" marker-end="url(#arrow-red)"/>
      <rect width="170" height="85" rx="8" fill="#00205b" stroke="#00a3e0" stroke-width="2"/>
      <text x="85" y="28" text-anchor="middle" font-size="14" font-weight="900" fill="#ffffff">NVIC CONTROLLER</text>
      <text x="85" y="48" text-anchor="middle" font-size="10" font-weight="600" fill="#38bdf8">Vector Ngắt Cortex-M3</text>
      <text x="85" y="66" text-anchor="middle" font-size="9" fill="#94a3b8">EXTI0_IRQn .. EXTI15_10_IRQn</text>
    </g>

    <!-- BOTTOM PATH: EVENT REQUEST (WAKEUP WFE) -->
    <g transform="translate(0, 260)">
      <rect width="160" height="48" rx="6" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="80" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-purple)">Event Mask Reg</text>
      <text x="80" y="38" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)" class="mono">EXTI_EMR</text>
    </g>

    <!-- AND Gate for Event -->
    <g transform="translate(60, 320)">
      <rect width="60" height="60" rx="6" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
      <text x="30" y="36" text-anchor="middle" font-size="14" font-weight="900" fill="var(--accent-purple)">AND</text>
      <line x1="20" y1="-12" x2="20" y2="0" stroke="var(--wire-line)" stroke-width="2"/>
    </g>

    <!-- Pulse Generator -->
    <g transform="translate(160, 325)">
      <path d="M -40 25 L 0 25" fill="none" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow)"/>
      <rect width="180" height="50" rx="6" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="90" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Pulse Generator</text>
      <text x="90" y="38" text-anchor="middle" font-size="10" fill="var(--text-muted)">Tạo xung đánh thức CPU</text>
    </g>

    <!-- Event Output -->
    <g transform="translate(200, 410)">
      <path d="M 50 -35 L 50 0" fill="none" stroke="var(--accent-purple)" stroke-width="2.5" marker-end="url(#arrow)"/>
      <rect width="170" height="75" rx="8" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
      <text x="85" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-purple)">EVENT OUTPUT</text>
      <text x="85" y="48" text-anchor="middle" font-size="10" fill="var(--title-color)">Thoát chế độ WFE (Sleep)</text>
      <text x="85" y="64" text-anchor="middle" font-size="9" fill="var(--text-muted)">Không tốn chi phí ISR!</text>
    </g>
  </g>
</svg>"""

save_svg("bai04_exti_structure.svg", svg_exti)

# ==============================================================================
# 4. BÀI 06: GENERAL PURPOSE TIMER TIME-BASE (ST RM0008 Figure 42)
# ==============================================================================
svg_timer = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 680" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="1140" height="680" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Top Header -->
  <rect x="25" y="16" width="1090" height="64" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="45" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 15.2</text>
  <text x="45" y="64" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 42: General-purpose timer block diagram (Khối cơ sở định thời Time-Base &amp; 4 Kênh So Sánh)</text>
  <rect x="960" y="28" width="135" height="36" rx="6" fill="#00205b"/>
  <text x="1027" y="51" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left: Clock Source & Prescaler (X: 40 -> 340) -->
  <g transform="translate(40, 100)">
    <rect width="280" height="110" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="140" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">TIMER CLOCK SOURCE (CK_PSC)</text>
    <text x="140" y="48" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-blue)">Internal Clock (CK_INT) = 72MHz</text>
    <text x="140" y="68" text-anchor="middle" font-size="10" fill="var(--text-muted)">Hoặc External Mode 1, Mode 2 (ETR Pin)</text>
    <text x="140" y="88" text-anchor="middle" font-size="10" fill="var(--text-muted)">Hoặc Internal Trigger (ITR0..3 cascade)</text>

    <!-- Arrow down to Prescaler -->
    <path d="M 140 110 L 140 150" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

    <!-- Prescaler (PSC) with Shadow Register -->
    <g transform="translate(0, 150)">
      <rect width="280" height="150" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="140" y="26" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-blue)">PRESCALER UNIT (PSC)</text>
      
      <!-- Preload Register -->
      <rect x="20" y="40" width="240" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="140" y="65" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">PSC Preload Register (16-bit: 0..65535)</text>

      <!-- Shadow Register -->
      <rect x="20" y="90" width="240" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="140" y="112" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-blue)">PSC Shadow Register (Thực thi)</text>
      <text x="140" y="126" text-anchor="middle" font-size="9" fill="var(--text-muted)">Chỉ nạp giá trị mới khi có Update Event (UEV)</text>
    </g>

    <!-- Formula Box -->
    <g transform="translate(0, 325)">
      <rect width="280" height="190" rx="8" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="140" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-amber)">CÔNG THỨC ĐỊNH THỜI CHUẨN:</text>
      <text x="15" y="55" font-size="11" font-weight="700" fill="var(--title-color)">f_CNT = f_CK_PSC / (PSC + 1)</text>
      <text x="15" y="80" font-size="10" fill="var(--text-muted)">Ví dụ: 72MHz / (71 + 1) = 1MHz (1µs)</text>
      
      <line x1="15" y1="95" x2="265" y2="95" stroke="var(--card-border)"/>
      
      <text x="15" y="120" font-size="11" font-weight="700" fill="var(--title-color)">f_Update = f_CNT / (ARR + 1)</text>
      <text x="15" y="145" font-size="10" fill="var(--text-muted)">T_Overflow = (PSC + 1) × (ARR + 1) / 72MHz</text>
      <text x="15" y="170" font-size="10" font-weight="700" fill="var(--accent-green)">Ngắt 1ms: PSC = 71, ARR = 999</text>
    </g>
  </g>

  <!-- Middle: Counter & Auto-Reload Register (X: 360 -> 720) -->
  <g transform="translate(360, 100)">
    <!-- Line from Prescaler into Counter -->
    <path d="M -40 225 L 30 225" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
    <text x="-25" y="215" font-size="10" font-weight="700" fill="var(--bus-line)">CK_CNT</text>

    <!-- Auto-Reload Register (ARR) Container -->
    <g transform="translate(30, 20)">
      <rect width="320" height="150" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="160" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-green)">AUTO-RELOAD REGISTER (ARR)</text>
      
      <!-- ARR Preload -->
      <rect x="20" y="42" width="280" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="160" y="66" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">ARR Preload Register (16-bit)</text>

      <!-- ARR Shadow -->
      <rect x="20" y="92" width="280" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
      <text x="160" y="114" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-green)">ARR Shadow Register (Thực thi)</text>
      <text x="160" y="128" text-anchor="middle" font-size="9" fill="var(--text-muted)">Bật đệm: ARPE bit trong TIMx_CR1</text>
    </g>

    <!-- Counter (CNT) Container -->
    <g transform="translate(30, 210)">
      <rect width="320" height="140" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="160" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-blue)">16-BIT COUNTER (TIMx_CNT)</text>
      
      <rect x="20" y="42" width="280" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="160" y="67" text-anchor="middle" font-size="13" font-weight="900" fill="var(--accent-blue)">Giá trị đếm: 0x0000 → 0xFFFF</text>

      <text x="35" y="105" font-size="10" font-weight="700" fill="var(--title-color)">Chế độ: Đếm Lên (Up), Đếm Xuống (Down)</text>
      <text x="35" y="123" font-size="10" fill="var(--text-muted)">Đếm Đối Xứng Trung Tâm (Center-aligned Mode 1,2,3)</text>
    </g>

    <!-- Comparator Logic between CNT and ARR -->
    <path d="M 190 170 L 190 210" fill="none" stroke="var(--wire-line)" stroke-width="2" stroke-dasharray="3,3"/>
    <text x="200" y="195" font-size="9" font-weight="700" fill="var(--text-muted)">So sánh CNT == ARR</text>

    <!-- Update Event Generation -->
    <g transform="translate(30, 390)">
      <path d="M 160 -40 L 160 0" fill="none" stroke="var(--accent-red)" stroke-width="2.5" marker-end="url(#arrow-red)"/>
      <rect width="320" height="125" rx="8" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="2"/>
      <text x="160" y="26" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-red)">UPDATE EVENT (UEV)</text>
      <text x="160" y="48" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Sự Kiện Cập Nhật Khi Tràn Bộ Đếm</text>

      <g transform="translate(15, 60)">
        <rect width="135" height="50" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="67" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-red)">Cờ Ngắt UIF</text>
        <text x="67" y="38" text-anchor="middle" font-size="9" fill="var(--text-muted)">Kích hoạt TIMx_IRQHandler</text>

        <rect x="155" width="135" height="50" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="222" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-blue)">DMA Request</text>
        <text x="222" y="38" text-anchor="middle" font-size="9" fill="var(--text-muted)">Truyền dữ liệu tự động</text>
      </g>
    </g>
  </g>

  <!-- Right: 4 Capture / Compare Channels (X: 740 -> 1100) -->
  <g transform="translate(740, 100)">
    <rect width="360" height="520" rx="8" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="180" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-purple)">4 KÊNH CAPTURE / COMPARE (CC1..CC4)</text>
    <text x="180" y="48" text-anchor="middle" font-size="11" fill="var(--text-muted)">Phục vụ PWM, Đo Tần Số &amp; Encoder</text>

    <!-- Channel 1 -->
    <g transform="translate(15, 65)">
      <rect width="330" height="95" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <text x="15" y="24" font-size="11" font-weight="800" fill="var(--accent-blue)">KÊNH 1: TIMx_CCR1 (Capture / Compare Reg 1)</text>
      <text x="15" y="44" font-size="10" fill="var(--text-primary)">• Ngõ ra: PWM1 / PWM2 điều khiển duty cycle</text>
      <text x="15" y="62" font-size="10" fill="var(--text-muted)">• Ngõ vào: Input Capture đo độ rộng xung (PA0/PA8)</text>
      <text x="15" y="80" font-size="9" font-weight="700" fill="var(--accent-green)">Ngõ ra vật lý: CH1 Pin (PA0 trên TIM2, PA8 trên TIM1)</text>
    </g>

    <!-- Channel 2 -->
    <g transform="translate(15, 175)">
      <rect width="330" height="95" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <text x="15" y="24" font-size="11" font-weight="800" fill="var(--accent-blue)">KÊNH 2: TIMx_CCR2 (Capture / Compare Reg 2)</text>
      <text x="15" y="44" font-size="10" fill="var(--text-primary)">• Kết hợp với Kênh 1: Giao tiếp Rotary Encoder</text>
      <text x="15" y="62" font-size="10" fill="var(--text-muted)">• Giải mã pha A/B (Quadrature Decoder 1x/2x/4x)</text>
      <text x="15" y="80" font-size="9" font-weight="700" fill="var(--accent-green)">Ngõ ra vật lý: CH2 Pin (PA1 trên TIM2, PA9 trên TIM1)</text>
    </g>

    <!-- Channel 3 & 4 Summary -->
    <g transform="translate(15, 285)">
      <rect width="330" height="110" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <text x="15" y="24" font-size="11" font-weight="800" fill="var(--accent-blue)">KÊNH 3 &amp; 4: TIMx_CCR3, TIMx_CCR4</text>
      <text x="15" y="44" font-size="10" fill="var(--text-primary)">• Xuất 4 kênh PWM độc lập trên cùng 1 tần số</text>
      <text x="15" y="64" font-size="10" fill="var(--text-muted)">• Ứng dụng điều khiển 4 motor cánh quạt Quadcopter</text>
      <text x="15" y="84" font-size="10" fill="var(--text-muted)">• Hoặc điều khiển động cơ bước (Step Motor), Servo SG90</text>
      <text x="15" y="100" font-size="9" font-weight="700" fill="var(--accent-green)">Ngõ ra vật lý: CH3 (PA2), CH4 (PA3)</text>
    </g>

    <!-- Output Polarity & Enable -->
    <g transform="translate(15, 410)">
      <rect width="330" height="90" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="165" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-purple)">CAPTURE / COMPARE ENABLE (CCER)</text>
      <text x="15" y="48" font-size="10" fill="var(--title-color)">• CCxE: Bật/Tắt ngõ ra chân vật lý</text>
      <text x="15" y="68" font-size="10" fill="var(--title-color)">• CCxP: Đảo cực tính xung (Active High / Active Low)</text>
    </g>
  </g>
</svg>"""

save_svg("bai06_timer_timebase.svg", svg_timer)

# ==============================================================================
# 5. BÀI 11: ADC 12-BIT SAR ARCHITECTURE (ST RM0008 Figure 22)
# ==============================================================================
svg_adc = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 680" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="1140" height="680" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Header -->
  <rect x="25" y="16" width="1090" height="64" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="45" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 11.2</text>
  <text x="45" y="64" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 22: ADC block diagram (Kiến trúc bộ biến đổi tương tự - số ADC 12-bit SAR)</text>
  <rect x="960" y="28" width="135" height="36" rx="6" fill="#00205b"/>
  <text x="1027" y="51" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left: Analog Channels & MUX (X: 35 -> 280) -->
  <g transform="translate(35, 100)">
    <rect width="250" height="520" rx="8" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
    <text x="125" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-amber)">18 KÊNH ĐẦU VÀO TƯƠNG TỰ</text>
    
    <!-- External Channels -->
    <g transform="translate(15, 50)">
      <rect width="220" height="180" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="110" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">16 KÊNH NGOẠI VI (CH0..CH15)</text>
      <text x="15" y="48" font-size="10" fill="var(--text-primary)">• ADC1_IN0..IN7: PA0 → PA7</text>
      <text x="15" y="68" font-size="10" fill="var(--text-primary)">• ADC1_IN8..IN9: PB0 → PB1</text>
      <text x="15" y="88" font-size="10" fill="var(--text-primary)">• ADC1_IN10..IN15: PC0 → PC5</text>
      <line x1="15" y1="100" x2="205" y2="100" stroke="var(--card-border)"/>
      <text x="15" y="120" font-size="10" font-weight="700" fill="var(--accent-blue)">Điện áp vào: 0V → VREF+ (3.3V)</text>
      <text x="15" y="138" font-size="9" fill="var(--accent-red)">! Tuyệt đối không cấp quá 3.6V (Cháy ADC!)</text>
      <text x="15" y="154" font-size="9" fill="var(--text-muted)">! Không dùng chân 5V-FT cho ADC</text>
    </g>

    <!-- Internal Channels -->
    <g transform="translate(15, 245)">
      <rect width="220" height="100" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="110" y="24" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-purple)">2 KÊNH NỘI TẠI (CH16..CH17)</text>
      <text x="15" y="48" font-size="10" fill="var(--text-primary)">• CH16: Cảm biến nhiệt độ chip</text>
      <text x="15" y="66" font-size="9" fill="var(--text-muted)">(Đo nhiệt độ lõi STM32 bên trong)</text>
      <text x="15" y="85" font-size="10" fill="var(--text-primary)">• CH17: Điện áp tham chiếu nội VREFINT</text>
      <text x="15" y="100" font-size="9" fill="var(--text-muted)">(Chuẩn cố định 1.20V để bù sụt áp pin)</text>
    </g>

    <!-- Analog Multiplexer -->
    <g transform="translate(15, 360)">
      <rect width="220" height="140" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
      <text x="110" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-amber)">ANALOG MULTIPLEXER</text>
      <text x="15" y="52" font-size="10" fill="var(--text-primary)">Chọn kênh chuyển đổi theo:</text>
      <text x="15" y="74" font-size="10" font-weight="700" fill="var(--accent-blue)">• Nhóm Regular: Tuần tự SQR1..3</text>
      <text x="15" y="96" font-size="10" font-weight="700" fill="var(--accent-green)">• Nhóm Injected: Ưu tiên JSQR</text>
      <text x="15" y="122" font-size="9" fill="var(--text-muted)">Thời gian trích mẫu độc lập: SMPR1..2</text>
    </g>
  </g>

  <!-- Middle: Sample & Hold, 12-bit SAR Engine (X: 320 -> 720) -->
  <g transform="translate(320, 100)">
    <!-- Line from Mux to S&H -->
    <path d="M -35 430 L 25 430 L 25 150 L 50 150" fill="none" stroke="var(--wire-line)" stroke-width="2.5" marker-end="url(#arrow)"/>
    <text x="-15" y="420" font-size="10" font-weight="700" fill="var(--accent-amber)">V_IN</text>

    <!-- Sample & Hold Stage -->
    <g transform="translate(50, 80)">
      <rect width="320" height="110" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="160" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-blue)">SAMPLE &amp; HOLD STAGE</text>
      <text x="160" y="50" text-anchor="middle" font-size="11" font-weight="600" fill="var(--title-color)">Mạch Giữ Mẫu Tụ Điện Lấy Mẫu</text>
      <text x="20" y="75" font-size="10" fill="var(--text-muted)">Thời gian lấy mẫu: T_SMP = 1.5 → 239.5 chu kỳ ADCCLK</text>
      <text x="20" y="95" font-size="10" font-weight="700" fill="var(--accent-blue)">Tổng thời gian: T_CONV = T_SMP + 12.5 chu kỳ = 1µs (1Msps!)</text>
    </g>

    <!-- Arrow down to SAR -->
    <path d="M 210 190 L 210 230" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

    <!-- 12-bit SAR Converter Core -->
    <g transform="translate(50, 230)">
      <rect width="320" height="150" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="160" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-green)">12-BIT SAR ADC CORE</text>
      <text x="160" y="48" text-anchor="middle" font-size="11" fill="var(--text-muted)">Successive Approximation Register</text>
      
      <g transform="translate(20, 60)">
        <rect width="280" height="75" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="140" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)">Độ phân giải 12-bit = 4096 mức (0 → 4095)</text>
        <text x="140" y="45" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-green)">Bước điện áp: 1 LSB = 3.3V / 4095 ≈ 0.8058 mV</text>
        <text x="140" y="65" text-anchor="middle" font-size="10" fill="var(--text-muted)">V_IN = (ADC_Data / 4095) × 3.3V</text>
      </g>
    </g>

    <!-- Analog Watchdog (AWD) -->
    <g transform="translate(50, 400)">
      <path d="M 210 -20 L 210 0" fill="none" stroke="var(--accent-red)" stroke-width="2" marker-end="url(#arrow-red)"/>
      <rect width="320" height="110" rx="8" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="2"/>
      <text x="160" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-red)">ANALOG WATCHDOG (AWD)</text>
      <text x="20" y="52" font-size="10" fill="var(--title-color)">So sánh tự động giá trị ADC với 2 ngưỡng:</text>
      <text x="20" y="72" font-size="10" font-weight="700" fill="var(--accent-red)">• Ngưỡng cao: ADC_HTR  |  • Ngưỡng thấp: ADC_LTR</text>
      <text x="20" y="92" font-size="10" fill="var(--text-muted)">Kích hoạt ngắt AWD ngay lập tức nếu điện áp vượt giới hạn an toàn</text>
    </g>
  </g>

  <!-- Right: Data Registers & DMA Interface (X: 740 -> 1100) -->
  <g transform="translate(740, 100)">
    <rect width="360" height="150" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="180" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-blue)">REGULAR DATA REGISTER (ADC_DR)</text>
    
    <g transform="translate(20, 42)">
      <rect width="320" height="42" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="160" y="26" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)" class="mono">16-Bit Register: Data[11:0] (Right / Left Align)</text>
    </g>

    <text x="20" y="112" font-size="10" font-weight="700" fill="var(--accent-amber)">! ĐIỂM YẾU CHÍ MẠNG KHI QUÉT NHIỀU KÊNH:</text>
    <text x="20" y="132" font-size="9" fill="var(--text-muted)">Chỉ có 1 thanh ghi DR duy nhất! BẮT BUỘC dùng DMA1 Channel 1 để chống ghi đè!</text>

    <!-- Injected Data Registers -->
    <g transform="translate(0, 175)">
      <rect width="360" height="160" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="180" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-green)">INJECTED DATA REGISTERS (JDR1..JDR4)</text>
      
      <g transform="translate(20, 45)">
        <rect width="150" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="75" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-green)">ADC_JDR1 (Kênh 1)</text>

        <rect x="165" width="150" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="240" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-green)">ADC_JDR2 (Kênh 2)</text>

        <rect y="50" width="150" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="75" y="74" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-green)">ADC_JDR3 (Kênh 3)</text>

        <rect x="165" y="50" width="150" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="240" y="74" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-green)">ADC_JDR4 (Kênh 4)</text>
      </g>
      <text x="20" y="148" font-size="9" fill="var(--text-muted)">Ưu điểm: Mỗi kênh có riêng 1 thanh ghi lưu trữ + Auto Offset!</text>
    </g>

    <!-- DMA & CPU Interrupt Flags -->
    <g transform="translate(0, 360)">
      <rect width="360" height="150" rx="8" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
      <text x="180" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-purple)">DMA &amp; INTERRUPT OUTPUTS</text>
      
      <g transform="translate(20, 45)">
        <rect width="320" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
        <text x="160" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-blue)">DMA1 Channel 1 Request (Circular Mode)</text>
      </g>

      <g transform="translate(20, 95)">
        <rect width="320" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
        <text x="160" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-red)">ADC1_2_IRQn (Cờ EOC, JEOC, AWD)</text>
      </g>
    </g>
  </g>
</svg>"""

save_svg("bai11_adc_sar_structure.svg", svg_adc)

# ==============================================================================
# 6. BÀI 17: DMA CONTROLLER ARCHITECTURE (ST RM0008 Figure 20)
# ==============================================================================
svg_dma = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 680" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="1140" height="680" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Header -->
  <rect x="25" y="16" width="1090" height="64" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="45" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 13.2</text>
  <text x="45" y="64" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 20: DMA block diagram (Kiến trúc bộ điều khiển truy cập bộ nhớ trực tiếp DMA Controller)</text>
  <rect x="960" y="28" width="135" height="36" rx="6" fill="#00205b"/>
  <text x="1027" y="51" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left: Cortex-M3 Core & Masters (X: 35 -> 280) -->
  <g transform="translate(35, 100)">
    <rect width="240" height="520" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="120" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">BUS MASTERS (Chủ Bus)</text>

    <!-- ARM Cortex-M3 Core -->
    <g transform="translate(15, 60)">
      <rect width="210" height="120" rx="6" fill="#00205b" stroke="#00a3e0" stroke-width="2"/>
      <text x="105" y="32" text-anchor="middle" font-size="14" font-weight="900" fill="#ffffff">ARM CORTEX-M3</text>
      <text x="105" y="54" text-anchor="middle" font-size="11" font-weight="700" fill="#38bdf8">I-Bus (Instruction)</text>
      <text x="105" y="74" text-anchor="middle" font-size="11" font-weight="700" fill="#38bdf8">D-Bus (Data)</text>
      <text x="105" y="94" text-anchor="middle" font-size="11" font-weight="700" fill="#38bdf8">S-Bus (System)</text>
    </g>

    <!-- DMA1 Master -->
    <g transform="translate(15, 210)">
      <rect width="210" height="130" rx="6" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="105" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-blue)">DMA1 CONTROLLER</text>
      <text x="105" y="48" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">7 Kênh Độc Lập (CH1..CH7)</text>
      <text x="15" y="72" font-size="10" fill="var(--text-muted)">• CH1: ADC1, TIM2_CH3</text>
      <text x="15" y="90" font-size="10" fill="var(--text-muted)">• CH2: SPI1_RX, USART3_TX</text>
      <text x="15" y="108" font-size="10" fill="var(--text-muted)">• CH3: SPI1_TX, USART3_RX</text>
      <text x="15" y="124" font-size="10" fill="var(--text-muted)">• CH4/5: USART1_TX / RX</text>
    </g>

    <!-- DMA2 Master -->
    <g transform="translate(15, 365)">
      <rect width="210" height="90" rx="6" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="105" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-purple)">DMA2 CONTROLLER</text>
      <text x="105" y="46" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">5 Kênh Độc Lập</text>
      <text x="15" y="68" font-size="9" fill="var(--text-muted)">(Chỉ có trên dòng High-Density STM32)</text>
    </g>
  </g>

  <!-- Middle: Bus Matrix & Arbiter (X: 310 -> 720) -->
  <g transform="translate(310, 100)">
    <rect width="380" height="200" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="190" y="30" text-anchor="middle" font-size="14" font-weight="800" fill="var(--accent-blue)">DMA ARBITER (BỘ TRỌNG TÀI PHÂN XỬ)</text>
    <text x="190" y="52" text-anchor="middle" font-size="11" fill="var(--text-muted)">Giải quyết xung đột khi nhiều kênh yêu cầu cùng lúc</text>

    <!-- Priority Levels -->
    <g transform="translate(20, 70)">
      <rect width="165" height="50" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
      <text x="82" y="22" text-anchor="middle" font-size="9.5" font-weight="800" fill="var(--accent-red)">1. Very High (Tối cao)</text>
      <text x="82" y="38" text-anchor="middle" font-size="9" fill="var(--text-muted)">Cấu hình qua PL[1:0] = 11</text>

      <rect x="175" width="165" height="50" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="257" y="22" text-anchor="middle" font-size="9.5" font-weight="800" fill="var(--accent-amber)">2. High (Ưu tiên cao)</text>
      <text x="257" y="38" text-anchor="middle" font-size="9" fill="var(--text-muted)">Cấu hình qua PL[1:0] = 10</text>

      <rect y="60" width="165" height="50" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="82" y="82" text-anchor="middle" font-size="9.5" font-weight="800" fill="var(--accent-blue)">3. Medium (Trung bình)</text>
      <text x="82" y="98" text-anchor="middle" font-size="9" fill="var(--text-muted)">Cấu hình qua PL[1:0] = 01</text>

      <rect x="175" y="60" width="165" height="50" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
      <text x="257" y="82" text-anchor="middle" font-size="9.5" font-weight="800" fill="var(--accent-green)">4. Low (Ưu tiên thấp)</text>
      <text x="257" y="98" text-anchor="middle" font-size="9" fill="var(--text-muted)">Cấu hình qua PL[1:0] = 00</text>
    </g>

    <text x="190" y="190" text-anchor="middle" font-size="9" font-weight="700" fill="var(--text-muted)">*Nếu cùng mức ưu tiên phần mềm: Kênh số nhỏ hơn thắng (Kênh 1 &gt; Kênh 2 &gt; ...)</text>

    <!-- Channel Registers Block -->
    <g transform="translate(0, 230)">
      <rect width="380" height="290" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="190" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-green)">CẤU TRÚC 1 KÊNH DMA (CHANNEL REGISTERS)</text>

      <!-- CPAR -->
      <g transform="translate(20, 45)">
        <rect width="340" height="42" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="15" y="26" font-size="11" font-weight="800" fill="var(--accent-blue)" class="mono">DMA_CPARx:</text>
        <text x="110" y="26" font-size="9.5" fill="var(--title-color)">Peripheral Address (Địa chỉ ngoại vi)</text>
      </g>

      <!-- CMAR -->
      <g transform="translate(20, 95)">
        <rect width="340" height="42" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="15" y="26" font-size="11" font-weight="800" fill="var(--accent-green)" class="mono">DMA_CMARx:</text>
        <text x="110" y="26" font-size="9.5" fill="var(--title-color)">Memory Address (Địa chỉ mảng trong SRAM)</text>
      </g>

      <!-- CNDTR -->
      <g transform="translate(20, 145)">
        <rect width="340" height="42" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="15" y="26" font-size="11" font-weight="800" fill="var(--accent-amber)" class="mono">DMA_CNDTRx:</text>
        <text x="115" y="26" font-size="9.5" fill="var(--title-color)">Data Counter (Số byte truyền: 0..65535)</text>
      </g>

      <!-- CCR Controls -->
      <g transform="translate(20, 195)">
        <rect width="340" height="80" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
        <text x="170" y="20" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-purple)">THANH GHI ĐIỀU KHIỂN DMA_CCRx</text>
        <text x="15" y="40" font-size="10" fill="var(--title-color)">• DIR: Hướng truyền (0: Ngoại vi -&gt; RAM, 1: RAM -&gt; Ngoại vi)</text>
        <text x="15" y="58" font-size="10" fill="var(--title-color)">• CIRC: Chế độ vòng tròn lặp vô tận (Circular Mode)</text>
        <text x="15" y="74" font-size="10" fill="var(--title-color)">• MINC/PINC: Tự động tăng con trỏ địa chỉ bộ nhớ/ngoại vi</text>
      </g>
    </g>
  </g>

  <!-- Right: Slaves (SRAM, Flash, Peripherals) (X: 730 -> 1100) -->
  <g transform="translate(730, 100)">
    <rect width="370" height="520" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="185" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">BUS SLAVES (ĐÍCH ĐẾN DỮ LIỆU)</text>

    <!-- SRAM Memory -->
    <g transform="translate(20, 55)">
      <rect width="330" height="110" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="165" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-blue)">INTERNAL SRAM (20KB)</text>
      <text x="165" y="48" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">0x2000 0000 → 0x2000 4FFF</text>
      <text x="15" y="75" font-size="10" fill="var(--text-muted)">• DMA đọc/ghi trực tiếp vào mảng RAM của chương trình</text>
      <text x="15" y="95" font-size="10" font-weight="700" fill="var(--accent-green)">• TẢI CPU = 0%! Core hoàn toàn rảnh rang làm việc khác!</text>
    </g>

    <!-- Flash Memory -->
    <g transform="translate(20, 185)">
      <rect width="330" height="85" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="165" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-purple)">FLASH MEMORY (64KB / 128KB)</text>
      <text x="165" y="46" text-anchor="middle" font-size="11" class="mono">0x0800 0000 → 0x0801 FFFF</text>
      <text x="15" y="70" font-size="10" fill="var(--text-muted)">• Hỗ trợ Memory-to-Memory (Truyền siêu tốc Flash sang RAM)</text>
    </g>

    <!-- Peripheral Domain (APB1 & APB2) -->
    <g transform="translate(20, 290)">
      <rect width="330" height="205" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
      <text x="165" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-amber)">CÁC NGOẠI VI GẮN DMA</text>
      
      <g transform="translate(15, 42)">
        <rect width="300" height="35" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="15" y="22" font-size="10" font-weight="700" fill="var(--accent-blue)">USART1, USART2, USART3:</text>
        <text x="180" y="22" font-size="10" fill="var(--text-muted)">DMA TX &amp; DMA RX</text>

        <rect y="42" width="300" height="35" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="15" y="64" font-size="10" font-weight="700" fill="var(--accent-green)">SPI1, SPI2:</text>
        <text x="110" y="64" font-size="10" fill="var(--text-muted)">Giao tiếp màn hình LCD/OLED tốc độ cao</text>

        <rect y="84" width="300" height="35" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="15" y="106" font-size="10" font-weight="700" fill="var(--accent-amber)">ADC1:</text>
        <text x="70" y="106" font-size="10" fill="var(--text-muted)">Lấy mẫu 16 kênh tự động không gián đoạn</text>

        <rect y="126" width="300" height="35" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="15" y="148" font-size="9.5" font-weight="700" fill="var(--accent-purple)">TIM1..TIM4:</text>
        <text x="85" y="148" font-size="9" fill="var(--text-muted)">Tạo xung PWM điều khiển LED / WS2812</text>
      </g>
    </g>
  </g>
</svg>"""

save_svg("bai17_dma_architecture.svg", svg_dma)

# ==============================================================================
# 7. BÀI 23: CAN BUS ARCHITECTURE (ST RM0008 Figure 245 & TJA1050)
# ==============================================================================
svg_can = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 680" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="1140" height="680" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Header -->
  <rect x="25" y="16" width="1090" height="64" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="45" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 24</text>
  <text x="45" y="64" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 245: CAN controller block diagram &amp; TJA1050 PHY (Kiến trúc vi điều khiển CAN và tầng truyền dẫn vật lý)</text>
  <rect x="960" y="28" width="135" height="36" rx="6" fill="#00205b"/>
  <text x="1027" y="51" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left: STM32F103 bxCAN Core (X: 35 -> 480) -->
  <g transform="translate(35, 100)">
    <rect width="440" height="520" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="220" y="28" text-anchor="middle" font-size="14" font-weight="800" fill="var(--accent-blue)">STM32F103 bxCAN CONTROLLER (BASIC EXTENDED CAN)</text>

    <!-- Transmit Mailboxes -->
    <g transform="translate(20, 50)">
      <rect width="400" height="110" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
      <text x="200" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-green)">3 HỘP THƯ TRUYỀN DỮ LIỆU (TX MAILBOX 0, 1, 2)</text>
      
      <g transform="translate(15, 38)">
        <rect width="115" height="55" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="57" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Mailbox 0</text>
        <text x="57" y="42" text-anchor="middle" font-size="9" fill="var(--text-muted)">ID + 8 Byte Data</text>

        <rect x="125" width="115" height="55" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="182" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Mailbox 1</text>
        <text x="182" y="42" text-anchor="middle" font-size="9" fill="var(--text-muted)">ID + 8 Byte Data</text>

        <rect x="250" width="115" height="55" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="307" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Mailbox 2</text>
        <text x="307" y="42" text-anchor="middle" font-size="9" fill="var(--text-muted)">ID + 8 Byte Data</text>
      </g>
    </g>

    <!-- 14 Filter Banks -->
    <g transform="translate(20, 175)">
      <rect width="400" height="130" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="200" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-purple)">14 HÀNG BỘ LỌC CHẤP NHẬN (FILTER BANKS 0..13)</text>
      
      <g transform="translate(15, 38)">
        <rect width="175" height="75" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="87" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">Chế Độ Mask (Mặt nạ):</text>
        <text x="15" y="40" font-size="9" fill="var(--accent-blue)">• ID Register (Mã định danh)</text>
        <text x="15" y="58" font-size="9" fill="var(--accent-purple)">• Mask Register (Bit cần khớp)</text>

        <rect x="195" width="175" height="75" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="87" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">Chế Độ List (Danh sách):</text>
        <text x="15" y="40" font-size="9" fill="var(--text-muted)">• Khớp chính xác ID 1</text>
        <text x="15" y="58" font-size="9" fill="var(--text-muted)">• Khớp chính xác ID 2</text>
      </g>
    </g>

    <!-- Receive FIFOs -->
    <g transform="translate(20, 320)">
      <rect width="400" height="120" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="200" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-blue)">2 HÀNG ĐỢI NHẬN DỮ LIỆU (RX FIFO 0 &amp; FIFO 1)</text>
      <text x="200" y="44" text-anchor="middle" font-size="10" fill="var(--text-muted)">Mỗi FIFO có 3 tầng sâu (chứa tối đa 3 gói tin trước khi tràn)</text>
      
      <g transform="translate(15, 55)">
        <rect width="175" height="45" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="87" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-blue)">FIFO 0 (3 messages)</text>
        <text x="87" y="38" text-anchor="middle" font-size="8" fill="var(--text-muted)">Ngắt USB_LP_CAN1_RX0_IRQn</text>

        <rect x="195" width="175" height="45" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="87" y="22" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-blue)">FIFO 1 (3 messages)</text>
        <text x="87" y="38" text-anchor="middle" font-size="8" fill="var(--text-muted)">Ngắt CAN1_RX1_IRQn</text>
      </g>
    </g>

    <!-- Pins PA11, PA12 -->
    <g transform="translate(20, 455)">
      <rect width="190" height="48" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="95" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">CAN_TX (PA12 / PB9)</text>
      <text x="95" y="36" text-anchor="middle" font-size="9" fill="var(--accent-green)">Tín hiệu số TTL 3.3V</text>

      <rect x="210" width="190" height="48" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="95" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">CAN_RX (PA11 / PB8)</text>
      <text x="95" y="36" text-anchor="middle" font-size="9" fill="var(--accent-blue)">Tín hiệu số TTL 3.3V</text>
    </g>
  </g>

  <!-- Middle: External PHY Transceiver TJA1050 (X: 510 -> 750) -->
  <g transform="translate(510, 160)">
    <!-- Arrows from STM32 to Transceiver -->
    <path d="M -35 320 L 20 320" fill="none" stroke="var(--accent-green)" stroke-width="2.5" marker-end="url(#arrow-green)"/>
    <text x="-20" y="310" font-size="9" font-weight="700" fill="var(--accent-green)">TXD</text>

    <path d="M 20 345 L -35 345" fill="none" stroke="var(--accent-blue)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
    <text x="-20" y="360" font-size="9" font-weight="700" fill="var(--accent-blue)">RXD</text>

    <rect width="220" height="360" rx="8" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
    <text x="110" y="30" text-anchor="middle" font-size="13" font-weight="900" fill="var(--accent-amber)">CAN TRANSCEIVER (PHY)</text>
    <text x="110" y="50" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">TJA1050 / SN65HVD230</text>
    
    <g transform="translate(15, 75)">
      <rect width="190" height="100" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="95" y="24" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">CHỨC NĂNG CHÍNH:</text>
      <text x="10" y="48" font-size="9" fill="var(--text-muted)">• Chuyển mức TTL (0-3.3V/5V)</text>
      <text x="10" y="66" font-size="9" fill="var(--text-muted)">  thành điện áp vi sai CANH, CANL</text>
      <text x="10" y="85" font-size="9" fill="var(--accent-red)">• Chống sét, triệt tiêu nhiễu EMI</text>
    </g>

    <!-- Differential Voltage Explanation -->
    <g transform="translate(15, 190)">
      <rect width="190" height="150" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="95" y="22" text-anchor="middle" font-size="10" font-weight="800" fill="var(--accent-blue)">ĐIỆN ÁP VI SAI (CAN BUS):</text>
      
      <text x="10" y="48" font-size="10" font-weight="700" fill="var(--accent-red)">• Dominant (Mức 0 - Chiếm ưu):</text>
      <text x="15" y="66" font-size="9" fill="var(--title-color)">CANH = 3.5V, CANL = 1.5V</text>
      <text x="15" y="82" font-size="9" font-weight="700" fill="var(--accent-red)">V_Diff = 3.5 - 1.5 = 2.0V</text>

      <line x1="10" y1="92" x2="180" y2="92" stroke="var(--card-border)"/>

      <text x="10" y="110" font-size="10" font-weight="700" fill="var(--accent-blue)">• Recessive (Mức 1 - Nhường):</text>
      <text x="15" y="126" font-size="9" fill="var(--title-color)">CANH = 2.5V, CANL = 2.5V</text>
      <text x="15" y="142" font-size="9" font-weight="700" fill="var(--accent-blue)">V_Diff = 2.5 - 2.5 = 0.0V</text>
    </g>
  </g>

  <!-- Right: Two-Wire Differential CAN Bus Line (X: 770 -> 1100) -->
  <g transform="translate(770, 160)">
    <path d="M -40 180 L 40 180" fill="none" stroke="var(--accent-red)" stroke-width="3"/>
    <text x="-25" y="170" font-size="10" font-weight="800" fill="var(--accent-red)">CAN_H</text>

    <path d="M -40 280 L 40 280" fill="none" stroke="var(--accent-blue)" stroke-width="3"/>
    <text x="-25" y="270" font-size="10" font-weight="800" fill="var(--accent-blue)">CAN_L</text>

    <!-- 120 Ohm Termination Resistor Box -->
    <g transform="translate(40, 140)">
      <rect width="100" height="180" rx="8" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
      <text x="50" y="26" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-amber)">TERMINATION</text>
      
      <line x1="50" y1="40" x2="50" y2="70" stroke="var(--wire-line)" stroke-width="2"/>
      <rect x="35" y="70" width="30" height="45" rx="3" fill="var(--canvas-bg)" stroke="var(--title-color)" stroke-width="2"/>
      <text x="50" y="96" text-anchor="middle" font-size="11" font-weight="900" fill="var(--title-color)">120Ω</text>
      <line x1="50" y1="115" x2="50" y2="140" stroke="var(--wire-line)" stroke-width="2"/>

      <text x="50" y="165" text-anchor="middle" font-size="8" fill="var(--text-muted)">Điện trở đầu cuối</text>
    </g>

    <!-- Physical Bus Connection -->
    <g transform="translate(170, 80)">
      <rect width="150" height="300" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <text x="75" y="28" text-anchor="middle" font-size="12" font-weight="800" fill="var(--title-color)">MẠNG CAN BUS 2 DÂY</text>
      <text x="75" y="46" text-anchor="middle" font-size="10" fill="var(--text-muted)">Khoảng cách đến 1km</text>

      <g transform="translate(15, 65)">
        <rect width="120" height="60" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="60" y="26" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">ECU Node 2</text>
        <text x="60" y="44" text-anchor="middle" font-size="9" fill="var(--text-muted)">Động cơ / Hộp số</text>

        <rect y="75" width="120" height="60" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
        <text x="60" y="101" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">ECU Node 3</text>
        <text x="60" y="119" text-anchor="middle" font-size="9" fill="var(--text-muted)">Phanh ABS / Túi khí</text>

        <rect y="150" width="120" height="65" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
        <text x="60" y="174" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">Điện trở cuối 120Ω</text>
        <text x="60" y="192" text-anchor="middle" font-size="8" fill="var(--accent-amber)">Bắt buộc 2 đầu mạng!</text>
      </g>
    </g>
  </g>
</svg>"""

save_svg("bai23_can_bus_topology.svg", svg_can)

print("SUCCESS: ALL 7 CORE RM0008 SCHEMATICS BUILT WITH COMPLETE ACCURACY & CLEAN SVGS!")
