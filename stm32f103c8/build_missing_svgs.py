import os

BASE_DIR = r"F:\Advance_C\stm32f103c8\images"
os.makedirs(BASE_DIR, exist_ok=True)

svgs = {}

# 1. Bai 08: Input Capture Principle & CCR1 latch
svgs["bai08_input_capture"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 400" width="100%" height="100%">
  <style>
    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-green: #059669;
      --accent-amber: #d97706;
      --accent-red: #dc2626;
      --accent-purple: #7c3aed;
      --wire-line: #334155;
    }
    path { fill: none; }
    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .mono { font-family: ui-monospace, Menlo, Consolas, monospace; }
  </style>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--wire-line)"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--accent-blue)"/>
    </marker>
  </defs>

  <rect width="920" height="400" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="460" y="36" text-anchor="middle" font-size="19" font-weight="700" fill="var(--title-color)">NGUYÊN LÝ HOẠT ĐỘNG KHỐI INPUT CAPTURE (TIMER)</text>
  <text x="460" y="58" text-anchor="middle" font-size="12.5" fill="var(--subtitle-color)">Tự động chốt giá trị bộ đếm TIMx_CNT vào thanh ghi TIMx_CCR1 khi phát hiện cạnh xung</text>

  <!-- Signal Waveform Panel -->
  <g transform="translate(40, 80)">
    <rect width="840" height="130" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="20" y="30" font-size="13" font-weight="700" fill="var(--accent-blue)">Tín hiệu ngõ vào (Input Pin PA6 / TIM3_CH1)</text>

    <!-- Waveform line -->
    <path d="M 50 95 L 200 95 L 200 45 L 600 45 L 600 95 L 800 95" stroke="var(--accent-blue)" stroke-width="3" stroke-linejoin="round"/>
    
    <!-- Rising edge marker -->
    <line x1="200" y1="100" x2="200" y2="120" stroke="var(--accent-green)" stroke-width="2" stroke-dasharray="3,3"/>
    <text x="200" y="118" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-green)">▲ Cạnh lên (t1)</text>

    <!-- Falling edge marker -->
    <line x1="600" y1="100" x2="600" y2="120" stroke="var(--accent-red)" stroke-width="2" stroke-dasharray="3,3"/>
    <text x="600" y="118" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-red)">▲ Cạnh xuống (t2)</text>

    <!-- Pulse width label -->
    <line x1="205" y1="35" x2="595" y2="35" stroke="var(--wire-line)" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
    <rect x="330" y="24" width="140" height="22" rx="4" fill="var(--canvas-bg)" stroke="var(--wire-line)"/>
    <text x="400" y="39" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--text-primary)">Độ rộng xung Δt = t2 - t1</text>
  </g>

  <!-- Hardware Latch Action Panels -->
  <g transform="translate(60, 230)">
    <rect width="360" height="140" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="180" y="26" text-anchor="middle" font-size="13.5" font-weight="700" fill="var(--accent-green)">BƯỚC 1: BẮT CẠNH LÊN (RISING EDGE)</text>
    <text x="20" y="52" font-size="12" fill="var(--text-primary)">1. Dò cạnh phát hiện điện áp tăng 0V → 3.3V</text>
    <text x="20" y="74" font-size="12" fill="var(--text-primary)">2. Sao chép tức thời: <tspan font-weight="700" fill="var(--accent-blue)">CCR1 = TIMx_CNT (t1)</tspan></text>
    <text x="20" y="96" font-size="12" fill="var(--text-primary)">3. Kéo cờ ngắt phần cứng: <tspan font-weight="700" fill="var(--accent-amber)">CC1IF = 1</tspan></text>
    <text x="20" y="118" font-size="11.5" fill="var(--text-muted)">4. Đổi cấu hình bộ bắt cạnh sang Cạnh Xuống</text>
  </g>

  <g transform="translate(500, 230)">
    <rect width="360" height="140" rx="8" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
    <text x="180" y="26" text-anchor="middle" font-size="13.5" font-weight="700" fill="var(--accent-red)">BƯỚC 2: BẮT CẠNH XUỐNG (FALLING EDGE)</text>
    <text x="20" y="52" font-size="12" fill="var(--text-primary)">1. Dò cạnh phát hiện điện áp tụt 3.3V → 0V</text>
    <text x="20" y="74" font-size="12" fill="var(--text-primary)">2. Sao chép tức thời: <tspan font-weight="700" fill="var(--accent-blue)">CCR1 = TIMx_CNT (t2)</tspan></text>
    <text x="20" y="96" font-size="12" fill="var(--text-primary)">3. Tính thời gian: <tspan font-weight="700" fill="var(--accent-purple)">Δt = t2 - t1 (us)</tspan></text>
    <text x="20" y="118" font-size="11.5" fill="var(--text-muted)">4. Đổi cấu hình bộ bắt cạnh quay lại Cạnh Lên</text>
  </g>
