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
    print(f"Generated: {filename}")

COMMON_STYLES = """
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
        --accent-blue: #0284c7;
        --accent-green: #10b981;
        --accent-amber: #f59e0b;
        --accent-red: #ef4444;
        --accent-purple: #8b5cf6;
        --wire-line: #94a3b8;
        --bus-line: #3b82f6;
      }
      @media (prefers-color-scheme: dark) {
        :root {
          --canvas-bg: #0b1120;
          --canvas-border: #1e293b;
          --card-bg: #1e293b;
          --card-border: #334155;
          --title-color: #f8fafc;
          --subtitle-color: #94a3b8;
          --text-primary: #f1f5f9;
          --text-muted: #94a3b8;
          --accent-blue: #38bdf8;
          --accent-green: #34d399;
          --accent-amber: #fbbf24;
          --accent-red: #f87171;
          --accent-purple: #c084fc;
          --wire-line: #475569;
          --bus-line: #60a5fa;
        }
      }
      text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    </style>
"""

# 1. Bai 04: EXTI & NVIC Routing
svg_exti = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 480" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="950" height="480" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="475" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">KIẾN TRÚC ĐIỀU HƯỚNG NGẮT NGOẠI VI STM32: EXTI &amp; NVIC</text>
  <text x="475" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Cơ chế dồn kênh AFIO_EXTICRx ghép nối các cổng GPIO vào 16 kênh ngắt EXTI và NVIC Core</text>

  <!-- GPIO Inputs -->
  <g transform="translate(30, 90)">
    <rect width="180" height="350" rx="10" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="90" y="30" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-blue)">GPIO PORTS</text>
    <text x="90" y="50" text-anchor="middle" font-size="11" fill="var(--text-muted)">(16 Pins per Port)</text>
    
    <rect x="15" y="70" width="150" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="90" y="95" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">PA0, PB0 ... PG0</text>

    <rect x="15" y="130" width="150" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="90" y="155" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">PA1, PB1 ... PG1</text>

    <rect x="15" y="190" width="150" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="90" y="215" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">PA4, PB4 ... PG4</text>

    <rect x="15" y="250" width="150" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="90" y="275" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">PA5..9, PB5..9</text>

    <rect x="15" y="300" width="150" height="36" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="90" y="323" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">PA10..15, PB10..15</text>
  </g>

  <!-- Multiplexing AFIO -->
  <g transform="translate(260, 90)">
    <rect width="200" height="350" rx="10" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
    <text x="100" y="30" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-amber)">AFIO MUX LOGIC</text>
    <text x="100" y="50" text-anchor="middle" font-size="11" fill="var(--text-muted)">AFIO_EXTICR1..4</text>

    <rect x="20" y="70" width="160" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="95" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">EXTICR1 [3:0]</text>

    <rect x="20" y="130" width="160" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="155" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">EXTICR1 [7:4]</text>

    <rect x="20" y="190" width="160" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="215" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">EXTICR2 [3:0]</text>

    <rect x="20" y="250" width="160" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="275" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">EXTICR2..3 [15:4]</text>

    <rect x="20" y="300" width="160" height="36" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="323" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">EXTICR4 [15:0]</text>
  </g>

  <!-- EXTI Controller -->
  <g transform="translate(510, 90)">
    <rect width="190" height="350" rx="10" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="95" y="30" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-purple)">EXTI CONTROLLER</text>
    <text x="95" y="50" text-anchor="middle" font-size="11" fill="var(--text-muted)">Edge Detect &amp; Mask</text>

    <rect x="20" y="70" width="150" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="95" y="95" text-anchor="middle" font-size="12" font-weight="600" fill="var(--accent-purple)">EXTI Line 0</text>

    <rect x="20" y="130" width="150" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="95" y="155" text-anchor="middle" font-size="12" font-weight="600" fill="var(--accent-purple)">EXTI Line 1</text>

    <rect x="20" y="190" width="150" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="95" y="215" text-anchor="middle" font-size="12" font-weight="600" fill="var(--accent-purple)">EXTI Line 4</text>

    <rect x="20" y="250" width="150" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="95" y="275" text-anchor="middle" font-size="12" font-weight="600" fill="var(--accent-purple)">EXTI Line 5..9</text>

    <rect x="20" y="300" width="150" height="36" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="95" y="323" text-anchor="middle" font-size="12" font-weight="600" fill="var(--accent-purple)">EXTI Line 10..15</text>
  </g>

  <!-- NVIC Core Controller -->
  <g transform="translate(750, 90)">
    <rect width="170" height="350" rx="10" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="85" y="30" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-green)">ARM NVIC</text>
    <text x="85" y="50" text-anchor="middle" font-size="11" fill="var(--text-muted)">Vector Table ISR</text>

    <rect x="15" y="70" width="140" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
    <text x="85" y="95" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-green)">EXTI0_IRQHandler</text>

    <rect x="15" y="130" width="140" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
    <text x="85" y="155" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-green)">EXTI1_IRQHandler</text>

    <rect x="15" y="190" width="140" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
    <text x="85" y="215" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-green)">EXTI4_IRQHandler</text>

    <rect x="15" y="250" width="140" height="40" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
    <text x="85" y="275" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-green)">EXTI9_5_IRQn</text>

    <rect x="15" y="300" width="140" height="36" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
    <text x="85" y="323" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-green)">EXTI15_10_IRQn</text>
  </g>

  <!-- Connection Arrows -->
  <path d="M 210 180 L 260 180" stroke="var(--bus-line)" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 460 180 L 510 180" stroke="var(--bus-line)" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 700 180 L 750 180" stroke="var(--accent-green)" stroke-width="2" marker-end="url(#arrow)"/>

  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--bus-line)"/>
    </marker>
  </defs>
