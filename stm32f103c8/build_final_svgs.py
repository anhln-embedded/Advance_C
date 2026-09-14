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

# 1. SG90 Servo Timing
svg_sg90 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 400" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="920" height="400" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="460" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">GIẢN ĐỒ XUNG ĐIỀU KHIỂN ĐỘNG CƠ RC SERVO SG90 (CHU KỲ 20MS / 50HZ)</text>
  <text x="460" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Độ rộng xung mức cao từ 0.5ms (-90°) đến 2.5ms (+90°)</text>

  <!-- 0.5ms Pulse (Góc -90°) -->
  <g transform="translate(60, 95)">
    <text x="0" y="22" font-size="13" font-weight="700" fill="var(--accent-blue)">Góc 0° / -90° (T_on = 0.5ms / CCR = 50)</text>
    <polyline points="0,60 40,60 40,25 70,25 70,60 800,60" fill="none" stroke="var(--accent-blue)" stroke-width="2.5"/>
    <line x1="40" y1="20" x2="70" y2="20" stroke="var(--accent-blue)" stroke-width="1.5"/>
    <text x="55" y="15" text-anchor="middle" font-size="10" fill="var(--accent-blue)">0.5ms</text>
  </g>

  <!-- 1.5ms Pulse (Góc 90°) -->
  <g transform="translate(60, 190)">
    <text x="0" y="22" font-size="13" font-weight="700" fill="var(--accent-green)">Góc Trung Tâm 90° (T_on = 1.5ms / CCR = 150)</text>
    <polyline points="0,60 40,60 40,25 130,25 130,60 800,60" fill="none" stroke="var(--accent-green)" stroke-width="2.5"/>
    <line x1="40" y1="20" x2="130" y2="20" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="85" y="15" text-anchor="middle" font-size="10" fill="var(--accent-green)">1.5ms</text>
  </g>

  <!-- 2.5ms Pulse (Góc 180°) -->
  <g transform="translate(60, 285)">
    <text x="0" y="22" font-size="13" font-weight="700" fill="var(--accent-amber)">Góc Tối Đa 180° / +90° (T_on = 2.5ms / CCR = 250)</text>
    <polyline points="0,60 40,60 40,25 190,25 190,60 800,60" fill="none" stroke="var(--accent-amber)" stroke-width="2.5"/>
    <line x1="40" y1="20" x2="190" y2="20" stroke="var(--accent-amber)" stroke-width="1.5"/>
    <text x="115" y="15" text-anchor="middle" font-size="10" fill="var(--accent-amber)">2.5ms</text>
  </g>
</svg>"""

save_svg("bai07_servo_sg90_timing.svg", svg_sg90)

# 2. I2C Transfer Sequence
svg_i2c_seq = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 400" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="920" height="400" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="460" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">TRÌNH TỰ TRUYỀN DỮ LIỆU I2C MASTER PHẦN CỨNG THEO SỰ KIỆN (EVENTS)</text>
  <text x="460" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Các bước kiểm tra cờ trạng thái SR1 và SR2 đảm bảo bus không bị treo</text>

  <g transform="translate(40, 100)">
    <!-- Step 1: START -->
    <rect x="0" y="0" width="150" height="120" rx="8" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="75" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-blue)">1. START BIT</text>
    <text x="75" y="55" text-anchor="middle" font-size="11" fill="var(--text-primary)">Bật CR1-&gt;START</text>
    <rect x="15" y="70" width="120" height="35" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="75" y="92" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-amber)">Chờ EV5 (SB = 1)</text>

    <!-- Arrow 1 -->
    <path d="M 150 60 L 180 60" stroke="var(--bus-line)" stroke-width="2"/>

    <!-- Step 2: ADDR -->
    <rect x="180" y="0" width="160" height="120" rx="8" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="260" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-purple)">2. GỬI ĐỊA CHỈ</text>
    <text x="260" y="55" text-anchor="middle" font-size="11" fill="var(--text-primary)">Ghi Slave Addr + W/R</text>
    <rect x="195" y="70" width="130" height="35" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="260" y="92" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-amber)">Chờ EV6 (ADDR = 1)</text>

    <!-- Arrow 2 -->
    <path d="M 340 60 L 370 60" stroke="var(--bus-line)" stroke-width="2"/>

    <!-- Step 3: CLEAR ADDR -->
    <rect x="370" y="0" width="150" height="120" rx="8" fill="var(--card-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="445" y="30" text-anchor="middle" font-size="13" font-weight="700" fill="var(--title-color)">3. XÓA CỜ ADDR</text>
    <text x="445" y="55" text-anchor="middle" font-size="11" fill="var(--text-primary)">Đọc thanh ghi SR1</text>
    <text x="445" y="75" text-anchor="middle" font-size="11" fill="var(--text-primary)">Đọc thanh ghi SR2</text>
    <text x="445" y="98" text-anchor="middle" font-size="10" fill="var(--text-muted)">(Tự động xóa)</text>

    <!-- Arrow 3 -->
    <path d="M 520 60 L 550 60" stroke="var(--bus-line)" stroke-width="2"/>

    <!-- Step 4: DATA TX -->
    <rect x="550" y="0" width="150" height="120" rx="8" fill="var(--card-bg)" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="625" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-green)">4. GỬI DỮ LIỆU</text>
    <text x="625" y="55" text-anchor="middle" font-size="11" fill="var(--text-primary)">Ghi DR = Data</text>
    <rect x="565" y="70" width="120" height="35" rx="4" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="625" y="92" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent-amber)">Chờ EV8 (TXE / BTF)</text>

    <!-- Arrow 4 -->
    <path d="M 700 60 L 730 60" stroke="var(--bus-line)" stroke-width="2"/>

    <!-- Step 5: STOP -->
    <rect x="730" y="0" width="110" height="120" rx="8" fill="var(--card-bg)" stroke="var(--accent-red)" stroke-width="2"/>
    <text x="785" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-red)">5. STOP</text>
    <text x="785" y="65" text-anchor="middle" font-size="11" fill="var(--text-primary)">CR1-&gt;STOP</text>
    <text x="785" y="90" text-anchor="middle" font-size="10" fill="var(--text-muted)">Giải phóng Bus</text>
  </g>

  <!-- Warning Box -->
  <g transform="translate(40, 260)">
    <rect width="840" height="90" rx="8" fill="var(--card-bg)" stroke="var(--accent-amber)" stroke-width="1.5"/>
    <text x="420" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-amber)">LƯU Ý SỐNG CÒN TRÁNH TREO VÒNG LẶP VÔ HẠN (DEADLOCK):</text>
    <text x="420" y="58" text-anchor="middle" font-size="12" fill="var(--text-primary)">Mọi hàm chờ cờ `while (!I2C_CheckEvent(...))` bắt buộc phải cài đặt biến Timeout. Nếu thiết bị I2C không phản hồi,</text>
    <text x="420" y="78" text-anchor="middle" font-size="12" fill="var(--text-primary)">hệ thống sẽ thoát lỗi thay vì bị đơ vĩnh viễn trong ngắt hoặc hàm truyền.</text>
  </g>
</svg>"""

