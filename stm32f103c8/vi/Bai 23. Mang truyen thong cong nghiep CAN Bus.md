# BÀI 23: MẠNG TRUYỀN THÔNG CÔNG NGHIỆP CAN BUS 2.0B

Chào mừng bạn đến với bài học thứ 23 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Nếu như UART chỉ truyền giữa 2 điểm (Point-to-Point) và I2C/SPI chỉ chạy được trên bo mạch cự ly ngắn (vài chục centimet), thì **CAN Bus (Controller Area Network)** là chuẩn truyền thông thống trị tuyệt đối trong ngành **Công nghiệp Ô tô (Automotive), Hàng không vũ trụ và Tự động hóa nhà máy**.

Được phát minh bởi tập đoàn Robert Bosch, CAN Bus nổi tiếng với khả năng **chống nhiễu điện từ cực mạnh**, truyền xa hàng kilomet, tự động kiểm tra lỗi và cơ chế phân xử đường truyền không phá hủy (**Non-destructive Bitwise Arbitration**). Bài học này sẽ giúp bạn làm chủ khối **bxCAN** của STM32F103, cấu hình bộ lọc tin nhắn phần cứng (**Filter Banks**) và truyền nhận dữ liệu theo chuẩn công nghiệp **CAN 2.0A / 2.0B**.

---

## 1. Nguyên Lý Điện Tử Và Tín Hiệu Vi Sai CAN Bus

Mạng CAN Bus sử dụng một cặp dây xoắn vi sai gồm **CAN_H (CAN High)** và **CAN_L (CAN Low)**:

<p align="center">
  <img src="images/bai23_can_bus_topology.svg" width="920" alt="Cấu trúc mạng truyền thông công nghiệp CAN Bus và Transceiver">
</p>

### 1.1 Hai mức logic vi sai:
1. **Mức Recessive (Bit logic `1` - Mức lặn)**:
   - Cả hai dây CAN_H và CAN_L đều ở mức điện áp xấp xỉ **2.5V**.
   - Điện áp vi sai: V_diff = V_CAN_H - V_CAN_L ≈ 0V.
2. **Mức Dominant (Bit logic `0` - Mức trội)**:
   - CAN_H được kéo lên **3.5V**, CAN_L bị kéo tụt xuống **1.5V**.
   - Điện áp vi sai: V_diff = 3.5V - 1.5V = 2.0V.

> [!IMPORTANT]
> **Quy tắc vàng của CAN Bus: DOMINANT (0) LUÔN ĐÈ BẸP RECESSIVE (1)!**
> Nếu Node A phát bit `1` (Recessive) trong khi Node B phát bit `0` (Dominant) trên cùng đường dây, điện áp vi sai trên bus sẽ ngay lập tức chuyển thành mức Dominant (2V). Nhờ tính chất này, CAN Bus thực hiện được cơ chế trọng tài phân xử thứ tự ưu tiên mà không làm hỏng gói tin của bên thắng cuộc!

### 1.2 Yêu cầu điện trở đầu cuối (Termination Resistor 120Ω):
- Ở hai đầu xa nhất của đường trục mạng CAN Bus, **bắt buộc phải có 2 điện trở 120Ω mắc song song giữa CAN_H và CAN_L**.
- Tổng trở đo được giữa CAN_H và CAN_L khi ngắt nguồn phải đúng bằng **60Ω**. Điện trở này có nhiệm vụ triệt tiêu sóng phản xạ cao tần trên đường truyền.

---

## 2. Cấu Trúc Khung Tin CAN (CAN Data Frame)

Khác với UART hay I2C truyền nhận dựa trên "địa chỉ thiết bị", **CAN Bus hoàn toàn không có khái niệm địa chỉ Node**. Thay vào đó, CAN Bus truyền nhận dựa trên **ID của nội dung thông điệp (Message Identifier)**:

<p align="center">
  <img src="images/bai23_can_frame_format.svg" width="940" alt="Cấu trúc khung dữ liệu chuẩn CAN 2.0A Standard Data Frame">
</p>

- **ID (Message Identifier)**:
  - Chuẩn **CAN 2.0A**: ID độ dài **11-bit** (Giá trị từ `0x000` đến `0x7FF`).
  - Chuẩn **CAN 2.0B**: ID mở rộng **29-bit** (Giá trị từ `0` đến 2^{29}-1).
  - **Quy tắc ưu tiên**: **ID có giá trị số càng nhỏ thì mức độ ưu tiên càng cao** (ví dụ ID `0x100` ưu tiên hơn ID `0x200`).
