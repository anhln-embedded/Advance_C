# BÀI 03: CHIẾN LƯỢC ĐỒNG BỘ MÃ NGUỒN KERNEL VÀ QUY TRÌNH BUILD BẰNG GOOGLE KLEAF / BAZEL

> Tóm tắt: Phân biệt giữa mã nguồn Android Platform và Android Kernel, thiết lập môi trường biên dịch chuẩn trên Ubuntu 22.04, đồng bộ mã nguồn nhân Raspberry Pi 4 bằng công cụ Repo và làm chủ quy trình biên dịch nhân hiện đại bằng Google Kleaf / Bazel Hermetic Sandbox.

---

## 1. Phân Định Ranh Giới: Android Platform Source vs Android Kernel Source

Một trong những sai lầm phổ biến nhất của các kỹ sư mới bước vào mảng Android BSP là nhầm lẫn giữa **Cây mã nguồn nền tảng Android (Android Platform Tree)** và **Cây mã nguồn nhân Android (Android Kernel Tree)**.

Trong kiến trúc AOSP hiện đại:
- **Android Platform Tree**: Chứa Framework (Java/Kotlin), System Services, Native Daemons, ART Runtime, Build System Soong (`Android.bp`), ứng dụng hệ thống và cấu hình phần cứng `device/`. Dung lượng tải về thường từ $250\text{ GB} → 400\text{ GB}$.
- **Android Kernel Tree**: Chứa mã nguồn nhân Linux, trình điều khiển thiết bị (Drivers), bảng tương thích Device Tree (`.dts`), và hệ thống build chuyên biệt của Google mang tên **Kleaf / Bazel**. Dung lượng tải về khoảng $30\text{ GB} → 50\text{ GB}$.

<p align="center">
  <img src="images/bai03_platform_vs_kernel_source_trees.svg" width="950" alt="Phân tách cây mã nguồn Android Platform Tree vs Kernel Tree">
</p>

> [!IMPORTANT]
> **Nguyên tắc đối soát mã nguồn thực tế:**
> Việc bạn biên dịch thành công một nhân Linux và khớp chính xác commit `7a9131c1065a` **không có nghĩa là toàn bộ mã nguồn Android Platform của bạn trùng khớp 100% với bản ROM KonstaKANG**.
> Tác giả KonstaKANG xây dựng các bản ROM dựa trên nhánh gốc của cộng đồng **Raspberry Vanilla** nhưng bổ sung thêm rất nhiều bản vá độc quyền (tối ưu hóa GPU Mesa, trình điều khiển màn hình cảm ứng, menu cài đặt nâng cao). Để kiểm soát hệ thống, bạn cần khóa (lock) manifest của cả hai cây mã nguồn độc lập.

---

## 2. Chuẩn Bị Môi Trường Biên Dịch Chuẩn (Build Environment)

Biên dịch Android Kernel bằng Google Kleaf đòi hỏi hệ điều hành máy tính phát triển (Build Host) phải đáp ứng cấu hình tiêu chuẩn:

### 1. Yêu cầu phần cứng máy tính Host:
- **Hệ điều hành**: Ubuntu 22.04 LTS (Jammy Jellyfish) x86_64 nguyên bản hoặc chạy trong Docker Container.
- **CPU**: Tối thiểu 8 cores (khuyến nghị 16 cores trở lên để chạy Bazel song song).
- **RAM**: Tối thiểu 16 GB (khuyến nghị 32 GB RAM, vì quá trình liên kết `ld.lld` nhân Linux 64-bit ngốn bộ nhớ rất lớn).
- **Dung lượng đĩa trống**: Tối thiểu 100 GB định dạng ext4 (không dùng NTFS trên ổ đĩa mạng vì Bazel yêu cầu hỗ trợ symlink và hardlink nghiêm ngặt).

### 2. Cài đặt các gói phụ trợ:
Mở terminal trên Ubuntu 22.04 và thực thi:

```bash
sudo apt update && sudo apt install -y \
  git git-lfs curl python3 python3-pip python3-setuptools \
  openjdk-17-jdk build-essential libncurses5 libssl-dev \
  bison flex rsync bc cpio libelf-dev zlib1g-dev

# Cài đặt công cụ Repo của Google
mkdir -p ~/.bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/.bin/repo
chmod a+rx ~/.bin/repo

# Thêm ~/.bin vào biến môi trường PATH
echo 'export PATH="$HOME/.bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Kiểm tra phiên bản công cụ
git --version
python3 --version
repo version
```

---

## 3. Khởi Tạo Và Đồng Bộ Cây Mã Nguồn Android Kernel

