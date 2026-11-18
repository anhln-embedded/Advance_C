# KẾ HOẠCH ÔN PHỎNG VẤN 3 NGÀY
## Embedded Software Engineer (LoRa / UWB) — Ưu tiên LoRa Track

> **Mục tiêu:** Chuẩn bị trong **3 ngày (~5–6 giờ/ngày)** để tự tin phỏng vấn kỹ thuật bằng **tiếng Việt** cho vị trí tích hợp LoRa/LoRaWAN trên Linux/AOSP trong hệ thống Connected EV Smart Instrument Cluster.
>
> **Chiến lược:** Không học dàn trải. Ưu tiên **LoRa/LoRaWAN (45%) → Linux SPI/driver (35%) → AOSP, hệ thống và phỏng vấn (20%)**. Tận dụng kinh nghiệm sẵn có về Embedded C/C++, OpenWrt/prplOS, Device Tree, kernel/userspace, ESP32 + SX1276/8 và RHMesh.

---

## 1. Đối chiếu nhanh JD và kinh nghiệm hiện tại

| Yêu cầu JD | Điểm đã có | Cần bổ sung trong 3 ngày |
|---|---|---|
| C/C++ Embedded | Firmware MCU, Embedded Linux | Ôn ngắn về buffer, lifetime, concurrency khi debug driver |
| Semtech LoRa over SPI | SX1276/SX1278 với ESP32, RF configuration | Cách port radio driver lên Linux |
| LoRaWAN MAC layer | Kinh nghiệm **LoRa Mesh (RadioHead)**, không phải LoRaWAN | **OTAA, keys, Class A/B/C, RX1/RX2, ADR, regional params** |
| Linux device integration | Device Tree, kernel integration, `ioctl` | `spi_driver`, `probe`, IRQ, character device, `poll` |
| Daemon/HAL/AIDL | `ubus`, middleware, daemon OpenWrt | Binder, AIDL HAL, init service, SELinux ở mức kiến trúc |
| Connected EV use cases | Telemetry, MQTT, low-level firmware | Fallback, queue, power states, remote wake-up |
| QA / debug | CDRouter, DNS, LAN port, NAT | Cách trình bày test–root cause–fix–regression |

**Giới hạn cần trình bày trung thực:** Bạn đã làm **LoRa Mesh trên ESP32**, chưa có bằng chứng triển khai **LoRaWAN MAC trên Linux/AOSP**. Cũng chưa nên nhận là đã viết LoRa kernel driver hay AIDL HAL thực tế.

---

## 2. NGÀY 1 — LoRa PHY, Semtech SX127x và LoRaWAN (5 giờ 30 phút)

**Mục tiêu cuối ngày:** Giải thích rõ sự khác nhau giữa LoRa, LoRa Mesh, LoRaWAN; mô tả OTAA và đường đi của một gói tin; giải thích RF configuration từng dùng trong dự án.

| Thời lượng | Chủ đề | Phải hiểu / làm được |
|---:|---|---|
| 60 phút | **LoRa PHY** | Spreading Factor (SF), Bandwidth (BW), Coding Rate (CR), RSSI, SNR, Time-on-Air, link budget, CAD |
| 60 phút | **SX1276/8 & SPI** | SPI mode, CS/NSS, reset, register, FIFO, DIO/IRQ, TX/RX state; bring-up và debug đọc register |
| 50 phút | **LoRa Mesh vs LoRaWAN** | RadioHead `RH_RF95`/`RHMesh`, multi-hop, route discovery; LoRaWAN star-of-stars, gateway, network server |
| 70 phút | **LoRaWAN MAC cơ bản** | OTAA vs ABP, Join Request/Join Accept, DevEUI/JoinEUI, các khóa theo phiên bản, session keys, MIC, frame counter |
| 50 phút | **LoRaWAN vận hành** | Class A/B/C, RX1/RX2, ADR, confirmed uplink, regional parameters, duty-cycle/airtime theo vùng |
| 40 phút | **Luyện kể dự án** | Nói dự án LoRa Mesh 90 giây; trả lời vì sao dùng Mesh, dùng RHMesh và giới hạn prototype |