- **DLC (Data Length Code - 4 bit)**: Số lượng byte dữ liệu truyền thực tế (từ 0 đến 8 bytes).
- **Data Field**: Tối đa **8 bytes** dữ liệu trong một khung truyền.

---

## 3. Khối bxCAN Phần Cứng Trên STM32F103

Khối **bxCAN (Basic Extended CAN)** của STM32F103C8T6 kết nối trên bus **APB1 (36MHz)**:
- Hỗ trợ đầy đủ cả 2 chuẩn **CAN 2.0A và CAN 2.0B**.
- Tốc độ truyền tối đa lên tới **1 Mbps (1 Mbit/s)**.
- **3 Hộp thư truyền (Transmit Mailboxes: Mailbox 0, 1, 2)**: Giúp truyền dữ liệu không bị nghẽn.
- **2 Hàng đợi nhận (Receive FIFOs: FIFO 0 và FIFO 1)**, mỗi FIFO chứa được 3 khung tin hoàn chỉnh.
- **14 Bộ lọc tin nhắn phần cứng (Filter Banks 0 đến 13)**.

---

## 4. Bộ Lọc Tin Nhắn Phần Cứng (CAN Filter Banks)

Mỗi giây có thể có hàng nghìn thông điệp chạy trên đường bus CAN. Nếu thông điệp nào CPU cũng phải nhảy vào đọc, CPU sẽ bị quá tải.
Khối Filter Banks của STM32 cho phép lọc ID **ngay từ cổng phần cứng**:
1. **Chế độ Mặt nạ (Id/Mask Mode)**: Định nghĩa một ID mong muốn và một Mặt nạ Mask. Chỉ những gói tin có các bit khớp với mặt nạ mới được lọt vào FIFO của CPU.
2. **Chế độ Danh sách (Identifier List Mode)**: Liệt kê chính xác danh sách các ID được phép nhận. Mọi ID khác đều bị phần cứng vứt bỏ thẳng tay!

---

## 5. Triển Khai Mã Nguồn Thực Chiến

### Kịch bản thực hành:
- Cấu hình CAN1 hoạt động ở chế độ **Loopback Mode phần mềm** (cho phép tự gửi và tự nhận nội bộ để kiểm tra mã nguồn mà không cần gắn IC Transceiver ngoài TJA1050).
- Sau khi kiểm tra tốt, chuyển sang chế độ **Normal Mode** nối với module thu phát TJA1050 (CAN_TX nối `PA12`, CAN_RX nối `PA11`).
- Tốc độ truyền: **500 kbps** (Tần số chuẩn của mạng động cơ ô tô OBD-II).
- Gửi gói tin Standard ID `0x123` chứa 8 byte dữ liệu cảm biến.
- Khi nhận được phản hồi, đảo trạng thái LED **PC13**.

---

### PHƯƠNG PHÁP 1: BARE-METAL REGISTER & CMSIS

File: `can_bus.c`