### Bước 1: Khởi tạo Repo với Kernel Manifest của Google
Tạo thư mục làm việc và trỏ tới nhánh nhân Android 17 LTS:

```bash
mkdir -p ~/android/kernel-rpi4
cd ~/android/kernel-rpi4

repo init \
  -u https://android.googlesource.com/kernel/manifest \
  -b common-android17-6.18-lts
```

### Bước 2: Tải và thiết lập Local Manifest của Raspberry Pi 4
Tải file manifest mở rộng của dự án Raspberry Vanilla để bổ sung cấu hình bo mạch BCM2711:

```bash
curl -o .repo/local_manifests/manifest_brcm_rpi.xml \
  -L https://raw.githubusercontent.com/raspberry-vanilla/android_kernel_manifest/android-17.0/manifest_brcm_rpi.xml \
  --create-dirs
```

### Bước 3: Tinh chỉnh Local Manifest tối ưu cho Lab
Trong quá trình triển khai thực tế trên bản ROM KonstaKANG 30/10/2026, để đảm bảo mã nguồn nhân trỏ chính xác vào cây nhân được vá lỗi của Raspberry Vanilla và có đầy đủ Firmware Wi-Fi/Bluetooth, tệp `.repo/local_manifests/manifest_brcm_rpi.xml` được cấu hình chuẩn mực như sau:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <remote name="github" fetch="https://github.com/" />
    
    <!-- Thay thế kernel/common gốc của Google bằng nhánh nhân hỗ trợ Raspberry Pi -->
    <remove-project name="kernel/common" />
    <project path="common"
             name="raspberry-vanilla/android_kernel_brcm_rpi"
             remote="github"
             revision="android-17.0" />
             
    <!-- Tải firmware phần cứng Broadcom độc quyền cần thiết cho hệ thống -->
    <project path="vendor/brcm"
             name="raspberry-vanilla/proprietary_vendor_brcm"
             remote="github"
             revision="android-17.0" />
</manifest>
```

### Bước 4: Thực thi đồng bộ mã nguồn (Repo Sync)
```bash
# Đồng bộ mã nguồn với 4 luồng song song (tùy chỉnh theo băng thông mạng)
repo sync -c -j4 --fail-fast
```

### Bước 5: Khóa Manifest và xác minh Git Commit
Sau khi quá trình đồng bộ hoàn tất, lập tức xuất file manifest cố định (`locked-manifest.xml`) để lưu lại chính xác trạng thái của mọi commit:

```bash
# Xuất manifest cố định
repo manifest -r -o locked-manifest.xml

# Kiểm tra Git Commit SHA-1 của thư mục common/
cd common
git log -1 --oneline
git rev-parse HEAD
cd ..
```

* **Kết quả đối soát thành công**:
  ```text
  7a9131c1065a28544c1b6592152981b4c4102367
  ```
  Commit này hoàn toàn trùng khớp với chuỗi SCM Hash `g7a9131c1065a` mà chúng ta đã điều tra từ `uname -r` ở Bài 02!

---

## 4. Giải Mã Hệ Thống Biên Dịch Google Kleaf / Bazel

Từ Android 13 trở đi, Google đã chính thức loại bỏ cách biên dịch nhân bằng lệnh `make` cổ điển (`ARCH=arm64 CROSS_COMPILE=... make`) và chuyển đổi hoàn toàn sang **Kleaf**.

Kleaf là một hệ thống quy tắc (Ruleset) được xây dựng trên nền tảng công cụ **Bazel**, mang lại 3 ưu thế vượt trội:

<p align="center">
  <img src="images/bai02_kleaf_bazel_kernel_build_flow.svg" width="950" alt="Quy trình biên dịch Kleaf Bazel cho Android Kernel">
</p>

### 1. Cơ chế Hermetic Toolchain (Bộ công cụ đóng kín):
Trong các bản Linux truyền thống, kết quả build nhân thường bị ảnh hưởng bởi phiên bản GCC hoặc Clang được cài trên máy tính host. Với Kleaf, toàn bộ trình biên dịch Clang/LLVM, `ld.lld`, `llvm-objcopy` được tải về dạng tiền biên dịch (Prebuilts) nằm ngay trong thư mục `prebuilts/clang/`. Bazel **tuyệt đối không sử dụng bất kỳ công cụ nào của Ubuntu Host**, đảm bảo tính tái lập (Reproducible Build) 100% trên mọi máy tính khác nhau.

### 2. Cơ chế Sandbox Isolation (Cô lập hộp cát):
Mỗi tác vụ biên dịch một file mã nguồn C không được chạy tự do trong thư mục gốc mà được đưa vào một thư mục tạm thời gọi là **Bazel Sandbox** (`/tmp/bazel-sandbox/...`).
- Trong Sandbox, mã nguồn chỉ có thể nhìn thấy các file header và thư viện được khai báo tường minh trong tệp `BUILD.bazel`.
- Bất kỳ hành vi gọi file ngoài luồng (undeclared dependency) đều sẽ bị Bazel chặn đứng ngay lập tức với mã lỗi `Action failed to make progress`.

### 3. Các quy tắc build cốt lõi trong Kleaf:
- **`kernel_build`**: Quy tắc định nghĩa quá trình xây dựng toàn bộ nhân Linux, sinh ra tệp nhị phân `vmlinux`, `Image`, cây thiết bị `.dtb` và bảng mã băm `Module.symvers`.
- **`ddk_headers`**: Quy tắc xuất bản tập hợp các file header nội bộ của nhân để phục vụ biên dịch các module ngoài cây mã nguồn (Out-of-tree Drivers).
- **`ddk_module`**: Quy tắc biên dịch một hoặc nhiều tệp `.c` thành tệp module nhân `.ko`.

---

## 5. Thực Hành Biên Dịch Nhân Raspberry Pi 4 Bằng Kleaf

### 1. Khắc phục phụ thuộc Firmware Broadcom trong Bazel Graph:
Trước khi build, do mục tiêu `kernel_build` của bo mạch RPi4 đòi hỏi file firmware quy chuẩn vô tuyến `regulatory.db`, chúng ta cần tạo một tệp định nghĩa tài nguyên cho `vendor/brcm`:

Tạo file `vendor/brcm/BUILD.bazel`:
```python
package(default_visibility = ["//visibility:public"])