</svg>"""

save_svg("bai04_exti_nvic_routing.svg", svg_exti)

# 2. Bai 05: SysTick Timer
svg_systick = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="900" height="420" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="450" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">KIẾN TRÚC ĐỒNG HỒ ĐỊNH THỜI CỐT LÕI SYSTICK TIMER (ARM CORTEX-M3)</text>
  <text x="450" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Bộ đếm lùi 24-bit (Down-counter) tạo nhịp thời gian hệ thống và OS Heartbeat</text>

  <!-- Clock Source MUX -->
  <g transform="translate(40, 110)">
    <rect width="180" height="230" rx="10" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="90" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-blue)">CLOCK SOURCE</text>
    
    <rect x="15" y="60" width="150" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="90" y="82" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">HCLK (72MHz)</text>
    <text x="90" y="98" text-anchor="middle" font-size="10" fill="var(--text-muted)">CLKSOURCE = 1</text>

    <rect x="15" y="130" width="150" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="90" y="152" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">HCLK / 8 (9MHz)</text>
    <text x="90" y="168" text-anchor="middle" font-size="10" fill="var(--text-muted)">CLKSOURCE = 0</text>
  </g>

  <!-- 24-bit Down-Counter Core -->
  <g transform="translate(270, 100)">
    <rect width="360" height="250" rx="10" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="180" y="30" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-purple)">24-BIT DOWN-COUNTER CORE</text>
    
    <rect x="30" y="55" width="300" height="50" rx="8" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
    <text x="180" y="78" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-amber)">SysTick-&gt;LOAD (Reload Register)</text>
    <text x="180" y="96" text-anchor="middle" font-size="11" fill="var(--text-muted)">Nạp giá trị ban đầu N (Tối đa 0x00FFFFFF)</text>

    <path d="M 180 105 L 180 135" stroke="var(--accent-purple)" stroke-width="2" stroke-dasharray="4,4"/>

    <rect x="30" y="135" width="300" height="50" rx="8" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="180" y="158" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-purple)">SysTick-&gt;VAL (Current Value)</text>
    <text x="180" y="176" text-anchor="middle" font-size="11" fill="var(--text-muted)">Đếm lùi: N → N-1 → ... → 1 → 0</text>

    <rect x="30" y="200" width="300" height="35" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="180" y="222" text-anchor="middle" font-size="10.5" font-weight="600" fill="var(--text-primary)">Khi VAL về 0: Bật cờ COUNTFLAG &amp; Nạp lại LOAD</text>
  </g>

  <!-- Output & Interrupt -->
  <g transform="translate(680, 110)">
    <rect width="180" height="230" rx="10" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="90" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-green)">INTERRUPT &amp; FLAG</text>
    
    <rect x="15" y="60" width="150" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
    <text x="90" y="85" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-green)">SysTick_Handler</text>
    <text x="90" y="105" text-anchor="middle" font-size="9.5" fill="var(--text-muted)">Ngắt định thời 1ms (TICKINT=1)</text>

    <rect x="15" y="145" width="150" height="60" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="90" y="170" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">OS Sched Tick</text>
    <text x="90" y="190" text-anchor="middle" font-size="11" fill="var(--text-muted)">FreeRTOS Heartbeat</text>
  </g>

  <!-- Connections -->
  <path d="M 220 220 L 270 220" stroke="var(--bus-line)" stroke-width="2"/>
  <path d="M 630 220 L 680 220" stroke="var(--accent-green)" stroke-width="2"/>
</svg>"""

