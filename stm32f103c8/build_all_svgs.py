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
        --box-blue: #eff6ff;
        --box-green: #ecfdf5;
        --box-amber: #fffbeb;
        --box-purple: #f5f3ff;
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
          --accent-blue: #38bdf8;
          --accent-green: #34d399;
          --accent-amber: #fbbf24;
          --accent-red: #f87171;
          --accent-purple: #a78bfa;
          --wire-line: #475569;
          --box-blue: #1e293b;
          --box-green: #064e3b;
          --box-amber: #78350f;
          --box-purple: #2e1065;
        }
      }

      .canvas-bg { fill: var(--canvas-bg); stroke: var(--canvas-border); stroke-width: 2; rx: 16; }
      .title-text { fill: var(--title-color); font-weight: 800; font-size: 20px; text-anchor: middle; font-family: 'Segoe UI', Arial, sans-serif; }
      .subtitle-text { fill: var(--subtitle-color); font-weight: 600; font-size: 13px; text-anchor: middle; font-family: 'Segoe UI', Arial, sans-serif; }
      .card-box { fill: var(--card-bg); stroke: var(--card-border); stroke-width: 1.5; rx: 10; }
      .txt-title { fill: var(--text-primary); font-weight: 700; font-size: 13px; font-family: 'Segoe UI', Arial, sans-serif; }
      .txt-desc { fill: var(--text-muted); font-size: 11px; font-weight: 500; font-family: 'Segoe UI', Arial, sans-serif; }
      .wire { stroke: var(--wire-line); stroke-width: 2; fill: none; }
      .wire-arrow { fill: var(--wire-line); }
      .tag-blue { fill: #0284c7; font-weight: 700; font-size: 11px; font-family: monospace; }
    </style>
    <filter id="shadowLight" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.08"/>
    </filter>
"""

# ==============================================================================
# 1. BÀI 02: CẤU TRÚC VẬT LÝ CHÂN GPIO STM32 (PULL-UP, DIODE, PMOS, NMOS, SCHMITT)
# ==============================================================================
svg_bai02_gpio = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" class="wire-arrow"/>
    </marker>
  </defs>

  <rect x="10" y="10" width="940" height="500" class="canvas-bg"/>
  <text x="480" y="45" class="title-text">CẤU TRÚC ĐIỆN TỬ VẬT LÝ CHÂN I/O STM32F103 (GPIO PAD)</text>
  <text x="480" y="70" class="subtitle-text">Mô hình phân tích transistor P-MOS, N-MOS, Diodes kẹp bảo vệ và Schmitt Trigger</text>

  <!-- Khối vi mạch chân I/O -->
  <rect x="140" y="95" width="760" height="390" class="card-box" stroke-dasharray="6,4"/>
  <text x="160" y="120" font-size="12" font-weight="bold" fill="var(--accent-blue)">STM32 I/O INTERNAL STRUCTURE (RM0008)</text>

  <!-- Chân Kim loại Ngoài (PAD) -->
  <rect x="30" y="250" width="90" height="60" rx="8" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2" filter="url(#shadowLight)"/>
  <text x="75" y="278" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle">PAD</text>
  <text x="75" y="296" font-size="11" font-weight="600" fill="#e0f2fe" text-anchor="middle">(Chân Pin I/O)</text>

  <!-- Đường dẫn từ Pad vào trong -->
  <line x1="120" y1="280" x2="800" y2="280" stroke="#0284c7" stroke-width="4"/>

  <!-- Khối Diode bảo vệ kẹp áp -->
  <g transform="translate(200, 150)">
    <rect x="0" y="0" width="130" height="50" rx="8" fill="var(--box-amber)" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="65" y="24" font-size="11" font-weight="700" fill="var(--text-primary)" text-anchor="middle">Diode Kẹp VDD</text>
    <text x="65" y="40" font-size="10" font-weight="600" fill="var(--accent-amber)" text-anchor="middle">Chống quá áp >3.3V</text>
    <line x1="65" y1="50" x2="65" y2="130" class="wire"/>
  </g>

  <g transform="translate(200, 360)">
    <rect x="0" y="0" width="130" height="50" rx="8" fill="var(--box-amber)" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="65" y="24" font-size="11" font-weight="700" fill="var(--text-primary)" text-anchor="middle">Diode Kẹp VSS</text>
    <text x="65" y="40" font-size="10" font-weight="600" fill="var(--accent-amber)" text-anchor="middle">Chống điện áp âm &lt;0V</text>
    <line x1="65" y1="0" x2="65" y2="-80" class="wire"/>
  </g>

  <!-- Khối Điện trở kéo Pull-up / Pull-down -->
  <g transform="translate(370, 130)">
    <rect x="0" y="0" width="150" height="70" rx="8" fill="var(--box-purple)" stroke="#8b5cf6" stroke-width="1.5"/>
    <text x="75" y="25" font-size="12" font-weight="700" fill="var(--text-primary)" text-anchor="middle">Pull-up (40kΩ)</text>
    <text x="75" y="45" font-size="10" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Điều khiển bởi ODR</text>
    <text x="75" y="60" font-size="10" font-weight="700" fill="var(--accent-purple)" text-anchor="middle">Kéo lên 3.3V</text>
    <line x1="75" y1="70" x2="75" y2="150" class="wire"/>
  </g>

  <g transform="translate(370, 350)">
    <rect x="0" y="0" width="150" height="70" rx="8" fill="var(--box-purple)" stroke="#8b5cf6" stroke-width="1.5"/>
    <text x="75" y="25" font-size="12" font-weight="700" fill="var(--text-primary)" text-anchor="middle">Pull-down (40kΩ)</text>
    <text x="75" y="45" font-size="10" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Điều khiển bởi ODR</text>
    <text x="75" y="60" font-size="10" font-weight="700" fill="var(--accent-purple)" text-anchor="middle">Kéo xuống GND</text>
    <line x1="75" y1="0" x2="75" y2="-70" class="wire"/>
  </g>

  <!-- Khối Đệm Ngõ Ra Output Driver (Push-Pull vs Open-Drain) -->
  <g transform="translate(560, 140)">
    <rect x="0" y="0" width="170" height="120" rx="8" fill="var(--box-green)" stroke="#10b981" stroke-width="1.5"/>
    <text x="85" y="25" font-size="12" font-weight="800" fill="#059669" text-anchor="middle">OUTPUT DRIVER</text>
    <rect x="15" y="38" width="140" height="30" rx="4" fill="var(--card-bg)" stroke="#10b981"/>
    <text x="85" y="58" font-size="11" font-weight="700" fill="var(--text-primary)" text-anchor="middle">P-MOS Transistor</text>
    <rect x="15" y="76" width="140" height="30" rx="4" fill="var(--card-bg)" stroke="#10b981"/>
    <text x="85" y="96" font-size="11" font-weight="700" fill="var(--text-primary)" text-anchor="middle">N-MOS Transistor</text>
    <line x1="85" y1="120" x2="85" y2="140" class="wire"/>
  </g>

  <!-- Khối Đọc Ngõ Vào Schmitt Trigger -->
  <g transform="translate(560, 310)">
    <rect x="0" y="0" width="170" height="100" rx="8" fill="var(--box-blue)" stroke="#0284c7" stroke-width="1.5"/>
    <text x="85" y="26" font-size="12" font-weight="800" fill="#0284c7" text-anchor="middle">INPUT CIRCUITRY</text>
    <rect x="15" y="38" width="140" height="48" rx="4" fill="var(--card-bg)" stroke="#0284c7"/>
    <text x="85" y="58" font-size="11" font-weight="700" fill="var(--text-primary)" text-anchor="middle">Schmitt Trigger</text>
    <text x="85" y="74" font-size="9.5" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Lọc nhiễu sườn xung</text>
    <line x1="85" y1="0" x2="85" y2="-30" class="wire"/>
    <!-- Đường đi vào IDR -->
    <line x1="170" y1="62" x2="220" y2="62" class="wire" marker-end="url(#arrow)"/>
  </g>

  <!-- Thanh ghi IDR -->
  <g transform="translate(790, 345)">
    <rect x="0" y="0" width="95" height="55" rx="6" fill="#0284c7" filter="url(#shadowLight)"/>
    <text x="47" y="24" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">GPIOx_IDR</text>
    <text x="47" y="42" font-size="9.5" font-weight="600" fill="#bae6fd" text-anchor="middle">(Input Data)</text>
  </g>

  <!-- Thanh ghi ODR -->
  <g transform="translate(745, 170)">
    <rect x="0" y="0" width="95" height="55" rx="6" fill="#059669" filter="url(#shadowLight)"/>
    <text x="47" y="24" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">GPIOx_ODR</text>
    <text x="47" y="42" font-size="9.5" font-weight="600" fill="#d1fae5" text-anchor="middle">(Output Data)</text>
    <line x1="0" y1="28" x2="-15" y2="28" class="wire" marker-end="url(#arrow)"/>
  </g>

</svg>"""

save_svg("bai02_gpio_structure.svg", svg_bai02_gpio)

# ==============================================================================
# 2. BÀI 02: KỸ THUẬT BIT-BANDING (REGION VS ALIAS)
# ==============================================================================
svg_bai02_bitband = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 420" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" class="wire-arrow"/>
    </marker>
  </defs>

  <rect x="10" y="10" width="900" height="400" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">CƠ CHẾ ĐỊNH ĐỊA CHỈ NGUYÊN TỬ BIT-BANDING (CORTEX-M3)</text>
  <text x="460" y="65" class="subtitle-text">Ánh xạ 1 Bit đơn lẻ trong Bit-Band Region thành 1 Ô nhớ 32-bit trong Alias Region</text>

  <!-- Cột 1: Vùng nhớ gốc (Bit-Band Region) -->
  <g transform="translate(40, 95)">
    <rect x="0" y="0" width="360" height="280" class="card-box"/>
    <rect x="0" y="0" width="360" height="40" rx="10" fill="#0284c7"/>
    <text x="180" y="25" font-size="13" font-weight="800" fill="#ffffff" text-anchor="middle">BIT-BAND REGION (VÙNG GỐC 1MB)</text>

    <text x="20" y="65" font-size="11" font-weight="700" fill="var(--text-muted)">Ngoại vi (0x40000000) hoặc SRAM (0x20000000)</text>

    <!-- Byte 0: 8 bits -->
    <g transform="translate(20, 85)">
      <rect x="0" y="0" width="320" height="45" rx="6" fill="var(--box-blue)" stroke="#0284c7"/>
      <!-- 8 ô bit -->
      <rect x="10" y="10" width="32" height="25" fill="#e0f2fe" stroke="#0284c7"/>
      <text x="26" y="27" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">b7</text>

      <rect x="45" y="10" width="32" height="25" fill="#e0f2fe" stroke="#0284c7"/>
      <text x="61" y="27" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">b6</text>

      <rect x="80" y="10" width="32" height="25" fill="#e0f2fe" stroke="#0284c7"/>
      <text x="96" y="27" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">b5</text>

      <rect x="115" y="10" width="32" height="25" fill="#e0f2fe" stroke="#0284c7"/>
      <text x="131" y="27" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">b4</text>

      <rect x="150" y="10" width="32" height="25" fill="#e0f2fe" stroke="#0284c7"/>
      <text x="166" y="27" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">b3</text>

      <rect x="185" y="10" width="32" height="25" fill="#e0f2fe" stroke="#0284c7"/>
      <text x="201" y="27" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">b2</text>

      <rect x="220" y="10" width="32" height="25" fill="#e0f2fe" stroke="#0284c7"/>
      <text x="236" y="27" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">b1</text>

      <!-- Bit 0 nổi bật -->
      <rect x="255" y="8" width="55" height="29" rx="4" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
      <text x="282" y="26" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">Bit 0</text>
    </g>

    <!-- Formula -->
    <rect x="20" y="160" width="320" height="95" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="35" y="185" font-size="11" font-weight="bold" fill="var(--accent-blue)">Công Thức Ánh Xạ Phần Cứng:</text>
    <text x="35" y="208" font-size="10.5" font-family="monospace" fill="var(--text-primary)">Alias_Addr = Alias_Base +</text>
    <text x="35" y="226" font-size="10.5" font-family="monospace" fill="var(--text-primary)">  (Byte_Offset * 32) + (Bit * 4)</text>
    <text x="35" y="245" font-size="9.5" font-weight="600" fill="var(--accent-green)">✔ 1 Lệnh ghi STR duy nhất (Atomic Operation)</text>
  </g>

  <!-- Mũi tên ánh xạ -->
  <path d="M 410 190 C 460 190, 460 190, 505 190" stroke="#ef4444" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
  <text x="460" y="175" font-size="10.5" font-weight="bold" fill="#ef4444" text-anchor="middle">ÁNH XẠ 1 - 1</text>

  <!-- Cột 2: Vùng nhớ bí danh (Bit-Band Alias Region) -->
  <g transform="translate(520, 95)">
    <rect x="0" y="0" width="360" height="280" class="card-box"/>
    <rect x="0" y="0" width="360" height="40" rx="10" fill="#10b981"/>
    <text x="180" y="25" font-size="13" font-weight="800" fill="#ffffff" text-anchor="middle">BIT-BAND ALIAS (VÙNG ÁNH XẠ 32MB)</text>

    <!-- Ô nhớ 32-bit tương ứng với Bit 0 -->
    <g transform="translate(20, 60)">
      <rect x="0" y="0" width="320" height="60" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
      <text x="160" y="26" font-size="12" font-weight="800" fill="#b91c1c" text-anchor="middle">Alias Word 0 (Địa chỉ 32-bit)</text>
      <text x="160" y="46" font-size="10" font-family="monospace" fill="#7f1d1d" text-anchor="middle">*Alias_Addr = 1  ➜  Ghi Bit 0 = 1</text>
    </g>

    <g transform="translate(20, 130)">
      <rect x="0" y="0" width="320" height="40" rx="6" fill="var(--card-bg)" stroke="var(--card-border)"/>
      <text x="160" y="25" font-size="11" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Alias Word 1 (Trỏ tới Bit 1)</text>
    </g>

    <g transform="translate(20, 180)">
      <rect x="0" y="0" width="320" height="40" rx="6" fill="var(--card-bg)" stroke="var(--card-border)"/>
      <text x="160" y="25" font-size="11" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Alias Word 2 (Trỏ tới Bit 2)</text>
    </g>

    <g transform="translate(20, 230)">
      <rect x="0" y="0" width="320" height="35" rx="6" fill="var(--card-bg)" stroke="var(--card-border)" stroke-dasharray="4,3"/>
      <text x="160" y="22" font-size="11" font-weight="600" fill="var(--text-muted)" text-anchor="middle">... Tiếp tục cho 32 triệu ô nhớ ...</text>
    </g>
  </g>

</svg>"""

save_svg("bai02_bit_banding.svg", svg_bai02_bitband)

# ==============================================================================
# 3. BÀI 02: GIẢN ĐỒ RUNG PHÍM VÀ LỌC CHỐNG RUNG (DEBOUNCE)
# ==============================================================================
svg_bai02_debounce = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 360" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
  </defs>

  <rect x="10" y="10" width="900" height="340" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">GIẢN ĐỒ XUNG RUNG TIẾP ĐIỂM (BOUNCE) VÀ THUẬT TOÁN DEBOUNCE</text>
  <text x="460" y="65" class="subtitle-text">Khử hiện tượng nảy xung cơ khí trong khoảng 15ms - 20ms bằng phần mềm</text>

  <!-- Đồ thị 1: Tín hiệu thực tế bị nhiễu -->
  <g transform="translate(40, 85)">
    <rect x="0" y="0" width="840" height="110" class="card-box"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#ef4444">1. TÍN HIỆU NÚT BẤM THỰC TẾ (CHƯA XỬ LÝ - BỊ NẢY XUNG NHIỄU):</text>
    
    <!-- Trục điện áp -->
    <text x="15" y="55" font-size="10.5" font-weight="bold" fill="var(--text-muted)">3.3V</text>
    <text x="15" y="95" font-size="10.5" font-weight="bold" fill="var(--text-muted)">0.0V</text>

    <!-- Đường sóng nảy xung -->
    <path d="M 60 50 L 220 50 L 220 90 L 240 90 L 240 55 L 260 55 L 260 90 L 275 90 L 275 60 L 290 60 L 290 90 L 800 90" 
          stroke="#ef4444" stroke-width="3" fill="none"/>

    <!-- Vùng highlight rung phím -->
    <rect x="215" y="40" width="85" height="58" fill="#fee2e2" fill-opacity="0.4" stroke="#ef4444" stroke-dasharray="3,3"/>
    <text x="257" y="32" font-size="10" font-weight="bold" fill="#b91c1c" text-anchor="middle">Rung phím (5-20ms)</text>
    <text x="550" y="80" font-size="11" font-weight="bold" fill="#b91c1c">⚠ CPU 72MHz hiểu nhầm là hàng chục lần bấm!</text>
  </g>

  <!-- Đồ thị 2: Tín hiệu sau khi Debounce -->
  <g transform="translate(40, 210)">
    <rect x="0" y="0" width="840" height="115" class="card-box"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#10b981">2. TÍN HIỆU SAU KHI LỌC DEBOUNCE (LẤY MẪU TRỄ 20MS):</text>

    <!-- Trục điện áp -->
    <text x="15" y="55" font-size="10.5" font-weight="bold" fill="var(--text-muted)">3.3V</text>
    <text x="15" y="95" font-size="10.5" font-weight="bold" fill="var(--text-muted)">0.0V</text>

    <!-- Đường sóng vuông chuẩn -->
    <path d="M 60 50 L 300 50 L 300 90 L 800 90" stroke="#10b981" stroke-width="3.5" fill="none"/>

    <!-- Mốc xác nhận phím -->
    <line x1="300" y1="35" x2="300" y2="105" stroke="#0284c7" stroke-width="2" stroke-dasharray="4,3"/>
    <rect x="310" y="45" width="220" height="30" rx="4" fill="var(--box-blue)" stroke="#0284c7"/>
    <text x="420" y="65" font-size="11" font-weight="bold" fill="#0284c7" text-anchor="middle">✔ Điểm xác nhận nút bấm hợp lệ</text>
  </g>

</svg>"""

save_svg("bai02_button_debounce.svg", svg_bai02_debounce)

# ==============================================================================
# 4. BÀI 03: SƠ ĐỒ CÂY PHÂN PHỐI XUNG NHỊP (CLOCK TREE 72MHZ)
# ==============================================================================
svg_bai03_clocktree = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 500" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" class="wire-arrow"/>
    </marker>
  </defs>

  <rect x="10" y="10" width="960" height="480" class="canvas-bg"/>
  <text x="490" y="42" class="title-text">CÂY PHÂN PHỐI XUNG NHỊP STM32F103 (CLOCK TREE 72MHZ)</text>
  <text x="490" y="66" class="subtitle-text">Hành trình nhân tần số từ thạch anh 8MHz qua PLL cấp cho lõi CPU và các Bus APB1, APB2</text>

  <!-- Nguồn thạch anh ngoài HSE 8MHz -->
  <g transform="translate(30, 160)">
    <rect x="0" y="0" width="140" height="80" rx="8" fill="#f8fafc" stroke="#3b82f6" stroke-width="2" filter="url(#shadowLight)"/>
    <text x="70" y="30" font-size="12" font-weight="800" fill="#1e3a8a" text-anchor="middle">HSE OSCILLATOR</text>
    <text x="70" y="50" font-size="14" font-weight="900" fill="#0284c7" text-anchor="middle">8.000 MHz</text>
    <text x="70" y="68" font-size="10" font-weight="600" fill="#64748b" text-anchor="middle">Thạch anh kim loại</text>
  </g>

  <!-- Mũi tên từ HSE vào PLL -->
  <line x1="170" y1="200" x2="215" y2="200" class="wire" marker-end="url(#arrow)"/>

  <!-- Bộ nhân tần PLL x9 -->
  <g transform="translate(220, 150)">
    <rect x="0" y="0" width="150" height="100" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadowLight)"/>
    <text x="75" y="30" font-size="13" font-weight="800" fill="#1d4ed8" text-anchor="middle">BỘ PLL x9</text>
    <text x="75" y="55" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">PLL Source: HSE</text>
    <text x="75" y="75" font-size="12" font-weight="800" fill="#10b981" text-anchor="middle">8MHz x 9 = 72MHz</text>
  </g>

  <!-- Mũi tên từ PLL sang SYSCLK MUX -->
  <line x1="370" y1="200" x2="415" y2="200" class="wire" marker-end="url(#arrow)"/>

  <!-- Khối SYSCLK 72MHz -->
  <g transform="translate(420, 150)">
    <rect x="0" y="0" width="150" height="100" rx="8" fill="#10b981" filter="url(#shadowLight)"/>
    <text x="75" y="32" font-size="13" font-weight="800" fill="#ffffff" text-anchor="middle">SYSCLK</text>
    <text x="75" y="60" font-size="18" font-weight="900" fill="#ffffff" text-anchor="middle">72 MHz</text>
    <text x="75" y="82" font-size="10.5" font-weight="600" fill="#d1fae5" text-anchor="middle">Xung Nhịp Hệ Thống</text>
  </g>

  <!-- Rẽ nhánh sang AHB và Core -->
  <line x1="570" y1="200" x2="630" y2="200" class="wire" marker-end="url(#arrow)"/>

  <!-- Khối AHB Bus HCLK -->
  <g transform="translate(635, 100)">
    <rect x="0" y="0" width="300" height="65" rx="8" fill="var(--card-bg)" stroke="#0284c7" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#0284c7">AHB Bus (HCLK = 72MHz)</text>
    <text x="15" y="48" font-size="10.5" fill="var(--text-muted)">Cấp cho: Cortex-M3 Core, DMA1, Flash &amp; SRAM</text>
  </g>

  <!-- Khối APB2 Bus (72MHz) -->
  <g transform="translate(635, 185)">
    <rect x="0" y="0" width="300" height="85" rx="8" fill="var(--card-bg)" stroke="#10b981" stroke-width="1.5"/>
    <text x="15" y="24" font-size="12" font-weight="bold" fill="#059669">APB2 Bus (PCLK2 = 72MHz - Tối Đa)</text>
    <text x="15" y="44" font-size="10" fill="var(--text-muted)">Cấp cho: GPIO A, B, C, D, USART1, SPI1, TIM1</text>
    <rect x="15" y="52" width="270" height="24" rx="4" fill="var(--box-amber)"/>
    <text x="25" y="68" font-size="9.5" font-weight="bold" fill="#b45309">ADC Prescaler /6 ➜ ADCCLK = 12MHz (≤ 14MHz)</text>
  </g>

  <!-- Khối APB1 Bus (36MHz) -->
  <g transform="translate(635, 290)">
    <rect x="0" y="0" width="300" height="85" rx="8" fill="var(--card-bg)" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="15" y="24" font-size="12" font-weight="bold" fill="#d97706">APB1 Bus (PCLK1 = 36MHz - Bắt Buộc /2)</text>
    <text x="15" y="44" font-size="10" fill="var(--text-muted)">Cấp cho: TIM2, TIM3, TIM4, USART2, I2C, SPI2, CAN</text>
    <rect x="15" y="52" width="270" height="24" rx="4" fill="var(--box-green)"/>
    <text x="25" y="68" font-size="9.5" font-weight="bold" fill="#047857">Nhân đôi xung Timer x2 ➜ TIM CLK = 72MHz!</text>
  </g>

  <!-- Lưu ý Flash Latency -->
  <g transform="translate(30, 400)">
    <rect x="0" y="0" width="905" height="50" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
    <text x="452" y="31" font-size="11.5" font-weight="bold" fill="#b91c1c" text-anchor="middle">
      ⚠ NGUYÊN TẮC BẮT BUỘC: Cấu hình 2 Wait States (FLASH_ACR LATENCY = 2) TRƯỚC KHI chuyển sang PLL 72MHz!
    </text>
  </g>

