# BÀI 01: TỔNG QUAN KIẾN TRÚC ANDROID BSP VÀ SƠ ĐỒ PHẦN CỨNG RASPBERRY PI 4

> Tóm tắt: Giới thiệu toàn cảnh phân tầng kiến trúc Android BSP hiện đại theo chuẩn Project Treble, đối chiếu giữa Linux nhúng truyền thống và Android AOSP, phân tích sơ đồ chân 40-pin GPIO của Raspberry Pi 4 Model B và tính toán mạch đệm điện tử bảo vệ cho đèn LED.

---

## 1. Bản Chất Của Android BSP (Board Support Package)

Trong kỹ thuật hệ thống nhúng, **Board Support Package (BSP)** là tập hợp mã nguồn, cấu hình phần cứng, trình điều khiển thiết bị (Device Drivers) và các giao diện trừu tượng hóa (HAL) giúp một hệ điều hành cấp cao có thể khởi động và vận hành trơn tru trên một bo mạch phần cứng cụ thể (SoC/SBC).

Tuy nhiên, giữa **Linux nhúng thông thường (Embedded Linux / Yocto / Buildroot)** và **Android AOSP (Android Open Source Project)** tồn tại một khoảng cách kiến trúc rất lớn:

<p align="center">
  <img src="images/bai01_embedded_linux_vs_android_bsp_comparison.svg" width="950" alt="Đối chiếu kiến trúc Linux nhúng vs Android AOSP Treble">
</p>

### Tại sao Android không cho phép ứng dụng truy cập GPIO trực tiếp?
1. **Nguyên tắc bảo mật Sandbox & SELinux**: Mọi ứng dụng Android đều chạy dưới một định danh người dùng riêng biệt (App UID, ví dụ `u0_a142`). Chính sách SELinux của Android mặc định áp dụng cơ chế *Least Privilege* và chặn 100% các cuộc gọi mở file trực tiếp vào `/dev/` hoặc `/sys/` từ ứng dụng không có đặc quyền.
2. **Ranh giới phân tách Project Treble**: Bắt đầu từ Android 8.0 trở đi (và chuẩn hóa hoàn toàn ở Android 14/15/17), Google phân tách hệ điều hành thành hai nửa độc lập:
   - **System Partition (`/system`)**: Chứa Android Framework, System Services, ART Runtime do Google quản lý, có thể cập nhật qua OTA (Generic System Image - GSI).
   - **Vendor Partition (`/vendor`)**: Chứa mã nguồn BSP, Kernel modules, Vendor HAL daemons do nhà sản xuất phần cứng (SoC Vendor / Board Maker) phát triển.
3. **Quản lý đa tiến trình và xung đột tài nguyên**: Nếu hai ứng dụng cùng lúc điều khiển một chân GPIO, việc không có tầng Framework quản lý sẽ dẫn đến xung đột trạng thái (Race Condition), làm sập hệ thống hoặc gây cháy bóng LED.

---

## 2. Giải Phẫu Kiến Trúc Toàn Trình: Từ Java APK Đến Chân GPIO

Để điều khiển một đèn LED vật lý trên Raspberry Pi 4 theo đúng chuẩn kỹ thuật của Google, hệ thống trải qua **6 tầng kiến trúc** chặt chẽ:

<p align="center">
  <img src="images/bai01_android_bsp_end_to_end_architecture.svg" width="950" alt="Kiến trúc toàn trình Android BSP trên Raspberry Pi 4">
</p>

### Chi tiết nhiệm vụ của từng tầng:

1. **Tầng Ứng dụng (Application Layer - `LedController.apk`)**:
   - Được viết bằng ngôn ngữ Java hoặc Kotlin.
   - Cung cấp giao diện người dùng (UI) trực quan với các nút bấm chức năng: **BẬT (ON)**, **TẮT (OFF)**, **NHẤP NHÁY (BLINK)** và thanh trượt cài đặt thời gian chu kỳ xung (`delay_on`, `delay_off`).
   - Sử dụng lớp Client SDK nội bộ `LedManager.java` thay vì tự thao tác socket hay Binder thô.