save_svg("bai05_systick_timer.svg", svg_systick)

# 3. Bai 06: General Purpose Timer Architecture
svg_timer_arch = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 460" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="940" height="460" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="470" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">KIẾN TRÚC KHỐI NGOẠI VI GENERAL PURPOSE TIMER (TIM2 - TIM5)</text>
  <text x="470" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Mối liên hệ giữa Time-base Generator (PSC, CNT, ARR) và 4 kênh Capture / Compare độc lập</text>

  <!-- Timebase Section -->
  <g transform="translate(40, 90)">
    <rect width="320" height="340" rx="10" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="160" y="32" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-blue)">TIME-BASE GENERATOR</text>
    
    <rect x="25" y="60" width="270" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="160" y="85" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">Prescaler (TIMx_PSC)</text>
    <text x="160" y="103" text-anchor="middle" font-size="9.5" fill="var(--text-muted)">Chia clock: CK_CNT = f_CK_PSC / (PSC + 1)</text>

    <rect x="25" y="145" width="270" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="160" y="170" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-blue)">Counter Register (TIMx_CNT)</text>
    <text x="160" y="188" text-anchor="middle" font-size="9.5" fill="var(--text-muted)">Bộ đếm 16-bit: Đếm lên (Up), xuống (Down), Center</text>

    <rect x="25" y="230" width="270" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="160" y="255" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-green)">Auto-Reload (TIMx_ARR)</text>
    <text x="160" y="273" text-anchor="middle" font-size="11" fill="var(--text-muted)">Giá trị ngưỡng chu kỳ tràn (Update Event UEV)</text>

    <text x="160" y="315" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-red)">Update Interrupt / DMA Request khi CNT = ARR</text>
  </g>

  <!-- Channels Section -->
  <g transform="translate(420, 90)">
    <rect width="480" height="340" rx="10" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="240" y="32" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-purple)">4 KÊNH CAPTURE / COMPARE (CH1 - CH4)</text>

    <!-- Channel 1 -->
    <g transform="translate(20, 60)">
      <rect width="440" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="20" y="25" font-size="13" font-weight="700" fill="var(--accent-purple)">CHANNEL 1</text>
      <text x="20" y="43" font-size="11" fill="var(--text-muted)">Thanh ghi CCR1: 0x4000 0034</text>
      <rect x="230" y="12" width="100" height="30" rx="4" fill="var(--accent-blue)" fill-opacity="0.2"/>
      <text x="280" y="32" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-blue)">TIMx_CH1 (Pin)</text>
      <text x="350" y="32" font-size="11" fill="var(--text-muted)">Input / PWM Out</text>
    </g>

    <!-- Channel 2 -->
    <g transform="translate(20, 125)">
      <rect width="440" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="20" y="25" font-size="13" font-weight="700" fill="var(--accent-purple)">CHANNEL 2</text>
      <text x="20" y="43" font-size="11" fill="var(--text-muted)">Thanh ghi CCR2: 0x4000 0038</text>
      <rect x="230" y="12" width="100" height="30" rx="4" fill="var(--accent-blue)" fill-opacity="0.2"/>
      <text x="280" y="32" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-blue)">TIMx_CH2 (Pin)</text>
      <text x="350" y="32" font-size="11" fill="var(--text-muted)">Input / PWM Out</text>
    </g>

    <!-- Channel 3 -->
    <g transform="translate(20, 190)">
      <rect width="440" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="20" y="25" font-size="13" font-weight="700" fill="var(--accent-purple)">CHANNEL 3</text>
      <text x="20" y="43" font-size="11" fill="var(--text-muted)">Thanh ghi CCR3: 0x4000 003C</text>
      <rect x="230" y="12" width="100" height="30" rx="4" fill="var(--accent-blue)" fill-opacity="0.2"/>
      <text x="280" y="32" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-blue)">TIMx_CH3 (Pin)</text>
      <text x="350" y="32" font-size="11" fill="var(--text-muted)">Input / PWM Out</text>
    </g>

    <!-- Channel 4 -->
    <g transform="translate(20, 255)">
      <rect width="440" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="20" y="25" font-size="13" font-weight="700" fill="var(--accent-purple)">CHANNEL 4</text>
      <text x="20" y="43" font-size="11" fill="var(--text-muted)">Thanh ghi CCR4: 0x4000 0040</text>
      <rect x="230" y="12" width="100" height="30" rx="4" fill="var(--accent-blue)" fill-opacity="0.2"/>
      <text x="280" y="32" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-blue)">TIMx_CH4 (Pin)</text>
      <text x="350" y="32" font-size="11" fill="var(--text-muted)">Input / PWM Out</text>
    </g>
  </g>

  <!-- Bus Link -->
  <path d="M 360 260 L 420 260" stroke="var(--bus-line)" stroke-width="3"/>
