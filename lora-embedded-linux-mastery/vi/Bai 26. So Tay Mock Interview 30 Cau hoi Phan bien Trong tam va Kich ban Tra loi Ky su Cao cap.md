# BÀI 26: SỔ TAY KỸ SƯ CAO CẤP: 30 CÂU HỎI PHẢN BIỆN KIẾN TRÚC & XỬ LÝ SỰ CỐ HỆ THỐNG

> Tóm tắt: Tổng hợp 30 câu hỏi kỹ thuật chuyên sâu và bài toán thiết kế hóc búa nhất trong hệ thống nhúng LoRa, Linux Kernel và Android Automotive / AOSP, cung cấp khung phân tích 4 bước chuẩn mực giúp kỹ sư giải quyết triệt để các thách thức kiến trúc thực chiến.

---

## 1. Cấu Trúc Khung Trả Lời Chuẩn Mực Của Kỹ Sư Cao Cấp

Khi đối mặt với các thách thức kỹ thuật và bài toán thiết kế hệ thống chuyên sâu, phương pháp phân tích của một kỹ sư có kinh nghiệm luôn bao gồm 4 mảnh ghép:
1. **Khái niệm kỹ thuật trực diện (Direct Principle)**: Trả lời thẳng vào bản chất, không vòng vo.
2. **Số liệu định lượng thực tế (Quantitative Metrics)**: Đưa ra các con số chính xác ($14\text{ dBm}$, $125\text{ kHz}$, $10\text{ µs}$, $-20\text{ dB}$).
3. **Phân tích sự đánh đổi kiến trúc (Trade-Off Analysis)**: Giải thích tại sao chọn phương án A mà không chọn phương án B.
4. **Biện pháp phòng ngừa rủi ro thực chiến (Production Safeguards)**: Nhắc đến các bẫy phần cứng, Watchdog, Timeout, bảo mật SELinux.

---

## 2. Phần 1: LoRa PHY & Bản Chất Phần Cứng Vô Tuyến (Câu 01 → 06)

### Câu 01: LoRa là gì và tại sao nó có thể thu được tín hiệu nằm dưới mức nhiễu nền?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: LoRa là công nghệ điều chế trải phổ tiếng ríu (Chirp Spread Spectrum - CSS) độc quyền của Semtech. Nó truyền dữ liệu bằng cách quét tuyến tính tần số sóng mang trên một dải băng thông ($BW$). Nhờ việc trải năng lượng tín hiệu trên phổ rộng, bộ giải điều chế của Semtech sử dụng thuật toán tương quan (Matched Filter Correlation), cho phép tích lũy năng lượng của các chirp qua thời gian. Do đó, ngay cả khi công suất tín hiệu yếu hơn nhiễu nhiệt môi trường tới 100 lần ($SNR = -20\text{ dB}$ ở cấu hình SF12), máy thu vẫn có thể phát hiện và khôi phục chính xác gói tin.

### Câu 02: Spreading Factor (SF) ảnh hưởng thế nào đến tốc độ, khoảng cách và thời gian phát sóng?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Mỗi bước tăng SF sẽ làm tăng gấp đôi số lượng chip vật lý trên mỗi biểu tượng ($2^{SF}$). Khi tăng từ SF7 lên SF12, độ nhạy thu tăng thêm $14\text{ dB}$ giúp cự ly truyền tăng gấp đôi trong không gian tự do. Tuy nhiên, thời gian phát một symbol tăng 32 lần, khiến tốc độ truyền dữ liệu tụt giảm từ $5.47\text{ kbps}$ xuống chỉ còn $293\text{ bps}$, đồng thời Time-on-Air tăng theo hàm mũ, làm tiêu hao nhiều pin hơn và dễ bị phạt vi phạm quy định Duty Cycle 1%.

### Câu 03: Channel Activity Detection (CAD) là gì và có loại bỏ được 100% va chạm gói tin không?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: CAD là cơ chế phần cứng của chip LoRa dùng để kiểm tra xem kênh truyền có đang bận hay không bằng cách kích hoạt bộ thu trong thời gian đúng 1 symbol ($T_s$) để tìm kiếm mẫu Up-chirp của Preamble. CAD tiết kiệm hơn 95% năng lượng so với việc mở cổng thu liên tục. Tuy nhiên, CAD **không thể triệt tiêu 100% va chạm** do hiện tượng Race Condition (hai node cùng quét CAD thấy rảnh và cùng phát tại một thời điểm) hoặc khi gói tin của node khác đã truyền xong Preamble và đang bắn phần Payload.

