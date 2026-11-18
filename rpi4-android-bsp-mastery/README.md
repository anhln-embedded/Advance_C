# Lập Trình Android BSP Chuyên Sâu Trên Raspberry Pi 4: Từ Linux Kernel Đến Stable AIDL HAL, Framework System Service & Java Application

> Khóa học kỹ thuật chuyên sâu toàn diện về Board Support Package (BSP) trên hệ điều hành Android, dẫn dắt kỹ sư qua toàn bộ phân tầng kiến trúc từ nhân Linux 6.18 LTS (GKI), hệ thống build Google Kleaf / Bazel, Device Tree Overlay, Linux LED Subsystem đến Stable AIDL HAL (NDK Backend), chính sách bảo mật SELinux, Android Framework System Service và ứng dụng Java APK điều khiển phần cứng thực tế.

---

## 1. Giới Thiệu Chuyên Đề & Mục Tiêu Đào Tạo

Trong ngành công nghiệp phát triển hệ điều hành nhúng thông minh (Android Automotive, Smart EV Cockpit, Industrial IoT Touchscreen, POS Terminal), việc xây dựng một tính năng điều khiển phần cứng không đơn thuần là mở một file GPIO rồi ghi dữ liệu. Một kiến trúc chuẩn mực của Google Android đòi hỏi phải tuân thủ nghiêm ngặt mô hình phân tách Treble, ranh giới bảo mật SELinux và kiến trúc IPC Binder nhiều tầng:

<p align="center">
  <img src="images/bai01_android_bsp_end_to_end_architecture.svg" width="950" alt="Kiến trúc toàn trình Android BSP trên Raspberry Pi 4">
</p>

### Mục tiêu kỹ thuật cốt lõi:
1. **Nắm vững hệ điều hành Android Image**: Phân tích và trích xuất dấu vết (fingerprint, kernel release, config, selinux) từ bản build KonstaKANG AOSP 17 (Linux 6.18 LTS).
2. **Làm chủ công nghệ build hiện đại Google Kleaf / Bazel**: Hiểu rõ kiến trúc hermetic toolchain (Clang), cơ chế sandbox isolation, DDK Module (`ddk_module`) và xử lý triệt để bài toán `vermagic` mismatch thông qua SCM Stamping (`workspace_status.json`).
3. **Lập trình Driver & Device Tree Overlay**: Cấu hình Device Tree node `gpio-leds` binding, điều khiển LED class (`brightness`, `trigger=timer`) thay vì thao tác thanh ghi thô.
4. **Phát triển Stable AIDL HAL**: Chuyển đổi từ HIDL lỗi thời sang chuẩn Stable AIDL (`@VintfStability`), viết Native Daemon bằng C++ NDK Backend (`libbinder_ndk`), khai báo VINTF Manifest và `init.rc`.
5. **Thực thi chính sách bảo mật SELinux**: Viết quy tắc Type Enforcement (`.te`), gán nhãn `file_contexts`, `service_contexts`, giải quyết dứt điểm các lỗi vi phạm `avc: denied` theo chuẩn CTS/VTS.
6. **Mở rộng Android Framework**: Thêm `LedService` vào `SystemServer`, quản lý luồng, cấp quyền `android.permission.CONTROL_LED`, xử lý Binder death recipient và xây dựng Client SDK `LedManager`.
7. **Xây dựng ứng dụng hoàn chỉnh**: Phát triển `LedController.apk` bằng Java thuần với đầy đủ tính năng ON, OFF, BLINK thời gian thực.

---

## 2. Hệ Thống Hình Ảnh & Sơ Đồ Kiến Trúc

Khóa học được trang bị hệ thống sơ đồ kiến trúc chuẩn vector SVG độ phân giải cao được tối ưu hóa cho hiển thị Web LMS:

1. **Sơ đồ phân tầng kiến trúc toàn trình**: `images/bai01_android_bsp_end_to_end_architecture.svg`
2. **Quy trình biên dịch Kleaf / Bazel & Vermagic SCM Stamping**: `images/bai02_kleaf_bazel_kernel_build_flow.svg`
3. **Mô hình bảo mật SELinux & Giao dịch Stable AIDL xuyên biên giới Treble**: `images/bai03_stable_aidl_selinux_security_model.svg`
4. **Sơ đồ mạch điện GPIO Pinout & Mạch bảo vệ đèn LED**: `images/bai04_rpi4_gpio_led_circuit_schematic.svg`