save_svg("bai15_i2c_transfer_sequence.svg", svg_i2c_seq)

# 3. CAN Bus Frame Format
svg_can_frame = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 380" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="940" height="380" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="470" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">CẤU TRÚC KHUNG DỮ LIỆU CHUẨN CAN 2.0A (STANDARD DATA FRAME)</text>
  <text x="470" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Các trường định dạng: Định danh 11-bit, Điều khiển, Trọng tải dữ liệu và Mã kiểm tra CRC</text>

  <!-- Frame Fields -->
  <g transform="translate(40, 110)">
    <!-- SOF -->
    <rect x="0" y="0" width="60" height="100" rx="6" fill="var(--accent-blue)" fill-opacity="0.2" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="30" y="45" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-blue)">SOF</text>
    <text x="30" y="70" text-anchor="middle" font-size="10" fill="var(--text-muted)">1 bit</text>

    <!-- Identifier -->
    <rect x="65" y="0" width="170" height="100" rx="6" fill="var(--accent-purple)" fill-opacity="0.2" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="150" y="40" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-purple)">IDENTIFIER</text>
    <text x="150" y="60" text-anchor="middle" font-size="11" fill="var(--text-primary)">11-bit ID (0..0x7FF)</text>
    <text x="150" y="80" text-anchor="middle" font-size="10" fill="var(--text-muted)">Quyết định trọng số ưu tiên</text>

    <!-- Control -->
    <rect x="240" y="0" width="120" height="100" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="300" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="var(--title-color)">CONTROL</text>
    <text x="300" y="60" text-anchor="middle" font-size="11" fill="var(--text-primary)">RTR, IDE, r0, DLC</text>
    <text x="300" y="80" text-anchor="middle" font-size="10" fill="var(--text-muted)">6 bits</text>

    <!-- Data -->
    <rect x="365" y="0" width="220" height="100" rx="6" fill="var(--accent-green)" fill-opacity="0.2" stroke="var(--accent-green)" stroke-width="2"/>
    <text x="475" y="40" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-green)">DATA FIELD</text>
    <text x="475" y="60" text-anchor="middle" font-size="12" fill="var(--text-primary)">0 đến 8 Bytes Payload</text>
    <text x="475" y="80" text-anchor="middle" font-size="10" fill="var(--text-muted)">Tùy biến kích thước theo DLC</text>

    <!-- CRC -->
    <rect x="590" y="0" width="120" height="100" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)" stroke-width="1.5"/>
    <text x="650" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="var(--title-color)">CRC FIELD</text>
    <text x="650" y="60" text-anchor="middle" font-size="11" fill="var(--text-primary)">15-bit CRC</text>
    <text x="650" y="80" text-anchor="middle" font-size="10" fill="var(--text-muted)">+ 1 bit Delimiter</text>

    <!-- ACK -->
    <rect x="715" y="0" width="80" height="100" rx="6" fill="var(--accent-amber)" fill-opacity="0.2" stroke="var(--accent-amber)" stroke-width="2"/>
    <text x="755" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-amber)">ACK</text>
    <text x="755" y="70" text-anchor="middle" font-size="10" fill="var(--text-muted)">2 bits</text>

    <!-- EOF -->
    <rect x="800" y="0" width="60" height="100" rx="6" fill="var(--accent-red)" fill-opacity="0.2" stroke="var(--accent-red)" stroke-width="2"/>
    <text x="830" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-red)">EOF</text>
    <text x="830" y="70" text-anchor="middle" font-size="10" fill="var(--text-muted)">7 bits</text>
  </g>

  <!-- Explanation -->
  <g transform="translate(40, 240)">
    <rect width="860" height="90" rx="8" fill="var(--card-bg)" stroke="var(--card-border)"/>
    <text x="30" y="32" font-size="13" font-weight="700" fill="var(--accent-purple)">ĐẶC TÍNH ARBITRATION (PHÂN XỬ TRUYỀN THÔNG TRÊN BUS):</text>
    <text x="30" y="56" font-size="12" fill="var(--text-primary)">• Bit mức `0` là bit Trội (Dominant), bit mức `1` là bit Lặn (Recessive).</text>
    <text x="30" y="76" font-size="12" fill="var(--text-primary)">• Node nào có Identifier mang giá trị nhỏ hơn sẽ chiếm quyền bus mà không làm hỏng dữ liệu (Không xung đột gói tin).</text>
  </g>