### Ghi nhớ bắt buộc ngày 1

- **LoRa** là công nghệ điều chế/lớp vật lý; **LoRaWAN** là giao thức mạng/MAC dùng LoRa PHY.
- **RadioHead RHMesh không phải LoRaWAN**. RHMesh hỗ trợ định tuyến/relay nhiều hop; LoRaWAN thông thường dùng kiến trúc star-of-stars.
- SF tăng thường cải thiện khả năng nhận tín hiệu yếu, nhưng **airtime tăng** và **throughput giảm**; BW, CR cũng tạo đánh đổi.
- Bộ thông số bạn đã dùng cho prototype: **433 MHz, 10 dBm, 125 kHz, CR 4/5, SF7**, packet CRC và CAD. Đây là **cấu hình thử nghiệm**, không phải mặc định hợp lệ ở mọi khu vực.
- **OTAA:** thiết bị gửi Join Request, nhận Join Accept hợp lệ và thiết lập session parameters/keys để truyền dữ liệu; chi tiết khóa phụ thuộc phiên bản LoRaWAN.
- **Class A** tiết kiệm điện, mở RX1/RX2 sau uplink; **Class B** có lịch nhận đồng bộ; **Class C** gần như luôn nhận khi không truyền nên tốn điện hơn.
- **ACK từng hop không đồng nghĩa ACK đầu-cuối**. Nếu gateway phải chắc chắn nhận được bản tin, cần xem xét xác nhận ở lớp ứng dụng.

### Tự kiểm tra — Ngày 1

- [ ] Nói được sự khác nhau giữa LoRa, LoRaWAN và LoRa Mesh trong 60 giây.
- [ ] Giải thích vì sao chọn SF7 / BW 125 kHz / CR 4/5 cho prototype.
- [ ] Mô tả luồng điều khiển SX1276 qua SPI và vai trò các chân DIO.
- [ ] Vẽ được sơ đồ LoRaWAN End Device → Gateway → Network Server → Application Server.
- [ ] Giải thích OTAA và điểm khác ABP.
- [ ] Giải thích Class A/B/C và cửa sổ RX1/RX2.
- [ ] Kể dự án LoRa Mesh mạch lạc trong 90 giây, không nhận nhầm là LoRaWAN.

### Câu hỏi tự luyện

1. LoRa khác LoRaWAN ở đâu? Dự án RHMesh của em thuộc loại nào?
2. Tại sao cần Mesh nếu bản thân LoRa đã truyền xa?
3. SF7 khác SF12 ở tốc độ và airtime như thế nào?
4. CAD là gì? Có bảo đảm không có collision không?
5. Khi một node không tìm được route tới sink, firmware của em xử lý thế nào?
6. Nếu chuyển RHMesh sang LoRaWAN thì phải thay những thành phần nào?
7. OTAA Join Request và Join Accept dùng để làm gì?
8. Nếu thiết bị cần nhận lệnh khi đang tiết kiệm điện, Class A và C có đánh đổi gì?

---

## 3. NGÀY 2 — Linux SPI Driver, Device Tree, IRQ và Character Device (5 giờ 30 phút)

**Mục tiêu cuối ngày:** Trả lời được: “Có một board Linux gắn SX1276 qua SPI, em sẽ bring-up radio từ đầu như thế nào?”

| Thời lượng | Chủ đề | Phải hiểu / làm được |
|---:|---|---|
| 60 phút | **Linux driver cơ bản** | Kernel/userspace, `probe()`/`remove()`, device/driver binding, tài nguyên thiết bị |
| 60 phút | **Linux SPI subsystem** | `struct spi_driver`, `struct spi_device`, SPI transfer, `spi_sync()`, bus number, chip select |
| 60 phút | **Device Tree + GPIO/IRQ** | `compatible`, `reg`, `spi-max-frequency`, reset GPIO, DIO IRQ, pinctrl, interrupt handling |
| 60 phút | **Character Device** | `open`, `read`, `write`, `ioctl`, `poll`; blocking vs non-blocking; đưa trạng thái radio lên userspace |
| 50 phút | **Debug SPI thực tế** | Datasheet, nguồn/reset, logic analyzer, MOSI/MISO/SCLK/CS, sai mode, timeout, IRQ không hoạt động |
| 40 phút | **Thiết kế giao diện Linux–LoRa** | So sánh userspace SPI (`spidev`) và kernel driver; queue/event và điều khiển radio |