2. **Tầng Android Framework (`system_server`)**:
   - Chạy trong tiến trình lõi `system_server` với quyền `system` (UID 1000).
   - Khởi tạo đối tượng `LedService.java` (kế thừa từ `ILedManager.Stub`) và đăng ký vào bộ điều phối dịch vụ toàn cục:
     ```java
     ServiceManager.addService("led_custom", new LedService(context));
     ```
   - **Kiểm tra quyền hạn (Security Enforcement)**: Xác thực xem ứng dụng gọi API có được cấp quyền `android.permission.CONTROL_LED` (quyền Signature hoặc System Privileged) hay không.
   - Duy trì kết nối Binder Proxy tới Vendor HAL và lắng nghe sự cố dừng đột ngột của tiến trình HAL thông qua `linkToDeath()`.

3. **Ranh giới Treble & Stable AIDL IPC**:
   - Giao tiếp giữa `system_server` và Native HAL Daemon vượt qua ranh giới tiến trình (IPC) thông qua thiết bị điều khiển `/dev/binder`.
   - Sử dụng định dạng giao tiếp **Stable AIDL** được gắn thẻ `@VintfStability` với gói định danh `vendor.example.hardware.led`.

4. **Tầng Trừu Tượng Phần Cứng (Vendor HAL Daemon)**:
   - Là một tiến trình Native C++ nhị phân độc lập chạy dưới đường dẫn `/vendor/bin/hw/vendor.example.hardware.led-service`.
   - Sử dụng thư viện backend Android NDK (`libbinder_ndk`).
   - Khởi tạo và đăng ký tên thể hiện dịch vụ: `vendor.example.hardware.led.ILed/default`.
   - Được quản lý vòng đời bởi tiến trình `init` thông qua kịch bản `init.rc` và được kiểm soát quyền bởi nhãn SELinux `vendor_led_hal`.
   - Mở và ghi giá trị an toàn vào các file điều khiển của nhân Linux (sysfs).

5. **Tầng Nhân Linux & Subsystem (Linux Kernel Space)**:
   - Sử dụng nhân Linux 6.18 LTS hỗ trợ kiến trúc Generic Kernel Image (GKI).
   - Không can thiệp ghi thanh ghi bừa bãi mà tận dụng hệ thống quản lý đèn LED tiêu chuẩn của Linux: **Linux LED Class Subsystem** (`drivers/leds/leds-gpio.c`).
   - Nhận diện chân phần cứng thông qua cây thiết bị **Device Tree Overlay** (`led-gpio.dtbo`) với binding `compatible = "gpio-leds"`.
   - Xuất hiện trực quan trong Userspace tại thư mục: `/sys/class/leds/user-led/`.

6. **Tầng Phần Cứng Vật Lý (Physical Hardware Layer)**:
   - Bo mạch máy tính đơn bo **Raspberry Pi 4 Model B**.
   - Bộ vi xử lý Broadcom **BCM2711 SoC** (Quad-core Cortex-A72).
   - Chân xuất tín hiệu vật lý: **Physical Pin 11 (BCM GPIO17)**.

---

## 3. Sơ Đồ Chân 40-Pin Header Raspberry Pi 4 & An Toàn Phần Cứng

Raspberry Pi 4 trang bị một dãy 40 chân cắm mở rộng (Expansion Header) với khoảng cách chân 2.54 mm. Việc hiểu rõ sơ đồ chân là yêu cầu sống còn trước khi cắm dây, nhằm tránh nguy cơ chập mạch phá hủy SoC:

<p align="center">
  <img src="images/bai04_rpi4_gpio_led_circuit_schematic.svg" width="950" alt="Sơ đồ mạch phần cứng và chân GPIO Raspberry Pi 4">
</p>

### Bảng tra cứu các chân nguồn và chân điều khiển quan trọng:

