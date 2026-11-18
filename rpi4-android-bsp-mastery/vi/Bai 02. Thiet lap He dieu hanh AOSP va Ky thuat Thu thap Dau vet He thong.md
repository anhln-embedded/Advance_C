# BÀI 02: THIẾT LẬP HỆ ĐIỀU HÀNH AOSP VÀ KỸ THUẬT THU THẬP DẤU VẾT HỆ THỐNG

> Tóm tắt: Hướng dẫn tải và kiểm tra toàn vẹn bản build KonstaKANG AOSP 17 cho Raspberry Pi 4, thiết lập kết nối ADB từ xa và thực thi quy trình điều tra dấu vết hệ điều hành (Reverse Engineering & OS Fingerprinting) để thu thập cấu hình nhân, chính sách bảo mật SELinux và trạng thái ngoại vi làm cơ sở đối chuẩn mã nguồn.

---

## 1. Nguồn Gốc Bản Build & Quy Trình Kiểm Tra Toàn Vẹn Tệp Tin

Trong quá trình phát triển BSP cho một thiết bị thực tế, kỹ sư thường phải làm việc trên một bản build Android đã được nạp sẵn trên phần cứng (Prebuilt Image). Bước đầu tiên mang tính sống còn là **xác minh nguồn gốc và tính toàn vẹn (Integrity Check)** của tệp tin ảnh hệ điều hành trước khi nạp vào thẻ nhớ microSD.

<p align="center">
  <img src="images/bai02_image_integrity_flash_workflow.svg" width="950" alt="Quy trình kiểm chuẩn mã băm SHA-256 và nạp ROM AOSP">
</p>

