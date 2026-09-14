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
# 1. BÀI 10: IWDG BLOCK DIAGRAM (ST RM0008 Figure 149)
# ==============================================================================
svg_iwdg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 680" width="100%" height="100%">
{COMMON_STYLES}
  <!-- Background Canvas -->
  <rect width="1140" height="680" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Top Title Bar -->
  <rect x="25" y="16" width="1090" height="64" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="45" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 17.2</text>
  <text x="45" y="64" font-size="13" font-weight="600" fill="var(--accent-blue)">Figure 149: Independent watchdog block diagram (Sơ đồ khối chức năng bộ giám sát độc lập IWDG)</text>
  <rect x="960" y="28" width="135" height="36" rx="6" fill="#00205b"/>
  <text x="1027" y="51" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left: Bus Interface & Control Registers (X: 35 -> 290) -->
  <g transform="translate(35, 100)">
    <rect width="255" height="520" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="127" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">BUS INTERFACE &amp; REGISTERS</text>
    <text x="127" y="46" text-anchor="middle" font-size="11" fill="var(--text-muted)">Miền Nguồn VDD (APB1 Bus Interface)</text>

    <!-- Key Register (IWDG_KR) -->
    <g transform="translate(15, 65)">
      <rect width="225" height="130" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="112" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-blue)">KEY REGISTER (IWDG_KR)</text>
      
      <text x="12" y="48" font-size="10" font-weight="700" fill="var(--accent-green)">• 0x5555: Mở khóa cấu hình PR &amp; RLR</text>
      <text x="12" y="68" font-size="10" font-weight="700" fill="var(--accent-blue)">• 0xAAAA: Nuôi chó (Nạp lại Counter)</text>
      <text x="12" y="88" font-size="10" font-weight="700" fill="var(--accent-red)">• 0xCCCC: Kích hoạt IWDG bắt đầu chạy</text>
      <line x1="10" y1="98" x2="215" y2="98" stroke="var(--card-border)"/>
      <text x="112" y="116" text-anchor="middle" font-size="9" fill="var(--text-muted)">Chống ghi đè vô ý khi code bị treo</text>
    </g>

    <!-- Prescaler Register (IWDG_PR) -->
    <g transform="translate(15, 210)">
      <rect width="225" height="80" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <text x="112" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)">PRESCALER REGISTER (IWDG_PR)</text>
      <text x="112" y="40" text-anchor="middle" font-size="10" class="mono">PR[2:0]: 3-bit chia tần số</text>
      <text x="112" y="58" text-anchor="middle" font-size="9" fill="var(--text-muted)">Hệ số chia: /4, /8, /16, /32, /64, /128, /256</text>
      <text x="112" y="72" text-anchor="middle" font-size="8" fill="var(--accent-amber)">(Chỉ ghi được khi đã mở khóa 0x5555)</text>
    </g>

    <!-- Reload Register (IWDG_RLR) -->
    <g transform="translate(15, 305)">
      <rect width="225" height="85" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
      <text x="112" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)">RELOAD REGISTER (IWDG_RLR)</text>
      <text x="112" y="40" text-anchor="middle" font-size="10" class="mono">RL[11:0]: 12-bit giá trị nạp</text>
      <text x="112" y="58" text-anchor="middle" font-size="9" fill="var(--text-muted)">Khoảng giá trị: 0x000 → 0xFFF (0..4095)</text>
      <text x="112" y="74" text-anchor="middle" font-size="8" fill="var(--accent-amber)">(Quy định chu kỳ timeout tối đa)</text>
    </g>

    <!-- Status Register (IWDG_SR) -->
    <g transform="translate(15, 405)">
      <rect width="225" height="95" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
      <text x="112" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-purple)">STATUS REGISTER (IWDG_SR)</text>
      <text x="12" y="44" font-size="10" fill="var(--text-primary)">• Bit 0 (PVU): Đang cập nhật Prescaler</text>
      <text x="12" y="64" font-size="10" fill="var(--text-primary)">• Bit 1 (RVU): Đang nạp lại Reload</text>
      <text x="112" y="84" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-purple)">Phải đợi cờ = 0 trước khi ghi tiếp!</text>
    </g>
  </g>

  <!-- Middle: Isolated Clock Domain & 12-bit Downcounter Core (X: 330 -> 720) -->
  <g transform="translate(330, 100)">
    <rect width="390" height="520" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="195" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-blue)">ISOLATED CORE DOMAIN (MIỀN NGUỒN RIÊNG)</text>
    <text x="195" y="46" text-anchor="middle" font-size="11" fill="var(--text-muted)">Hoạt động độc lập ngay cả khi CPU ở chế độ Sleep/Stop/Standby</text>

    <!-- Clock Source: LSI -->
    <g transform="translate(20, 65)">
      <rect width="350" height="70" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
      <text x="175" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-amber)">LOW-SPEED INTERNAL RC OSCILLATOR (LSI)</text>
      <text x="175" y="44" text-anchor="middle" font-size="13" font-weight="900" fill="var(--title-color)">Tần Số Danh Định: ~40kHz (30kHz - 60kHz)</text>
      <text x="175" y="60" text-anchor="middle" font-size="9" fill="var(--text-muted)">Hoàn toàn độc lập với thạch anh chính HSE và xung nhịp APB</text>
    </g>

    <!-- Arrow from LSI down to Prescaler -->
    <path d="M 195 135 L 195 165" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
    <text x="205" y="154" font-size="9" font-weight="700" fill="var(--bus-line)">f_LSI</text>

    <!-- 8-bit Prescaler -->
    <g transform="translate(20, 165)">
      <rect width="350" height="85" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="175" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-blue)">8-BIT PRESCALER (BỘ CHIA TẦN SỐ)</text>
      <text x="175" y="46" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Hệ số chia cấu hình từ IWDG_PR: /4, /8.. /256</text>
      <text x="175" y="66" text-anchor="middle" font-size="10" fill="var(--text-muted)">Ví dụ: 40kHz / 64 = 625Hz (Mỗi nhịp đếm T_tick = 1.6ms)</text>
    </g>

    <!-- Arrow down to Downcounter -->
    <path d="M 195 250 L 195 285" fill="none" stroke="var(--bus-line)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
    <text x="205" y="272" font-size="9" font-weight="700" fill="var(--bus-line)">CK_CNT</text>

    <!-- 12-bit Downcounter Unit -->
    <g transform="translate(20, 285)">
      <rect width="350" height="135" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="175" y="26" text-anchor="middle" font-size="13" font-weight="900" fill="var(--accent-green)">12-BIT DOWNCOUNTER (BỘ ĐẾM LÙI)</text>
      
      <rect x="25" y="40" width="300" height="40" rx="4" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
      <text x="175" y="65" text-anchor="middle" font-size="13" font-weight="900" fill="var(--title-color)">Giá trị đếm: RLR[11:0] → ... → 0x000</text>

      <text x="175" y="102" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-blue)">• Lệnh nạp lại: Ghi 0xAAAA vào IWDG_KR</text>
      <text x="175" y="120" text-anchor="middle" font-size="9" fill="var(--text-muted)">Bộ đếm lập tức nhảy về giá trị ban đầu cài trong IWDG_RLR</text>
    </g>

    <!-- Formula Box -->
    <g transform="translate(20, 435)">
      <rect width="350" height="70" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="175" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-amber)">CÔNG THỨC THỜI GIAN TIMEOUT IWDG:</text>
      <text x="175" y="42" text-anchor="middle" font-size="12" font-weight="900" fill="var(--title-color)">T_timeout = (Prescaler × (RLR + 1)) / f_LSI</text>
      <text x="175" y="58" text-anchor="middle" font-size="9" fill="var(--accent-green)">Ví dụ Timeout 1.0s: Prescaler = 64, RLR = 624</text>
    </g>
  </g>

  <!-- Right: Zero Detector & Reset Generation to RCC (X: 760 -> 1100) -->
  <g transform="translate(760, 100)">
    <rect width="340" height="520" rx="8" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="2"/>
    <text x="170" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-red)">RESET GENERATION LOGIC</text>
    <text x="170" y="46" text-anchor="middle" font-size="11" fill="var(--text-muted)">Mạch So Sánh &amp; Tạo Tín Hiệu Reset Cứng</text>

    <!-- Zero Comparator -->
    <g transform="translate(20, 140)">
      <!-- Line from Downcounter into Comparator -->
      <path d="M -50 45 L 0 45" fill="none" stroke="var(--wire-line)" stroke-width="2.5" marker-end="url(#arrow)"/>
      <rect width="300" height="90" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-red)" stroke-width="2"/>
      <text x="150" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-red)">ZERO COMPARATOR (SO SÁNH 0)</text>
      <text x="150" y="48" text-anchor="middle" font-size="12" font-weight="900" fill="var(--title-color)">Điều kiện: Counter == 0x000</text>
      <text x="150" y="70" text-anchor="middle" font-size="10" fill="var(--text-muted)">Xảy ra khi phần mềm bị treo quá thời hạn cho ăn</text>
    </g>

    <!-- Arrow down to Reset pulse -->
    <path d="M 170 230 L 170 270" fill="none" stroke="var(--accent-red)" stroke-width="2.5" marker-end="url(#arrow-red)"/>

    <!-- Reset Pulse Generator -->
    <g transform="translate(20, 270)">
      <rect width="300" height="85" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="150" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--title-color)">RESET PULSE GENERATOR</text>
      <text x="150" y="46" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-red)">Tạo xung Reset tích cực mức thấp</text>
      <text x="150" y="66" text-anchor="middle" font-size="10" fill="var(--text-muted)">Độ rộng xung tối thiểu: ~8 chu kỳ LSI</text>
    </g>

    <!-- Output to RCC Controller -->
    <g transform="translate(20, 395)">
      <path d="M 170 -40 L 170 0" fill="none" stroke="var(--accent-red)" stroke-width="3" marker-end="url(#arrow-red)"/>
      <rect width="300" height="105" rx="8" fill="#00205b" stroke="#00a3e0" stroke-width="2"/>
      <text x="150" y="30" text-anchor="middle" font-size="14" font-weight="900" fill="#ffffff">RCC RESET CONTROLLER</text>
      <text x="150" y="52" text-anchor="middle" font-size="11" font-weight="700" fill="#38bdf8">KÍCH HOẠT HARD RESET TOÀN BỘ CHIP</text>
      <line x1="20" y1="62" x2="280" y2="62" stroke="#1e293b"/>
      <text x="150" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#f87171">Bật cờ IWDGRSTF trong thanh ghi RCC_CSR</text>
      <text x="150" y="94" text-anchor="middle" font-size="9" fill="#94a3b8">(Cho phép firmware nhận biết nguyên nhân Reset)</text>
    </g>
  </g>