</svg>"""

save_svg("bai06_timer_architecture.svg", svg_timer_arch)

# 4. Bai 07: PWM Duty Cycle Waveforms
svg_pwm_duty = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 420" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="920" height="420" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="460" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">DẠNG SÓNG ĐIỀU CHẾ ĐỘ RỘNG XUNG PWM (PULSE WIDTH MODULATION)</text>
  <text x="460" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Biểu diễn điện áp ngõ ra tương đương theo tỷ lệ Duty Cycle (CCR / ARR)</text>

  <!-- 25% Duty Cycle -->
  <g transform="translate(60, 95)">
    <text x="0" y="25" font-size="14" font-weight="700" fill="var(--accent-blue)">Duty Cycle 25% (V_avg = 0.825V)</text>
    <polyline points="0,70 60,70 60,35 110,35 110,70 260,70 260,35 310,35 310,70 460,70 460,35 510,35 510,70 660,70 660,35 710,35 710,70 800,70" 
              fill="none" stroke="var(--accent-blue)" stroke-width="2.5"/>
    <line x1="0" y1="70" x2="800" y2="70" stroke="var(--wire-line)" stroke-width="1" stroke-dasharray="2,2"/>
  </g>

  <!-- 50% Duty Cycle -->
  <g transform="translate(60, 195)">
    <text x="0" y="25" font-size="14" font-weight="700" fill="var(--accent-green)">Duty Cycle 50% (V_avg = 1.650V)</text>
    <polyline points="0,70 60,70 60,35 160,35 160,70 260,70 260,35 360,35 360,70 460,70 460,35 560,35 560,70 660,70 660,35 760,35 760,70 800,70" 
              fill="none" stroke="var(--accent-green)" stroke-width="2.5"/>
    <line x1="0" y1="70" x2="800" y2="70" stroke="var(--wire-line)" stroke-width="1" stroke-dasharray="2,2"/>
  </g>

  <!-- 75% Duty Cycle -->
  <g transform="translate(60, 295)">
    <text x="0" y="25" font-size="14" font-weight="700" fill="var(--accent-amber)">Duty Cycle 75% (V_avg = 2.475V)</text>
    <polyline points="0,70 60,70 60,35 210,35 210,70 260,70 260,35 410,35 410,70 460,70 460,35 610,35 610,70 660,70 660,35 800,35" 
              fill="none" stroke="var(--accent-amber)" stroke-width="2.5"/>
    <line x1="0" y1="70" x2="800" y2="70" stroke="var(--wire-line)" stroke-width="1" stroke-dasharray="2,2"/>
  </g>
</svg>"""

