---
name: web-markdown-authoring
description: "Quy chuẩn bắt buộc khi AI soạn thảo tài liệu, bài giảng kỹ thuật định dạng Markdown (.md) để hiển thị hoàn hảo, không lỗi trên giao diện Web, LMS, Blog và Documentation CMS."
---

# Web Markdown Authoring Standard (Quy Chuẩn Soạn Thảo Markdown Cho Web)

Skill này cung cấp bộ quy tắc vàng (Golden Rules) giúp AI tạo ra các tệp `.md` chuyên nghiệp, tương thích 100% với các bộ phân tích cú pháp web (Marked, MDX, Rehype/Remark, Next.js, Docusaurus, VitePress).

---

## 🛑 BẢNG TRA CỨU CÁC LỖI THƯỜNG GẶP & CÁCH KHẮC PHỤC

| Hiện tượng lỗi trên Web | Nguyên nhân gốc rễ | Cách viết SAI ❌ | Cách viết CHUẨN WEB ✅ |
| :--- | :--- | :--- | :--- |
| **Hiện chữ thô `[!TIP]`, `[!NOTE]`** | Viết dính dòng hoặc dùng tag không hỗ trợ | `> [!TIP] Nội dung trên cùng dòng` | `> [!TIP]`<br>`> Nội dung nằm ở dòng sau` |
| **Hiện chữ thô `$\to$`** | Dùng LaTeX inline khi web không có KaTeX | `A $\to$ B $\to$ C` | `A → B → C` (dùng Unicode) |
| **Tóm tắt bị trùng lặp / hiện dấu `**`** | Thiếu `> Tóm tắt:` riêng biệt hoặc lồng `**` | Không có dòng tóm tắt, tự lấy đoạn đầu | `> Tóm tắt: Câu tóm tắt thuần túy` |
| **Link bị chặn không bấm được** | Dùng đường dẫn cục bộ máy tính `file:///` | `[Bài 1](file:///F:/doc.md)` | `[Bài 1](/tutorials/topic/bai-1)` |
| **Ảnh bị vỡ / icon lỗi** | Thiếu file thật hoặc sai đường dẫn public | `![](/local/path/img.png)` | `<img src="images/name.svg" width="900" alt="...">` |
| **Bảng vỡ khung cột** | Thiếu dòng gạch ngăn cách header | Kẻ ô thiếu dòng `\| :--- \|` | Luôn có `\| :--- \| :--- \|` |
| **Code block không màu cú pháp** | Không khai báo tên ngôn ngữ | ```` ```` (không có tên ngôn ngữ) | ````c ```` hoặc ````python ```` |

---

## 0. TÓM TẮT BÀI HỌC (HOÀN TOÀN TÙY CHỌN - OPTIONAL)

Khung tóm tắt (Summary Card) **KHÔNG BẮT BUỘC**, phụ thuộc hoàn toàn vào tác giả có muốn thêm hay không:
- **Mặc định (Khuyến nghị khi không cần thiết)**: KHÔNG cần thêm dòng tóm tắt. Bài viết sẽ hiển thị thẳng vào nội dung sau tiêu đề `# H1`, không xuất hiện khung tóm tắt cam, không sợ bị trùng lặp nội dung.
- **Khi tác giả chủ động muốn có khung tóm tắt nổi bật**:
  - Đặt cú pháp `> Tóm tắt: [Nội dung]` ngay dưới tiêu đề `# H1`.
  - Viết câu thuần túy (Plain Text), không lồng `**in đậm**` hay ký tự thô.
  - Viết ngắn gọn (1-2 câu). Khi có dòng này, hệ thống sẽ tự động tách riêng vào khung tóm tắt và không bị lặp lại trong thân bài.

---

## 1. QUY CHUẨN CALLOUT / ALERTS (GFM CALLOUTS)