### Câu 04: Chân PA_BOOST khác chân RFO trên chip SX1276 như thế nào?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Chân RFO là ngõ ra công suất phát hiệu suất cao, đạt tối đa $+14\text{ dBm}$ với dòng tiêu thụ vừa phải (~$28\text{ mA}$). Chân PA_BOOST sử dụng tầng khuếch đại công suất chuyên dụng có thể đẩy công suất phát lên tới $+20\text{ dBm}$ (100 mW) nhưng dòng tiêu thụ vọt lên $120\text{ mA}$. Khi dùng PA_BOOST, bắt buộc phải kích hoạt thêm thanh ghi `RegPaDac` và phải gắn anten chuẩn $50\ \Omega$ để tránh sóng phản xạ đánh thủng tầng PA.

### Câu 05: Khi nào bắt buộc phải bật cờ Low Data Rate Optimization (LDRO)?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Theo quy chuẩn của Semtech, bất cứ khi nào thời gian tồn tại của một symbol $T_s = 2^{SF} / BW$ vượt quá **$16\text{ ms}$**, cờ LDRO bắt buộc phải được kích hoạt đồng bộ ở cả bên phát và bên thu (điển hình là cấu hình SF11 và SF12 ở băng thông 125 kHz). Khi bật LDRO, modem sẽ tự động phân bổ thêm các bit dự phòng dịch tần để triệt tiêu hiện tượng trôi dạt tần số của thạch anh do biến đổi nhiệt độ.

### Câu 06: Hiện tượng Receiver Saturation xảy ra khi nào và cách khắc phục trong lab?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Khi đặt hai module LoRa cách nhau dưới 1 mét và phát ở công suất lớn (+14 đến +20 dBm), công suất RF đi vào cổng thu vượt quá $-30\text{ dBm}$, làm mạch khuếch đại tạp âm thấp (LNA) bị bão hòa phi tuyến, méo dạng chirp và gây rớt gói tin hàng loạt. Để khắc phục khi thử nghiệm trên bàn lab, ta phải hạ công suất phát xuống mức tối thiểu (2 dBm) hoặc tháo bớt anten và đặt cách xa nhau từ 2–3 mét.

---

## 3. Phần 2: LoRaWAN & Giao Thức Mạng (Câu 07 → 12)

### Câu 07: Phân biệt sự khác nhau giữa LoRa, LoRaWAN và RadioHead RHMesh?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: LoRa là công nghệ điều chế vô tuyến ở Tầng Vật lý (PHY Layer) của Semtech. LoRaWAN là chuẩn giao thức mạng hoàn chỉnh ở Tầng MAC/Network do LoRa Alliance quản lý, sử dụng kiến trúc hình sao mở rộng (Star-of-Stars) với các thực thể Gateway và Cloud Server. RadioHead RHMesh là một giao thức định tuyến đa chặng Ad-hoc độc lập chạy trên LoRa PHY, không sử dụng Gateway hay Cloud Server của LoRa Alliance và hoàn toàn không tương thích với LoRaWAN.

### Câu 08: Trình bày quy trình bắt tay Over-the-Air Activation (OTAA) và các khóa bảo mật được sinh ra?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Thiết bị gửi bản tin `Join Request` (chứa `DevEUI`, `JoinEUI`, `DevNonce` và mã MIC tính bằng `AppKey`). Server kiểm tra hợp lệ và phản hồi bằng gói `Join Accept` (chứa `DevAddr`, `JoinNonce`, `NetID` được mã hóa bằng `AppKey`). Sau khi nhận gói, cả hai bên độc lập sử dụng thuật toán AES-128 để dẫn xuất ra 2 khóa phiên: **`NwkSKey`** (dùng cho LNS kiểm tra tính toàn vẹn MIC và quản trị mạng) và **`AppSKey`** (dùng cho Application Server giải mã dữ liệu người dùng).

### Câu 09: Tại sao thiết bị dùng ABP lại dễ bị rớt gói vĩnh viễn sau khi khởi động lại?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Với ABP, các khóa và địa chỉ `DevAddr` được nạp cứng. Khi thiết bị khởi động lại, bộ đếm gói tin `FCnt` trong RAM bị reset về 0. Khi thiết bị phát gói tin với $FCnt = 0$, Network Server đối chiếu thấy $0 \le FCnt_{cu}$ nên coi đây là cuộc tấn công phát lại (Replay Attack) và âm thầm vứt bỏ gói tin cho đến khi bộ đếm của thiết bị vượt qua giá trị cũ đã lưu trên server.