<p align="center">
  <img src="images/bai01_android_bsp_end_to_end_architecture.svg" width="950" alt="Kiến trúc toàn trình Android BSP trên Raspberry Pi 4">
</p>

---

## 3. Khung Chương Trình Đào Tạo (Syllabus Roadmap)

Chuyên đề được phân chia thành **6 Học phần (21 Bài học thực chiến)**:

### Module 1: Nền Tảng Phần Cứng Raspberry Pi 4 & Phân Tích Android OS Image
- **Bài 01**: Tổng quan kiến trúc toàn trình Android BSP, sơ đồ chân GPIO Raspberry Pi 4 và an toàn phần cứng.
- **Bài 02**: Tải image KonstaKANG AOSP, nạp thẻ nhớ, thiết lập ADB qua mạng TCP và trích xuất dấu vết hệ điều hành.

### Module 2: Môi Trường Biên Dịch Nhân AOSP: Google Kleaf, Bazel & Out-of-tree Kernel Module
- **Bài 03**: Chiến lược dò tìm và đồng bộ mã nguồn AOSP Kernel tương thích (`android_kernel_manifest`, `android_kernel_brcm_rpi`).
- **Bài 04**: Giải mã hệ thống build Google Kleaf / Bazel: Hermetic Clang Toolchain, Sandbox Isolation và cấu hình defconfig RPi4.
- **Bài 05**: Lab thực hành 1: Xây dựng Kernel Module Hello World đầu tiên bằng Bazel DDK (`ddk_module`), giải quyết phụ thuộc Firmware `regulatory.db`.
- **Bài 06**: Bí mật `vermagic`, `CONFIG_MODVERSIONS`, CRC symbol matching, SCM Stamping (`workspace_status.json`) và cơ chế ký số Module.
- **Bài 07**: Kỹ thuật nạp và gỡ bỏ Kernel Module qua ADB (`insmod`, `rmmod`), phân tích Kernel Ring Buffer (`dmesg`) và hiện tượng Kernel Tainting.

### Module 3: Hệ Thống GPIO, Device Tree & Phân Tầng Linux LED Class Subsystem
- **Bài 08**: Giải phẫu kiến trúc Linux GPIO: Từ sysfs cổ điển đến GPIO Descriptor Core (`gpiod_*`) và Controller BCM2711.
- **Bài 09**: Cấu trúc Device Tree và viết Device Tree Overlay (`.dts` / `.dtbo`) cho `gpio-leds` binding trên Raspberry Pi 4.
- **Bài 10**: Lab thực hành 2: Đưa chân GPIO17 vào Linux LED Class (`/sys/class/leds/user-led/`), điều khiển `brightness` và kích hoạt chế độ nhấp nháy phần cứng `timer trigger`.

### Module 4: Tầng Trừu Tượng Phần Cứng Android (Vendor HAL) Chuẩn Stable AIDL
- **Bài 11**: So sánh kiến trúc HAL: Từ Legacy HAL đến HIDL (deprecated) và chuẩn hóa Stable AIDL (`@VintfStability`) trong Android hiện đại.
- **Bài 12**: Thiết kế giao diện AIDL `ILed.aidl`, cấu hình `Android.bp` sinh mã C++ NDK Backend và thư viện `libbinder_ndk`.
- **Bài 13**: Lab thực hành 3: Lập trình Native HAL Daemon C++ (`vendor.example.hardware.led-service`), xử lý File I/O an toàn và quản lý luồng điều khiển LED.
- **Bài 14**: Cấu hình VINTF Manifest (`manifest.xml`) và cơ chế khởi chạy dịch vụ qua `init.rc`.
- **Bài 15**: Thiết lập chính sách bảo mật SELinux chuyên sâu: Type Enforcement, gán nhãn `file_contexts`, `service_contexts` và kỹ thuật gỡ lỗi vi phạm `avc: denied`.

