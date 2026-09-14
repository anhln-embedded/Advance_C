import os
import glob
import re

replacements = {
    "Bai 03. He thong xung nhip RCC va Clock Tree.md": [
        (
            r"```[\s\S]*?CÁC NGUỒN XUNG NHỊP[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai03_clock_tree.svg" width="920" alt="Sơ đồ cây xung nhịp STM32F103 Clock Tree">\n</p>'
        )
    ],
    "Bai 04. Ngat ngoai EXTI va Bo dieu khien ngat NVIC.md": [
        (
            r"```[\s\S]*?ARM CORTEX-M3 CORE[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai04_exti_nvic_routing.svg" width="950" alt="Kiến trúc điều hướng ngắt ngoại vi STM32: EXTI & NVIC">\n</p>'
        )
    ],
    "Bai 05. SysTick Timer va Dinh thoi khong chan Non-blocking.md": [
        (
            r"```[\s\S]*?Xung nhịp \(HCLK 72MHz[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai05_systick_timer.svg" width="900" alt="Kiến trúc đồng hồ định thời cốt lõi SysTick Timer">\n</p>'
        )
    ],
    "Bai 06. General Purpose Timer TIM2 - TIM4.md": [
        (
            r"```[\s\S]*?TIMERS TRÊN STM32F103[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai06_timer_architecture.svg" width="940" alt="Kiến trúc ngoại vi General Purpose Timer TIM2 - TIM5">\n</p>'
        ),
        (
            r"```[\s\S]*?Xung nhịp ngoại vi TIMx_CLK[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai06_timer_timebase.svg" width="900" alt="Nguyên lý hoạt động khối Time-Base Generator Timer">\n</p>'
        )
    ],
    "Bai 07. Dieu xung PWM Pulse Width Modulation.md": [
        (
            r"```[\s\S]*?3\.3V\s+\+-------+[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai07_pwm_duty_cycle.svg" width="920" alt="Dạng sóng điều chế độ rộng xung PWM và Duty Cycle">\n</p>'
        ),
        (
            r"```[\s\S]*?Giá trị đếm[\s\S]*?ARR\s+┌[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai07_pwm_principle.svg" width="900" alt="Nguyên lý so sánh bộ đếm CNT và CCR tạo xung PWM">\n</p>'
        ),
        (
            r"```[\s\S]*?SERVO SG90 TIMING[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai07_servo_sg90_timing.svg" width="920" alt="Giản đồ xung điều khiển động cơ RC Servo SG90">\n</p>'
        )
    ],
    "Bai 10. Watchdog Timers IWDG va WWDG.md": [
        (
            r"```[\s\S]*?Nguồn xung LSI độc lập[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai10_watchdog_comparison.svg" width="940" alt="So sánh bộ giám sát hệ thống STM32: IWDG vs WWDG">\n</p>'
        )
    ],
    "Bai 11. ADC 12-bit Co ban Polling va Ngat EOC.md": [
        (
            r"```[\s\S]*?Điện Áp Tương Tự \(0V - 3\.3V\)[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai11_adc_sar_structure.svg" width="940" alt="Kiến trúc bộ chuyển đổi ADC 12-bit SAR STM32F103">\n</p>'
        )
    ],
    "Bai 13. USART UART Co ban va Cau hinh printf.md": [
        (
            r"```[\s\S]*?Điện áp nghỉ \(Idle = 3\.3V[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai13_uart_frame_format.svg" width="850" alt="Cấu trúc khung truyền dữ liệu UART Frame Format">\n</p>'
        )
    ],
    "Bai 14. UART Nang cao Bo dem vong Ring Buffer va Parser CLI.md": [
        (
            r"```[\s\S]*?\+-------+-------+-------+-------+[\s\S]*?Dữ liệu đã đọc[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai14_ring_buffer_fifo.svg" width="920" alt="Cơ chế bộ đệm vòng tròn Circular Ring Buffer FIFO">\n</p>'
        )
    ],
    "Bai 15. Giao tiep I2C Master Phan cung va OLED SSD1306 EEPROM.md": [
        (
            r"```[\s\S]*?\+3\.3V ──────────────┬──────────────┬───────────────[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai15_i2c_bus_topology.svg" width="900" alt="Sơ đồ mạch và cấu hình chân Bus I2C Open-Drain">\n</p>'
        ),
        (
            r"```[\s\S]*?\[ Bật START \] ──> Chờ cờ SB[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai15_i2c_transfer_sequence.svg" width="920" alt="Trình tự truyền dữ liệu I2C Master phần cứng theo sự kiện EVx">\n</p>'
        )
    ],
    "Bai 16. Giao tiep SPI Master Phan cung va Flash W25Q64 TFT LCD.md": [
        (
            r"```[\s\S]*?STM32F103 \(Master\)[\s\S]*?W25Q64[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai16_spi_topology.svg" width="900" alt="Sơ đồ kết nối Bus SPI 4 dây Master và Slave">\n</p>'
        )
    ],
    "Bai 17. DMA Controller Chuyen sau UART va ADC.md": [
        (
            r"```[\s\S]*?\+-------------------+\s+\|\s+ARM Cortex-M3[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai17_dma_architecture.svg" width="900" alt="Kiến trúc bộ điều khiển Direct Memory Access (DMA Controller)">\n</p>'
        )
    ],
    "Bai 18. Che do tiet kiem nang luong Low Power Modes.md": [
        (
            r"```[\s\S]*?Dòng tiêu thụ[\s\S]*?30mA ───┐[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai18_low_power_modes.svg" width="920" alt="So sánh các chế độ tiết kiệm năng lượng STM32 Low Power Modes">\n</p>'
        )
    ],
    "Bai 20. Nhap mon FreeRTOS tren STM32 voi SPL va CMSIS.md": [
        (
            r"```[\s\S]*?BỘ LẬP LỊCH \(FREERTOS SCHEDULER\)[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai20_freertos_architecture.svg" width="900" alt="Kiến trúc bộ lập lịch hệ điều hành thời gian thực FreeRTOS">\n</p>'
        )
    ],
    "Bai 21. FreeRTOS Dong bo hoa va Giao tiep da Task.md": [
        (
            r"```[\s\S]*?Task Gửi \(Sender\)[\s\S]*?Ghi vào đuôi Queue[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai21_freertos_sync.svg" width="940" alt="Cơ chế đồng bộ hóa và truyền dữ liệu đa nhiệm FreeRTOS">\n</p>'
        )
    ],
    "Bai 23. Mang truyen thong cong nghiep CAN Bus.md": [
        (
            r"```[\s\S]*?ĐƯỜNG TRUYỀN DÂY XOẮN[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai23_can_bus_topology.svg" width="920" alt="Cấu trúc mạng truyền thông công nghiệp CAN Bus và Transceiver">\n</p>'
        ),
        (
            r"```[\s\S]*?SOF\s+│\s+Identifier \(11 bits\)[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai23_can_frame_format.svg" width="940" alt="Cấu trúc khung dữ liệu chuẩn CAN 2.0A Standard Data Frame">\n</p>'
        )
    ],
    "Bai 25. Thiet ke Custom ISP Bootloader va Cap nhat Firmware tu xa.md": [
        (
            r"```[\s\S]*?Địa chỉ Flash\s+Vùng Nhớ[\s\S]*?0x0800 0000[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai25_bootloader_flash_layout.svg" width="900" alt="Phân vùng bộ nhớ Flash STM32 cho Bootloader và Ứng dụng">\n</p>'
        ),
        (
            r"```[\s\S]*?Địa chỉ bắt đầu của Application \(0x0800 3000\)[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai25_vector_table_jump.svg" width="920" alt="Quy trình chuyển tiếp thực thi từ Bootloader sang Application">\n</p>'
        )
    ],
    "Bai 26. Ky thuat Debugging chuyen sau va Xu ly su co HardFault.md": [
        (
            r"```[\s\S]*?Con trỏ ngăn xếp \(MSP hoặc PSP\)[\s\S]*?```",
            '<p align="center">\n  <img src="images/bai26_hardfault_stack_frame.svg" width="900" alt="Cấu trúc khung ngăn xếp Stack Frame khi xảy ra ngắt HardFault">\n</p>'
        )
    ]
}

for fname, pattern_list in replacements.items():
    if not os.path.exists(fname):
        print(f"File not found: {fname}")
        continue
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    for pat, rep in pattern_list:
        if re.search(pat, content):
            content = re.sub(pat, rep, content, count=1)
            modified = True
        else:
            print(f"Pattern not found in {fname}: {pat[:50]}")

    if modified:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated: {fname}")

print("REPLACEMENT COMPLETED!")