### Câu 10: Phân biệt Class A, Class B và Class C trong LoRaWAN?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Class A tiết kiệm điện nhất, chỉ mở 2 cửa sổ thu ngắn RX1 (sau 1s) và RX2 (sau 2s) sau khi vừa phát xong một gói Uplink. Class B mở thêm các cửa sổ nhận định kỳ (Ping Slots) được đồng bộ thời gian bằng sóng Beacon từ Gateway. Class C mở cổng thu liên tục gần như 100% thời gian (trừ lúc đang phát), độ trễ nhận lệnh tức thì (< 100 ms) nhưng tiêu tốn dòng ~11 mA liên tục nên bắt buộc phải dùng nguồn điện cố định.

### Câu 11: Thuật toán Adaptive Data Rate (ADR) hoạt động thế nào và tại sao cấm dùng cho thiết bị di động?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Máy chủ LNS thu thập giá trị SNR của 20 gói tin gần nhất để tính toán biên độ dự phòng tín hiệu ($SNR_{margin}$). Nếu tín hiệu mạnh, LNS gửi lệnh `LinkADRReq` yêu cầu thiết bị hạ SF xuống SF7 và giảm công suất phát để tiết kiệm pin. Thuật toán này **bắt buộc cấm dùng cho thiết bị di động** (xe điện, tracker) vì kênh truyền thay đổi liên tục. Nếu xe đang ở gần Gateway bị ép xuống SF7/2dBm rồi sau đó di chuyển ra xa hoặc vào hầm ngầm, thiết bị sẽ bị mất kết nối hoàn toàn.

### Câu 12: Bẫy "Hop-by-hop ACK" trong mạng Mesh là gì?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Trong thư viện RHMesh, hàm `sendtoWait()` trả về thành công khi nhận được ACK từ **node trung gian kế tiếp (Next Hop)**, chứ không phải từ đích cuối (Gateway). Nếu node trung gian đó sau đó bị mất nguồn hoặc đầy hàng đợi, gói tin sẽ bị mất vĩnh viễn mà node phát ban đầu không hề hay biết. Để đảm bảo độ tin cậy tuyệt đối, hệ thống bắt buộc phải thiết kế thêm tầng xác nhận đầu cuối **Application End-to-End ACK**.

---

## 4. Phần 3: Linux SPI Subsystem & Kernel Driver (Câu 13 → 18)

### Câu 13: Trình bày các bước mang một chip SX1276 từ vi điều khiển sang bo mạch Linux?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Gồm 4 bước: (1) Khai báo phần cứng trong Device Tree (bộ điều khiển SPI, tần số max, chân reset GPIO, chân ngắt DIO0); (2) Viết một `spi_driver` đăng ký chuỗi `compatible` để kernel khớp Device Tree và gọi hàm `probe()`; (3) Trong hàm `probe()`, reset chip, đọc kiểm tra `RegVersion = 0x12`, và đăng ký ngắt luồng `request_threaded_irq()`; (4) Đăng ký một Character Device cung cấp các hàm `open`, `read`, `write`, `ioctl`, `poll` cho userspace.

### Câu 14: Tại sao bắt buộc phải dùng `request_threaded_irq()` thay vì `request_irq()` cho chip LoRa trên Linux?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Khi ngắt DIO0 phát sinh, driver bắt buộc phải gọi hàm `spi_sync()` để đọc trạng thái thanh ghi và trích xuất FIFO. Bản chất của `spi_sync()` trên Linux là một hàm có khả năng ngủ (**Sleeping/Blocking**) để chờ DMA phần cứng truyền xong. Trình phục vụ ngắt cứng thông thường của `request_irq()` chạy trong Atomic Context không được phép ngủ (nếu gọi sẽ gây Crash Kernel Panic: *"scheduling while atomic"*). Do đó bắt buộc phải dùng `request_threaded_irq()` để chuyển việc gọi SPI sang một Kernel Thread riêng biệt chạy trong Process Context có quyền ngủ.

### Câu 15: Vai trò của cờ `IRQF_ONESHOT` trong `request_threaded_irq()` là gì?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Do chân ngắt DIO0 của SX1276 là ngắt chốt mức cao (nó giữ nguyên mức cao cho đến khi thanh ghi được xóa qua SPI). Nếu không có cờ `IRQF_ONESHOT`, ngay khi hàm ngắt cứng Top-half vừa nhả quyền, phần cứng GPIO sẽ phát hiện chân DIO0 vẫn đang ở mức 1 và kích hoạt ngắt liên tục vô tận (Interrupt Storm), làm treo cứng CPU trước khi Kernel Thread kịp chạy. Cờ `IRQF_ONESHOT` yêu cầu kernel khóa đường ngắt đó lại và chỉ mở ra sau khi Kernel Thread xử lý xong.