</svg>"""

save_svg("bai03_clock_tree.svg", svg_bai03_clocktree)

# ==============================================================================
# 5. BÀI 06: KHỐI TIME-BASE GENERATOR CỦA TIMER (PSC, ARR, CNT)
# ==============================================================================
svg_bai06_timebase = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 440" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" class="wire-arrow"/>
    </marker>
  </defs>

  <rect x="10" y="10" width="900" height="420" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">CẤU TRÚC KHỐI CƠ SỞ THỜI GIAN TIME-BASE GENERATOR (TIM2 - TIM4)</text>
  <text x="460" y="66" class="subtitle-text">Mối quan hệ nhịp đếm giữa Prescaler (PSC), Counter (CNT) và Auto-Reload (ARR)</text>

  <!-- Nguồn xung ngoại vi 72MHz -->
  <g transform="translate(40, 160)">
    <rect x="0" y="0" width="160" height="70" rx="8" fill="#1e293b" filter="url(#shadowLight)"/>
    <text x="80" y="28" font-size="11" font-weight="700" fill="#94a3b8" text-anchor="middle">XUNG NGOẠI VI</text>
    <text x="80" y="52" font-size="16" font-weight="900" fill="#38bdf8" text-anchor="middle">TIMx_CLK 72MHz</text>
  </g>

  <line x1="200" y1="195" x2="255" y2="195" class="wire" marker-end="url(#arrow)"/>

  <!-- Khối Prescaler PSC -->
  <g transform="translate(260, 140)">
    <rect x="0" y="0" width="170" height="110" rx="8" fill="var(--card-bg)" stroke="#0284c7" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="170" height="32" rx="8" fill="#0284c7"/>
    <text x="85" y="22" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">PRESCALER (PSC)</text>
    <text x="85" y="56" font-size="11" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">Bộ chia 16-bit (1-65536)</text>
    <text x="85" y="78" font-size="10" font-family="monospace" fill="var(--text-muted)" text-anchor="middle">f_cnt = f_clk / (PSC+1)</text>
    <text x="85" y="98" font-size="10.5" font-weight="700" fill="#10b981" text-anchor="middle">PSC = 7199 ➜ 10 kHz</text>
  </g>

  <line x1="430" y1="195" x2="485" y2="195" class="wire" marker-end="url(#arrow)"/>

  <!-- Khối Counter CNT -->
  <g transform="translate(490, 130)">
    <rect x="0" y="0" width="170" height="130" rx="8" fill="var(--card-bg)" stroke="#10b981" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="170" height="32" rx="8" fill="#10b981"/>
    <text x="85" y="22" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">COUNTER (CNT)</text>
    <text x="85" y="60" font-size="11" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">Bộ Đếm 16-bit</text>
    <text x="85" y="82" font-size="14" font-weight="900" fill="#059669" text-anchor="middle">0 ➜ ARR</text>
    <text x="85" y="110" font-size="10" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Đếm tăng dần (Up-count)</text>
  </g>

  <!-- Khối Auto-Reload ARR ở trên so sánh xuống -->
  <g transform="translate(490, 290)">
    <rect x="0" y="0" width="170" height="90" rx="8" fill="var(--card-bg)" stroke="#f59e0b" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="170" height="30" rx="8" fill="#f59e0b"/>
    <text x="85" y="20" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">AUTO-RELOAD (ARR)</text>
    <text x="85" y="52" font-size="11" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">Ngưỡng tràn chu kỳ</text>
    <text x="85" y="74" font-size="11" font-weight="800" fill="#b45309" text-anchor="middle">ARR = 9999 (10000 nhịp)</text>
    <line x1="85" y1="0" x2="85" y2="-30" class="wire" marker-end="url(#arrow)"/>
  </g>

  <!-- Mũi tên sự kiện tràn Update Event -->
  <line x1="660" y1="195" x2="715" y2="195" class="wire" marker-end="url(#arrow)"/>

  <!-- Khối Sự Kiện Tràn (Update Event) -->
  <g transform="translate(720, 140)">
    <rect x="0" y="0" width="160" height="110" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="2" filter="url(#shadowLight)"/>
    <text x="80" y="28" font-size="11" font-weight="bold" fill="#991b1b" text-anchor="middle">SỰ KIỆN TRÀN</text>
    <text x="80" y="50" font-size="12" font-weight="900" fill="#dc2626" text-anchor="middle">UPDATE EVENT (UEV)</text>
    <text x="80" y="74" font-size="10.5" font-weight="700" fill="#b91c1c" text-anchor="middle">Bật cờ UIF = 1</text>
    <text x="80" y="94" font-size="10" font-weight="bold" fill="#047857" text-anchor="middle">Ngắt định kỳ đúng 1.0s!</text>
  </g>

</svg>"""