</svg>"""

save_svg("bai10_iwdg_block_diagram.svg", svg_iwdg)

# ==============================================================================
# 2. BÀI 10: WWDG BLOCK DIAGRAM & TIMING (ST RM0008 Figure 150 & 151)
# ==============================================================================
svg_wwdg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 720" width="100%" height="100%">
{COMMON_STYLES}
  <!-- Background Canvas -->
  <rect width="1180" height="720" rx="12" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>

  <!-- Top Title Bar -->
  <rect x="25" y="16" width="1130" height="64" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
  <text x="45" y="42" font-size="17" font-weight="800" fill="var(--title-color)">STMicroelectronics RM0008 Reference Manual — Section 18.2 &amp; 18.3</text>
  <text x="45" y="64" font-size="13" font-weight="600" fill="var(--accent-amber)">Figure 150 &amp; 151: Window watchdog block diagram &amp; timing window (Sơ đồ khối và cửa sổ thời gian WWDG)</text>
  <rect x="1000" y="28" width="135" height="36" rx="6" fill="#00205b"/>
  <text x="1067" y="51" text-anchor="middle" font-size="12" font-weight="800" fill="#ffffff">STM32F103</text>

  <!-- Left: Clock Source & Prescaler (X: 35 -> 280) -->
  <g transform="translate(35, 95)">
    <rect width="245" height="360" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="122" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">CLOCK &amp; PRESCALERS</text>
    <text x="122" y="46" text-anchor="middle" font-size="11" fill="var(--text-muted)">Nguồn Xung Từ Bus APB1</text>

    <!-- PCLK1 Clock Input -->
    <g transform="translate(15, 65)">
      <rect width="215" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
      <text x="107" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-blue)">PCLK1 CLOCK (APB1 BUS)</text>
      <text x="107" y="44" text-anchor="middle" font-size="12" font-weight="900" fill="var(--title-color)">Tối Đa: 36.0 MHz</text>
      <text x="107" y="56" text-anchor="middle" font-size="9" fill="var(--text-muted)">(Độ chính xác thạch anh rất cao)</text>
    </g>

    <!-- Arrow down to 4096 divider -->
    <path d="M 122 130 L 122 155" fill="none" stroke="var(--bus-line)" stroke-width="2" marker-end="url(#arrow-blue)"/>

    <!-- Fixed Divider /4096 -->
    <g transform="translate(15, 155)">
      <rect width="215" height="60" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="107" y="24" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)">BỘ CHIA CỐ ĐỊNH / 4096</text>
      <text x="107" y="44" text-anchor="middle" font-size="10" fill="var(--text-muted)">PCLK1 / 4096 = 8.789 kHz (ở 36MHz)</text>
    </g>

    <!-- Arrow down to Timebase Prescaler -->
    <path d="M 122 215 L 122 240" fill="none" stroke="var(--bus-line)" stroke-width="2" marker-end="url(#arrow-blue)"/>

    <!-- Configurable Timebase Prescaler WDGTB -->
    <g transform="translate(15, 240)">
      <rect width="215" height="100" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
      <text x="107" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-amber)">WDGTB[1:0] PRESCALER</text>
      <text x="107" y="42" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">Bộ chia 2-bit trong WWDG_CFR:</text>
      <text x="15" y="62" font-size="9" fill="var(--text-muted)">• 00: /1  |  • 01: /2</text>
      <text x="15" y="78" font-size="9" fill="var(--text-muted)">• 10: /4  |  • 11: /8</text>
      <text x="107" y="94" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-blue)">f_WWDG = (PCLK1 / 4096) / 2^WDGTB</text>
    </g>
  </g>

  <!-- Middle: Registers & 7-bit Counter (X: 305 -> 720) -->
  <g transform="translate(305, 95)">
    <rect width="415" height="360" rx="8" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="2"/>
    <text x="207" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-amber)">WWDG REGISTERS &amp; 7-BIT COUNTER CORE</text>

    <!-- Window Register W[6:0] -->
    <g transform="translate(20, 50)">
      <rect width="375" height="80" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
      <text x="187" y="24" text-anchor="middle" font-size="12" font-weight="800" fill="var(--accent-purple)">7-BIT WINDOW REGISTER: W[6:0]</text>
      <text x="187" y="44" text-anchor="middle" font-size="11" font-weight="700" fill="var(--title-color)">Nằm trong thanh ghi cấu hình WWDG_CFR (Bits [6:0])</text>
      <text x="187" y="64" text-anchor="middle" font-size="10" fill="var(--accent-purple)">Cài đặt ngưỡng trên của cửa sổ cho phép nạp lại (Ví dụ: 0x50)</text>
    </g>

    <!-- 7-bit Downcounter T[6:0] -->
    <g transform="translate(20, 145)">
      <rect width="375" height="110" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="2"/>
      <text x="187" y="24" text-anchor="middle" font-size="13" font-weight="900" fill="var(--accent-green)">7-BIT DOWNCOUNTER: T[6:0] (WWDG_CR)</text>
      
      <g transform="translate(20, 38)">
        <rect width="60" height="36" rx="4" fill="#00205b"/>
        <text x="30" y="18" text-anchor="middle" font-size="10" font-weight="800" fill="#ffffff">Bit 7</text>
        <text x="30" y="30" text-anchor="middle" font-size="9" fill="#38bdf8">WDGA</text>

        <rect x="70" width="60" height="36" rx="4" fill="#dc2626"/>
        <text x="100" y="18" text-anchor="middle" font-size="10" font-weight="800" fill="#ffffff">Bit 6 (T6)</text>
        <text x="100" y="30" text-anchor="middle" font-size="9" fill="#fee2e2">MSB</text>

        <rect x="140" width="195" height="36" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
        <text x="237" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="var(--title-color)">Bits [5:0]: T5..T0</text>
        <text x="237" y="30" text-anchor="middle" font-size="9" fill="var(--text-muted)">Giá trị đếm lùi: 0x3F → 0x00</text>
      </g>

      <text x="187" y="98" text-anchor="middle" font-size="9" font-weight="700" fill="var(--title-color)">Bộ đếm chạy từ 0x7F về 0x3F (Tổng cộng 64 nhịp)</text>
    </g>

    <!-- Early Wakeup Interrupt (EWI) -->
    <g transform="translate(20, 270)">
      <rect width="375" height="75" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
      <text x="187" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-blue)">EARLY WAKEUP INTERRUPT (EWI - Bit 9 CFR)</text>
      <text x="187" y="42" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-green)">Kích hoạt ngắt khi Counter chạm đúng mốc 0x40</text>
      <text x="187" y="60" text-anchor="middle" font-size="9" fill="var(--text-muted)">Cứu vãn dữ liệu khẩn cấp hoặc ghi Blackbox log trước khi sập nguồn</text>
    </g>
  </g>

  <!-- Right: Dual Comparator Logic & Reset (X: 745 -> 1145) -->
  <g transform="translate(745, 95)">
    <rect width="400" height="360" rx="8" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="2"/>
    <text x="200" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--accent-red)">DUAL COMPARATOR &amp; RESET CONTROLLER</text>

    <!-- Comparator 1: Too early refresh -->
    <g transform="translate(15, 50)">
      <rect width="370" height="85" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
      <text x="185" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-red)">1. BỘ SO SÁNH CỬA SỔ (TOO EARLY REFRESH)</text>
      <text x="185" y="42" text-anchor="middle" font-size="11" font-weight="900" fill="var(--title-color)">Nếu phần mềm nạp lại khi T[6:0] &gt; W[6:0]</text>
      <text x="185" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-red)">→ KÍCH HOẠT HARD RESET NGAY LẬP TỨC!</text>
      <text x="185" y="76" text-anchor="middle" font-size="8" fill="var(--text-muted)">(Ngăn chặn code bị lỗi lặp Refresh liên tục)</text>
    </g>

    <!-- Comparator 2: Timeout when T6 drops to 0 -->
    <g transform="translate(15, 145)">
      <rect width="370" height="85" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
      <text x="185" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="var(--accent-red)">2. BỘ PHÁT HIỆN TRÀN (TIMEOUT - TOO LATE)</text>
      <text x="185" y="42" text-anchor="middle" font-size="11" font-weight="900" fill="var(--title-color)">Khi Counter đếm lùi từ 0x40 xuống 0x3F (Bit T6 = 0)</text>
      <text x="185" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-red)">→ KÍCH HOẠT HARD RESET DO HẾT GIỜ!</text>
      <text x="185" y="76" text-anchor="middle" font-size="8" fill="var(--text-muted)">(Quá hạn cho ăn do phần mềm bị kẹt vòng lặp)</text>
    </g>

    <!-- OR Gate to Reset Output -->
    <g transform="translate(15, 245)">
      <rect width="370" height="100" rx="6" fill="#00205b" stroke="#00a3e0" stroke-width="2"/>
      <text x="185" y="28" text-anchor="middle" font-size="13" font-weight="900" fill="#ffffff">WWDG RESET OUTPUT (RCC)</text>
      <text x="185" y="50" text-anchor="middle" font-size="11" font-weight="700" fill="#f87171">Gửi xung Reset đến Bộ Điều Khiển RCC</text>
      <line x1="20" y1="62" x2="350" y2="62" stroke="#1e293b"/>
      <text x="185" y="80" text-anchor="middle" font-size="10" font-weight="700" fill="#38bdf8">Cờ WWDGRSTF trong thanh ghi RCC_CSR được bật lên 1</text>
      <text x="185" y="94" text-anchor="middle" font-size="9" fill="#94a3b8">Đồng thời phát ngắt WWDG_IRQn đến NVIC (tại mốc 0x40)</text>
    </g>
  </g>

  <!-- Bottom: Window Watchdog Timing Diagram (RM0008 Figure 151) (Y: 475 -> 705) -->
  <g transform="translate(35, 475)">
    <rect width="1110" height="230" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="555" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="var(--title-color)">ST RM0008 FIGURE 151: GIẢN ĐỒ THỜI GIAN CỬA SỔ WWDG (WINDOW WATCHDOG TIMING)</text>

    <!-- Horizontal Timing Bar -->
    <g transform="translate(40, 50)">
      <!-- Zone 1: Refresh Forbidden (0x7F to Window W) -->
      <rect x="0" y="20" width="360" height="60" rx="6" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
      <text x="180" y="46" text-anchor="middle" font-size="12" font-weight="900" fill="#b91c1c">VÙNG CẤM CHO ĂN (TOO EARLY)</text>
      <text x="180" y="65" text-anchor="middle" font-size="10" font-weight="700" fill="#dc2626">Làm mới ở đây → RESET NGAY LẬP TỨC!</text>

      <!-- Zone 2: Valid Window (Window W to 0x40) -->
      <rect x="360" y="20" width="380" height="60" rx="6" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
      <text x="550" y="46" text-anchor="middle" font-size="13" font-weight="900" fill="#047857">CỬA SỔ NẠP HỢP LỆ (REFRESH WINDOW)</text>
      <text x="550" y="65" text-anchor="middle" font-size="10" font-weight="700" fill="#059669">✔ NẠP LẠI AN TOÀN TRONG KHOẢNG NÀY!</text>

      <!-- Zone 3: Timeout Zone (0x3F to 0x00) -->
      <rect x="740" y="20" width="290" height="60" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
      <text x="885" y="46" text-anchor="middle" font-size="12" font-weight="900" fill="#b91c1c">HẾT GIỜ (TOO LATE / TIMEOUT)</text>
      <text x="885" y="65" text-anchor="middle" font-size="10" font-weight="700" fill="#dc2626">T6 = 0 → RESET NGAY LẬP TỨC!</text>

      <!-- Ticks and Markers -->
      <!-- Max Counter Tick (0x7F) -->
      <line x1="0" y1="10" x2="0" y2="85" stroke="var(--wire-line)" stroke-width="2"/>
      <text x="0" y="5" text-anchor="middle" font-size="11" font-weight="800" fill="var(--title-color)">0x7F (Max)</text>

      <!-- Window W Tick -->
      <line x1="360" y1="10" x2="360" y2="85" stroke="#7c3aed" stroke-width="2.5" stroke-dasharray="4,4"/>
      <text x="360" y="5" text-anchor="middle" font-size="12" font-weight="900" fill="#7c3aed">Window Value W[6:0]</text>

      <!-- 0x40 EWI Tick -->
      <line x1="740" y1="10" x2="740" y2="85" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="4,4"/>
      <text x="740" y="5" text-anchor="middle" font-size="12" font-weight="900" fill="#0284c7">0x40 (Ngắt EWI)</text>

      <!-- 0x3F Tick -->
      <line x1="1030" y1="10" x2="1030" y2="85" stroke="#dc2626" stroke-width="2"/>
      <text x="1030" y="5" text-anchor="middle" font-size="11" font-weight="800" fill="#dc2626">0x3F (Reset)</text>
    </g>

    <!-- Explanation Box at Bottom -->
    <g transform="translate(40, 150)">
      <rect width="1030" height="60" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="15" y="22" font-size="11" font-weight="800" fill="var(--accent-blue)">Quy Tắc Vận Hành Window Watchdog (WWDG Rule):</text>
      <text x="15" y="38" font-size="10" fill="var(--text-primary)">1. Nếu cho ăn quá sớm (khi Counter còn lớn hơn ngưỡng W): Bị coi là chạy sai nhịp độ thời gian → Kích hoạt Reset cứng ngay!</text>
      <text x="15" y="52" font-size="10" fill="var(--text-primary)">2. Nếu cho ăn quá trễ (khi Counter giảm qua 0x40 xuống 0x3F): Bị coi là phần mềm bị treo đơ → Kích hoạt Reset do hết giờ!</text>
    </g>
  </g>
</svg>"""

save_svg("bai10_wwdg_block_diagram.svg", svg_wwdg)

print("SUCCESS: BAI 10 RM0008 SCHEMATICS BUILT PERFECTLY!")