### Câu 16: Phân biệt `spidev` ở Userspace và Kernel Driver chuyên dụng?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: `spidev` là driver tổng quát có sẵn của kernel, cho phép ứng dụng Userspace tự gọi `ioctl` để bắn các byte SPI thô. Ưu điểm là phát triển nhanh, an toàn (daemon crash không làm sập OS). Nhược điểm là độ trễ ngắt lớn hơn (~100 µs) và khó quản lý phân quyền bảo mật SELinux. Kernel Driver chuyên dụng xử lý ngắt trong kernel cực nhanh (< 10 µs), đóng gói thành `/dev/lora0` sạch sẽ nhưng chi phí phát triển cao và lỗi code có thể làm sập toàn bộ OS.

### Câu 17: Làm thế nào để gỡ lỗi khi đọc thanh ghi qua bus SPI luôn trả về `0x00` hoặc `0xFF`?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Dùng máy phân tích logic hoặc oscilloscope kẹp vào 4 chân SPI. Nếu ra `0x00`: Kiểm tra chân MISO có bị chập mass không, kiểm tra nguồn VDD đã cấp tới chân chip chưa. Nếu ra `0xFF`: Kiểm tra đường MISO có bị hở chân (Floating) không, hoặc kiểm tra chân NSS có thực sự kéo xuống mức $0\text{V}$ khi truyền không (nếu NSS bị treo ở 3.3V, chip sẽ không xuất dữ liệu ra MISO). Kiểm tra thêm tốc độ clock và SPI Mode (phải là Mode 0).

### Câu 18: Hàm `poll()` trong Character Driver hoạt động thế nào và tại sao cần thiết?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Hàm `poll()` cho phép các tiến trình Userspace gọi `epoll_wait()` hoặc `select()` để ngủ sâu (0% CPU) và chỉ thức dậy khi có dữ liệu sẵn sàng đọc (`EPOLLIN`). Trong driver, hàm `poll()` gọi `poll_wait()` để đăng ký một `wait_queue_head_t`. Khi ngắt Threaded IRQ thu được gói tin LoRa, nó gọi `wake_up_interruptible()`, đánh thức ứng dụng Userspace dậy đọc dữ liệu ngay lập tức mà không cần chạy vòng lặp thăm dò liên tục.

---

## 5. Phần 4: AOSP, AIDL & Hệ Thống Xe Điện Thông Minh (Câu 19 → 24)

### Câu 19: Kiến trúc phân tầng AOSP từ ứng dụng Android xuống chip LoRa gồm những thành phần nào?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Gồm 5 tầng: (1) Android App (Java/Kotlin); (2) System Service chạy trong `system_server` quản lý quyền và hàng đợi; (3) Giao diện Binder IPC định nghĩa bằng Stable AIDL (`ILoRaRadio.aidl`); (4) Vendor HAL Service (C++) hiện thực logic điều khiển; (5) Nhân Linux Kernel chứa driver `/dev/lora0` được quản lý bởi chính sách bảo mật SELinux.

### Câu 20: SELinux bảo vệ tài nguyên phần cứng LoRa trên Android như thế nào?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: SELinux áp dụng cơ chế kiểm soát truy cập bắt buộc (MAC). Trong file `file_contexts`, node `/dev/lora0` được gán nhãn kiểu `u:object_r:lora_device:s0`. Trong file chính sách `hal_lora.te`, ta chỉ cấp quyền `allow hal_lora_default lora_device:chr_file { open read write ioctl };` cho riêng tiến trình Vendor HAL. Mọi ứng dụng thông thường hoặc mã độc cố tình mở `/dev/lora0` sẽ bị nhân Linux chặn đứng ngay lập tức với lỗi `avc: denied`.