save_svg("bai06_timer_timebase.svg", svg_bai06_timebase)

# ==============================================================================
# 6. BÀI 07: NGUYÊN LÝ SO SÁNH OUTPUT COMPARE VÀ PWM MODE 1
# ==============================================================================
svg_bai07_pwm = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 440" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
  </defs>

  <rect x="10" y="10" width="920" height="420" class="canvas-bg"/>
  <text x="470" y="42" class="title-text">NGUYÊN LÝ ĐIỀU CHẾ ĐỘ RỘNG XUNG (PWM MODE 1)</text>
  <text x="470" y="66" class="subtitle-text">So sánh liên tục giá trị bộ đếm CNT với ngưỡng so sánh CCR để tạo dạng sóng ngõ ra</text>

  <!-- Đồ thị 1: So sánh CNT và CCR -->
  <g transform="translate(60, 90)">
    <rect x="0" y="0" width="820" height="150" class="card-box"/>
    <!-- Trục tung -->
    <text x="20" y="30" font-size="11" font-weight="bold" fill="#0284c7">ARR (Chu kỳ)</text>
    <text x="20" y="75" font-size="11" font-weight="bold" fill="#ef4444">CCR (Ngưỡng)</text>
    <text x="20" y="130" font-size="11" font-weight="bold" fill="var(--text-muted)">0</text>

    <!-- Đường đếm răng cưa CNT -->
    <path d="M 80 130 L 280 25 L 280 130 L 480 25 L 480 130 L 680 25 L 680 130" stroke="#0284c7" stroke-width="3" fill="none"/>
    <text x="180" y="70" font-size="11" font-weight="bold" fill="#0284c7">CNT đếm lên ➔</text>

    <!-- Đường CCR nét đứt ngang -->
    <line x1="80" y1="75" x2="750" y2="75" stroke="#ef4444" stroke-width="2" stroke-dasharray="6,4"/>
    <text x="760" y="78" font-size="11" font-weight="bold" fill="#ef4444">CCR</text>
  </g>

  <!-- Đồ thị 2: Dạng sóng ngõ ra PWM chân I/O -->
  <g transform="translate(60, 260)">
    <rect x="0" y="0" width="820" height="140" class="card-box"/>
    <text x="20" y="25" font-size="12" font-weight="bold" fill="#10b981">TÍN HIỆU NGÕ RA CHÂN GPIO (PWM MODE 1):</text>
    <text x="20" y="60" font-size="11" font-weight="bold" fill="var(--text-muted)">3.3V (HIGH)</text>
    <text x="20" y="110" font-size="11" font-weight="bold" fill="var(--text-muted)">0.0V (LOW)</text>

    <!-- Xung vuông -->
    <!-- Chu kỳ 1 -->
    <path d="M 80 110 L 80 55 L 185 55 L 185 110 L 280 110 L 280 55 L 385 55 L 385 110 L 480 110 L 480 55 L 585 55 L 585 110 L 680 110" 
          stroke="#10b981" stroke-width="3.5" fill="none"/>

    <!-- Vùng Ton và Toff -->
    <line x1="80" y1="45" x2="185" y2="45" stroke="#0284c7" stroke-width="1.5"/>
    <text x="132" y="40" font-size="10.5" font-weight="bold" fill="#0284c7" text-anchor="middle">Ton (CNT &lt; CCR)</text>

    <line x1="185" y1="45" x2="280" y2="45" stroke="#ef4444" stroke-width="1.5"/>
    <text x="232" y="40" font-size="10.5" font-weight="bold" fill="#ef4444" text-anchor="middle">Toff (CNT ≥ CCR)</text>

    <line x1="80" y1="125" x2="280" y2="125" stroke="#10b981" stroke-width="2"/>
    <text x="180" y="138" font-size="11" font-weight="bold" fill="#047857" text-anchor="middle">CHU KỲ T (Period = ARR + 1)</text>

    <!-- Công thức Duty Cycle -->
    <rect x="520" y="20" width="280" height="50" rx="6" fill="var(--box-green)" stroke="#10b981"/>
    <text x="660" y="40" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">Hệ số công tác (Duty Cycle %):</text>
    <text x="660" y="58" font-size="12" font-weight="800" fill="#047857" text-anchor="middle">Duty (%) = (CCR / (ARR + 1)) * 100%</text>
  </g>