</svg>"""

# 2. Bai 08: HC-SR04 ultrasonic timing
svgs["bai08_hcsr04_timing"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 430" width="100%" height="100%">
  <style>
    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-green: #059669;
      --accent-amber: #d97706;
      --accent-red: #dc2626;
      --accent-purple: #7c3aed;
      --wire-line: #334155;
    }
    path { fill: none; }
    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .mono { font-family: ui-monospace, Menlo, Consolas, monospace; }
  </style>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--wire-line)"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--accent-red)"/>
    </marker>
  </defs>

  <rect width="940" height="430" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="470" y="36" text-anchor="middle" font-size="19" font-weight="700" fill="var(--title-color)">GIẢN ĐỒ THỜI GIAN CẢM BIẾN SIÊU ÂM HC-SR04</text>
  <text x="470" y="58" text-anchor="middle" font-size="12.5" fill="var(--subtitle-color)">Xung kích TRIG 10us, chùm sóng siêu âm 40kHz phát đi và độ rộng xung phản hồi ECHO</text>

  <!-- TRIG Line -->
  <g transform="translate(40, 80)">
    <text x="0" y="35" font-size="13" font-weight="700" fill="var(--accent-blue)">1. Chân TRIG</text>
    <text x="0" y="52" font-size="11" fill="var(--text-muted)">(Kích từ MCU)</text>
    <path d="M 120 40 L 160 40 L 160 15 L 200 15 L 200 40 L 860 40" stroke="var(--accent-blue)" stroke-width="2.5"/>
    <text x="180" y="8" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-blue)">≥ 10µs</text>
  </g>

  <!-- Sonic Burst Line -->
  <g transform="translate(40, 150)">
    <text x="0" y="35" font-size="13" font-weight="700" fill="var(--accent-amber)">2. Sóng Siêu Âm</text>
    <text x="0" y="52" font-size="11" fill="var(--text-muted)">(Tần số 40kHz)</text>
    <path d="M 120 40 L 220 40 L 230 15 L 240 40 L 250 15 L 260 40 L 270 15 L 280 40 L 290 15 L 300 40 L 310 15 L 320 40 L 860 40" stroke="var(--accent-amber)" stroke-width="2"/>
    <text x="270" y="8" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-amber)">8 chu kỳ sóng 40kHz</text>
    <rect x="740" y="10" width="100" height="50" rx="4" fill="var(--card-bg)" stroke="var(--card-border)" stroke-dasharray="3,3"/>
    <text x="790" y="38" text-anchor="middle" font-size="12" font-weight="700" fill="var(--text-muted)">VẬT CẢN</text>
    <path d="M 330 25 L 730 25" stroke="var(--accent-amber)" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#arrow)"/>
    <path d="M 730 45 L 330 45" stroke="var(--accent-red)" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#arrow-red)"/>
  </g>

  <!-- ECHO Line -->
  <g transform="translate(40, 230)">
    <text x="0" y="35" font-size="13" font-weight="700" fill="var(--accent-green)">3. Chân ECHO</text>
    <text x="0" y="52" font-size="11" fill="var(--text-muted)">(Đo bằng Timer)</text>
    <path d="M 120 40 L 320 40 L 320 15 L 680 15 L 680 40 L 860 40" stroke="var(--accent-green)" stroke-width="2.5"/>
    <line x1="320" y1="8" x2="680" y2="8" stroke="var(--wire-line)" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
    <rect x="420" y="-3" width="160" height="22" rx="4" fill="var(--canvas-bg)" stroke="var(--wire-line)"/>
    <text x="500" y="12" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--text-primary)">Thời gian phản hồi (Techo)</text>
  </g>

  <!-- Formula Callout Box -->
  <g transform="translate(40, 320)">
    <rect width="860" height="85" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="25" y="28" font-size="13" font-weight="700" fill="var(--accent-blue)">CÔNG THỨC QUY ĐỔI KHOẢNG CÁCH THỰC TẾ:</text>
    <text x="25" y="54" font-size="12.5" fill="var(--text-primary)">• Vận tốc âm thanh: <tspan font-weight="700">v = 340 m/s = 0.034 cm/µs</tspan> (Sóng di chuyển 2 lượt: tới vật cản và dội ngược lại).</text>
    <text x="25" y="74" font-size="13" font-weight="700" fill="var(--accent-purple)">• Khoảng cách (cm) = (Techo × 0.034) / 2 = Techo / 58</text>
    <text x="550" y="74" font-size="13" font-weight="700" fill="var(--accent-purple)">• Khoảng cách (inch) = Techo / 148</text>
  </g>
</svg>"""