### Câu 21: Thiết kế cơ chế Telematics Fallback từ 4G sang LoRa cho xe điện thông minh như thế nào?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Một tiến trình giám sát kết nối (Connection Monitor) liên tục kiểm tra đường truyền 4G. Nếu mất kết nối quá 15 giây (cơ chế trễ Hysteresis chống chập chờn sóng), hệ thống chuyển sang chế độ Fallback: Toàn bộ dữ liệu đo xa phức tạp (JSON) bị tạm dừng và lưu đệm vào Flash (Store-and-Forward). Hệ thống chỉ trích xuất các thông số sinh tồn (Tọa độ GPS, vận tốc, SOC pin, mã lỗi SOS) nén chặt thành gói tin nhị phân 12 bytes phát qua LoRa với chu kỳ 1–2 phút một lần để tuân thủ quy chuẩn vô tuyến. Khi 4G ổn định trở lại trong 30 giây, hệ thống tự động đồng bộ lại lịch sử từ Flash lên đám mây.

### Câu 22: Khi xe điện tắt máy hoàn toàn (Power-off), cơ chế Remote Wake-up bằng LoRa hoạt động ra sao?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Phần cứng phân tách làm hai miền nguồn: Miền nguồn Always-on (AON) nuôi một vi điều khiển phụ Cortex-M0+ và chip LoRa tiêu thụ dòng chỉ $10\text{ µA}$. Miền nguồn hiệu năng cao nuôi SoC Android chính bị cắt điện hoàn toàn (0W). Khi người dùng gửi lệnh đánh thức từ xa, chip LoRa bắt sóng và đánh thức Co-processor phụ. Co-processor xác thực mã mật mã HMAC. Nếu hợp lệ, nó kích hoạt chân `PWR_EN` của IC nguồn PMIC để bật nguồn cho SoC Android khởi động và thực thi lệnh mở xe.

### Câu 23: Làm thế nào để chống tấn công làm cạn bình ắc quy xe điện (Battery Draining Attack) qua LoRa?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Nếu cứ thấy sóng LoRa là bật nguồn SoC Android, kẻ xấu có thể spam sóng để xe liên tục khởi động làm cạn bình ắc quy 12V. Biện pháp phòng vệ: Mọi gói tin đánh thức bắt buộc phải chứa một mã xác thực chữ ký điện tử dùng một lần (HMAC-SHA256 kết hợp Timestamp và Nonce). Vi điều khiển phụ Cortex-M0+ sẽ giải mã và kiểm tra chữ ký này trong vòng 5 ms; nếu chữ ký không khớp, nó lập tức hủy gói tin và **tuyệt đối không bật nguồn SoC chính**, đồng thời khóa nhận sóng trong 15 phút nếu bị spam liên tục quá 3 lần.

### Câu 24: Khi SoC Android vừa khởi động xong sau khi được đánh thức từ xa, làm sao nó biết được lệnh cần thực thi là gì?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Toàn bộ nội dung gói tin lệnh được lưu tạm trong bộ nhớ RAM tĩnh của vi điều khiển phụ Co-processor (vốn luôn được cấp nguồn). Khi hệ điều hành Android hoàn tất quá trình boot kernel, một Daemon phần cứng sẽ gửi lệnh truy vấn qua bus I2C/UART nội bộ tới Co-processor: *"Nguyên nhân đánh thức là gì?"*. Co-processor sẽ truyền payload lệnh đã lưu sang cho Android thực thi (như mở khóa cốp xe).

---

## 6. Phần 5: Kinh Nghiệm Thực Chiến & Khắc Phục Sự Cố (Câu 25 → 30)

### Câu 25: Kể một lỗi phần cứng hoặc firmware phức tạp nhất mà em từng tự điều tra và giải quyết?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Trình bày theo khung CAR (Context - Action - Result): *"Trong dự án LoRa prototype trước đây, hệ thống bị hiện tượng mất gói tin lên tới 40% khi đem ra thử nghiệm ngoài trời vào buổi trưa. Em đã dùng thiết bị SDR đo phổ và phát hiện tần số phát bị lệch 28 kHz. Nguyên nhân là do thạch anh giá rẻ bị trôi dạt nhiệt độ vượt quá ngưỡng dung sai 25% BW của chip SX1276. Em đã khắc phục ngay bằng cách bật cờ phần mềm LowDataRateOptimize (LDRO), và sau đó nâng cấp schematic sang dùng linh kiện thạch anh bù nhiệt TCXO ±1 ppm. Kết quả là hệ thống chạy ổn định 100% trong buồng nhiệt 70°C."*

