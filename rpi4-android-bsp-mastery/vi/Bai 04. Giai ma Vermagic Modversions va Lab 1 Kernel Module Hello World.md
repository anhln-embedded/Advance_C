# BÀI 04: GIẢI MÃ VERMAGIC, MODVERSIONS VÀ LAB 1 KERNEL MODULE HELLO WORLD

> Tóm tắt: Phân tích tường tận cơ chế kiểm tra tương thích nhị phân của nhân Linux (Vermagic & CONFIG_MODVERSIONS), kỹ thuật điều khiển SCM Stamping để loại bỏ hậu tố `-maybe-dirty`, và thực hành xây dựng, nạp, gỡ bỏ Kernel Module Hello World đầu tiên trên Android 17 / Raspberry Pi 4 bằng Google Kleaf Bazel.

---

## 1. Bí Mật Cơ Chế Kiểm Soát Tính Toàn Vẹn: Vermagic & SCM Stamping

Khi bạn cố gắng nạp một tệp module nhân (`.ko`) vào hệ điều hành Android bằng lệnh `insmod`, nhân Linux không thực thi mã lệnh ngay lập tức mà kích hoạt một chuỗi các rào cản kiểm tra an toàn nhị phân nghiêm ngặt:

<p align="center">
  <img src="images/bai04_module_binary_verification_pipeline.svg" width="950" alt="Chuỗi kiểm soát tương thích nhị phân khi nạp Kernel Module">
</p>

### 1.1. Chuỗi Vermagic (Version Magic String) là gì?
Chuỗi `vermagic` là một đoạn văn bản ASCII được nhúng vào section `.modinfo` của tệp nhị phân ELF `.ko`. Chuỗi này được cấu thành từ 3 thành phần chính:

```text
6.18.38-g7a9131c1065a-v8 SMP preempt mod_unload modversions aarch64
|______| |___________| |_| |_______________________________________|
   |           |        |                      |
Base Version  SCM-Hash LocalVer          Kernel Feature Flags
```

1. **Phiên bản nhân gốc (Base Version)**: `6.18.38` (được định nghĩa trong tệp `Makefile` gốc của kernel: `VERSION`, `PATCHLEVEL`, `SUBLEVEL`).
2. **Hậu tố quản lý mã nguồn (SCM Version)**: `-g7a9131c1065a` (đại diện cho Git Commit Hash).
3. **Phiên bản cục bộ (Local Version)**: `-v8` (được cấu hình trong `CONFIG_LOCALVERSION`).
4. **Các cờ tính năng phần cứng & nhân**:
   - `SMP`: Hỗ trợ đa xử lý đối xứng (Symmetric Multiprocessing).
   - `preempt`: Nhân hỗ trợ chế độ chiếm quyền ưu tiên thời gian thực.
   - `mod_unload`: Hỗ trợ gỡ bỏ module đang chạy.
   - `modversions`: Bắt buộc kiểm tra mã băm CRC của symbol.
   - `aarch64`: Kiến trúc vi xử lý 64-bit ARMv8.

---

## 2. Bẫy Lỗi Kinh Điển: Hậu Tố `-maybe-dirty` Và Kỹ Thuật SCM Stamping

Trong lần đầu tiên biên dịch module bằng Kleaf trên môi trường Bazel, kỹ sư sẽ thường xuyên gặp hiện tượng module bị từ chối nạp với log:

```text
insmod: failed to load hello_android.ko: Exec format error
dmesg: version magic '6.18.38-maybe-dirty-v8' should be '6.18.38-g7a9131c1065a-v8'
```

### Tại sao lại xuất hiện chữ `-maybe-dirty`?
Hệ thống Kbuild của Linux có script `scripts/setlocalversion`. Khi phát hiện trong thư mục Git có bất kỳ tệp tin nào chưa được commit hoặc cây mã nguồn được build bên ngoài môi trường kiểm soát Git tiêu chuẩn (chính là cơ chế cô lập Sandbox của Bazel), script sẽ tự động gán hậu tố `-dirty` hoặc `-maybe-dirty` để cảnh báo rằng nhân này không phải là một bản phát hành chính thức (Clean Release).

### Giải pháp kỹ thuật chuẩn mực:
Để loại bỏ triệt để hậu tố này và đồng bộ chính xác với bản build đang chạy trên thiết bị, chúng ta áp dụng cơ chế **SCM Override** chính thống của Google Kleaf:

