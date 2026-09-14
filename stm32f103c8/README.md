# STM32F103 Microcontroller Curriculum Standard (Bilingual VI / EN)

Tài liệu hướng dẫn cấu trúc thư mục mẫu chuẩn cho khóa học **Lập Trình STM32F103 Chuyên Sâu (ARM Cortex-M3 Bare-Metal & SPL)** với sự hỗ trợ đầy đủ 2 ngôn ngữ: Tiếng Việt (VI) và Tiếng Anh (EN).

---

## 1. Cấu Trúc Thư Mục Mẫu (Folder Structure)

```
stm32f103c8/
├── vi/                               # Toàn bộ bài giảng tiếng Việt (26 bài học)
│   ├── Bai 01. Tong quan STM32F103, Cai dat cong cu va Project Blink LED dau tien.md
│   ├── Bai 02. Phan tich chuyen sau GPIO va Ky thuat Bit-Banding.md
│   ├── Bai 03. He thong xung nhip RCC va Clock Tree.md
│   └── ... (đến Bài 26)
├── en/                               # Toàn bộ bài giảng tiếng Anh tương ứng
│   ├── Lesson 01. STM32F103 Overview Toolchain Setup and First Blink LED.md
│   ├── Lesson 02. Deep-Dive GPIO Architecture and Bit-Banding Technique.md
│   └── ... (các bài học tiếp theo)
├── images/                           # Kho tài nguyên sơ đồ khối, vi mạch, hardware schematic SVG/PNG
│   ├── bai01_pinout.svg
│   ├── bai02_gpio_structure.svg
│   ├── bai02_bit_banding.svg
│   └── ...
├── images_url_map.json               # Bản đồ ánh xạ URL Cloudflare / Uploads cho toàn bộ ảnh
└── README.md                         # Tài liệu hướng dẫn cấu trúc & quy chuẩn soạn thảo
```

---

## 2. Quy Tắc Đặt Tên Tệp (Naming Conventions)

Hệ thống phân tích tự động ghép cặp song ngữ (Bilingual Markdown Importer) trên nền tảng `embedded-aiot.com` dựa vào quy tắc sau:

1. **Phiên bản tiếng Việt**:
   - Thư mục: `vi/`
   - Tên tệp bắt đầu bằng `Bai XX.` (ví dụ: `Bai 01. ...md`, `Bai 02. ...md`).
   - Thứ tự bài học được trích xuất tự động từ số `XX`.

2. **Phiên bản tiếng Anh**:
   - Thư mục: `en/`
   - Tên tệp bắt đầu bằng `Lesson XX.` (hoặc `Bai XX. ...en.md`).
   - Thứ tự bài học `XX` trùng khớp với bài tiếng Việt tương ứng để hệ thống tự động nhận diện và ghép cặp vào cùng một bài học trên giao diện web.

---

## 3. Quy Chuẩn Nhúng Hình Ảnh & Sơ Đồ Kỹ Thuật

- Tất cả hình ảnh (SVG, PNG, WebP) được lưu trữ tập trung trong thư mục chung: `images/`.
- Trong file Markdown (cả `vi/` và `en/`), cú pháp nhúng hình ảnh chuẩn web:
  ```html
  <p align="center">
    <img src="images/bai02_gpio_structure.svg" width="900" alt="Cấu trúc điện tử chân GPIO STM32F103">
  </p>
  ```
- Khi chạy script đồng bộ `sync_images_and_course.ts`, hệ thống sẽ tự động quét ảnh, tải lên Cloud Storage và thay thế mọi đường dẫn cục bộ `images/...` thành đường dẫn trực tiếp trên Cloud CDN `/uploads/...`.

---

## 4. Quy Trình Đồng Bộ Lên Website (Sync to Production)

Để đẩy toàn bộ nội dung bài giảng mới và hình ảnh cập nhật lên hệ thống website `embedded-aiot.com`:

1. Chuyển vào thư mục dự án web:
   ```bash
   cd f:/embedded-lab-web
   ```

2. Chạy script đồng bộ hóa:
   ```bash
   npx tsx scripts/sync_images_and_course.ts
   ```

3. Kiểm tra bài giảng trực tiếp trên website:
   - Truy cập: `https://embedded-aiot.com/courses/lap-trinh-stm32f103-chuyen-sau`
   - Sử dụng nút gạt ngôn ngữ **VI / EN** trên thanh tiêu đề để kiểm tra khả năng chuyển đổi tức thì giữa nội dung tiếng Việt và tiếng Anh.