</svg>"""

save_svg("bai07_pwm_principle.svg", svg_bai07_pwm)

# ==============================================================================
# 7. BÀI 13: CẤU TRÚC KHUNG TRUYỀN UART (8-N-1)
# ==============================================================================
svg_bai13_uart_frame = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 340" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
  </defs>

  <rect x="10" y="10" width="900" height="320" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">CẤU TRÚC KHUNG TRUYỀN DỮ LIỆU NỐI TIẾP UART (FRAME 8-N-1)</text>
  <text x="460" y="66" class="subtitle-text">Quy chuẩn mức điện áp tín hiệu TX/RX: Mức nghỉ High (3.3V), Start bit 0V và 8 Data bits</text>

  <g transform="translate(40, 95)">
    <rect x="0" y="0" width="840" height="180" class="card-box"/>

    <!-- Mức điện áp -->
    <text x="15" y="45" font-size="11" font-weight="bold" fill="var(--text-muted)">3.3V (1)</text>
    <text x="15" y="125" font-size="11" font-weight="bold" fill="var(--text-muted)">0.0V (0)</text>

    <!-- Đường sóng UART -->
    <!-- Idle -> Start(0) -> b0(1) -> b1(0) -> b2(1) -> b3(1) -> b4(0) -> b5(1) -> b6(0) -> b7(0) -> Stop(1) -> Idle -->
    <path d="M 60 40 L 120 40 L 120 120 L 180 120 L 180 40 L 240 40 L 240 120 L 300 120 L 300 40 L 420 40 L 420 120 L 480 120 L 480 40 L 540 40 L 540 120 L 660 120 L 660 40 L 800 40" 
          stroke="#0284c7" stroke-width="3.5" fill="none"/>

    <!-- Phân chia các ô Bit -->
    <!-- Idle -->
    <rect x="60" y="135" width="60" height="35" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
    <text x="90" y="157" font-size="10" font-weight="bold" fill="var(--text-muted)" text-anchor="middle">IDLE</text>

    <!-- Start Bit -->
    <rect x="120" y="135" width="60" height="35" rx="4" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
    <text x="150" y="157" font-size="10.5" font-weight="bold" fill="#b91c1c" text-anchor="middle">START</text>

    <!-- 8 Data Bits -->
    <rect x="180" y="135" width="480" height="35" rx="4" fill="var(--box-blue)" stroke="#0284c7"/>
    <text x="420" y="157" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">8 DATA BITS (LSB b0 ➔ MSB b7)</text>

    <!-- Stop Bit -->
    <rect x="660" y="135" width="60" height="35" rx="4" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <text x="690" y="157" font-size="10.5" font-weight="bold" fill="#047857" text-anchor="middle">STOP</text>

    <!-- Idle sau -->
    <rect x="720" y="135" width="80" height="35" rx="4" fill="var(--card-bg)" stroke="var(--card-border)"/>
    <text x="760" y="157" font-size="10" font-weight="bold" fill="var(--text-muted)" text-anchor="middle">IDLE</text>
  </g>

</svg>"""

save_svg("bai13_uart_frame_format.svg", svg_bai13_uart_frame)