Tạo tệp `common/workspace_status.json`:
```json
{
    "SCMVERSION": "-g7a9131c1065a"
}
```

Khi thực thi lệnh build Bazel, bắt buộc phải truyền cờ `--config=stamp` kèm tham chiếu tệp manifest đã khóa:
```bash
tools/bazel build \
  --config=stamp \
  --repo_manifest="$(realpath .):$(realpath locked-manifest.xml)" \
  //labs/hello_android:hello_android
```

> [!CAUTION]
> **Cảnh báo về đạo đức kỹ thuật & An toàn hệ thống:**
> Tuyệt đối không bao giờ dùng các công cụ Hex Editor để sửa đè chuỗi chữ ký `vermagic` bên trong tệp `.ko`. Việc ép nạp một module được build từ một cây mã nguồn không khớp cấu hình sẽ dẫn đến hiện tượng sai lệch cấu trúc dữ liệu (`struct padding`), gây hỏng bộ nhớ RAM (Memory Corruption) và làm khởi động lại kernel đột ngột (Kernel Panic)!

---

## 3. Cơ Chế Kiểm Tra Mã Băm Symbol (`CONFIG_MODVERSIONS`)

Khi cờ `CONFIG_MODVERSIONS=y` được kích hoạt, trình biên dịch sẽ tạo ra mã băm CRC 32-bit cho từng hàm mà module gọi tới (ví dụ `_printk`, `module_layout`). Các mã băm này được lưu trữ trong section `__versions` của module.

```bash
# Kiểm tra các symbol mà module phụ thuộc vào
llvm-readelf -s bazel-bin/labs/hello_android/hello_android/hello_android.ko | grep -E 'printk|module_layout'
```

Khi gọi `insmod`, kernel sẽ đối chiếu mã băm CRC này với bảng ký hiệu nội bộ của nó. Nếu khớp 100%, module mới được cấp phép nạp vào không gian nhớ của nhân. Nhờ đó, tính toàn vẹn nhị phân được bảo vệ ở cấp độ hàm số học chứ không dừng lại ở chuỗi ký tự bên ngoài.

---

## 4. Lab 1: Xây Dựng Kernel Module Hello World Bằng Bazel DDK

### Bước 1: Soạn thảo mã nguồn C của Module
Tạo thư mục `labs/hello_android` trong cây thư mục nhân:

```bash
mkdir -p labs/hello_android
```

Tạo tệp `labs/hello_android/hello_android.c`:

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

// Hàm khởi tạo - Được gọi khi nạp module bằng insmod
static int __init hello_android_init(void)
{
    pr_info("hello_android: ========================================\n");
    pr_info("hello_android: Hello Android Kernel! SoC BCM2711 RPi4\n");
    pr_info("hello_android: Module running on Linux 6.18 AOSP 17\n");
    pr_info("hello_android: ========================================\n");
    return 0; // Trả về 0 báo hiệu khởi tạo thành công
}

// Hàm dọn dẹp - Được gọi khi gỡ bỏ module bằng rmmod
static void __exit hello_android_exit(void)
{
    pr_info("hello_android: Goodbye Android Kernel! Cleaned up successfully.\n");
}

// Đăng ký các điểm nhập (Entry Points) với nhân Linux
module_init(hello_android_init);
module_exit(hello_android_exit);

// Khai báo thông tin siêu dữ liệu (Metadata) bắt buộc
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Embedded-AIoT Lab PTIT");
MODULE_DESCRIPTION("First Out-of-tree Android Kernel Module built with Bazel Kleaf");
MODULE_VERSION("1.0.0");
```

### Bước 2: Viết tệp quy tắc xây dựng `BUILD.bazel`
Tạo tệp `labs/hello_android/BUILD.bazel`:

```python
load("@kleaf//build/kernel/kleaf:kernel.bzl", "ddk_module")

ddk_module(
    name = "hello_android",
    srcs = ["hello_android.c"],
    out = "hello_android.ko",
    kernel_build = "//common:rpi4",
    deps = [
        # Bổ sung toàn bộ header của kiến trúc aarch64 để tránh lỗi thiếu compiler-version.h
        "//common:all_headers_aarch64",
    ],
)
```

### Bước 3: Biên dịch Module
Đứng tại thư mục gốc của cây kernel, chạy lệnh:

```bash
tools/bazel build \
  --config=stamp \
  --repo_manifest="$(realpath .):$(realpath locked-manifest.xml)" \
  //labs/hello_android:hello_android