filegroup(
    name = "rpi4_firmware",
    srcs = glob([
        "rpi4/proprietary/vendor/firmware/**",
    ]),
)
```

Đồng thời, kiểm tra trong `common/BUILD.bazel` để đảm bảo mục tiêu `kernel_build(name = "rpi4")` có chứa dependency `//vendor/brcm:rpi4_firmware` trong thuộc tính `srcs`.

### 2. Kích hoạt lệnh biên dịch nhân:
Sử dụng công cụ `tools/bazel` đi kèm trong cây mã nguồn:

```bash
# Biên dịch toàn bộ nhân và Device Tree cho Raspberry Pi 4
tools/bazel build \
  --config=fast \
  --config=stamp \
  //common:rpi4
```

* **Ý nghĩa của các cờ biên dịch**:
  - `--config=fast`: Tối ưu hóa tốc độ biên dịch bằng cách bỏ qua một số bước kiểm tra tài liệu không cần thiết.
  - `--config=stamp`: Kích hoạt cơ chế đóng dấu phiên bản Git (SCM Stamping) để nhúng chính xác chuỗi commit hash vào thông tin phiên bản nhân.
  - `//common:rpi4`: Định danh gói và mục tiêu (Bazel Target) cần biên dịch.

### 3. Kiểm tra sản phẩm đầu ra (Build Artifacts):
Sau khi Bazel báo `Build completed successfully`, toàn bộ kết quả biên dịch sẽ nằm trong thư mục symlink `bazel-bin/`:

```bash
# Liệt kê các tệp nhân và Device Tree đã tạo ra
ls -lh bazel-bin/common/rpi4/arch/arm64/boot/Image
ls -lh bazel-bin/common/rpi4/arch/arm64/boot/dts/broadcom/bcm2711-rpi-4-b.dtb

# Kiểm tra bảng ký hiệu mã băm Module.symvers
ls -lh bazel-bin/common/rpi4/Module.symvers
```

Bảng `Module.symvers` này chính là tài nguyên tối quan trọng sẽ được sử dụng ở bài học tiếp theo để liên kết và tạo ra module Hello World tương thích tuyệt đối với hệ thống!

---

## 6. Bài Tập Tự Đánh Giá & Vận Dụng

1. **Phân tích cơ chế Sandbox**: Tại sao một đoạn mã C trong kernel module `#include <linux/compiler-version.h>` có thể biên dịch thành công khi dùng lệnh `make` ngoài host nhưng lại thất bại khi build qua Bazel DDK nếu thiếu phụ thuộc `//common:all_headers_aarch64`?
2. **Khám phá `Module.symvers`**: Mở file `bazel-bin/common/rpi4/Module.symvers` bằng lệnh `head -n 20`. Cho biết cấu trúc của mỗi dòng trong file này bao gồm những trường thông tin gì?
3. **Thực hành cấu hình**: Thử kiểm tra nội dung file `common/arch/arm64/configs/android_rpi4_defconfig`. Tìm xem cờ `CONFIG_LOCALVERSION` đang được thiết lập là chuỗi ký tự nào?