# 3. Bai 09: Rotary Encoder Quadrature Signals & Hardware Decoder
svgs["bai09_encoder_signals"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 440" width="100%" height="100%">
  <style>
    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-green: #059669;
      --accent-amber: #d97706;
      --accent-red: #dc2626;
      --accent-purple: #7c3aed;
      --wire-line: #334155;
    }
    path { fill: none; }
    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  </style>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--wire-line)"/>
    </marker>
  </defs>

  <rect width="940" height="440" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="470" y="36" text-anchor="middle" font-size="19" font-weight="700" fill="var(--title-color)">TÍN HIỆU ENCODER VUÔNG GÓC VÀ KHỐI GIẢI MÃ PHẦN CỨNG</text>
  <text x="470" y="58" text-anchor="middle" font-size="12.5" fill="var(--subtitle-color)">Dạng sóng lệch pha 90° (Phase A &amp; Phase B) và bộ đếm 2 chiều tự động không tốn CPU</text>

  <!-- Left: CW Direction -->
  <g transform="translate(30, 80)">
    <rect width="420" height="200" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="210" y="26" text-anchor="middle" font-size="13.5" font-weight="700" fill="var(--accent-green)">QUAY THUẬN (CLOCKWISE - CW): BỘ ĐẾM TĂNG (+)</text>
    <text x="20" y="52" font-size="11.5" fill="var(--text-muted)">TI1 (Phase A) dẫn trước TI2 (Phase B) đúng 90 độ:</text>

    <!-- TI1 line -->
    <text x="20" y="80" font-size="12" font-weight="700" fill="var(--accent-blue)">TI1:</text>
    <path d="M 55 85 L 85 85 L 85 65 L 145 65 L 145 85 L 205 85 L 205 65 L 265 65 L 265 85 L 325 85 L 325 65 L 385 65" stroke="var(--accent-blue)" stroke-width="2"/>

    <!-- TI2 line -->
    <text x="20" y="125" font-size="12" font-weight="700" fill="var(--accent-purple)">TI2:</text>
    <path d="M 55 130 L 115 130 L 115 110 L 175 110 L 175 130 L 235 130 L 235 110 L 295 110 L 295 130 L 355 130 L 355 110 L 385 110" stroke="var(--accent-purple)" stroke-width="2"/>

    <!-- State table summary -->
    <rect x="20" y="150" width="380" height="36" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="210" y="172" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--accent-green)">Khi TI1 sườn lên: TI2 đang mức 0 → Phần cứng tăng CNT++</text>
  </g>

  <!-- Right: CCW Direction -->
  <g transform="translate(490, 80)">
    <rect width="420" height="200" rx="8" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
    <text x="210" y="26" text-anchor="middle" font-size="13.5" font-weight="700" fill="var(--accent-red)">QUAY NGHỊCH (COUNTER-CW): BỘ ĐẾM GIẢM (-)</text>
    <text x="20" y="52" font-size="11.5" fill="var(--text-muted)">TI2 (Phase B) dẫn trước TI1 (Phase A) đúng 90 độ:</text>

    <!-- TI1 line -->
    <text x="20" y="80" font-size="12" font-weight="700" fill="var(--accent-blue)">TI1:</text>
    <path d="M 55 85 L 115 85 L 115 65 L 175 65 L 175 85 L 235 85 L 235 65 L 295 65 L 295 85 L 355 85 L 355 65 L 385 65" stroke="var(--accent-blue)" stroke-width="2"/>

    <!-- TI2 line -->
    <text x="20" y="125" font-size="12" font-weight="700" fill="var(--accent-purple)">TI2:</text>
    <path d="M 55 110 L 85 110 L 85 130 L 145 130 L 145 110 L 205 110 L 205 130 L 265 130 L 265 110 L 325 110 L 325 130 L 385 130" stroke="var(--accent-purple)" stroke-width="2"/>

    <!-- State table summary -->
    <rect x="20" y="150" width="380" height="36" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="210" y="172" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--accent-red)">Khi TI1 sườn lên: TI2 đang mức 1 → Phần cứng giảm CNT--</text>
  </g>

  <!-- Bottom: Hardware Logic Routing -->
  <g transform="translate(30, 300)">
    <rect width="880" height="115" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="20" y="24" font-size="13" font-weight="700" fill="var(--accent-blue)">SƠ ĐỒ PHẦN CỨNG BỘ GIẢI MÃ ENCODER TRONG TIMER (TIM2, TIM3, TIM4):</text>
    
    <rect x="20" y="42" width="130" height="42" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-blue)"/>
    <text x="85" y="67" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">Chân TI1 (PA6)</text>

    <rect x="20" y="60" width="0" height="0"/>
    <rect x="180" y="42" width="150" height="42" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="255" y="67" text-anchor="middle" font-size="12" font-weight="600" fill="var(--text-primary)">Bộ Lọc Số IC1F/IC2F</text>

    <rect x="360" y="42" width="220" height="42" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)"/>
    <text x="470" y="67" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-amber)">Mạch Giải Mã Encoder Logic</text>

    <rect x="610" y="42" width="250" height="42" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
    <text x="735" y="67" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-green)">Bộ Đếm TIMx_CNT (Up/Down)</text>

    <!-- Connectors -->
    <path d="M 150 63 L 180 63" stroke="var(--wire-line)" stroke-width="1.5" marker-end="url(#arrow)"/>
    <path d="M 330 63 L 360 63" stroke="var(--wire-line)" stroke-width="1.5" marker-end="url(#arrow)"/>
    <path d="M 580 63 L 610 63" stroke="var(--wire-line)" stroke-width="1.5" marker-end="url(#arrow)"/>
    <text x="470" y="102" text-anchor="middle" font-size="11" fill="var(--text-muted)">Hệ số nhân 4X (Encoder Mode 3 đếm cả 2 cạnh TI1 &amp; TI2): 100 xung/vòng cho ra 400 xung đếm/vòng</text>
  </g>