### Danh sách 5 thẻ được chuẩn hóa:
1. `> [!NOTE]` hoặc `> [!INFO]`: Thông tin ghi chú kỹ thuật.
2. `> [!TIP]`: Mẹo tối ưu hóa mã nguồn, hiệu năng, kinh nghiệm thực chiến.
3. `> [!IMPORTANT]`: Điểm cốt lõi, bắt buộc phải chú ý về kiến trúc hoặc phần cứng.
4. `> [!WARNING]`: Cảnh báo rủi ro, lỗi biên dịch, lỗi nạp chip.
5. `> [!CAUTION]` hoặc `> [!DANGER]`: Nguy cơ hỏng linh kiện, chập cháy nguồn điện, mất dữ liệu.

### Quy tắc cú pháp:
- **Dòng 1**: Chỉ chứa cú pháp định danh: `> [!TÊN_THẺ]`
- **Dòng 2 trở đi**: Bắt đầu bằng `> ` và chứa nội dung.
- **Nếu có danh sách con (list)**: Mỗi gạch đầu dòng phải có `> - ` hoặc `> 1. ` rõ ràng.

```markdown
> [!IMPORTANT]
> **Lưu ý phần cứng tối quan trọng:**
> - Cấu hình chân BOOT0 về mức 0 (GND) để vi điều khiển boot từ Flash nội.
> - Đèn LED nối với chân PC13 theo sơ đồ Active-Low:
>   - Xuất mức logic 0: Đèn LED SÁNG.
>   - Xuất mức logic 1: Đèn LED TẮT.
```

---

## 2. KÝ HIỆU TOÁN HỌC & MŨI TÊN (UNICODE OVER LATEX)

Trên các trang web tin tức, LMS và blog kỹ thuật, **không phải lúc nào KaTeX/MathJax cũng được tích hợp cho cú pháp `$...$`**. Do đó:
- **TUYỆT ĐỐI KHÔNG** dùng `$\to$`, `$\Rightarrow$`, `$\le$`, `$\ge$` cho các liên kết luồng đơn giản.
- **LUÔN DÙNG KÝ TỰ UNICODE NGUYÊN BẢN**:
  - Mũi tên: `→`, `⇒`, `←`, `⇐`, `↔`
  - So sánh & Tính toán: `≤`, `≥`, `≈`, `≠`, `±`, `×`, `÷`
  - Đơn vị điện tử & Kỹ thuật: `Ω`, `kΩ`, `µF`, `µs`, `mA`, `°C`
  - Logic bit: `AND (&)`, `OR (|)`, `XOR (^)`, `NOT (~)`

*Ví dụ:*
- ❌ Sai: `Thanh ghi $\to$ Ngoại vi $\to$ FreeRTOS`
- ✅ Đúng: `Thanh ghi → Ngoại vi → FreeRTOS`

---

## 3. QUY CHUẨN LIÊN KẾT (URL & SLUGS - TUYỆT ĐỐI CẤM `file:///`)

1. **Tuyệt đối cấm**:
   - `file:///...` (trình duyệt bảo mật chặn 100% từ giao thức https/http).
   - Đường dẫn thư mục máy tính: `C:\Users\...`, `F:\Advance_C\...`.
2. **Liên kết nội bộ trang web**:
   - Dùng URL tương đối (Relative Path) theo định dạng slug:
     `[Xem bài 2: GPIO](/tutorials/stm32f103/bai-02-gpio-bit-banding)`
   - Nếu bài viết chưa xuất bản lên web, chỉ ghi in đậm tên bài viết:
     `👉 **Bài 02: Phân tích chuyên sâu GPIO và kỹ thuật Bit-Banding**`
3. **Liên kết tài nguyên bên ngoài**:
   - Luôn sử dụng URL đầy đủ với giao thức `https://`:
     `[Keil MDK Community Edition](https://www.keil.arm.com/mdk-community/)`

---

## 4. QUY CHUẨN HÌNH ẢNH & SƠ ĐỒ KỸ THUẬT