```c
#include "stm32f10x.h"

void CAN1_Init_Register(void)
{
    // 1. Enable clocks for GPIOA and CAN1 on APB1 bus
    RCC->APB2ENR |= (1 << 2);  // IOPAEN = 1
    RCC->APB1ENR |= (1 << 25); // CAN1EN = 1

    // 2. Configure PA11 (CAN_RX): Input with Pull-Up
    GPIOA->CRH &= ~(0x0F << 12);
    GPIOA->CRH |= (0x08 << 12); // Input Pull-up
    GPIOA->ODR |= (1 << 11);

    // 3. Configure PA12 (CAN_TX): AF Output Push-Pull 50MHz
    GPIOA->CRH &= ~(0x0F << 16);
    GPIOA->CRH |= (0x0B << 16); // AF_PP 50MHz

    // 4. REQUEST INITIALIZATION MODE (INRQ = 1)
    CAN1->MCR |= (1 << 0); // INRQ = 1 (Initialization Request)
    CAN1->MCR &= ~(1 << 1); // Exit Sleep Mode (SLEEP = 0)
    while (!(CAN1->MSR & (1 << 0))); // Wait until INAK flag = 1

    // 5. Configure features in CAN_MCR:
    // - Automatic retransmission on error (NART = 0)
    // - Automatic bus wakeup enabled (AWUM = 1)
    CAN1->MCR |= (1 << 6); // ABOM = 1 (Automatic Bus-Off Management)

    // 6. CONFIGURE 500kbps BIT TIMING IN CAN_BTR (APB1 Clock = 36MHz)
    // Baud rate = 36MHz / (BRP * (1 + TS1 + TS2))
    // Settings: Prescaler (BRP) = 4, Time Segment 1 (TS1) = 12, Time Segment 2 (TS2) = 5
    // Total time quanta (tq) = 1 + 12 + 5 = 18 tq
    // Baudrate = 36,000,000 / (4 * 18) = 500,000 bps = 500 kbps!
    CAN1->BTR = 0;
    CAN1->BTR |= (4 - 1)  << 0;   // BRP[9:0] = 3
    CAN1->BTR |= (12 - 1) << 16;  // TS1[3:0] = 11
    CAN1->BTR |= (5 - 1)  << 20;  // TS2[2:0] = 4
    CAN1->BTR |= (1 - 1)  << 24;  // SJW[1:0] = 0

    // TEST MODE: Enable Loopback mode for internal loopback without wires
    // (Omit this line when using physical TJA1050 transceiver)
    CAN1->BTR |= (1 << 30); // LBKM = 1 (Loopback Mode)

    // 7. EXIT INITIALIZATION MODE, START NORMAL OPERATION
    CAN1->MCR &= ~(1 << 0); // INRQ = 0
    while (CAN1->MSR & (1 << 0)); // Wait for INAK = 0

    // 8. CONFIGURE FILTER BANK 0 TO ACCEPT ALL IDENTIFIERS
    CAN1->FMR |= (1 << 0);  // FINIT = 1 (Enter filter initialization)
    CAN1->FA1R &= ~(1 << 0); // Deactivate Filter 0 for modification

    CAN1->FS1R |= (1 << 0); // 32-bit scale configuration (1 Single 32-bit filter)
    CAN1->FM1R &= ~(1 << 0); // Identifier Mask Mode
    CAN1->sFilterRegister[0].FR1 = 0x00000000; // ID = 0
    CAN1->sFilterRegister[0].FR2 = 0x00000000; // Mask = 0 (Accept all IDs)
    CAN1->FFA1R &= ~(1 << 0); // Assign to FIFO 0

    CAN1->FA1R |= (1 << 0);  // Reactivate Filter 0
    CAN1->FMR &= ~(1 << 0);  // FINIT = 0 (Exit filter initialization)
}

// Transmit CAN 2.0A frame (11-bit Standard ID)
uint8_t CAN1_SendPacket(uint16_t std_id, uint8_t *data, uint8_t len)
{
    // Check if Transmit Mailbox 0 is empty (TME0 = 1 in TSR)
    if (!(CAN1->TSR & (1 << 26)))
    {
        return 0; // Mailbox busy
    }

    // 1. Configure 11-bit Standard ID in TIR (Bits 31-21)
    CAN1->sTxMailBox[0].TIR = 0;
    CAN1->sTxMailBox[0].TIR |= (uint32_t)(std_id << 21); // Standard ID
    CAN1->sTxMailBox[0].TIR &= ~(1 << 1); // RTR = 0 (Data Frame)
    CAN1->sTxMailBox[0].TIR &= ~(1 << 2); // IDE = 0 (Standard ID 11-bit)

    // 2. Set Data Length Code (DLC)
    CAN1->sTxMailBox[0].TDTR &= ~0x0F;
    CAN1->sTxMailBox[0].TDTR |= (len & 0x0F);

    // 3. Load up to 8 data bytes into TDLR and TDHR registers
    CAN1->sTxMailBox[0].TDLR = ((uint32_t)data[3] << 24) |
                               ((uint32_t)data[2] << 16) |
                               ((uint32_t)data[1] << 8)  |
                               ((uint32_t)data[0]);

    CAN1->sTxMailBox[0].TDHR = ((uint32_t)data[7] << 24) |
                               ((uint32_t)data[6] << 16) |
                               ((uint32_t)data[5] << 8)  |
                               ((uint32_t)data[4]);

    // 4. Trigger transmission by setting TXRQ bit in TIR
    CAN1->sTxMailBox[0].TIR |= (1 << 0); // TXRQ = 1

    return 1; // Message queued in mailbox successfully
}

// Receive frame from FIFO 0
uint8_t CAN1_ReceivePacket(uint16_t *std_id, uint8_t *data, uint8_t *len)
{
    // Check if FIFO 0 contains messages (Bits 1-0 in RF0R > 0)
    if ((CAN1->RF0R & 0x03) == 0)
    {
        return 0; // FIFO empty
    }

    // Read ID
    *std_id = (uint16_t)(CAN1->sFIFOMailBox[0].RIR >> 21);

    // Read data length
    *len = (uint8_t)(CAN1->sFIFOMailBox[0].RDTR & 0x0F);

    // Read 8 data bytes
    uint32_t low_data  = CAN1->sFIFOMailBox[0].RDLR;
    uint32_t high_data = CAN1->sFIFOMailBox[0].RDHR;

    data[0] = (uint8_t)(low_data);
    data[1] = (uint8_t)(low_data >> 8);
    data[2] = (uint8_t)(low_data >> 16);
    data[3] = (uint8_t)(low_data >> 24);

    data[4] = (uint8_t)(high_data);
    data[5] = (uint8_t)(high_data >> 8);
    data[6] = (uint8_t)(high_data >> 16);
    data[7] = (uint8_t)(high_data >> 24);

    // Release FIFO 0 output mailbox by setting RFOM0 = 1
    CAN1->RF0R |= (1 << 5);

    return 1;
}

int main(void)
{
    // LED PC13
    RCC->APB2ENR |= (1 << 4);
    GPIOC->CRH &= ~(0x0F << 20);
    GPIOC->CRH |= (0x02 << 20);

    CAN1_Init_Register();

    uint8_t tx_data[8] = { 0x01, 0x02, 0x03, 0x04, 0xAA, 0xBB, 0xCC, 0xDD };
    uint8_t rx_data[8];
    uint16_t rx_id;
    uint8_t rx_len;

    while (1)
    {
        // Transmit CAN message with ID 0x123
        CAN1_SendPacket(0x123, tx_data, 8);

        // Receive message in Loopback mode
        if (CAN1_ReceivePacket(&rx_id, rx_data, &rx_len))
        {
            if (rx_id == 0x123)
            {
                GPIOC->ODR ^= (1 << 13); // Toggle LED PC13 indicating successful reception!
            }
        }

        for (volatile int i = 0; i < 2000000; i++);
    }
}
```