</svg>"""

# 4. Bai 12: ADC Scan Mode Sequence & ADC_DR Overwrite Problem
svgs["bai12_adc_scan_mode"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 430" width="100%" height="100%">
  <style>
    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-green: #059669;
      --accent-amber: #d97706;
      --accent-red: #dc2626;
      --accent-purple: #7c3aed;
      --wire-line: #334155;
    }
    path { fill: none; }
    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .mono { font-family: ui-monospace, Menlo, Consolas, monospace; }
  </style>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--wire-line)"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--accent-red)"/>
    </marker>
  </defs>

  <rect width="940" height="430" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="470" y="36" text-anchor="middle" font-size="19" font-weight="700" fill="var(--title-color)">CƠ CHẾ QUÉT KÊNH TUẦN TỰ (ADC SCAN MODE) VÀ VẤN ĐỀ GHI ĐÈ</text>
  <text x="470" y="58" text-anchor="middle" font-size="12.5" fill="var(--subtitle-color)">Sự cần thiết của khối DMA khi chuyển đổi nhiều kênh tương tự trên thanh ghi duy nhất ADC_DR</text>

  <!-- Left: Sequence Flow -->
  <g transform="translate(30, 80)">
    <rect width="400" height="320" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="200" y="26" text-anchor="middle" font-size="13.5" font-weight="700" fill="var(--accent-blue)">TIẾN TRÌNH QUÉT CÁC KÊNH (SCAN SEQUENCE)</text>
    
    <!-- Step 1 -->
    <rect x="25" y="45" width="350" height="48" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="40" y="68" font-size="12" font-weight="700" fill="var(--accent-blue)">Bước 1: Chuyển đổi Kênh 0 (PA0)</text>
    <text x="40" y="84" font-size="11" fill="var(--text-muted)">Lưu kết quả Kênh 0 vào thanh ghi ADC_DR ──> Sinh cờ EOC</text>

    <!-- Step 2 -->
    <rect x="25" y="115" width="350" height="48" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="40" y="138" font-size="12" font-weight="700" fill="var(--accent-blue)">Bước 2: Chuyển đổi Kênh 1 (PA1)</text>
    <text x="40" y="154" font-size="11" fill="var(--text-muted)">Lưu kết quả Kênh 1 vào thanh ghi ADC_DR ──> Sinh cờ EOC</text>

    <!-- Step 3 -->
    <rect x="25" y="185" width="350" height="48" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="40" y="208" font-size="12" font-weight="700" fill="var(--accent-blue)">Bước 3: Chuyển đổi Kênh 16 (Nhiệt độ nội)</text>
    <text x="40" y="224" font-size="11" fill="var(--text-muted)">Lưu kết quả Kênh 16 vào thanh ghi ADC_DR ──> Hoàn tất</text>

    <!-- Connecting arrows -->
    <path d="M 200 93 L 200 115" stroke="var(--wire-line)" stroke-width="1.5" marker-end="url(#arrow)"/>
    <path d="M 200 163 L 200 185" stroke="var(--wire-line)" stroke-width="1.5" marker-end="url(#arrow)"/>

    <rect x="25" y="255" width="350" height="48" rx="6" fill="#fef2f2" stroke="var(--accent-red)"/>
    <text x="200" y="278" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-red)">NGUY HIỂM KHI KHÔNG CÓ DMA:</text>
    <text x="200" y="294" text-anchor="middle" font-size="11" fill="var(--accent-red)">Giá trị Kênh 1 &amp; Kênh 16 lập tức ghi đè làm mất dữ liệu Kênh 0!</text>
  </g>

  <!-- Right: Architecture & Solution -->
  <g transform="translate(460, 80)">
    <rect width="450" height="320" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="225" y="26" text-anchor="middle" font-size="13.5" font-weight="700" fill="var(--accent-green)">GIẢI PHÁP TIÊU CHUẨN CÔNG NGHIỆP: ADC + DMA</text>

    <!-- Register box -->
    <rect x="30" y="45" width="390" height="60" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
    <text x="225" y="70" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-amber)">THANH GHI DỮ LIỆU DUY NHẤT: ADC_DR (16-bit)</text>
    <text x="225" y="90" text-anchor="middle" font-size="11.5" fill="var(--text-muted)">Địa chỉ: 0x4001 244C (Chỉ chứa giá trị của kênh đo gần nhất!)</text>

    <!-- DMA Arrow -->
    <path d="M 225 105 L 225 145" stroke="var(--accent-green)" stroke-width="3" marker-end="url(#arrow)"/>
    <rect x="135" y="115" width="180" height="22" rx="4" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
    <text x="225" y="130" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-green)">DMA Kênh 1 Tự Động Chuyển</text>

    <!-- SRAM Buffer Array -->
    <rect x="30" y="150" width="390" height="145" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="45" y="174" font-size="12.5" font-weight="700" fill="var(--accent-green)">MẢNG BỘ NHỚ SRAM (RAM Buffer): uint16_t adc_buf[3]</text>
    
    <rect x="45" y="185" width="360" height="28" rx="4" fill="#f0fdf4" stroke="var(--card-border)"/>
    <text x="55" y="204" font-size="11.5" font-weight="600" fill="var(--text-primary)">adc_buf[0] ◄── DMA nạp giá trị Kênh 0 (PA0)</text>

    <rect x="45" y="218" width="360" height="28" rx="4" fill="#f0fdf4" stroke="var(--card-border)"/>
    <text x="55" y="237" font-size="11.5" font-weight="600" fill="var(--text-primary)">adc_buf[1] ◄── DMA nạp giá trị Kênh 1 (PA1)</text>

    <rect x="45" y="251" width="360" height="28" rx="4" fill="#f0fdf4" stroke="var(--card-border)"/>
    <text x="55" y="270" font-size="11.5" font-weight="600" fill="var(--text-primary)">adc_buf[2] ◄── DMA nạp giá trị Kênh 16 (Nhiệt độ chip)</text>
  </g>
</svg>"""

