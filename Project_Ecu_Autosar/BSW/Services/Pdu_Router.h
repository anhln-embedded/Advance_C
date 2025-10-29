#ifndef PDU_ROUTER_H
#define PDU_ROUTER_H

#include <stdio.h>
#include <string.h>

// Các giao thức truyền thông giả lập
#define PROTOCOL_CAN 0x01
#define PROTOCOL_LIN 0x02
#define PROTOCOL_ETHERNET 0x03

// Cấu trúc mô phỏng một PDU (Protocol Data Unit)
typedef struct {
    int protocol_id;  // Giao thức của PDU (CAN, LIN, Ethernet, ...)
    char data[50];    // Dữ liệu của PDU
    int length;       // Độ dài dữ liệu
}Pdu_Type;
typedef enum{
    INIT_OK,
    INIT_NOT_OK
}Can_status;
// Khởi tạo hệ thống PDU Router
void PduR_Init(void);

// Định tuyến PDU dựa trên giao thức
void PduR_RoutePdu(Pdu_Type* pdu);

//biến toàn cục để cập nhật trạng thái khởi tạo ngoại vi CAN
extern Can_status can_state;

#endif // PDU_ROUTER_H