### Câu 26: Hiệu ứng chiếm đoạt sóng (Capture Effect) trong LoRa là gì và ảnh hưởng thế nào đến mạng nhiều node?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Khi hai gói tin LoRa phát cùng tần số và đâm vào nhau tại Gateway, nếu gói tin của node gần có công suất mạnh hơn gói tin của node xa từ $6\text{ dB}$ trở lên ($RSSI_1 - RSSI_2 \ge 6\text{ dB}$), bộ thu của Gateway sẽ bỏ rơi gói tin yếu và giải mã thành công gói tin mạnh. Điều này dẫn tới hiện tượng các node ở gần luôn chèn ép và làm biến mất dữ liệu của các node ở xa (Near-Far Problem), đòi hỏi phải dùng thuật toán ADR để giảm công suất của các node ở gần.

### Câu 27: Làm thế nào để đóng gói tọa độ GPS (Kinh độ/Vĩ độ) từ 16 bytes số thực float/double xuống chỉ còn 6 bytes?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Vĩ độ ($-90^\circ$ đến $+90^\circ$, dải $180^\circ$) và Kinh độ ($-180^\circ$ đến $+180^\circ$, dải $360^\circ$). Một số nguyên không dấu 24-bit có $2^{24} = 16,777,216$ mức. Ta ánh xạ tuyến tính vĩ độ bằng công thức: $Lat_{24} = \text{round}((Lat + 90) \times (16,777,215 / 180))$. Mỗi tọa độ chỉ tốn đúng 3 bytes (24 bits) nhưng đạt độ phân giải không gian $1.1\text{ mét}$. Hai tọa độ chỉ tốn đúng $6\text{ bytes}$ thay vì $16\text{ bytes}$ số thực `double`!

### Câu 28: Sự khác nhau giữa cấu hình Explicit Header Mode và Implicit Header Mode trong LoRa?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Trong Explicit Header Mode, phần đầu gói tin chứa thông tin về độ dài payload, tỷ lệ mã hóa CR và cờ bật tắt CRC. Chế độ này linh hoạt khi gói tin có độ dài thay đổi. Trong Implicit Header Mode, phần Header bị lược bỏ hoàn toàn để tiết kiệm vài millisecond Time-on-Air, nhưng bắt buộc cả bên phát và bên thu phải được nạp cứng cùng một độ dài payload và CR từ trước.

### Câu 29: Nếu phải chọn giữa FreeRTOS và Embedded Linux cho một thiết bị LoRa Gateway, em chọn hệ điều hành nào?
* **Phân tích kỹ thuật & Giải pháp chuẩn mực**: Bắt buộc phải chọn **Embedded Linux**. Một Gateway LoRaWAN (dùng chip SX1302/03) phải xử lý đồng thời 8 đến 16 kênh tần số với hàng nghìn gói tin mỗi phút, kết nối mạng Internet qua 4G/Ethernet, hỗ trợ bảo mật TLS và chạy phần mềm Basic Station / Packet Forwarder. FreeRTOS phù hợp cho thiết bị đầu cuối End Device (cảm biến pin hoặc cụm MCU đo xa), trong khi Gateway đòi hỏi sức mạnh quản lý bộ nhớ ảo (MMU), mạng IP phức tạp và hệ thống tệp tin của Linux.

### Câu 30: "Em chưa từng triển khai LoRaWAN MAC trên AOSP trong thực tế, tại sao công ty nên tuyển em?"
* **Kịch bản trả lời (Trung thực và Thuyết phục)**:
> *"Dạ, em xin phép trả lời thẳng thắn: Trong các dự án trước đây, em đã trực tiếp làm chủ tầng vật lý LoRa trên chip Semtech SX1276 qua bus SPI, hiểu sâu sắc về thanh ghi, máy trạng thái, tối ưu năng lượng và từng tự triển khai mạng LoRa Mesh bằng thư viện RadioHead. Song song đó, ở công việc hiện tại, em làm việc hàng ngày với Embedded Linux, Device Tree, Kernel Driver, phân tích mạng và gỡ lỗi hệ thống.
> Việc tích hợp LoRaWAN trên AOSP thực chất là sự giao thoa giữa hai thế mạnh em đã có: lớp dưới là điều khiển phần cứng SPI/IRQ trên Linux mà em đã nắm vững, lớp trên là giao tiếp liên tiến trình Binder/AIDL và cơ chế mạng mà em có tư duy hệ thống để tiếp cận rất nhanh. Em hiểu rõ ranh giới giữa những gì mình đã làm thực tế và những gì đang ở mức nghiên cứu kiến trúc, và em tự tin rằng với nền tảng kỹ thuật gốc vững chắc, em sẽ hòa nhập và làm chủ công việc trong vòng 2 đến 3 tuần đầu tiên!"*