# 5. Bai 14: USART IDLE Line Timing
svgs["bai14_uart_idle_line"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 380" width="100%" height="100%">
  <style>
    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-green: #059669;
      --accent-amber: #d97706;
      --accent-red: #dc2626;
      --accent-purple: #7c3aed;
      --wire-line: #334155;
    }
    path { fill: none; }
    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .mono { font-family: ui-monospace, Menlo, Consolas, monospace; }
  </style>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--wire-line)"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--accent-green)"/>
    </marker>
  </defs>

  <rect width="920" height="380" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="460" y="36" text-anchor="middle" font-size="19" font-weight="700" fill="var(--title-color)">GIẢN ĐỒ THỜI GIAN NGẮT NHÀN RỖI (USART IDLE LINE DETECTION)</text>
  <text x="460" y="58" text-anchor="middle" font-size="12.5" fill="var(--subtitle-color)">Cơ chế phát hiện kết thúc gói tin có chiều dài thay đổi mà không cần ký tự kết thúc</text>

  <!-- Waveform panel -->
  <g transform="translate(40, 80)">
    <rect width="840" height="150" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="20" y="30" font-size="13" font-weight="700" fill="var(--accent-blue)">Tín hiệu đường truyền UART RX:</text>

    <!-- Bytes packets -->
    <rect x="50" y="60" width="110" height="40" rx="4" fill="#e0f2fe" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="105" y="85" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-blue)">Byte 1 (RXNE)</text>

    <rect x="180" y="60" width="110" height="40" rx="4" fill="#e0f2fe" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="235" y="85" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-blue)">Byte 2 (RXNE)</text>

    <rect x="310" y="60" width="110" height="40" rx="4" fill="#e0f2fe" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="365" y="85" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-blue)">Byte N (RXNE)</text>

    <!-- Idle Line (Continuous High) -->
    <path d="M 420 80 L 780 80" stroke="var(--accent-amber)" stroke-width="3"/>
    <text x="550" y="70" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-amber)">Đường truyền rảnh rỗi (Mức HIGH liên tục)</text>

    <!-- 1 Frame width marker -->
    <line x1="430" y1="110" x2="670" y2="110" stroke="var(--wire-line)" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
    <rect x="490" y="100" width="120" height="20" rx="3" fill="var(--canvas-bg)" stroke="var(--wire-line)"/>
    <text x="550" y="114" text-anchor="middle" font-size="11" font-weight="600" fill="var(--text-primary)">Đúng 1 Khung (1 Frame)</text>

    <!-- IDLE flag trigger point -->
    <line x1="670" y1="50" x2="670" y2="120" stroke="var(--accent-green)" stroke-width="2" stroke-dasharray="3,3"/>
    <polygon points="665,40 675,40 670,50" fill="var(--accent-green)"/>
    <text x="670" y="35" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-green)">Kéo cờ IDLE = 1!</text>
  </g>

  <!-- Explanation Callout Box -->
  <g transform="translate(40, 250)">
    <rect width="840" height="100" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="25" y="28" font-size="13" font-weight="700" fill="var(--accent-green)">ƯU ĐIỂM CỦA NGẮT IDLE TRONG THIẾT KẾ BỘ GIAO DIỆN CLI &amp; GIAO THỨC TRUYỀN THÔNG:</text>
    <text x="25" y="52" font-size="12" fill="var(--text-primary)">1. Bắt trọn vẹn toàn bộ chuỗi ký tự hoặc gói tin nhị phân không cố định kích thước (Variable Length Frame).</text>
    <text x="25" y="72" font-size="12" fill="var(--text-primary)">2. Không làm CPU quá tải: CPU chỉ vào hàm xử lý đúng một lần duy nhất sau khi toàn bộ gói tin đã được nhận xong.</text>
    <text x="25" y="92" font-size="12" fill="var(--text-muted)">* Quy trình xóa cờ IDLE theo RM0008: Đọc thanh ghi USART_SR tiếp theo đọc thanh ghi USART_DR.</text>
  </g>