### Sơ đồ kiến trúc cần thuộc

```text
Android App / System Service
            |
      AIDL / Binder
            |
       LoRa Daemon
            |
  LoRaWAN MAC / Radio HAL
            |
       Linux interface
            |
   SPI + GPIO + Interrupt
            |
       Semtech SX127x
```

> Đây là **một kiến trúc tham khảo** suy ra từ JD. Không nhất thiết toàn bộ MAC chạy trong kernel; tùy thiết kế sản phẩm, driver hoặc radio HAL có thể ở userspace.

### Quy trình bring-up SX1276 trên Linux (nên thuộc theo thứ tự)

1. **Đọc datasheet và sơ đồ board:** xác định nguồn, reset, SPI, DIO/IRQ, antenna/RF switch.
2. **Kiểm tra cấu hình nền tảng:** SPI controller, pinmux, chip select, Device Tree, clock và GPIO.
3. **Xác nhận giao tiếp SPI:** kiểm tra waveform bằng logic analyzer, thử đọc register nhận dạng và debug dữ liệu đọc trả về.
4. **Thiết lập radio:** frequency, SF, BW, CR, TX power, FIFO, IRQ mask.
5. **Kiểm tra TX/RX:** dùng một thiết bị LoRa đối ứng, xử lý RxDone/TxDone/CRC/timeout.
6. **Kết nối tầng cao:** dùng radio HAL, LoRaWAN MAC và daemon; thêm queue, error handling.
7. **Kiểm thử độ ổn định:** reset, suspend/resume, lỗi SPI, mất tín hiệu, tải cao.

### Tự kiểm tra — Ngày 2

- [ ] Giải thích `probe()` được gọi khi nào và Device Tree hỗ trợ binding ra sao.
- [ ] Phân biệt SPI controller, SPI device, chip select và mode (CPOL/CPHA).
- [ ] Trình bày cách debug trường hợp SPI toàn `0xFF` hoặc `0x00`.
- [ ] Phân biệt IRQ top-half, threaded IRQ và xử lý ở process context.
- [ ] Giải thích `ioctl()` và `poll()` dùng để làm gì trong character driver.
- [ ] So sánh `spidev` userspace với kernel driver về độ phức tạp, IRQ và quản lý tài nguyên.
- [ ] Vẽ được kiến trúc từ Android app đến Semtech chip.

### Câu hỏi tự luyện

1. Nếu đọc sai `RegVersion` SX1276, em debug thế nào?
2. SPI mode 0 khác mode 3 ra sao? CS có vai trò gì?
3. Vì sao Device Tree có thể khiến driver không `probe()`?
4. DIO IRQ phát sinh khi RX hoàn tất; kernel nên xử lý gì và gửi sự kiện lên userspace thế nào?
5. Tại sao `poll()` hữu ích hơn việc daemon cứ lặp gọi `read()` không ngừng?
6. Khi nào chọn `spidev` và khi nào viết kernel driver riêng?

---

## 4. NGÀY 3 — AOSP, System Design và Mock Interview (5 giờ 30 phút)

**Mục tiêu cuối ngày:** Trình bày dự án và kinh nghiệm KAON/VNPT tự nhiên; hiểu kiến trúc AIDL/HAL đủ để trao đổi với interviewer; giải thích được phương án LoRa telematics và remote wake-up.