</svg>"""

save_svg("bai23_can_frame_format.svg", svg_can_frame)

# 4. Bootloader Vector Table Jump
svg_jump = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 380" width="100%" height="100%">
{COMMON_STYLES}
  <rect width="920" height="380" rx="14" fill="var(--canvas-bg)" stroke="var(--canvas-border)" stroke-width="2"/>
  <text x="460" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="var(--title-color)">QUY TRÌNH CHUYỂN TIẾP THỰC THI: BOOTLOADER → APPLICATION</text>
  <text x="460" y="62" text-anchor="middle" font-size="13" fill="var(--subtitle-color)">Kiểm tra tính hợp lệ của ngăn xếp MSP và nhảy đến con trỏ Reset Handler</text>

  <!-- Memory Box -->
  <g transform="translate(50, 100)">
    <rect width="360" height="230" rx="10" fill="var(--card-bg)" stroke="var(--accent-blue)" stroke-width="2"/>
    <text x="180" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-blue)">VECTOR TABLE CỦA APPLICATION</text>

    <rect x="25" y="55" width="310" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="40" y="80" font-size="12" font-weight="700" fill="var(--title-color)">Địa chỉ: 0x0800 3000</text>
    <text x="40" y="102" font-size="12" fill="var(--accent-amber)">Giá trị Initial MSP: 0x2000 5000 (RAM Top)</text>

    <rect x="25" y="135" width="310" height="65" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="40" y="160" font-size="12" font-weight="700" fill="var(--title-color)">Địa chỉ: 0x0800 3004</text>
    <text x="40" y="182" font-size="12" fill="var(--accent-green)">Con trỏ Reset_Handler: 0x0800 3125 (Thumb)</text>
  </g>

  <!-- Jump Sequence Steps -->
  <g transform="translate(460, 100)">
    <rect width="410" height="230" rx="10" fill="var(--card-bg)" stroke="var(--accent-purple)" stroke-width="2"/>
    <text x="205" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent-purple)">3 BƯỚC THỰC THI CHUYỂN GIAO QUYỀN ĐIỀU KHIỂN</text>

    <rect x="20" y="55" width="370" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="30" y="82" font-size="11" font-weight="600" fill="var(--text-primary)">1. Vô hiệu hóa toàn bộ ngắt: __disable_irq()</text>

    <rect x="20" y="110" width="370" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--card-border)"/>
    <text x="30" y="137" font-size="10.5" font-weight="600" fill="var(--text-primary)">2. Nạp đỉnh ngăn xếp: __set_MSP(*((uint32_t*)APP_ADDR))</text>

    <rect x="20" y="165" width="370" height="45" rx="6" fill="var(--canvas-bg)" stroke="var(--accent-green)" stroke-width="1.5"/>
    <text x="30" y="192" font-size="11" font-weight="700" fill="var(--accent-green)">3. Nhảy đến hàm Application: app_entry()</text>
  </g>

  <path d="M 410 200 L 460 200" stroke="var(--bus-line)" stroke-width="2"/>
</svg>"""

save_svg("bai25_vector_table_jump.svg", svg_jump)

print("ALL ADVANCED SVGS COMPLETED!")