save_svg("bai07_pwm_duty_cycle.svg", svg_pwm_duty)

# 5. Bai 10: Watchdog Timers (IWDG vs WWDG)
svg_watchdog = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 440" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="940" height="440" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="470" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">SO SÁNH BỘ GIÁM SÁT HỆ THỐNG: IWDG vs WWDG</text>
  <text x="470" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Phân biệt Independent Watchdog (Độc lập) và Window Watchdog (Cửa sổ ngắt an toàn)</text>

  <!-- IWDG Column -->
  <g transform="translate(50, 90)">
    <rect width="400" height="320" rx="10" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="200" y="32" text-anchor="middle" font-size="16" font-weight="700" fill="var(--accent-blue)">INDEPENDENT WATCHDOG (IWDG)</text>
    
    <rect x="20" y="55" width="360" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="35" y="82" font-size="12" font-weight="600" fill="var(--text-primary)">Nguồn Clock: LSI (~40kHz) Độc lập hoàn toàn</text>

    <rect x="20" y="110" width="360" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="35" y="137" font-size="12" font-weight="600" fill="var(--text-primary)">Đếm lùi 12-bit: Từ Reload về 0x000</text>

    <rect x="20" y="165" width="360" height="50" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="35" y="188" font-size="12" font-weight="600" fill="var(--text-primary)">Cơ chế nạp lại: Ghi 0xAAAA vào IWDG_KR</text>
    <text x="35" y="204" font-size="10" fill="var(--text-muted)">Cho phép reload bất cứ lúc nào trước khi chạm 0</text>

    <rect x="20" y="225" width="360" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
    <text x="35" y="252" font-size="12" font-weight="700" fill="var(--accent-red)">Nếu đếm về 0: KÍCH HOẠT HARD RESET MCU</text>

    <text x="200" y="295" text-anchor="middle" font-size="11" font-weight="600" fill="var(--text-muted)">Ứng dụng: Chống treo toàn bộ hệ thống / Nguồn cấp</text>
  </g>

  <!-- WWDG Column -->
  <g transform="translate(490, 90)">
    <rect width="400" height="320" rx="10" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
    <text x="200" y="32" text-anchor="middle" font-size="16" font-weight="700" fill="var(--accent-amber)">WINDOW WATCHDOG (WWDG)</text>

    <rect x="20" y="55" width="360" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="35" y="82" font-size="12" font-weight="600" fill="var(--text-primary)">Nguồn Clock: PCLK1 (APB1 Bus) Tần số cao</text>

    <rect x="20" y="110" width="360" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="35" y="137" font-size="12" font-weight="600" fill="var(--text-primary)">Đếm lùi 7-bit: T[6:0] (0x7F về 0x3F)</text>

    <rect x="20" y="165" width="360" height="50" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="35" y="188" font-size="12" font-weight="600" fill="var(--text-primary)">Vùng nạp hợp lệ: CHỈ GIỮA Window và 0x40</text>
    <text x="35" y="204" font-size="10" fill="var(--text-muted)">Reload quá sớm (&gt; W) hoặc quá muộn (≤ 0x3F) đều Reset!</text>

    <rect x="20" y="225" width="360" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="35" y="252" font-size="12" font-weight="700" fill="var(--accent-green)">Có ngắt sớm EWI (Early Wakeup Interrupt @ 0x40)</text>

    <text x="200" y="295" text-anchor="middle" font-size="11" font-weight="600" fill="var(--text-muted)">Ứng dụng: Giám sát chương trình chạy đúng nhịp thời gian</text>
  </g>