| Thời lượng | Chủ đề | Phải hiểu / làm được |
|---:|---|---|
| 45 phút | **AOSP nền tảng** | Android app, framework, native service, HAL, Linux kernel; Binder IPC và AIDL |
| 30 phút | **Daemon & bảo mật** | Android `init.rc`, service lifecycle, SELinux domain/sepolicy, quyền truy cập device node |
| 45 phút | **EV system design** | Telematics fallback, payload queue, retry/ACK, dữ liệu nhỏ, power states, remote wake-up |
| 60 phút | **Kể kinh nghiệm thực tế** | LoRa Mesh prototype; KAON CDRouter; VNPT/U-Boot/Device Tree; phần nào đã làm và chưa làm |
| 120 phút | **Mock Interview** | 10–12 câu theo JD, trả lời miệng, hỏi sâu, chấm điểm, sửa câu trả lời |
| 30 phút | **Ôn điểm yếu** | Chỉ xem lại những câu sai, học 3–5 khái niệm quan trọng nhất |

### Kiến thức AOSP cần nắm ở mức kiến trúc

- **AIDL** mô tả API để client/service giao tiếp qua Binder.
- **HAL** tạo lớp trừu tượng giữa phần mềm Android và phần cứng, giúp app không phải trực tiếp truy cập register/SPI.
- **Daemon** quản lý radio, queue, lỗi và trạng thái kết nối; không nên để nhiều ứng dụng tùy ý điều khiển cùng chip.
- **SELinux** giới hạn quyền của service khi truy cập device node và các tài nguyên hệ thống.
- **Remote wake-up:** Nếu SoC thật sự tắt nguồn, cần một thành phần phần cứng còn cấp nguồn (ví dụ MCU/radio subsystem) nhận tín hiệu rồi tạo sự kiện đánh thức; một daemon không tự chạy khi CPU/SoC đã tắt.

### Hai tình huống system design phải luyện

**Tình huống A — Telematics fallback:**

> Xe mất kết nối cellular nhưng vẫn cần gửi dữ liệu trạng thái quan trọng qua LoRa.

Phải trình bày được: ưu tiên thông điệp, kích thước payload, queue có giới hạn, lưu đệm khi mất sóng, retry/backoff, năng lượng, security và quy định tần số/airtime.

**Tình huống B — Remote wake-up:**

> Xe vào chế độ tiết kiệm năng lượng nhưng người dùng cần gửi lệnh đánh thức từ xa.

Phải làm rõ: nguồn nào luôn bật, LoRa radio nhận khi nào, ai xác thực lệnh, MCU/PMIC đánh thức SoC như thế nào, tránh đánh thức sai hoặc bị spam lệnh.

### Tự kiểm tra — Ngày 3

- [ ] Giải thích khác nhau giữa `ubus` và Binder/AIDL mà không nói chúng giống hệt nhau.
- [ ] Mô tả cách ứng dụng Android gọi LoRa daemon/HAL.
- [ ] Biết lý do cần SELinux policy cho service truy cập thiết bị.
- [ ] Trình bày ít nhất một phương án telematics fallback khả thi với giới hạn băng thông LoRa.
- [ ] Nói được tại sao remote wake-up cần quan tâm phần cứng/power domain.
- [ ] Kể dự án LoRa Mesh trong 90 giây, có vai trò cá nhân và giới hạn kỹ thuật.
- [ ] Kể một lỗi CDRouter trong 90 giây theo: **yêu cầu → nguyên nhân → sửa → kiểm thử**.
- [ ] Luyện trả lời trung thực câu “Em chưa làm LoRaWAN trên AOSP, vậy tại sao anh nên tuyển em?”

---

## 5. Hai phần giới thiệu nên luyện nói

### 5.1. Giới thiệu dự án LoRa Mesh (khoảng 90 giây)

> Khi còn là sinh viên, em tham gia phát triển prototype cảnh báo cháy bằng LoRa Mesh, sử dụng ESP32 và transceiver Semtech SX1276/SX1278. Mục tiêu là các node cảm biến có thể gửi dữ liệu về gateway, kể cả khi cần truyền qua node trung gian. Em tập trung nghiên cứu giải pháp mesh, lựa chọn RadioHead RH_RF95/RHMesh, phát triển firmware theo các module như đọc cảm biến, LoRa transport, relay, alarm và Wi-Fi/MQTT. Em bring-up radio qua SPI, cấu hình SF7, BW 125 kHz, CR 4/5, công suất 10 dBm ở tần số 433 MHz dùng cho prototype, đồng thời theo dõi RSSI để debug. Phần mạng sử dụng RHMesh để tìm route và truyền nhiều hop. Đây là LoRa Mesh, chưa phải LoRaWAN, nhưng dự án giúp em hiểu phần cứng Semtech, LoRa PHY và xử lý truyền nhận ở firmware.