</svg>"""

# 6. Bai 16: SPI 8-bit Shift Register Exchange
svgs["bai16_spi_shift_register"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 400" width="100%" height="100%">
  <style>
    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-green: #059669;
      --accent-amber: #d97706;
      --accent-red: #dc2626;
      --accent-purple: #7c3aed;
      --wire-line: #334155;
    }
    path { fill: none; }
    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .mono { font-family: ui-monospace, Menlo, Consolas, monospace; }
  </style>
  <defs>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--accent-blue)"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--accent-green)"/>
    </marker>
  </defs>

  <rect width="940" height="400" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="470" y="36" text-anchor="middle" font-size="19" font-weight="700" fill="var(--title-color)">BẢN CHẤT HOÁN ĐỔI DỮ LIỆU QUA HAI THANH GHI DỊCH SPI (SHIFT REGISTER)</text>
  <text x="470" y="58" text-anchor="middle" font-size="12.5" fill="var(--subtitle-color)">Cứ mỗi xung nhịp SCK, 1 bit trượt đi trên đường MOSI và đồng thời 1 bit trượt về trên đường MISO</text>

  <!-- Master Shift Register Box -->
  <g transform="translate(40, 90)">
    <rect width="360" height="180" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="180" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-blue)">STM32 MASTER SHIFT REGISTER</text>
    <text x="180" y="50" text-anchor="middle" font-size="11.5" fill="var(--text-muted)">Thanh ghi dịch phát/nhận 8-bit nội</text>

    <!-- 8 bits cells -->
    <g transform="translate(20, 70)">
      <rect x="0" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="20" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b7</text>

      <rect x="40" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="60" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b6</text>

      <rect x="80" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="100" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b5</text>

      <rect x="120" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="140" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b4</text>

      <rect x="160" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="180" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b3</text>

      <rect x="200" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="220" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b2</text>

      <rect x="240" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="260" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b1</text>

      <rect x="280" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="300" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-blue)">b0</text>
    </g>

    <text x="180" y="145" text-anchor="middle" font-size="11.5" fill="var(--text-muted)">Dữ liệu dịch ra từ b7 ──> Dữ liệu mới nạp vào b0</text>
  </g>

  <!-- Slave Shift Register Box -->
  <g transform="translate(540, 90)">
    <rect width="360" height="180" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="180" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-green)">SLAVE SHIFT REGISTER (W25Q64 / SENSOR)</text>
    <text x="180" y="50" text-anchor="middle" font-size="11.5" fill="var(--text-muted)">Thanh ghi dịch của thiết bị ngoại vi</text>

    <!-- 8 bits cells -->
    <g transform="translate(20, 70)">
      <rect x="0" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="20" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b7</text>

      <rect x="40" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="60" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b6</text>

      <rect x="80" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="100" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b5</text>

      <rect x="120" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="140" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b4</text>

      <rect x="160" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="180" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b3</text>

      <rect x="200" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="220" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b2</text>

      <rect x="240" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="260" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--text-primary)">b1</text>

      <rect x="280" y="0" width="40" height="40" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
      <text x="300" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-green)">b0</text>
    </g>

    <text x="180" y="145" text-anchor="middle" font-size="11.5" fill="var(--text-muted)">Dữ liệu mới nạp vào b0 ◄── Dữ liệu dịch ra từ b7</text>
  </g>

  <!-- Bus Communication Wires -->
  <!-- Top MOSI Wire -->
  <path d="M 400 180 L 535 180" stroke="var(--accent-blue)" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <rect x="405" y="155" width="130" height="20" rx="3" fill="var(--canvas-bg)" stroke="var(--accent-blue)"/>
  <text x="470" y="169" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-blue)">MOSI (Master Out)</text>

  <!-- Bottom MISO Wire -->
  <path d="M 540 230 L 405 230" stroke="var(--accent-green)" stroke-width="2.5" marker-end="url(#arrow-green)"/>
  <rect x="405" y="235" width="130" height="20" rx="3" fill="var(--canvas-bg)" stroke="var(--accent-green)"/>
  <text x="470" y="249" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-green)">MISO (Slave Out)</text>

  <!-- Rule Callout Box -->
  <g transform="translate(40, 295)">
    <rect width="860" height="85" rx="8" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
    <text x="25" y="26" font-size="13" font-weight="700" fill="var(--accent-purple)">QUY TẮC CỐT LÕI CỦA GIAO TIẾP SPI:</text>
    <text x="25" y="48" font-size="12" fill="var(--text-primary)">• SPI là giao tiếp song công toàn phần (Full-Duplex): Truyền đi 1 byte thì ĐỒNG THỜI nhận về đúng 1 byte.</text>
    <text x="25" y="68" font-size="12" fill="var(--text-primary)">• Khi Master muốn ĐỌC dữ liệu từ Slave, Master bắt buộc phải GỬI 1 byte giả lập (Dummy Byte, thường là 0xFF) để cấp xung SCK.</text>
  </g>
</svg>"""