</svg>"""

save_svg("bai10_watchdog_comparison.svg", svg_watchdog)

# 6. Bai 11: ADC SAR 12-bit Structure
svg_adc_sar = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 440" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="940" height="440" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="470" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">KIẾN TRÚC BỘ CHUYỂN ĐỔI ADC 12-BIT SAR STM32F103</text>
  <text x="470" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Mạch lấy mẫu Sample &amp; Hold, Multiplexer 16 kênh và thuật toán xấp xỉ liên tiếp (SAR)</text>

  <!-- Input MUX -->
  <g transform="translate(40, 95)">
    <rect width="200" height="310" rx="10" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="100" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-blue)">ANALOG INPUT MUX</text>
    
    <rect x="20" y="55" width="160" height="35" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="77" text-anchor="middle" font-size="12" fill="var(--text-primary)">IN0 (PA0) .. IN3 (PA3)</text>

    <rect x="20" y="105" width="160" height="35" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="127" text-anchor="middle" font-size="12" fill="var(--text-primary)">IN4 (PA4) .. IN7 (PA7)</text>

    <rect x="20" y="155" width="160" height="35" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="177" text-anchor="middle" font-size="12" fill="var(--text-primary)">IN8 (PB0) .. IN9 (PB1)</text>

    <rect x="20" y="205" width="160" height="35" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="227" text-anchor="middle" font-size="12" fill="var(--text-primary)">IN16: Cảm biến nhiệt nội</text>

    <rect x="20" y="255" width="160" height="35" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="100" y="277" text-anchor="middle" font-size="12" fill="var(--text-primary)">IN17: Điện áp VREFINT 1.2V</text>
  </g>

  <!-- Sample & Hold and Comparator -->
  <g transform="translate(280, 110)">
    <rect width="360" height="280" rx="10" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="180" y="32" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-purple)">SAR CONVERTER ENGINE</text>
    
    <rect x="30" y="60" width="300" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="180" y="87" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">Khối lấy mẫu &amp; Giữ áp (Sample &amp; Hold - C_sample)</text>

    <rect x="30" y="120" width="300" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
    <text x="180" y="147" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-amber)">Bộ so sánh điện áp (Comparator)</text>

    <rect x="30" y="180" width="300" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="180" y="207" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">Mạng điện trở phân áp DAC phản hồi nội</text>

    <text x="180" y="250" text-anchor="middle" font-size="11" fill="var(--text-muted)">Thời gian chuyển đổi: Tconv = Ts + 12.5 chu kỳ ADC_CLK</text>
  </g>

  <!-- Output Registers -->
  <g transform="translate(680, 110)">
    <rect width="220" height="280" rx="10" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="110" y="32" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-green)">DATA REGISTERS</text>
    
    <rect x="15" y="65" width="190" height="55" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
    <text x="105" y="90" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-green)">ADC_DR (16-bit)</text>
    <text x="105" y="108" text-anchor="middle" font-size="11" fill="var(--text-muted)">Kết quả 12-bit (0..4095)</text>

    <rect x="15" y="140" width="190" height="50" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="105" y="165" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">Cờ ngắt EOC</text>
    <text x="105" y="181" text-anchor="middle" font-size="10" fill="var(--text-muted)">End of Conversion Interrupt</text>

    <rect x="15" y="205" width="190" height="50" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)"/>
    <text x="105" y="230" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-blue)">Kênh DMA Request</text>
    <text x="105" y="246" text-anchor="middle" font-size="10" fill="var(--text-muted)">Tự động lưu RAM liên tục</text>
  </g>

  <path d="M 240 250 L 280 250" stroke="var(--bus-line)" stroke-width="2"/>
  <path d="M 640 250 L 680 250" stroke="var(--bus-line)" stroke-width="2"/>
</svg>"""