---

## 6. Xung Đột Phần Cứng Sống Còn Giữa USB Và CAN Trên STM32F103

> [!CAUTION]
> **Không thể sử dụng đồng thời USB và CAN trên cùng một vi điều khiển STM32F103:**
> Theo tài liệu Reference Manual RM0008 mục USB/CAN Interface:
> Khối ngoại vi **USB Device** và khối ngoại vi **bxCAN** trên STM32F103 **dùng chung một vùng nhớ đệm Packet Buffer RAM dung lượng 512 bytes (SRAM 0x4000 6000)**!
> - Khi bạn bật clock cho USB, khối CAN sẽ bị vô hiệu hóa.
> - Khi bạn bật clock cho CAN, khối USB sẽ bị vô hiệu hóa.
> Bạn **không thể chạy đồng thời cả cổng USB và cổng CAN cùng một lúc** trên STM32F103C8T6! (Nếu muốn dùng cả hai, bạn phải nâng cấp lên dòng STM32F105/F107 Connectivity Line hoặc chuyển sang dòng STM32F4).

---

## 7. Bài Tập Thực Hành

1. **Bài tập 1 (Giao tiếp giữa 2 bo mạch Blue Pill qua CAN Bus)**: Nối 2 bo mạch Blue Pill qua 2 module TJA1050 (CAN_H nối CAN_H, CAN_L nối CAN_L kèm trở 120Ω). Bấm nút trên bo mạch 1 thì đèn LED trên bo mạch 2 chớp tắt.
2. **Bài tập 2 (Bộ lọc ID khắt khe)**: Cấu hình Filter Bank 1 ở chế độ Danh sách (List Mode) chỉ cho phép nhận duy nhất 2 ID là `0x321` và `0x555`. Thử gửi các ID khác từ mạng và chứng minh CPU không hề bị làm phiền.
3. **Bài tập 3 (Giao thức chẩn đoán ô tô OBD-II)**: Tìm hiểu cấu trúc bản tin OBD-II tiêu chuẩn (ID phát lệnh `0x7DF`, ID phản hồi từ động cơ `0x7E8`). Viết hàm đóng gói truy vấn tốc độ động cơ (PID `0x0C`) và nhiệt độ nước làm mát (PID `0x05`).