1. **Cấu trúc nhúng hình ảnh chuẩn Web**:
   Khuyến khích dùng thẻ HTML `<figure>` hoặc `<p align="center">` có thuộc tính kích thước rõ ràng để chống layout shift (CLS):
   ```markdown
   <p align="center">
     <img src="images/bai01_pinout.svg" width="900" alt="Sơ đồ chân STM32F103 Blue Pill">
   </p>
   ```
2. **Quy tắc đường dẫn ảnh**:
   - Dùng đường dẫn tương đối `images/ten_file.svg` (hoặc `images/ten_file.png`).
   - Luôn đặt file ảnh trong thư mục `images/` nằm cùng cấp với file Markdown.
   - Luôn có thuộc tính `alt="..."` mô tả ngắn gọn, chính xác hình ảnh.

---

## 5. QUY CHUẨN KHỐI MÃ NGUỒN (CODE BLOCKS)

1. Luôn khai báo định danh ngôn ngữ (language tag) sau ba dấu backtick:
   - C nhúng: ````c ````
   - C++: ````cpp ````
   - Python: ````python ````
   - Bash/Terminal: ````bash ````
   - Cấu hình: ````json ````, ````yaml ````
   - Sơ đồ luồng: ````mermaid ````
2. Không để trống language tag:
   - ❌ Sai: ```` ````
   - ✅ Đúng: ````c ````
3. Khuyến khích thêm chú thích ngắn gọn ở đầu khối mã:
   ```c
   // Cấu hình chân PC13: General Purpose Output Push-Pull, tốc độ tối đa 2MHz
   GPIOC->CRH &= ~(0xF << 20); // Xóa cấu hình cũ của PC13
   GPIOC->CRH |= (0x2 << 20);  // MODE13 = 10 (Output 2MHz), CNF13 = 00 (Push-Pull)
   ```

---

## 6. QUY CHUẨN BẢNG DỮ LIỆU (GFM TABLES)

- Luôn có dòng ngăn cách phân định header `| :--- | :--- |`.
- Căn lề phù hợp:
  - Căn trái cho tên, chuỗi, diễn giải: `:---`
  - Căn giữa cho mã thanh ghi, địa chỉ hex, kích thước, trạng thái: `:---:`
  - Căn phải cho số liệu, tần số: `---:`
- Nếu trong 1 ô cần xuống dòng, dùng thẻ `<br>` thay vì ấn enter xuống dòng.

```markdown
| Thanh Ghi | Địa Chỉ Hex | Bit Trường | Căn Giữa | Chức Năng Chi Tiết |
| :--- | :---: | :---: | :---: | :--- |
| `RCC_APB2ENR` | `0x4002 1018` | Bit 4 | `IOPCEN` | Cấp xung nhịp cho Bus GPIOC |
| `GPIOC_CRH` | `0x4001 1004` | Bit 20-23 | `MODE13 / CNF13` | Cấu hình tốc độ và chế độ ngõ ra |
```

---

## 7. CẤU TRÚC PHÂN CẤP HEADINGS (CHUẨN SEO & MỤC LỤC TỰ ĐỘNG)

- **# H1**: Tiêu đề duy nhất của bài học ở đầu file (ví dụ: `# BÀI 01: TỔNG QUAN STM32F103...`).
- **## H2**: Các phần chính được đánh số (ví dụ: `## 1. Link Tải Phần Mềm`, `## 2. Kiến Trúc Bộ Nhớ`).
- **### H3**: Các mục con chi tiết (ví dụ: `### 1.1 Môi trường Keil C`, `### 1.2 Driver nạp`).
- **#### H4**: Tiểu mục chuyên sâu (nếu có).
- Tuyệt đối không nhảy cấp (từ H2 nhảy thẳng xuống H4 mà bỏ qua H3), vì sẽ làm hỏng mục lục tự động (Table of Contents) trên thanh bên phải của giao diện web.