| Số Chân Vật Lý (Physical Pin) | Tên Tín Hiệu (BCM GPIO) | Mức Điện Áp Định Mức | Đặc Tính Kỹ Thuật & Cảnh Báo An Toàn |
| :---: | :--- | :---: | :--- |
| **Pin 1** | `3V3 Power` | 3.3V DC | Nguồn cấp tối đa 50 mA cho cảm biến ngoài |
| **Pin 2** | `5V Power` | 5.0V DC | 🛑 **CỰC KỲ NGUY HIỂM**: Đấu trực tiếp từ cổng nguồn Type-C |
| **Pin 4** | `5V Power` | 5.0V DC | 🛑 **CỰC KỲ NGUY HIỂM**: Tuyệt đối không chạm que đo vào chân này |
| **Pin 6** | `GND` | 0V | Chân mass (tiếp địa) chung cho toàn bộ mạch điện |
| **Pin 9** | `GND` | 0V | Chân mass phụ |
| **Pin 11** | `BCM GPIO17` | 3.3V LVCMOS | ⭐ **Chân ngõ ra điều khiển đèn LED được chọn trong khóa học** |
| **Pin 12** | `BCM GPIO18` | 3.3V LVCMOS | Chân hỗ trợ điều xung phần cứng (PWM0) |

> [!CAUTION]
> **Quy tắc an toàn phần cứng tối quan trọng đối với Raspberry Pi:**
> - Tất cả các chân GPIO của Raspberry Pi 4 hoạt động ở mức logic **3.3V (LVCMOS)** và **KHÔNG CÓ KHẢ NĂNG CHỊU ĐƯỢC 5V (Not 5V-Tolerant)**.
> - Nếu để que đo hoặc dây nhảy vô tình chạm từ **Pin 2/4 (5V)** sang **Pin 11 (GPIO17)**, điện áp 5V sẽ đánh thủng diode bảo vệ nội bộ và phá hủy hoàn toàn khối ngoại vi I/O của vi xử lý BCM2711 ngay lập tức.
> - Luôn ngắt nguồn điện của Raspberry Pi trước khi cắm hoặc rút dây nối trên breadboard.

---

## 4. Tính Toán Mạch Đệm Điện Tử Cho Đèn LED (Định Luật Ohm)

Một diode phát quang (LED) là phần tử phi tuyến tính có đặc tuyến $I-V$ hàm mũ. Khi được phân cực thuận vượt qua ngưỡng điện áp mở ($V_F$), điện trở trong của LED giảm xuống gần như bằng 0. Nếu mắc trực tiếp LED vào chân GPIO mà không có điện trở hạn dòng, dòng điện sẽ vọt lên hàng trăm mA, làm cháy LED và hỏng cổng ra của SoC.

<p align="center">
  <img src="images/bai01_led_circuit_loop_schematic.svg" width="950" alt="Sơ đồ vòng kín mạch đệm GPIO17 và định luật Kirchhoff">
</p>

### 1. Công thức tính toán:
Theo định luật Ohm và định luật Kirchhoff về điện áp (KVL):
$$V_{OH} - V_R - V_F = 0 \implies V_{OH} - (I_{LED} \times R) - V_F = 0$$

Biến đổi tìm giá trị điện trở $R$:
$$R = \frac{V_{OH} - V_F}{I_{LED}}$$

Trong đó:
- $V_{OH}$: Điện áp ngõ ra mức cao của chân GPIO BCM2711 ($3.3\text{ V}$).
- $V_F$: Điện áp phân cực thuận sụt trên LED (Forward Voltage). Với LED đỏ tiêu chuẩn, $V_F \approx 1.8\text{ V} → 2.0\text{ V}$.
- $I_{LED}$: Dòng điện định mức mong muốn chạy qua LED để đạt độ sáng tối ưu mà vẫn tiết kiệm điện và an toàn cho vi mạch ($4\text{ mA} → 10\text{ mA}$).

### 2. Số liệu tính toán cụ thể:
Giả sử chọn dòng an toàn $I_{LED} = 4\text{ mA} = 0.004\text{ A}$ với đèn LED màu đỏ ($V_F = 2.0\text{ V}$):
$$R = \frac{3.3\text{ V} - 2.0\text{ V}}{0.004\text{ A}} = \frac{1.3\text{ V}}{0.004\text{ A}} = 325\ \Omega$$