# ==============================================================================
# 8. BÀI 15: SƠ ĐỒ MẠCH GIAO TIẾP I2C (OPEN-DRAIN & PULL-UP)
# ==============================================================================
svg_bai15_i2c_circuit = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 400" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
  </defs>

  <rect x="10" y="10" width="900" height="380" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">SƠ ĐỒ NGUYÊN LÝ MẠCH GIAO TIẾP I2C MASTER PHẦN CỨNG</text>
  <text x="460" y="66" class="subtitle-text">Cấu trúc cực máng hở (Open-Drain) bắt buộc kết hợp điện trở kéo lên Pull-Up 4.7kΩ</text>

  <!-- Đường nguồn VDD 3.3V -->
  <line x1="80" y1="110" x2="840" y2="110" stroke="#ef4444" stroke-width="3"/>
  <text x="50" y="115" font-size="12" font-weight="bold" fill="#ef4444">3.3V</text>

  <!-- Hai điện trở kéo 4.7k -->
  <g transform="translate(420, 110)">
    <line x1="20" y1="0" x2="20" y2="35" class="wire"/>
    <rect x="10" y="35" width="20" height="45" rx="3" fill="var(--box-amber)" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="20" y="62" font-size="8.5" font-weight="bold" fill="#b45309" text-anchor="middle">4.7k</text>
    <line x1="20" y1="80" x2="20" y2="130" class="wire"/>

    <line x1="70" y1="0" x2="70" y2="35" class="wire"/>
    <rect x="60" y="35" width="20" height="45" rx="3" fill="var(--box-amber)" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="70" y="62" font-size="8.5" font-weight="bold" fill="#b45309" text-anchor="middle">4.7k</text>
    <line x1="70" y1="80" x2="70" y2="90" class="wire"/>
  </g>

  <!-- Hai đường SCL và SDA -->
  <line x1="80" y1="200" x2="840" y2="200" stroke="#0284c7" stroke-width="3"/>
  <text x="45" y="205" font-size="12" font-weight="bold" fill="#0284c7">SCL</text>

  <line x1="80" y1="240" x2="840" y2="240" stroke="#10b981" stroke-width="3"/>
  <text x="45" y="245" font-size="12" font-weight="bold" fill="#10b981">SDA</text>

  <!-- Thiết bị 1: STM32 I2C Master -->
  <g transform="translate(100, 260)">
    <rect x="0" y="0" width="220" height="100" rx="10" fill="var(--card-bg)" stroke="#0284c7" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="220" height="30" rx="10" fill="#0284c7"/>
    <text x="110" y="20" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">STM32F103 (MASTER)</text>
    <text x="25" y="55" font-size="11" font-weight="bold" fill="#0284c7">PB6 (SCL) ──┐</text>
    <text x="25" y="80" font-size="11" font-weight="bold" fill="#10b981">PB7 (SDA) ──┴── Open-Drain Mode</text>
    <line x1="110" y1="0" x2="110" y2="-60" class="wire"/>
    <line x1="140" y1="0" x2="140" y2="-20" class="wire"/>
  </g>

  <!-- Thiết bị 2: OLED SSD1306 -->
  <g transform="translate(360, 260)">
    <rect x="0" y="0" width="210" height="100" rx="10" fill="var(--card-bg)" stroke="#10b981" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="210" height="30" rx="10" fill="#10b981"/>
    <text x="105" y="20" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">OLED SSD1306 (SLAVE)</text>
    <text x="105" y="55" font-size="11" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">Địa chỉ I2C: 0x78</text>
    <text x="105" y="80" font-size="10.5" fill="var(--text-muted)" text-anchor="middle">Màn hình 128x64</text>
    <line x1="90" y1="0" x2="90" y2="-60" class="wire"/>
    <line x1="120" y1="0" x2="120" y2="-20" class="wire"/>
  </g>

  <!-- Thiết bị 3: EEPROM AT24C08 -->
  <g transform="translate(620, 260)">
    <rect x="0" y="0" width="210" height="100" rx="10" fill="var(--card-bg)" stroke="#8b5cf6" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="210" height="30" rx="10" fill="#8b5cf6"/>
    <text x="105" y="20" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">EEPROM AT24C08 (SLAVE)</text>
    <text x="105" y="55" font-size="11" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">Địa chỉ I2C: 0xA0</text>
    <text x="105" y="80" font-size="10.5" fill="var(--text-muted)" text-anchor="middle">Bộ nhớ lưu trữ 8Kbit</text>
    <line x1="90" y1="0" x2="90" y2="-60" class="wire"/>
    <line x1="120" y1="0" x2="120" y2="-20" class="wire"/>
  </g>

</svg>"""

save_svg("bai15_i2c_bus_topology.svg", svg_bai15_i2c_circuit)

# ==============================================================================
# 9. BÀI 16: SƠ ĐỒ KẾT NỐI SPI 4 DÂY (FULL DUPLEX)
# ==============================================================================
svg_bai16_spi = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 380" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" class="wire-arrow"/>
    </marker>
  </defs>

  <rect x="10" y="10" width="900" height="360" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">SƠ ĐỒ GIAO TIẾP ĐỒNG BỘ NỐI TIẾP TỐC ĐỘ CAO SPI (FULL-DUPLEX)</text>
  <text x="460" y="66" class="subtitle-text">Truyền nhận song công đồng thời giữa Master và Slave qua 4 đường tín hiệu chuyên biệt</text>

  <!-- Master: STM32F103 -->
  <g transform="translate(60, 95)">
    <rect x="0" y="0" width="260" height="230" rx="12" fill="var(--card-bg)" stroke="#0284c7" stroke-width="2.5" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="260" height="40" rx="12" fill="#0284c7"/>
    <text x="130" y="25" font-size="13" font-weight="800" fill="#ffffff" text-anchor="middle">STM32F103 (SPI MASTER)</text>

    <text x="240" y="75" font-size="12" font-weight="bold" fill="#0284c7" text-anchor="end">PA5 (SCK) ──</text>
    <text x="240" y="115" font-size="12" font-weight="bold" fill="#10b981" text-anchor="end">PA7 (MOSI) ──</text>
    <text x="240" y="155" font-size="12" font-weight="bold" fill="#f59e0b" text-anchor="end">PA6 (MISO) ──</text>
    <text x="240" y="195" font-size="12" font-weight="bold" fill="#ef4444" text-anchor="end">PA4 (CS / NSS) ──</text>
  </g>

  <!-- Đường dây tín hiệu -->
  <!-- SCK -->
  <line x1="320" y1="165" x2="590" y2="165" stroke="#0284c7" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="455" y="158" font-size="11" font-weight="bold" fill="#0284c7" text-anchor="middle">Xung nhịp Clock (SCK)</text>

  <!-- MOSI -->
  <line x1="320" y1="205" x2="590" y2="205" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="455" y="198" font-size="11" font-weight="bold" fill="#10b981" text-anchor="middle">Master Out Slave In (MOSI)</text>

  <!-- MISO (Chiều ngược lại!) -->
  <line x1="600" y1="245" x2="330" y2="245" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="455" y="238" font-size="11" font-weight="bold" fill="#d97706" text-anchor="middle">◀ Master In Slave Out (MISO)</text>

  <!-- CS -->
  <line x1="320" y1="285" x2="590" y2="285" stroke="#ef4444" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="455" y="278" font-size="11" font-weight="bold" fill="#ef4444" text-anchor="middle">Chip Select (CS - Active Low)</text>

  <!-- Slave: Flash W25Q64 -->
  <g transform="translate(600, 95)">
    <rect x="0" y="0" width="260" height="230" rx="12" fill="var(--card-bg)" stroke="#10b981" stroke-width="2.5" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="260" height="40" rx="12" fill="#10b981"/>
    <text x="130" y="25" font-size="13" font-weight="800" fill="#ffffff" text-anchor="middle">W25Q64 / TFT (SLAVE)</text>

    <text x="20" y="75" font-size="12" font-weight="bold" fill="#0284c7">── CLK (Clock)</text>
    <text x="20" y="115" font-size="12" font-weight="bold" fill="#10b981">── DI (Data In)</text>
    <text x="20" y="155" font-size="12" font-weight="bold" fill="#f59e0b">── DO (Data Out)</text>
    <text x="20" y="195" font-size="12" font-weight="bold" fill="#ef4444">── /CS (Chip Select)</text>
  </g>

</svg>"""

save_svg("bai16_spi_topology.svg", svg_bai16_spi)