### 5.2. Kết nối kinh nghiệm hiện tại với JD (khoảng 60 giây)

> Hiện tại em làm Embedded Software Engineer, chủ yếu với firmware OpenWrt/prplOS, kernel integration, middleware và networking. Em đã xử lý các lỗi CDRouter, ví dụ DNS over TLS và ánh xạ cổng LAN trong Device Tree, đồng thời nghiên cứu tích hợp FULLCONENAT. Trước đó em có dự án LoRa Mesh trên ESP32 với chip Semtech. Vì vậy em muốn phát triển theo hướng kết hợp hai mảng này: bring-up LoRa trên Linux, tích hợp protocol stack và tạo giao diện cho ứng dụng. Em chưa trực tiếp phát triển LoRaWAN MAC hoặc AIDL HAL trên AOSP, nhưng đã có nền tảng Embedded Linux, C/C++, SPI, giao tiếp không dây và debug nhiều lớp để tiếp cận công việc.

---

## 6. Mock Interview — 15 câu trọng tâm theo JD

**LoRa / LoRaWAN**

1. LoRa, LoRaWAN và RHMesh khác nhau thế nào?
2. SF/BW/CR ảnh hưởng gì đến data rate, airtime, độ nhạy và độ tin cậy?
3. SX1276 giao tiếp ESP32 qua SPI như thế nào? Cần debug tín hiệu nào?
4. RHMesh tìm route và truyền nhiều hop thế nào? ACK từng hop có bảo đảm tới sink không?
5. OTAA join gồm các bước nào? Khóa và frame counter dùng làm gì?
6. Class A/B/C khác nhau thế nào? Chọn class cho xe đang sleep ra sao?
7. ADR là gì? Khi nào có lợi hoặc không phù hợp?

**Linux / Driver**

8. Mang SX1276 từ ESP32 sang Linux: em triển khai theo thứ tự nào?
9. Device Tree, `spi_driver`, `probe()`, IRQ và GPIO phối hợp ra sao?
10. Khi `spi_sync()` lỗi hoặc đọc sai register, em debug ở đâu?
11. Tại sao cần `ioctl()` và `poll()` cho một character device?

**AOSP / EV**

12. Thiết kế daemon/AIDL HAL cho ứng dụng Android gửi payload LoRa thế nào?
13. Xử lý hàng đợi khi mất sóng, timeout, nhiều request đồng thời như thế nào?
14. Thiết kế remote wake-up khi SoC suspend hoặc power-off ra sao?

**Kinh nghiệm**

15. Kể một lỗi thực tế em tự điều tra, sửa source/firmware và kiểm thử lại; phân biệt phần tự viết và phần dùng mã nguồn mở.

**Cách luyện:** Trả lời mỗi câu 60–120 giây → yêu cầu interviewer hỏi sâu 1 câu → tự chấm: (a) đúng kỹ thuật, (b) có ví dụ, (c) trung thực, (d) trả lời có cấu trúc.

---

## 7. Các bẫy dễ bị hỏi xoáy

| Tránh nói | Nên nói |
|---|---|
| “Em đã triển khai LoRaWAN” | “Em đã làm LoRa Mesh bằng RHMesh; đang ôn LoRaWAN MAC để chuyển nền tảng.” |
| “LoRa dùng Mesh mặc định” | “LoRa là PHY; Mesh là tầng giao thức/định tuyến bổ sung.” |
| “ACK của RHMesh nghĩa là gateway đã nhận” | “ACK từng hop không tự động bảo đảm end-to-end delivery.” |
| “Cứ tăng SF là tốt hơn” | “SF tăng có thể cải thiện độ nhạy nhưng tăng airtime và giảm tốc độ.” |
| “AIDL là driver” | “AIDL định nghĩa interface IPC; driver/radio HAL xử lý phần cứng ở lớp dưới.” |
| “Daemon Android tự đánh thức xe khi SoC tắt” | “Cần thành phần được cấp nguồn để nhận radio/wake event và đánh thức SoC.” |
| “Tích hợp FULLCONENAT làm giảm conntrack” | “FULLCONENAT thay đổi NAT mapping/filtering; conntrack vẫn theo dõi từng flow.” |