save_svg("bai11_adc_sar_structure.svg", svg_adc_sar)

# 7. Bai 14: Circular Ring Buffer FIFO
svg_ring_buffer = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 440" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="920" height="440" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="460" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">CƠ CHẾ BỘ ĐỆM VÒNG TRÒN (CIRCULAR RING BUFFER FIFO)</text>
  <text x="460" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Xử lý không nghẽn ngõ vào UART Rx Interrupt với hai con trỏ Head (Ghi) và Tail (Đọc)</text>

  <!-- Linear Representation -->
  <g transform="translate(60, 110)">
    <rect width="800" height="150" rx="10" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="2"/>
    <text x="400" y="32" text-anchor="middle" font-size="14" font-weight="700" fill="var(--title-color)">MẢNG BỘ NHỚ RAM LIÊN TỤC: uint8_t buffer[BUFFER_SIZE]</text>

    <!-- Cells -->
    <g transform="translate(40, 55)">
      <rect x="0" y="0" width="85" height="50" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="42" y="30" text-anchor="middle" font-size="12" fill="var(--text-muted)">Idx 0</text>

      <rect x="85" y="0" width="85" height="50" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="127" y="30" text-anchor="middle" font-size="12" fill="var(--text-muted)">Idx 1</text>

      <rect x="170" y="0" width="85" height="50" fill="var(--accent-blue)" fill-opacity="0.2" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="212" y="30" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-blue)">DATA 2</text>

      <rect x="255" y="0" width="85" height="50" fill="var(--accent-blue)" fill-opacity="0.2" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="297" y="30" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-blue)">DATA 3</text>

      <rect x="340" y="0" width="85" height="50" fill="var(--accent-blue)" fill-opacity="0.2" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="382" y="30" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-blue)">DATA 4</text>

      <rect x="425" y="0" width="85" height="50" fill="var(--accent-green)" fill-opacity="0.2" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="467" y="30" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-green)">NEW</text>

      <rect x="510" y="0" width="85" height="50" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="552" y="30" text-anchor="middle" font-size="12" fill="var(--text-muted)">Idx 6</text>

      <rect x="595" y="0" width="85" height="50" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="637" y="30" text-anchor="middle" font-size="12" fill="var(--text-muted)">Idx 7</text>
    </g>

    <!-- Pointers -->
    <text x="252" y="135" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-purple)">▲ tail_ptr (Read)</text>
    <text x="507" y="135" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-green)">▲ head_ptr (Write)</text>
  </g>

  <!-- Equations -->
  <g transform="translate(60, 290)">
    <rect width="800" height="110" rx="10" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="40" y="35" font-size="14" font-weight="700" fill="var(--accent-blue)">NGUYÊN TẮC TOÁN HỌC ĐỊNH TUYẾN CHỈ SỐ:</text>
    <text x="40" y="65" font-size="13" fill="var(--text-primary)">• Ghi dữ liệu: buffer[head] = rx_data; head = (head + 1) % BUFFER_SIZE;</text>
    <text x="40" y="90" font-size="13" fill="var(--text-primary)">• Đọc dữ liệu: tx_data = buffer[tail]; tail = (tail + 1) % BUFFER_SIZE;</text>
    <text x="560" y="65" font-size="12" font-weight="700" fill="var(--accent-amber)">Rỗng: head == tail</text>
    <text x="560" y="90" font-size="12" font-weight="700" fill="var(--accent-red)">Đầy: (head + 1) % SIZE == tail</text>
  </g>