# 7. Bai 19: STM32F103 Flash Memory Map & User Config Page 63
svgs["bai19_flash_memory_map"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 420" width="100%" height="100%">
  <style>
    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-green: #059669;
      --accent-amber: #d97706;
      --accent-red: #dc2626;
      --accent-purple: #7c3aed;
      --wire-line: #334155;
    }
    path { fill: none; }
    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .mono { font-family: ui-monospace, Menlo, Consolas, monospace; }
  </style>

  <rect width="920" height="420" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="460" y="36" text-anchor="middle" font-size="19" font-weight="700" fill="var(--title-color)">CẤU TRÚC PHÂN TRANG BỘ NHỚ FLASH VÀ VÙNG LƯU THAM SỐ</text>
  <text x="460" y="58" text-anchor="middle" font-size="12.5" fill="var(--subtitle-color)">STM32F103C8T6 Flash 64KB (64 Trang, mỗi trang đúng 1024 Bytes = 1KB)</text>

  <!-- Memory Blocks Stack -->
  <g transform="translate(60, 85)">
    <!-- Page 0 -->
    <rect x="0" y="0" width="450" height="50" rx="4" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="15" y="30" font-size="12.5" font-weight="700" fill="var(--accent-blue)">Page 0 (0x0800 0000 - 0x0800 03FF)</text>
    <text x="310" y="30" font-size="12" fill="var(--text-muted)">Vector Table (1KB)</text>

    <!-- Page 1..61 -->
    <rect x="0" y="60" width="450" height="85" rx="4" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="15" y="95" font-size="12.5" font-weight="700" fill="var(--text-primary)">Page 1 đến Page 61 (0x0800 0400 - 0x0800 F7FF)</text>
    <text x="15" y="120" font-size="11.5" fill="var(--text-muted)">Chứa toàn bộ mã thực thi của chương trình ứng dụng (Application Firmware Code)</text>

    <!-- Page 62 -->
    <rect x="0" y="155" width="450" height="45" rx="4" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="15" y="182" font-size="12" font-weight="600" fill="var(--text-muted)">Page 62 (0x0800 F800 - 0x0800 FBFF) - Vùng đệm dự phòng</text>

    <!-- Page 63 - User safe config -->
    <rect x="0" y="210" width="450" height="70" rx="4" fill="#f0fdf4" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="15" y="238" font-size="13" font-weight="700" fill="var(--accent-green)">Page 63 (0x0800 FC00 - 0x0800 FFFF) [1024 Bytes]</text>
    <text x="15" y="260" font-size="12" font-weight="600" fill="var(--accent-green)">TRANG AN TOÀN LƯU THAM SỐ NGƯỜI DÙNG (USER NON-VOLATILE DATA)</text>
  </g>

  <!-- Right: Operational Rules Callout -->
  <g transform="translate(540, 85)">
    <rect width="330" height="280" rx="8" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
    <text x="165" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-amber)">QUY TẮC VẬT LÝ BỘ NHỚ FLASH:</text>

    <text x="15" y="55" font-size="12" font-weight="700" fill="var(--accent-red)">1. Chỉ có thể ghi 1 → 0</text>
    <text x="15" y="75" font-size="11.5" fill="var(--text-primary)">Phần cứng không thể tự đổi bit 0 thành bit 1 khi ghi đè.</text>

    <text x="15" y="105" font-size="12" font-weight="700" fill="var(--accent-blue)">2. Muốn đổi 0 → 1: Phải Xóa Trang</text>
    <text x="15" y="125" font-size="11.5" fill="var(--text-primary)">Lệnh Page Erase xóa 1024B về giá trị 0xFFFF.</text>

    <text x="15" y="155" font-size="12" font-weight="700" fill="var(--accent-green)">3. Đơn vị ghi tối thiểu (Half-Word)</text>
    <text x="15" y="175" font-size="11.5" fill="var(--text-primary)">Phải ghi theo đơn vị 16-bit (2 bytes) hoặc 32-bit (Word).</text>

    <text x="15" y="205" font-size="12" font-weight="700" fill="var(--accent-purple)">4. Trình tự Mở Khóa FPEC Key</text>
    <text x="15" y="225" font-size="11" class="mono" fill="var(--text-muted)">KEY1: 0x45670123</text>
    <text x="15" y="243" font-size="11" class="mono" fill="var(--text-muted)">KEY2: 0xCDEF89AB</text>
  </g>