---

## 8. Checklist cuối cùng trước khi vào phỏng vấn

### Kiến thức

- [ ] Phân biệt LoRa / LoRaWAN / LoRa Mesh.
- [ ] Giải thích được SF, BW, CR, RSSI, SNR, CAD và airtime.
- [ ] Nắm được SX1276 SPI, reset, FIFO, TX/RX, DIO IRQ.
- [ ] Nắm luồng OTAA, RX1/RX2, Class A/B/C, ADR, key và frame counter.
- [ ] Hiểu regional frequency rules ở mức nguyên tắc; không mặc định 433 MHz hợp lệ mọi nơi.
- [ ] Nắm cách Linux bind SPI device qua Device Tree và `probe()`.
- [ ] Hiểu character device, `ioctl()`, `poll()` và daemon.
- [ ] Hiểu vai trò AIDL/HAL, Binder, SELinux ở mức hệ thống.

### Kỹ năng kể chuyện kỹ thuật

- [ ] Có bài giới thiệu bản thân 45–60 giây.
- [ ] Kể dự án LoRa Mesh trong 90 giây, nói rõ phần mình làm.
- [ ] Kể một case đã fix CDRouter (DNS over TLS hoặc LAN multiport).
- [ ] Nói rõ phần chỉ nghiên cứu/tích hợp/chưa test production.
- [ ] Sẵn sàng giải thích “tại sao ứng tuyển dù chưa làm LoRaWAN trên AOSP”.

### Ngay trước buổi phỏng vấn (20–30 phút)

- [ ] Xem lại sơ đồ hệ thống LoRa trên Linux và bảng so sánh LoRa/LoRaWAN.
- [ ] Nhắc lại 5 từ khóa: **OTAA – SPI/IRQ – Class A – AIDL – Debugging**.
- [ ] Luyện miệng 2 câu chuyện mạnh nhất từ CV, không cố học thêm chủ đề mới.

---

## 9. Tài liệu tham khảo để tra nhanh (không cần đọc hết)

- Semtech SX1276/77/78/79 datasheet — sơ đồ chân, register, IRQ, LoRa modulation.
- [LoRa Alliance — LoRaWAN](https://lora-alliance.org/) — kiến trúc và thông số giao thức.
- [Semtech LoRaMac-node (mã nguồn tham khảo)](https://github.com/Lora-net/LoRaMac-node) — nghiên cứu cấu trúc MAC (repository đã archive, không nên coi là mặc định cho thiết kế mới).
- [Semtech SWL2001 / LoRa Basics Modem](https://github.com/Lora-net/SWL2001) — nghiên cứu stack và hướng phát triển mới.
- [Linux kernel SPI documentation](https://docs.kernel.org/spi/spi-summary.html) — SPI device/driver.
- [Android AIDL HAL](https://source.android.com/docs/core/architecture/aidl/aidl-hals) — thiết kế interface trên AOSP.
- [RadioHead documentation](https://www.airspayce.com/mikem/arduino/RadioHead/) — RH_RF95, RHMesh.

---

**Nguyên tắc ôn cấp tốc:** Trong 3 ngày, ưu tiên **hiểu nguyên lý + trình bày được cách làm + trả lời câu hỏi phản biện**. Không đặt mục tiêu tự viết hoàn chỉnh LoRaWAN stack hoặc AOSP HAL trong thời gian này. Phỏng vấn bằng tiếng Việt, giữ các từ khóa kỹ thuật chuẩn như SPI, IRQ, MAC, OTAA, Device Tree, AIDL và Conntrack.