</svg>"""

save_svg("bai14_ring_buffer_fifo.svg", svg_ring_buffer)

# 8. Bai 21: FreeRTOS Synchronization (Queue & Semaphore)
svg_freertos_sync = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 440" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="940" height="440" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="470" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">CƠ CHẾ ĐỒNG BỘ HÓA VÀ TRUYỀN DỮ LIỆU ĐA NHIỆM TRONG FREERTOS</text>
  <text x="470" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Mô hình Hàng đợi (Queue), Đèn báo nhị phân (Binary Semaphore) và Khóa loại trừ Mutex</text>

  <!-- Queue Mechanism -->
  <g transform="translate(40, 95)">
    <rect width="860" height="150" rx="10" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="430" y="28" text-anchor="middle" font-size="15" font-weight="700" fill="var(--accent-blue)">FREERTOS MESSAGE QUEUE (TRUYỀN THEO BẢN SAO / COPY BY VALUE)</text>

    <!-- Sender Task -->
    <rect x="30" y="50" width="180" height="70" rx="8" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="120" y="78" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-green)">TASK SENDER</text>
    <text x="120" y="100" text-anchor="middle" font-size="11" fill="var(--text-muted)">xQueueSendToBack()</text>

    <!-- Queue Body -->
    <g transform="translate(260, 55)">
      <rect width="340" height="60" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <rect x="10" y="10" width="60" height="40" rx="4" fill="var(--accent-blue)" fill-opacity="0.3" stroke="var(--accent-blue)"/>
      <text x="40" y="35" text-anchor="middle" font-size="11" font-weight="600" fill="var(--text-primary)">Item 0</text>

      <rect x="80" y="10" width="60" height="40" rx="4" fill="var(--accent-blue)" fill-opacity="0.3" stroke="var(--accent-blue)"/>
      <text x="110" y="35" text-anchor="middle" font-size="11" font-weight="600" fill="var(--text-primary)">Item 1</text>

      <rect x="150" y="10" width="60" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="180" y="35" text-anchor="middle" font-size="11" fill="var(--text-muted)">Empty</text>

      <rect x="220" y="10" width="110" height="40" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="275" y="35" text-anchor="middle" font-size="11" fill="var(--text-muted)">Free Slots...</text>
    </g>

    <!-- Receiver Task -->
    <rect x="650" y="50" width="180" height="70" rx="8" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
    <text x="740" y="78" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-purple)">TASK RECEIVER</text>
    <text x="740" y="100" text-anchor="middle" font-size="11" fill="var(--text-muted)">xQueueReceive()</text>

    <path d="M 210 85 L 260 85" stroke="var(--bus-line)" stroke-width="2"/>
    <path d="M 600 85 L 650 85" stroke="var(--bus-line)" stroke-width="2"/>
  </g>

  <!-- Semaphore & Mutex Section -->
  <g transform="translate(40, 265)">
    <!-- Semaphore -->
    <rect x="0" y="0" width="415" height="150" rx="10" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
    <text x="207" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-amber)">BINARY SEMAPHORE (ĐỒNG BỘ SỰ KIỆN)</text>
    <text x="25" y="65" font-size="12" fill="var(--text-primary)">• ISR / Hardware Event mở khóa: xSemaphoreGiveFromISR()</text>
    <text x="25" y="95" font-size="12" fill="var(--text-primary)">• Task ngủ chờ sự kiện: xSemaphoreTake(sem, portMAX_DELAY)</text>
    <text x="25" y="125" font-size="11" fill="var(--text-muted)">⇒ Giải phóng hoàn toàn thời gian CPU khi chưa có ngắt</text>

    <!-- Mutex -->
    <rect x="445" y="0" width="415" height="150" rx="10" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="652" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-green)">MUTEX &amp; KẾ THỪA MỨC ƯU TIÊN</text>
    <text x="470" y="65" font-size="12" fill="var(--text-primary)">• Bảo vệ tài nguyên dùng chung (UART Console, I2C Bus...)</text>
    <text x="470" y="95" font-size="12" fill="var(--text-primary)">• Cơ chế Priority Inheritance chống nghịch đảo quyền ưu tiên</text>
    <text x="470" y="125" font-size="11" fill="var(--accent-red)">Tuyệt đối không được gọi Mutex bên trong ngắt ISR!</text>
  </g>
</svg>"""

save_svg("bai21_freertos_sync.svg", svg_freertos_sync)

print("ALL EXTRA SVGS SUCCESSFULLY GENERATED!")