# ==============================================================================
# 10. BÀI 17: KIẾN TRÚC DMA CONTROLLER & MA TRẬN BUS AHB
# ==============================================================================
svg_bai17_dma = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 420" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" class="wire-arrow"/>
    </marker>
  </defs>

  <rect x="10" y="10" width="900" height="400" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">KIẾN TRÚC MA TRẬN BUS VÀ BỘ ĐIỀU KHIỂN TRUY XUẤT BỘ NHỚ DMA</text>
  <text x="460" y="66" class="subtitle-text">Truyền nhận dữ liệu song song trực tiếp giữa RAM và Ngoại vi hoàn toàn không tốn CPU</text>

  <!-- CPU Cortex-M3 -->
  <g transform="translate(360, 95)">
    <rect x="0" y="0" width="200" height="60" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2" filter="url(#shadowLight)"/>
    <text x="100" y="28" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">CPU CORE</text>
    <text x="100" y="48" font-size="14" font-weight="900" fill="#38bdf8" text-anchor="middle">ARM Cortex-M3</text>
  </g>

  <!-- Ma trận Bus AHB -->
  <g transform="translate(80, 180)">
    <rect x="0" y="0" width="760" height="50" rx="6" fill="#0284c7" filter="url(#shadowLight)"/>
    <text x="380" y="32" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle">MA TRẬN BUS AHB (AHB BUS MATRIX &amp; ARBITER)</text>
  </g>

  <!-- Đường kết nối CPU xuống AHB -->
  <line x1="460" y1="155" x2="460" y2="180" class="wire" stroke-width="3"/>

  <!-- RAM & Flash -->
  <g transform="translate(80, 260)">
    <rect x="0" y="0" width="210" height="120" rx="8" fill="var(--card-bg)" stroke="#10b981" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="210" height="30" rx="8" fill="#10b981"/>
    <text x="105" y="20" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">BỘ NHỚ HỆ THỐNG</text>
    <text x="105" y="58" font-size="12" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">SRAM (20KB)</text>
    <text x="105" y="80" font-size="11" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Flash Memory (64KB)</text>
    <text x="105" y="102" font-size="10" font-weight="700" fill="#059669" text-anchor="middle">Mảng đệm Dữ liệu (Buffers)</text>
    <line x1="105" y1="0" x2="105" y2="-30" class="wire" stroke-width="3"/>
  </g>

  <!-- DMA Controller -->
  <g transform="translate(355, 260)">
    <rect x="0" y="0" width="210" height="120" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="210" height="30" rx="8" fill="#2563eb"/>
    <text x="105" y="20" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">DMA1 CONTROLLER</text>
    <text x="105" y="58" font-size="13" font-weight="900" fill="#1d4ed8" text-anchor="middle">7 Kênh Độc Lập</text>
    <text x="105" y="80" font-size="10.5" font-weight="600" fill="#475569" text-anchor="middle">Tự động chuyển dữ liệu</text>
    <text x="105" y="102" font-size="10" font-weight="bold" fill="#10b981" text-anchor="middle">⚡ 0% CPU LOAD!</text>
    <line x1="105" y1="0" x2="105" y2="-30" class="wire" stroke-width="3"/>
  </g>

  <!-- Ngoại vi Peripherals -->
  <g transform="translate(630, 260)">
    <rect x="0" y="0" width="210" height="120" rx="8" fill="var(--card-bg)" stroke="#f59e0b" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="210" height="30" rx="8" fill="#f59e0b"/>
    <text x="105" y="20" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">KHỐI NGOẠI VI</text>
    <text x="105" y="58" font-size="11" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">ADC1 (Scan đa kênh)</text>
    <text x="105" y="80" font-size="11" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">USART1 (TX/RX buffer)</text>
    <text x="105" y="102" font-size="10.5" font-weight="bold" fill="#d97706" text-anchor="middle">SPI1 / I2C1 / Timers</text>
    <line x1="105" y1="0" x2="105" y2="-30" class="wire" stroke-width="3"/>
  </g>

</svg>"""

save_svg("bai17_dma_architecture.svg", svg_bai17_dma)

# ==============================================================================
# 11. BÀI 18: SO SÁNH DÒNG TIÊU THỤ CÁC CHẾ ĐỘ NGUỒN THẤP (LOW POWER MODES)
# ==============================================================================
svg_bai18_lowpower = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 400" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
  </defs>

  <rect x="10" y="10" width="900" height="380" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">SO SÁNH CÁC CẤP ĐỘ TIẾT KIỆM NĂNG LƯỢNG (LOW POWER MODES)</text>
  <text x="460" y="66" class="subtitle-text">Tối ưu hóa thời lượng pin cho thiết bị IoT từ 30mA xuống còn 2.5µA</text>

  <!-- Cột 1: Run Mode -->
  <g transform="translate(50, 95)">
    <rect x="0" y="0" width="185" height="260" rx="10" fill="var(--card-bg)" stroke="#ef4444" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="185" height="35" rx="10" fill="#ef4444"/>
    <text x="92" y="23" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">1. RUN MODE</text>

    <text x="92" y="65" font-size="22" font-weight="900" fill="#ef4444" text-anchor="middle">~30 mA</text>
    <text x="92" y="85" font-size="11" font-weight="600" fill="var(--text-muted)" text-anchor="middle">72MHz Full Speed</text>

    <line x1="15" y1="100" x2="170" y2="100" stroke="var(--card-border)"/>
    <text x="20" y="125" font-size="10.5" fill="var(--text-primary)">• CPU: Đang chạy</text>
    <text x="20" y="150" font-size="10.5" fill="var(--text-primary)">• Ngoại vi: Hoạt động</text>
    <text x="20" y="175" font-size="10.5" fill="var(--text-primary)">• RAM: Lưu trữ tốt</text>
    <text x="20" y="200" font-size="10.5" fill="var(--text-primary)">• Clock: HSE &amp; PLL ON</text>
    <text x="92" y="240" font-size="10" font-weight="bold" fill="#b91c1c" text-anchor="middle">Pin CR2032: ~7 Giờ</text>
  </g>

  <!-- Cột 2: Sleep Mode -->
  <g transform="translate(260, 95)">
    <rect x="0" y="0" width="185" height="260" rx="10" fill="var(--card-bg)" stroke="#f59e0b" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="185" height="35" rx="10" fill="#f59e0b"/>
    <text x="92" y="23" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">2. SLEEP MODE</text>

    <text x="92" y="65" font-size="22" font-weight="900" fill="#d97706" text-anchor="middle">~10 mA</text>
    <text x="92" y="85" font-size="11" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Lệnh __WFI()</text>

    <line x1="15" y1="100" x2="170" y2="100" stroke="var(--card-border)"/>
    <text x="20" y="125" font-size="10.5" fill="var(--text-primary)">• CPU: TẠM DỪNG</text>
    <text x="20" y="150" font-size="10.5" fill="var(--text-primary)">• Ngoại vi: Vẫn chạy</text>
    <text x="20" y="175" font-size="10.5" fill="var(--text-primary)">• RAM: Giữ nguyên</text>
    <text x="20" y="200" font-size="10.5" fill="var(--text-primary)">• Thức: Bất kỳ ngắt nào</text>
    <text x="92" y="240" font-size="10" font-weight="bold" fill="#d97706" text-anchor="middle">Pin CR2032: ~1 Ngày</text>
  </g>

  <!-- Cột 3: Stop Mode -->
  <g transform="translate(470, 95)">
    <rect x="0" y="0" width="185" height="260" rx="10" fill="var(--card-bg)" stroke="#0284c7" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="185" height="35" rx="10" fill="#0284c7"/>
    <text x="92" y="23" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">3. STOP MODE</text>

    <text x="92" y="65" font-size="22" font-weight="900" fill="#0284c7" text-anchor="middle">~20 µA</text>
    <text x="92" y="85" font-size="11" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Dừng Clock hệ thống</text>

    <line x1="15" y1="100" x2="170" y2="100" stroke="var(--card-border)"/>
    <text x="20" y="125" font-size="10.5" fill="var(--text-primary)">• CPU: TẮT NGUỒN</text>
    <text x="20" y="150" font-size="10.5" fill="var(--text-primary)">• Ngoại vi: Tắt hết</text>
    <text x="20" y="175" font-size="10.5" font-weight="bold" fill="#0284c7">• RAM: BẢO LƯU 100%</text>
    <text x="20" y="200" font-size="10.5" fill="var(--text-primary)">• Thức: Ngắt ngoài EXTI</text>
    <text x="92" y="240" font-size="10" font-weight="bold" fill="#0284c7" text-anchor="middle">Pin CR2032: ~1.5 Năm</text>
  </g>

  <!-- Cột 4: Standby Mode -->
  <g transform="translate(680, 95)">
    <rect x="0" y="0" width="185" height="260" rx="10" fill="var(--card-bg)" stroke="#10b981" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="185" height="35" rx="10" fill="#10b981"/>
    <text x="92" y="23" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">4. STANDBY MODE</text>

    <text x="92" y="65" font-size="22" font-weight="900" fill="#059669" text-anchor="middle">2.5 µA</text>
    <text x="92" y="85" font-size="11" font-weight="600" fill="var(--text-muted)" text-anchor="middle">Ngủ sâu nhất (Deep)</text>

    <line x1="15" y1="100" x2="170" y2="100" stroke="var(--card-border)"/>
    <text x="20" y="125" font-size="10.5" fill="var(--text-primary)">• Lõi CPU 1.8V: CẮT</text>
    <text x="20" y="150" font-size="10.5" fill="#ef4444">• RAM: BỊ XÓA TRẮNG</text>
    <text x="20" y="175" font-size="10.5" fill="var(--text-primary)">• Chỉ giữ RTC &amp; BKP</text>
    <text x="20" y="200" font-size="10.5" fill="var(--text-primary)">• Thức: Chân WKUP PA0</text>
    <text x="92" y="240" font-size="10" font-weight="bold" fill="#059669" text-anchor="middle">Pin CR2032: ~5-10 Năm</text>
  </g>

</svg>"""

save_svg("bai18_low_power_modes.svg", svg_bai18_lowpower)

# ==============================================================================
# 12. BÀI 20: KIẾN TRÚC ĐA NHIỆM BỘ LẬP LỊCH FREERTOS SCHEDULER
# ==============================================================================
svg_bai20_freertos = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 400" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" class="wire-arrow"/>
    </marker>
  </defs>

  <rect x="10" y="10" width="900" height="380" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">KIẾN TRÚC ĐA NHIỆM HỆ ĐIỀU HÀNH THỜI GIAN THỰC FREERTOS</text>
  <text x="460" y="66" class="subtitle-text">Bộ lập lịch chiếm quyền (Preemptive Scheduler) phân bổ thời gian thực thi cho các Task độc lập</text>

  <!-- Khối Scheduler -->
  <g transform="translate(160, 95)">
    <rect x="0" y="0" width="600" height="60" rx="10" fill="#0284c7" filter="url(#shadowLight)"/>
    <text x="300" y="28" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle">FREERTOS PREEMPTIVE SCHEDULER</text>
    <text x="300" y="48" font-size="11" font-weight="600" fill="#bae6fd" text-anchor="middle">Điều phối bởi ngắt SysTick (1ms) và chuyển ngữ cảnh bằng PendSV</text>
  </g>

  <!-- Mũi tên từ Scheduler xuống Task 1 và Task 2 -->
  <line x1="300" y1="155" x2="300" y2="195" class="wire" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="620" y1="155" x2="620" y2="195" class="wire" stroke-width="2.5" marker-end="url(#arrow)"/>

  <!-- Task 1 (High Priority) -->
  <g transform="translate(160, 200)">
    <rect x="0" y="0" width="280" height="150" rx="10" fill="var(--card-bg)" stroke="#10b981" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="280" height="32" rx="10" fill="#10b981"/>
    <text x="140" y="22" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">TASK 1 (ƯU TIÊN CAO - PRIORITY 2)</text>
    <text x="140" y="55" font-size="11" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">Tác vụ khẩn cấp / Xử lý cảm biến</text>
    <text x="140" y="75" font-size="10.5" fill="var(--text-muted)" text-anchor="middle">Đang chạy (Running State)</text>

    <!-- Ngăn xếp riêng -->
    <rect x="20" y="90" width="240" height="45" rx="6" fill="var(--box-green)" stroke="#10b981"/>
    <text x="140" y="110" font-size="10.5" font-weight="bold" fill="#047857" text-anchor="middle">Stack Riêng: Con trỏ PSP1</text>
    <text x="140" y="126" font-size="9.5" font-family="monospace" fill="#065f46" text-anchor="middle">R0-R3, R12, LR, PC, xPSR</text>
  </g>

  <!-- Task 2 (Low Priority) -->
  <g transform="translate(480, 200)">
    <rect x="0" y="0" width="280" height="150" rx="10" fill="var(--card-bg)" stroke="#f59e0b" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="280" height="32" rx="10" fill="#f59e0b"/>
    <text x="140" y="22" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">TASK 2 (ƯU TIÊN THẤP - PRIORITY 1)</text>
    <text x="140" y="55" font-size="11" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">Tác vụ phụ / Chớp tắt LED PC13</text>
    <text x="140" y="75" font-size="10.5" fill="var(--text-muted)" text-anchor="middle">Trạng thái ngủ (Blocked do vTaskDelay)</text>

    <!-- Ngăn xếp riêng -->
    <rect x="20" y="90" width="240" height="45" rx="6" fill="var(--box-amber)" stroke="#f59e0b"/>
    <text x="140" y="110" font-size="10.5" font-weight="bold" fill="#b45309" text-anchor="middle">Stack Riêng: Con trỏ PSP2</text>
    <text x="140" y="126" font-size="9.5" font-family="monospace" fill="#78350f" text-anchor="middle">Biến cục bộ &amp; Ngữ cảnh CPU</text>
  </g>

</svg>"""

save_svg("bai20_freertos_architecture.svg", svg_bai20_freertos)

# ==============================================================================
# 13. BÀI 23: SƠ ĐỒ MẠNG VI SAI CAN BUS (TJA1050 & 120 OHM)
# ==============================================================================
svg_bai23_can = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 400" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
  </defs>

  <rect x="10" y="10" width="920" height="380" class="canvas-bg"/>
  <text x="470" y="42" class="title-text">SƠ ĐỒ MẠNG TRUYỀN THÔNG CÔNG NGHIỆP VÀ Ô TÔ CAN BUS 2.0B</text>
  <text x="470" y="66" class="subtitle-text">Đường truyền vi sai xoắn đôi CAN_H / CAN_L kết hợp bộ thu phát Transceiver TJA1050</text>

  <!-- Đường truyền CAN_H -->
  <line x1="80" y1="130" x2="860" y2="130" stroke="#ef4444" stroke-width="3.5"/>
  <text x="45" y="135" font-size="12" font-weight="bold" fill="#ef4444">CAN_H</text>

  <!-- Trở đầu cuối trái 120 ohm -->
  <rect x="90" y="140" width="22" height="45" rx="3" fill="var(--box-amber)" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="101" y="167" font-size="8.5" font-weight="bold" fill="#b45309" text-anchor="middle">120Ω</text>
  <line x1="101" y1="130" x2="101" y2="140" class="wire"/>
  <line x1="101" y1="185" x2="101" y2="195" class="wire"/>

  <!-- Trở đầu cuối phải 120 ohm -->
  <rect x="830" y="140" width="22" height="45" rx="3" fill="var(--box-amber)" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="841" y="167" font-size="8.5" font-weight="bold" fill="#b45309" text-anchor="middle">120Ω</text>
  <line x1="841" y1="130" x2="841" y2="140" class="wire"/>
  <line x1="841" y1="185" x2="841" y2="195" class="wire"/>

  <!-- Đường truyền CAN_L -->
  <line x1="80" y1="195" x2="860" y2="195" stroke="#0284c7" stroke-width="3.5"/>
  <text x="45" y="200" font-size="12" font-weight="bold" fill="#0284c7">CAN_L</text>

  <!-- Node 1: Engine ECU -->
  <g transform="translate(180, 230)">
    <rect x="0" y="0" width="240" height="130" rx="10" fill="var(--card-bg)" stroke="#0284c7" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="240" height="30" rx="10" fill="#0284c7"/>
    <text x="120" y="20" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">NODE 1: ENGINE ECU (STM32)</text>

    <rect x="20" y="42" width="200" height="35" rx="5" fill="var(--box-blue)" stroke="#0284c7"/>
    <text x="120" y="64" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">Transceiver TJA1050</text>

    <text x="120" y="100" font-size="10.5" fill="var(--text-muted)" text-anchor="middle">PA11 (RX) / PA12 (TX)</text>
    <line x1="70" y1="42" x2="70" y2="-100" class="wire" stroke="#ef4444"/>
    <line x1="100" y1="42" x2="100" y2="-35" class="wire" stroke="#0284c7"/>
  </g>

  <!-- Node 2: Brake ABS -->
  <g transform="translate(520, 230)">
    <rect x="0" y="0" width="240" height="130" rx="10" fill="var(--card-bg)" stroke="#10b981" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="240" height="30" rx="10" fill="#10b981"/>
    <text x="120" y="20" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">NODE 2: BRAKE ABS (STM32)</text>

    <rect x="20" y="42" width="200" height="35" rx="5" fill="var(--box-green)" stroke="#10b981"/>
    <text x="120" y="64" font-size="11" font-weight="bold" fill="#047857" text-anchor="middle">Transceiver TJA1050</text>

    <text x="120" y="100" font-size="10.5" fill="var(--text-muted)" text-anchor="middle">PA11 (RX) / PA12 (TX)</text>
    <line x1="70" y1="42" x2="70" y2="-100" class="wire" stroke="#ef4444"/>
    <line x1="100" y1="42" x2="100" y2="-35" class="wire" stroke="#0284c7"/>
  </g>

</svg>"""

save_svg("bai23_can_bus_topology.svg", svg_bai23_can)

# ==============================================================================
# 14. BÀI 25: PHÂN VÙNG BỘ NHỚ FLASH CHO BOOTLOADER VÀ APPLICATION
# ==============================================================================
svg_bai25_bootloader = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 400" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" class="wire-arrow"/>
    </marker>
  </defs>

  <rect x="10" y="10" width="900" height="380" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">PHÂN VÙNG BỘ NHỚ FLASH CHO CUSTOM ISP BOOTLOADER</text>
  <text x="460" y="66" class="subtitle-text">Kiến trúc chuyển hướng Vector Ngắt (SCB->VTOR) và hàm Jump to Application</text>

  <!-- Thanh bộ nhớ Flash tổng thể -->
  <g transform="translate(60, 95)">
    <!-- Phân vùng 1: Bootloader 12KB -->
    <rect x="0" y="0" width="220" height="110" rx="8" fill="#eff6ff" stroke="#0284c7" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="220" height="32" rx="8" fill="#0284c7"/>
    <text x="110" y="22" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">BOOTLOADER (12KB)</text>
    <text x="110" y="55" font-size="11" font-family="monospace" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">0x0800 0000 - 0x0800 2FFF</text>
    <text x="110" y="78" font-size="10.5" fill="var(--text-muted)" text-anchor="middle">• Page 0 - Page 11</text>
    <text x="110" y="98" font-size="10.5" font-weight="700" fill="#0284c7" text-anchor="middle">Nhận firmware qua UART</text>

    <!-- Phân vùng 2: User Application 52KB -->
    <rect x="235" y="0" width="565" height="110" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="235" y="0" width="565" height="32" rx="8" fill="#10b981"/>
    <text x="517" y="22" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">USER APPLICATION AREA (52KB)</text>
    <text x="517" y="55" font-size="11" font-family="monospace" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">0x0800 3000 - 0x0800 FFFF</text>
    <text x="517" y="78" font-size="10.5" fill="var(--text-muted)" text-anchor="middle">• Page 12 - Page 63 (Chương trình chính của khách hàng)</text>
    <text x="517" y="98" font-size="10.5" font-weight="700" fill="#059669" text-anchor="middle">Bảng Vector Ngắt Mới (SCB->VTOR = 0x08003000)</text>
  </g>

  <!-- Hộp chi tiết 2 ô nhớ đầu tiên của Application -->
  <g transform="translate(60, 230)">
    <rect x="0" y="0" width="800" height="120" class="card-box"/>
    <text x="20" y="28" font-size="12" font-weight="bold" fill="#0284c7">2 Ô NHỚ ĐẦU TIÊN QUYẾT ĐỊNH CỦA APPLICATION TẠI 0x08003000:</text>

    <g transform="translate(30, 45)">
      <rect x="0" y="0" width="350" height="55" rx="6" fill="var(--box-blue)" stroke="#0284c7"/>
      <text x="175" y="24" font-size="11" font-family="monospace" font-weight="bold" fill="#0284c7" text-anchor="middle">Địa chỉ: 0x0800 3000</text>
      <text x="175" y="44" font-size="10.5" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">Initial MSP (Giá trị nạp vào con trỏ ngăn xếp RAM)</text>
    </g>

    <g transform="translate(410, 45)">
      <rect x="0" y="0" width="350" height="55" rx="6" fill="var(--box-green)" stroke="#10b981"/>
      <text x="175" y="24" font-size="11" font-family="monospace" font-weight="bold" fill="#059669" text-anchor="middle">Địa chỉ: 0x0800 3004</text>
      <text x="175" y="44" font-size="10.5" font-weight="bold" fill="var(--text-primary)" text-anchor="middle">Reset_Handler Pointer (Địa chỉ hàm nhảy khởi động)</text>
    </g>
  </g>

</svg>"""

save_svg("bai25_bootloader_flash_layout.svg", svg_bai25_bootloader)

# ==============================================================================
# 15. BÀI 26: KHUNG NGĂN XẾP STACK FRAME KHI SẬP CHIP HARDFAULT
# ==============================================================================
svg_bai26_hardfault = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 440" width="100%" height="100%">
  <defs>
    {COMMON_STYLES}
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" class="wire-arrow"/>
    </marker>
  </defs>

  <rect x="10" y="10" width="900" height="420" class="canvas-bg"/>
  <text x="460" y="42" class="title-text">GIẢI MÃ KHUNG NGĂN XẾP (STACK FRAME) KHI SẬP CHIP HARDFAULT</text>
  <text x="460" y="66" class="subtitle-text">Lõi ARM Cortex-M3 tự động lưu 8 thanh ghi vào RAM để kỹ sư truy tìm thủ phạm gây lỗi</text>

  <!-- Khung ngăn xếp Stack Frame -->
  <g transform="translate(80, 95)">
    <rect x="0" y="0" width="300" height="300" rx="10" fill="var(--card-bg)" stroke="#ef4444" stroke-width="2" filter="url(#shadowLight)"/>
    <rect x="0" y="0" width="300" height="32" rx="10" fill="#ef4444"/>
    <text x="150" y="22" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">CORTEX-M3 STACK FRAME (RAM)</text>

    <!-- 8 ô thanh ghi -->
    <g transform="translate(20, 42)">
      <rect x="0" y="0" width="260" height="26" fill="var(--card-bg)" stroke="var(--card-border)"/>
      <text x="130" y="18" font-size="11" font-family="monospace" fill="var(--text-muted)" text-anchor="middle">SP + 0x00 : R0</text>

      <rect x="0" y="26" width="260" height="26" fill="var(--card-bg)" stroke="var(--card-border)"/>
      <text x="130" y="44" font-size="11" font-family="monospace" fill="var(--text-muted)" text-anchor="middle">SP + 0x04 : R1</text>

      <rect x="0" y="52" width="260" height="26" fill="var(--card-bg)" stroke="var(--card-border)"/>
      <text x="130" y="70" font-size="11" font-family="monospace" fill="var(--text-muted)" text-anchor="middle">SP + 0x08 : R2</text>

      <rect x="0" y="78" width="260" height="26" fill="var(--card-bg)" stroke="var(--card-border)"/>
      <text x="130" y="96" font-size="11" font-family="monospace" fill="var(--text-muted)" text-anchor="middle">SP + 0x0C : R3</text>

      <rect x="0" y="104" width="260" height="26" fill="var(--card-bg)" stroke="var(--card-border)"/>
      <text x="130" y="122" font-size="11" font-family="monospace" fill="var(--text-muted)" text-anchor="middle">SP + 0x10 : R12</text>

      <rect x="0" y="130" width="260" height="30" fill="#eff6ff" stroke="#0284c7"/>
      <text x="130" y="150" font-size="11" font-family="monospace" font-weight="bold" fill="#0284c7" text-anchor="middle">SP + 0x14 : LR (Hàm Gọi)</text>

      <!-- PC Nổi bật đỏ -->
      <rect x="0" y="160" width="260" height="36" rx="4" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
      <text x="130" y="183" font-size="12" font-family="monospace" font-weight="900" fill="#b91c1c" text-anchor="middle">SP + 0x18 : PC (DÒNG CODE LỖI!)</text>

      <rect x="0" y="196" width="260" height="26" fill="var(--card-bg)" stroke="var(--card-border)"/>
      <text x="130" y="214" font-size="11" font-family="monospace" fill="var(--text-muted)" text-anchor="middle">SP + 0x1C : xPSR (Trạng thái)</text>
    </g>
  </g>

  <!-- Mũi tên từ PC sang phần phân tích -->
  <line x1="390" y1="280" x2="445" y2="280" class="wire" stroke="#ef4444" stroke-width="3" marker-end="url(#arrow)"/>

  <!-- Bảng giải mã lỗi và các thanh ghi SCB -->
  <g transform="translate(450, 95)">
    <rect x="0" y="0" width="410" height="300" class="card-box"/>
    <rect x="0" y="0" width="410" height="32" rx="10" fill="#1e293b"/>
    <text x="205" y="22" font-size="12" font-weight="bold" fill="#38bdf8" text-anchor="middle">CÁC THANH GHI CHẨN ĐOÁN LỖI PHẦN CỨNG (SCB)</text>

    <g transform="translate(20, 50)">
      <text x="0" y="20" font-size="12" font-weight="bold" fill="#ef4444">• PC (Program Counter):</text>
      <text x="15" y="40" font-size="11" fill="var(--text-primary)">Địa chỉ Hex chính xác của dòng lệnh C gây crash.</text>
      <text x="15" y="58" font-size="10.5" font-family="monospace" fill="#0284c7">addr2line -e app.elf 0x080004BC ➜ main.c:142</text>

      <text x="0" y="90" font-size="12" font-weight="bold" fill="#0284c7">• SCB->BFAR (BusFault Address):</text>
      <text x="15" y="110" font-size="11" fill="var(--text-primary)">Lưu địa chỉ vùng nhớ cấm mà con trỏ vừa cố tình ghi vào!</text>

      <text x="0" y="140" font-size="12" font-weight="bold" fill="#f59e0b">• SCB->CFSR (Fault Status):</text>
      <text x="15" y="160" font-size="11" fill="var(--text-primary)">Phân loại: Chia cho 0 (DIVBYZERO), Lệnh sai (UNDEFINSTR),</text>
      <text x="15" y="178" font-size="11" fill="var(--text-primary)">hoặc không căn chỉnh địa chỉ (UNALIGNED).</text>

      <rect x="0" y="195" width="370" height="35" rx="6" fill="var(--box-green)" stroke="#10b981"/>
      <text x="185" y="217" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">✔ Định vị chính xác 100% nguyên nhân sập chip!</text>
    </g>
  </g>

</svg>"""

save_svg("bai26_hardfault_stack_frame.svg", svg_bai26_hardfault)

print("SUCCESS: ALL SYSTEM SVGS BUILT AND SAVED!")