* **Lựa chọn thực tế**: Chọn điện trở chuẩn thương mại gần nhất trong thang E24 là **$330\ \Omega$** (vạch màu: Cam - Cam - Nâu - Vàng kim).
* **Kiểm tra công suất tiêu tán trên điện trở**:
  $$P_R = I_{LED}^2 \times R = (0.004)^2 \times 330 \approx 0.0053\text{ W} = 5.3\text{ mW}$$
  Mức công suất này hoàn toàn an toàn đối với các điện trở cắm thông dụng công suất $1/4\text{ W}$ ($250\text{ mW}$) hoặc $1/8\text{ W}$ ($125\text{ mW}$).

---

## 5. So Sánh Hai Chiến Lược Lập Trình Driver: `gpio-leds` vs Tự Viết Character Driver

Khi làm việc ở tầng nhân Linux cho mục đích điều khiển đèn LED, kỹ sư thường đứng trước hai lựa chọn:

| Tiêu Chí Kỹ Thuật | Phương Án 1: Dùng Subsystem Chuẩn `gpio-leds` (Khuyến nghị) | Phương Án 2: Tự Viết Custom Character Driver |
| :--- | :--- | :--- |
| **Độ tin cậy & Ổn định** | Tuyệt đối cao, mã nguồn đã được cộng đồng Linux duy trì hàng chục năm | Phụ thuộc vào trình độ của kỹ sư, dễ dính lỗi rò rỉ bộ nhớ, race condition |
| **Giao tiếp phần cứng** | Tích hợp sâu vào cây thiết bị Device Tree (`compatible = "gpio-leds"`) | Phải tự khai báo Device Node, Major/Minor number, hàm `file_operations` |
| **Hỗ trợ nhấp nháy (Blink)** | Hỗ trợ sẵn chế độ phần cứng **`timer trigger`** qua sysfs (`delay_on`, `delay_off`) | Bắt buộc phải tự lập trình Kernel Timer (`struct timer_list`) phức tạp |
| **Tương thích Android GKI** | Tương thích 100% với Android Common Kernel, không cần nạp module ngoài | Phải biên dịch out-of-tree module `.ko` và xử lý bài toán `vermagic` |
| **Mục đích phù hợp** | Sản phẩm thương mại thực tế (Production), tối ưu hóa thời gian phát triển | Phù hợp cho việc nghiên cứu nội bộ hoặc khi phần cứng có giao thức mã hóa riêng |

Trong chuyên đề này, chúng ta sẽ thực hành **cả hai phương pháp**:
- Ở **Lab 1**: Tự viết một Kernel Module out-of-tree hoàn chỉnh bằng Bazel/Kleaf để hiểu sâu cơ chế nạp module của Android.
- Ở **Lab 2 & 3**: Triển khai `gpio-leds` và tích hợp vào Native AIDL HAL theo đúng chuẩn kỹ thuật của Google.

---

## 6. Bài Tập Tự Đánh Giá & Vận Dụng

1. **Phân tích dòng điện SoC**: Tra cứu tài liệu kỹ thuật của Broadcom BCM2711 ARM Peripherals. Cho biết dòng điện tổng tối đa cho phép chảy qua toàn bộ các chân GPIO cùng lúc là bao nhiêu mA? Nếu mắc 10 bóng LED cùng sáng thì cần chọn dòng điện mỗi bóng là bao nhiêu để không sập nguồn?
2. **Thiết kế mạch Active-Low**: Hãy vẽ lại sơ đồ mạch nếu LED được mắc theo kiểu Active-Low (Cathode nối vào GPIO, Anode nối lên nguồn 3.3V). Khi đó trong Device Tree ta phải khai báo cờ nào thay cho `GPIO_ACTIVE_HIGH`?
3. **Phản biện kiến trúc**: Tại sao một kỹ sư phần mềm Android không nên sử dụng hàm `Runtime.getRuntime().exec("echo 1 > /sys/class/leds/...")` bên trong ứng dụng Java APK? Liệt kê ít nhất 3 nguy cơ về bảo mật, hiệu năng và tính tương thích Treble.