```

* **Kiểm tra tệp nhị phân đầu ra**:
  ```bash
  ls -lh bazel-bin/labs/hello_android/hello_android/hello_android.ko
  file bazel-bin/labs/hello_android/hello_android/hello_android.ko
  ```

* **Đối soát chuỗi vermagic trước khi gửi sang board**:
  ```bash
  strings bazel-bin/labs/hello_android/hello_android/hello_android.ko | grep '^vermagic='
  ```
  Kết quả mong đợi:
  ```text
  vermagic=6.18.38-g7a9131c1065a-v8 SMP preempt mod_unload modversions aarch64
  ```

---

## 5. Thực Hành Nạp Và Gỡ Bỏ Module Trên Thiết Bị Qua ADB

### Bước 1: Đẩy tệp module sang Raspberry Pi 4
Thư mục `/data/local/tmp` là vùng nhớ có quyền ghi và thực thi phù hợp cho lập trình viên trên bản ROM Android `userdebug`:

```bash
adb push bazel-bin/labs/hello_android/hello_android/hello_android.ko /data/local/tmp/
```

### Bước 2: Nạp module vào nhân Linux
Mở ADB shell với quyền root:

```bash
adb root
adb shell

# Đứng trong shell của Android:
cd /data/local/tmp
insmod hello_android.ko
```

### Bước 3: Kiểm tra trạng thái nạp và bộ đệm log nhân (`dmesg`)
```bash
# Kiểm tra module đã xuất hiện trong danh sách quản lý của kernel hay chưa
lsmod | grep hello_android

# Xem nhật ký của kernel vừa ghi lại
dmesg | grep hello_android
```

* **Nhật ký thực tế ghi nhận từ hệ thống**:
  ```text
  hello_android: loading out-of-tree module taints kernel.
  hello_android: module verification failed: signature and/or required key missing - tainting kernel
  hello_android: ========================================
  hello_android: Hello Android Kernel! SoC BCM2711 RPi4
  hello_android: Module running on Linux 6.18 AOSP 17
  hello_android: ========================================
  ```

### 5.1. Phân tích các thông báo trong log:
1. `loading out-of-tree module taints kernel`:
   - Đây là thông báo **hoàn toàn bình thường**. Nhân Linux ghi nhận một cờ Taint (`O` - Out-of-tree) để báo rằng module này được biên dịch ngoài cây mã nguồn chính thức của Google/Broadcom.
2. `module verification failed: signature and/or required key missing`:
   - Nhân Linux phát hiện module này chưa được ký bằng khóa riêng tư (Private Key) của nhà phát hành bản ROM. Do cờ `sig_enforce=N`, kernel chỉ ghi nhận thêm cờ Taint (`E` - Unsigned module) chứ không chặn đứng việc nạp.
3. `Hello Android Kernel!`:
   - Xác nhận hàm `hello_android_init()` đã được thực thi hoàn hảo trong không gian nhân (Ring 0 / EL1) của Raspberry Pi 4!

### Bước 4: Gỡ bỏ module khỏi hệ thống
```bash
# Gỡ bỏ module
rmmod hello_android

# Kiểm tra lại danh sách module
lsmod | grep hello_android

# Kiểm tra log dọn dẹp
dmesg | tail -n 20 | grep hello_android
```

* **Log thu được**:
  ```text
  hello_android: Goodbye Android Kernel! Cleaned up successfully.
  ```

---

## 6. Bài Tập Tự Đánh Giá & Vận Dụng

1. **Thực nghiệm cố ý làm sai Vermagic**: Thử mở tệp `common/workspace_status.json`, thay đổi giá trị commit hash thành một chuỗi khác (ví dụ `-g111122223333`), biên dịch lại module và nạp vào Raspberry Pi 4. Quan sát mã lỗi mà lệnh `insmod` và `dmesg` trả về.
2. **Khảo sát tham số Module (Module Parameters)**: Mở rộng tệp `hello_android.c`, sử dụng macro `module_param(led_pin, int, 0644)` để cho phép người dùng truyền số chân GPIO vào khi nạp module: `insmod hello_android.ko led_pin=17`.
3. **Phân tích bộ nhớ Module**: Sử dụng lệnh `adb shell cat /proc/modules` để tìm xem module `hello_android` khi nạp vào nhân chiếm dung lượng bao nhiêu byte trong bộ nhớ RAM, và địa chỉ cơ sở (Base Address) của nó trong không gian nhớ ảo của kernel là gì?