### Thông số kiểm chuẩn của bản phát hành tham chiếu:
- **Tên tệp tin**: `AOSP17-20261030-KonstaKANG-rpi4.zip`
- **Trang phân phối chính thức**: [KonstaKANG Raspberry Pi 4 AOSP 17](https://konstakang.com/devices/rpi4/AOSP17/)
- **Mã băm SHA-256 chuẩn**:
  ```text
  9c02408206053b8bcbf7591a02d8d28d09becf17cfa522f52a945c5f87deb709
  ```

### Lệnh tính mã băm trên máy tính phát triển:

* **Trên Windows (PowerShell)**:
  ```powershell
  Get-FileHash .\AOSP17-20261030-KonstaKANG-rpi4.zip -Algorithm SHA256
  ```

* **Trên Linux / macOS (Bash)**:
  ```bash
  sha256sum AOSP17-20261030-KonstaKANG-rpi4.zip
  ```

> [!WARNING]
> **Cảnh báo bản quyền & Giấy phép sử dụng:**
> - Bản ROM KonstaKANG chứa các thành phần tuân theo giấy phép **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.
> - Tác giả nghiêm cấm các hành vi sử dụng cho mục đích thương mại hoặc tự ý tải lại (re-upload/mirror) lên các máy chủ khác mà không có sự cho phép. Mọi liên kết chia sẻ bắt buộc phải dẫn về trang web gốc của dự án.

---

## 2. Quy Trình Nạp Image & Khởi Động Lần Đầu

1. Sử dụng công cụ **Raspberry Pi Imager** (hoặc `dd` trên Linux / BalenaEtcher).
2. Chọn tệp ảnh đã giải nén (file `.img`).
3. Chọn chính xác ổ đĩa thẻ nhớ microSD (dung lượng khuyến nghị $\ge 16\text{ GB}$, chuẩn Class 10 U3 A2 để đảm bảo tốc độ đọc ghi ngẫu nhiên cho Android).
4. Nhấn **Write** và chờ quá trình xác thực hoàn tất trước khi rút thẻ nhớ ra.
5. Cắm thẻ vào Raspberry Pi 4, kết nối chuột, bàn phím, cáp micro-HDMI lên màn hình và cắm nguồn USB-C (chuẩn $5\text{V} / 3\text{A}$).
6. Khi Android khởi động vào màn hình chính:
   - Truy cập **Settings** $→$ **About tablet** $→$ Chạm liên tục 7 lần vào mục **Build number** để mở khóa chế độ lập trình viên (**Developer options**).
   - Truy cập **System** $→$ **Developer options**: Bật mục **USB debugging** và **Network ADB debugging** (cho phép gỡ lỗi qua mạng LAN).

---

## 3. Thiết Lập Cầu Nối Gỡ Lỗi Android (ADB Over TCP/IP)

Trên máy tính phát triển, kiểm tra công cụ `adb` trong Android SDK Platform-Tools:

```bash
# Kiểm tra phiên bản ADB trên host
adb version

# Kết nối tới Raspberry Pi 4 qua địa chỉ IP (thay thế bằng IP thực tế của board)
adb connect 192.168.1.150:5555

# Xác nhận thiết bị đã ở trạng thái 'device'
adb devices
```

Kết quả mong đợi:
```text
List of devices attached
192.168.1.150:5555    device
```

---

## 4. Kỹ Thuật Trích Xuất Dấu Vết Hệ Thống (OS & Kernel Fingerprinting)

Để có thể biên dịch mã nguồn tương thích 100% với một hệ thống Android đang chạy, kỹ sư bắt buộc phải trích xuất đủ **5 nhóm dấu vết kỹ thuật**:

<p align="center">
  <img src="images/bai02_os_reverse_fingerprinting_tree.svg" width="950" alt="Cây thu thập dấu vết hệ thống Android và Kernel">
</p>

### 4.1. Trích xuất dấu vết Android Build Properties
Chạy chuỗi lệnh sau để lấy thông tin phiên bản AOSP:

```bash
adb shell getprop ro.build.fingerprint
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.type
adb shell getprop ro.product.device
```

* **Dữ liệu thực tế ghi nhận từ baseline lab**:
  - `ro.build.version.release`: `17` (Android 17 Preview / AOSP)
  - `ro.build.version.sdk`: `36`
  - `ro.product.device`: `rpi4`
  - `ro.build.type`: `userdebug` (Cho phép quyền root trên shell ADB thông qua lệnh `adb root`)

### 4.2. Trích xuất danh tính nhân Linux (Kernel Identity)
Đây là dữ liệu quyết định trực tiếp đến chuỗi **`vermagic`** của mọi driver module:

```bash
adb shell uname -a
adb shell uname -r
adb shell cat /proc/version
adb shell cat /proc/cmdline
```

* **Dữ liệu phân tích chuyên sâu**:
  ```text
  Linux localhost 6.18.38-g7a9131c1065a-v8 #1 SMP PREEMPT Thu Oct 30 14:15:20 UTC 2026 aarch64
  ```
  - **Phiên bản nhân gốc (Base Version)**: `6.18.38` (Nhân Linux Long Term Support - LTS).
  - **Hậu tố mã nguồn Git (SCM Suffix)**: `-g7a9131c1065a`.
    - Ký tự `g` đại diện cho Git.
    - Chuỗi `7a9131c1065a` chính là **12 ký tự đầu của Git Commit SHA-1** của nhánh kernel đã build ra bản ROM này!
  - **Hậu tố phiên bản cục bộ (Local Version)**: `-v8` (Quy định kiến trúc 64-bit ARMv8 trong file defconfig của Raspberry Pi).

### 4.3. Giải nén và phân tích cấu hình nhân (`/proc/config.gz`)
Nhân Android thường được cấu hình cờ `CONFIG_IKCONFIG_PROC=y`, cho phép trích xuất toàn bộ file `.config` lúc biên dịch trực tiếp từ bộ nhớ RAM:

```bash
# Tải file nén cấu hình về máy tính host
adb pull /proc/config.gz ./device_config.gz
zcat ./device_config.gz > ./device_kernel.config

# Lọc các tham số quyết định đến khả năng nạp Kernel Module:
grep -E 'CONFIG_MODULES|CONFIG_MODVERSIONS|CONFIG_MODULE_SIG|CONFIG_LEDS|CONFIG_GPIO' ./device_kernel.config
```

* **Kết quả đối soát cực kỳ quan trọng**:
  ```ini
  CONFIG_MODULES=y                  # Cho phép nạp module ngoài vào kernel
  CONFIG_MODULE_UNLOAD=y           # Cho phép gỡ bỏ module bằng lệnh rmmod
  CONFIG_MODVERSIONS=y             # Kích hoạt kiểm tra mã băm CRC của symbol
  CONFIG_MODULE_SIG=y              # Hỗ trợ cơ chế ký số module (Module Signature)
  CONFIG_MODULE_SIG_ALL=y          # Tự động ký tất cả module nội bộ lúc build
  CONFIG_LEDS_CLASS=y              # Kích hoạt Linux LED Subsystem
  CONFIG_LEDS_GPIO=y               # Kích hoạt driver điều khiển LED qua GPIO
  CONFIG_OF=y                      # Kích hoạt cơ chế nạp cấu hình qua Device Tree
  ```

> [!IMPORTANT]
> **Hệ quả của cờ `CONFIG_MODVERSIONS=y`:**
> Khi cờ này được bật, nhân Linux không chỉ kiểm tra chuỗi phiên bản chữ thô, mà còn so sánh **mã băm CRC 32-bit** của từng hàm kernel mà module gọi (ví dụ `printk`, `module_layout`). Bất kỳ sự sai lệch nào về cấu trúc dữ liệu (`struct`) giữa header lúc build module và kernel đang chạy đều sẽ khiến lệnh `insmod` bị từ chối với lỗi `disagrees about version of symbol`.

### 4.4. Kiểm tra chính sách bảo mật & ký số module
```bash
# Kiểm tra trạng thái SELinux (Enforcing hay Permissive)
adb shell getenforce

# Kiểm tra xem hệ thống có khóa hoàn toàn việc nạp module hay không
adb shell cat /proc/sys/kernel/modules_disabled

# Kiểm tra xem kernel có ép buộc chữ ký số hợp lệ mới cho nạp module hay không
adb shell cat /sys/module/module/parameters/sig_enforce
```

* **Kết quả quan sát**:
  - `modules_disabled`: `0` (Hệ thống cho phép nạp thêm module).
  - `sig_enforce`: `N` (Kernel có hỗ trợ chữ ký nhưng **không bắt buộc** ở chế độ cưỡng chế nghiêm ngặt. Khi nạp module chưa ký, kernel sẽ chỉ cảnh báo và đánh dấu trạng thái *Kernel Taint* chứ không chặn đứng).

### 4.5. Khảo sát các nút điều khiển ngoại vi hiện có (Sysfs Nodes)
```bash
# Kiểm tra các bóng đèn LED đã được kernel khởi tạo sẵn
adb shell ls -la /sys/class/leds/

# Kiểm tra giao diện GPIO
adb shell ls -la /sys/class/gpio/
adb shell ls -la /dev/gpiochip*
```

---

## 5. Tạo Tệp Hồ Sơ Tham Chiếu Hệ Thống (`device-baseline.txt`)

Sau khi hoàn tất quá trình điều tra, kỹ sư cần tổng hợp toàn bộ thông tin vào tệp hồ sơ kỹ thuật để làm căn cứ đối soát xuyên suốt toàn bộ dự án:

```text
==================================================================
TỆP HỒ SƠ THAM CHIẾU HỆ THỐNG (DEVICE BASELINE AUDIT)
Dự án: Raspberry Pi 4 Model B - Android BSP Mastery
Ngày kiểm định: 30/10/2026
==================================================================

[1. PHẦN CỨNG]
- Bo mạch: Raspberry Pi 4 Model B Rev 1.5 (RAM 4GB)
- Vi xử lý: Broadcom BCM2711 SoC (Cortex-A72 Quad-core)
- Chân điều khiển LED mục tiêu: BCM GPIO17 (Physical Pin 11)
- Chân tiếp địa mạch điện: GND (Physical Pin 6)

[2. PHIÊN BẢN ANDROID]
- Bản phân phối: KonstaKANG AOSP 17
- Ngày phát hành: 30/10/2026
- Android Release: 17 (SDK 36)
- Build Type: userdebug
- Build Fingerprint: raspberry/rpi4/rpi4:17/...:userdebug/test-keys

[3. DANH TÍNH NHÂN LINUX (KERNEL IDENTITY)]
- Release String: 6.18.38-g7a9131c1065a-v8
- Base Version: 6.18.38
- Git SCM Commit: 7a9131c1065a28544c1b6592152981b4c4102367
- Local Version: -v8
- Cấu trúc cờ Vermagic: SMP preempt mod_unload modversions aarch64

[4. CHÍNH SÁCH BẢO MẬT & NẠP MODULE]
- SELinux Mode: Enforcing
- modules_disabled: 0 (Được phép nạp module)
- sig_enforce: N (Cảnh báo Taint khi thiếu chữ ký, không panic)
- Modversions: Có kích hoạt (Bắt buộc khớp Module.symvers)

[5. TRẠNG THÁI NGOẠI VI]
- LED Class Subsystem: Sẵn sàng tại /sys/class/leds/
- GPIO Subsystem: Hỗ trợ cả /dev/gpiochipX và Device Tree gpio-leds
==================================================================
```

---

## 6. Bài Tập Tự Đánh Giá & Vận Dụng

1. **Phân tích SCM Hash**: Giả sử lệnh `uname -r` trên bo mạch trả về `6.18.38-v8` (không có đoạn `-g<hash>`). Điều này phản ánh điều gì về quá trình biên dịch kernel của nhà phát triển bản ROM đó? Cờ cấu hình nào trong nhân kiểm soát hành vi này?
2. **Kỹ thuật trích xuất `config.gz`**: Nếu trên một bo mạch Android lạ, lệnh `adb shell ls /proc/config.gz` báo lỗi `No such file or directory`, bạn sẽ dùng những giải pháp nào khác để tái tạo lại file cấu hình `.config` của nhân đó?
3. **Thực hành ADB Scripting**: Viết một đoạn script Bash ngắn (`audit_device.sh`) tự động chạy toàn bộ các lệnh kiểm tra trên và xuất ra báo cáo tóm tắt dưới dạng bảng Markdown.