### Module 5: Tích Hợp Android Framework System Service & SDK Manager Pattern
- **Bài 16**: Kiến trúc Android System Services: Vai trò của `system_server`, cơ chế đăng ký và xuất bản dịch vụ qua `ServiceManager`.
- **Bài 17**: Xây dựng `LedService.java` nội bộ: Quản lý kết nối Binder tới Vendor HAL, xử lý ngắt kết nối (Death Recipient) và mô hình phân quyền (`enforceCallingOrSelfPermission`).
- **Bài 18**: Thiết kế thư viện Client SDK `LedManager.java` cho tầng ứng dụng qua mô hình `getSystemService(LedManager.class)`.

### Module 6: Phát Triển Ứng Dụng Java APK, Đo Kiểm Toàn Trình & Xử Lý Sự Cố Thực Tế
- **Bài 19**: Lab thực hành 4: Viết ứng dụng `LedController.apk` bằng Java: Thiết kế giao diện người dùng, điều khiển ON/OFF, điều chỉnh chu kỳ xung nháy BLINK.
- **Bài 20**: Quy trình đóng gói, tích hợp và triển khai toàn trình (End-to-End Build & Deployment Flow) từ Kernel, DTB, HAL Daemon đến APK.
- **Bài 21**: Ma trận kiểm thử toàn diện (Test Matrix), phân tích độ trễ IPC Binder, tài nguyên CPU/RAM và cẩm nang xử lý sự cố thực chiến (Troubleshooting Guide).

---

## 4. Bảng So Sánh Kiến Trúc Chuyên Sâu

| Hạng mục so sánh | Hướng tiếp cận Android Hack (Không chuẩn) | Hướng tiếp cận Android BSP Production (Chuẩn Google) |
| :--- | :--- | :--- |
| **Quyền truy cập** | Cấp root (`su`) cho ứng dụng, mở quyền `chmod 777` bừa bãi | Tuân thủ mô hình phân quyền người dùng (App UID $→$ Framework $→$ HAL) |
| **Giao tiếp phần cứng** | Ứng dụng Java trực tiếp mở `/sys/class/gpio` bằng `Runtime.exec()` | Đi qua Stable AIDL IPC, Vendor HAL Daemon và Linux LED subsystem |
| **Bảo mật SELinux** | Chuyển hệ điều hành sang `permissive` mode để né lỗi | Cấu hình Type Enforcement rõ ràng: domain, exec, service, sysfs file permissions |
| **Giao thức HAL** | Dùng HIDL cũ hoặc gán mã nhúng C++ JNI trực tiếp vào app | Stable AIDL (`@VintfStability`), NDK Backend, tương thích hoàn toàn Treble |
| **Điều khiển LED nhấp nháy** | Viết vòng lặp `Thread.sleep()` gây tốn CPU và giật giao diện UI | Sử dụng `timer trigger` của kernel hoặc timer chuyên dụng trong HAL Daemon |

---

## 5. Quy Chuẩn Kỹ Thuật Khi Đóng Góp Bài Viết

Mọi tài liệu trong kho lưu trữ này phải tuân thủ nghiêm ngặt **Web Markdown Authoring Standard**:
1. **Khung tóm tắt**: Mỗi bài học có thể mở đầu bằng `> Tóm tắt: ...` (hoặc `> Summary: ...`) viết thuần túy 1–2 câu, không in đậm lồng ghép.
2. **Ký hiệu kỹ thuật**: Luôn sử dụng ký tự Unicode nguyên bản (`→`, `⇒`, `≤`, `≥`, `µA`, `dBm`, `kHz`, `MHz`). Tuyệt đối không dùng LaTeX inline dạng mũi tên gây lỗi hiển thị trên CMS.
3. **GFM Callouts**: Sử dụng chuẩn 5 thẻ: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`. Tên thẻ đặt riêng tại dòng 1.
4. **Hình ảnh**: Lưu tập trung tại thư mục `images/`, sử dụng thẻ HTML canh giữa `<p align="center"><img src="images/..." width="900" alt="..."></p>`.
5. **Khối mã nguồn & Đồ họa**: Luôn khai báo định danh ngôn ngữ rõ ràng (`c`, `cpp`, `bash`, `dts`, `aidl`, `java`, `xml`). Tuyệt đối không dùng Mermaid flowchart trực tiếp trong tài liệu (gây vỡ bố cục và thẩm mỹ kém trên web); toàn bộ sơ đồ phân tầng, quy trình nhị phân và mạch phần cứng được thiết kế thành đồ họa vector SVG chuyên nghiệp lưu trong `images/`.