</svg>"""

# 8. Bai 24: USB 48MHz Clock Tree & Descriptors
svgs["bai24_usb_clock_tree"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 380" width="100%" height="100%">
  <style>
    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-green: #059669;
      --accent-amber: #d97706;
      --accent-red: #dc2626;
      --accent-purple: #7c3aed;
      --wire-line: #334155;
    }
    path { fill: none; }
    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  </style>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="var(--wire-line)"/>
    </marker>
  </defs>

  <rect width="920" height="380" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="460" y="36" text-anchor="middle" font-size="19" font-weight="700" fill="var(--title-color)">HỆ THỐNG XUNG NHỊP KHỐI USB 2.0 FULL SPEED (48MHz)</text>
  <text x="460" y="58" text-anchor="middle" font-size="12.5" fill="var(--subtitle-color)">Cơ chế phân chia tần số từ PLL 72MHz qua bộ chia USBPRE /1.5</text>

  <!-- Diagram flow -->
  <g transform="translate(40, 95)">
    <!-- Crystal 8MHz -->
    <rect x="0" y="20" width="160" height="60" rx="6" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="80" y="46" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-blue)">Thạch Anh Ngoài</text>
    <text x="80" y="66" text-anchor="middle" font-size="12" fill="var(--text-muted)">HSE = 8.000 MHz</text>

    <!-- PLL x9 -->
    <rect x="220" y="20" width="180" height="60" rx="6" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
    <text x="310" y="46" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-amber)">Bộ Nhân PLL (x9)</text>
    <text x="310" y="66" text-anchor="middle" font-size="12" fill="var(--text-muted)">SYSCLK = 72.000 MHz</text>

    <!-- USB Prescaler /1.5 -->
    <rect x="460" y="20" width="180" height="60" rx="6" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="1.5"/>
    <text x="550" y="46" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-purple)">USB Prescaler (/1.5)</text>
    <text x="550" y="66" text-anchor="middle" font-size="12" fill="var(--text-muted)">Bit USBPRE = 0</text>

    <!-- Target USB Clock -->
    <rect x="700" y="15" width="180" height="70" rx="6" fill="#f0fdf4" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="790" y="44" text-anchor="middle" font-size="13.5" font-weight="700" fill="var(--accent-green)">USB CLOCK</text>
    <text x="790" y="68" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-green)">48.000 MHz (±0.25%)</text>

    <!-- Connectors -->
    <path d="M 160 50 L 220 50" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow)"/>
    <path d="M 400 50 L 460 50" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow)"/>
    <path d="M 640 50 L 700 50" stroke="var(--wire-line)" stroke-width="2" marker-end="url(#arrow)"/>
  </g>

  <!-- Hardware Warning Panel -->
  <g transform="translate(40, 220)">
    <rect width="840" height="125" rx="8" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="1.5"/>
    <text x="25" y="28" font-size="13.5" font-weight="700" fill="var(--accent-red)">LƯU Ý PHẦN CỨNG BẮT BUỘC TRÊN CHÂN D+ (USB PULL-UP RESISTOR):</text>
    <text x="25" y="52" font-size="12.5" fill="var(--text-primary)">• Đường D+ bắt buộc phải có điện trở kéo lên 3.3V trị số đúng <tspan font-weight="700" fill="var(--accent-blue)">1.5kΩ</tspan> để máy tính nhận diện thiết bị Full Speed.</text>
    <text x="25" y="74" font-size="12.5" fill="var(--text-primary)">• Lỗi Blue Pill Trung Quốc: Thường bị hàn nhầm điện trở <tspan font-weight="700" fill="var(--accent-red)">R10 = 10kΩ hoặc 4.7kΩ</tspan> khiến Windows báo lỗi "Device Descriptor Request Failed".</text>
    <text x="25" y="96" font-size="12.5" fill="var(--text-muted)">• Giải pháp khắc phục: Hàn song song thêm điện trở hoặc chủ động kéo chân PA12 xuống GND trước khi khởi tạo USB.</text>
  </g>
</svg>"""

# Write all SVGs to files, plus _light and _dark variants
for name, content in svgs.items():
    # Base
    base_path = os.path.join(BASE_DIR, f"{name}.svg")
    with open(base_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Light
    light_content = content.replace(
        """    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;""",
        """    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #e2e8f0;
      --card-bg: #f8fafc;
      --card-border: #cbd5e1;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #1e293b;
      --text-muted: #64748b;"""
    )
    light_path = os.path.join(BASE_DIR, f"{name}_light.svg")
    with open(light_path, "w", encoding="utf-8") as f:
        f.write(light_content)

    # Dark
    dark_content = content.replace(
        """    :root {
      --canvas-bg: #ffffff;
      --canvas-border: #cbd5e1;
      --card-bg: #f8fafc;
      --card-border: #94a3b8;
      --title-color: #0f172a;
      --subtitle-color: #475569;
      --text-primary: #0f172a;
      --text-muted: #64748b;""",
        """    :root {
      --canvas-bg: #0f172a;
      --canvas-border: #334155;
      --card-bg: #1e293b;
      --card-border: #475569;
      --title-color: #f8fafc;
      --subtitle-color: #94a3b8;
      --text-primary: #f1f5f9;
      --text-muted: #94a3b8;"""
    ).replace('fill="#f0fdf4"', 'fill="#064e3b"').replace('fill="#fef2f2"', 'fill="#450a0a"').replace('fill="#e0f2fe"', 'fill="#0c4a6e"')
    dark_path = os.path.join(BASE_DIR, f"{name}_dark.svg")
    with open(dark_path, "w", encoding="utf-8") as f:
        f.write(dark_content)

print(f"Successfully generated {len(svgs)} missing schematics (total {len(svgs)*3} files including variants).")
