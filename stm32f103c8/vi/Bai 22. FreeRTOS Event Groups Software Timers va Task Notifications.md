# BÀI 22: EVENT GROUPS, SOFTWARE TIMERS VÀ TASK NOTIFICATIONS

Chào mừng bạn đến với bài học thứ 22 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Ở bài 21, bạn đã làm chủ Queue, Semaphore và Mutex. Tuy nhiên, việc tạo nhiều Queue và Semaphore sẽ tiêu tốn đáng kể bộ nhớ RAM hạn hẹp (20KB) của vi điều khiển STM32F103C8T6.

Trong bài học này, chúng ta sẽ mở khóa 3 tính năng cao cấp và tối ưu nhất của FreeRTOS:
1. **Event Groups**: Đồng bộ hóa đa điều kiện (chờ nhiều sự kiện xảy ra đồng thời theo logic AND / OR).
2. **Software Timers**: Tạo hàng loạt bộ định thời phần mềm chính xác mà không tốn một Timer phần cứng nào.
3. **Task Notifications ("Vũ khí bí mật")**: Kỹ thuật truyền tin trực tiếp giữa các Task siêu nhẹ, **nhanh hơn Semaphore 45% và tiết kiệm 100% dung lượng RAM**!

---

## 1. Event Groups: Đồng Bộ Hóa Đa Điều Kiện

Nếu một Task chỉ có thể tiếp tục thực thi khi **tất cả 3 điều kiện đều thỏa mãn**:
- Điều kiện A: Cảm biến đã khởi động xong.
- Điều kiện B: Đã kết nối mạng thành công.
- Điều kiện C: Người dùng đã bấm nút Start.

Nếu dùng Semaphore thông thường, bạn phải tạo 3 Semaphore riêng biệt và kiểm tra tuần tự rất phức tạp. **Event Group** giải quyết bài toán này chỉ với một biến 24-bit duy nhất:

<p align="center">
  <img src="images/bai22_freertos_advanced_sync.svg" width="940" alt="Các cơ chế đồng bộ nâng cao trong FreeRTOS: Event Groups và Task Notifications">
</p>

### 1.1 Hai chế độ chờ cờ sự kiện:
- **Chờ bất kỳ cờ nào bật (Wait for ANY - Logic OR)**: Chỉ cần 1 trong các sự kiện xảy ra là Task thức dậy ngay.
- **Chờ TẤT CẢ các cờ cùng bật (Wait for ALL - Logic AND)**: Phải hội tụ đầy đủ tất cả các cờ bit chỉ định thì Task mới được phép chạy.

---

## 2. Software Timers: Bộ Định Thời Phần Mềm Không Tốn Phần Cứng

STM32F103 chỉ có 4 Timer phần cứng. Nếu dự án của bạn cần 10 bộ định thời độc lập (chớp tắt 3 LED ở các tần số khác nhau, đọc cảm biến mỗi 2 giây, gửi bản tin nhịp tim mỗi 10 giây...), bạn sẽ nhanh chóng hết tài nguyên phần cứng.

**Software Timers** của FreeRTOS cho phép bạn tạo ra không giới hạn số lượng Timer chạy hoàn toàn bằng phần mềm:
- Được điều phối ngầm bởi **Timer Service Daemon Task** của FreeRTOS.
- **Hai loại Timer**:
  1. **One-shot Timer**: Đếm đúng một khoảng thời gian quy định, gọi hàm Callback thực thi một lần rồi dừng hẳn.
  2. **Auto-reload Timer**: Đếm hết thời gian quy định, gọi hàm Callback và tự động nạp lại chu kỳ để chạy lặp đi lặp lại vô tận.

---

## 3. Task Notifications: Cơ Chế Truyền Tin Siêu Tốc Zero-RAM

Trong các phiên bản FreeRTOS hiện đại, mỗi Task khi được tạo ra đều có sẵn một mảng số nguyên 32-bit tích hợp ngay bên trong cấu trúc quản lý Task (**Task Control Block - TCB**).
Bạn có thể gửi tín hiệu trực tiếp tới biến này của một Task mà **không cần phải cấp phát thêm bất kỳ đối tượng Semaphore hay Queue nào trong RAM**!

<p align="center">
  <img src="images/bai22_task_notifications.svg" width="940" alt="Cơ chế hoạt động của Task Notifications trong FreeRTOS">
</p>

### 3.1 Ưu điểm vượt trội của Task Notifications:
- **Tốc độ nhanh hơn 45%**: Do không cần đi qua các tầng logic kiểm tra hàng đợi phức tạp.
- **Tiết kiệm RAM tuyệt đối (Zero RAM overhead)**: Không tốn thêm byte RAM nào vì vùng nhớ đã nằm sẵn trong TCB của Task.
- Thay thế hoàn hảo cho **Binary Semaphore** và **Counting Semaphore** trong 90% các ứng dụng thực tế.

---

## 4. Triển Khai Mã Nguồn Thực Chiến

### Kịch bản thực hành:
1. **Event Group**: Task điều khiển chính `vTaskSystemManager` chờ đồng thời 2 cờ bit:
   - Bit 0 (`BIT_SENSOR_READY`): Do Task cảm biến bật sau 1 giây.
   - Bit 1 (`BIT_FLASH_READY`): Do Task kiểm tra bộ nhớ bật sau 2 giây.
   - Khi cả 2 bit cùng bật (`Wait for ALL`), in thông điệp *"All Systems Go!"* ra UART.
2. **Software Timer**: Tạo một Auto-reload Timer chu kỳ **500ms** để chớp tắt đèn LED PC13 tự động mà không cần tốn một Task hay vòng lặp nào!
3. **Task Notifications**: Ngắt ngoài nút bấm PA0 gửi thông báo trực tiếp `xTaskNotifyGiveFromISR` để đánh thức một Task xử lý khẩn cấp.

---

File: `freertos_advanced.c`

```c
#include "stm32f10x.h"
#include <stdio.h>
#include "FreeRTOS.h"
#include "task.h"
#include "event_groups.h"
#include "timers.h"

// Define event bit masks
#define BIT_SENSOR_READY   (1 << 0) // Bit 0
#define BIT_FLASH_READY    (1 << 1) // Bit 1
#define ALL_SYSTEMS_BITS   (BIT_SENSOR_READY | BIT_FLASH_READY)

EventGroupHandle_t xSystemEventGroup;
TimerHandle_t      xLedTimer;
TaskHandle_t       xAlertTaskHandle = NULL;

// 1. Software Timer Callback: Toggle LED PC13 every 500ms
void vLedTimerCallback(TimerHandle_t xTimer)
{
    GPIOC->ODR ^= (1 << 13); // Toggle LED PC13 state
}

// 2. Simulated Sensor Startup Task
void vTaskInitSensor(void *pvParameters)
{
    // Simulate 1-second Sensor initialization delay
    vTaskDelay(pdMS_TO_TICKS(1000));
    printf("[Init] Sensor Hardware is READY!\r\n");

    // Set bit 0 in Event Group
    xEventGroupSetBits(xSystemEventGroup, BIT_SENSOR_READY);

    vTaskDelete(NULL); // Task complete, delete self
}

// 3. Simulated Flash Storage Startup Task
void vTaskInitFlash(void *pvParameters)
{
    // Simulate 2-second Flash self-test delay
    vTaskDelay(pdMS_TO_TICKS(2000));
    printf("[Init] Flash Memory is READY!\r\n");

    // Set bit 1 in Event Group
    xEventGroupSetBits(xSystemEventGroup, BIT_FLASH_READY);

    vTaskDelete(NULL); // Delete current task
}

// 4. System Manager Task: Wait for BOTH conditions (Logic AND)
void vTaskSystemManager(void *pvParameters)
{
    EventBits_t uxBits;

    printf("[Manager] Waiting for all subsystems to initialize...\r\n");

    // =========================================================================
    // WAIT FOR EVENT GROUP: xEventGroupWaitBits()
    // Parameters:
    // 1. Event Group Handle
    // 2. Bits to wait for (ALL_SYSTEMS_BITS)
    // 3. pdTRUE: Clear bits on exit after conditions met
    // 4. pdTRUE: Wait for ALL bits (Logic AND)
    // 5. portMAX_DELAY: Wait indefinitely
    // =========================================================================
    uxBits = xEventGroupWaitBits(xSystemEventGroup,
                                ALL_SYSTEMS_BITS,
                                pdTRUE,
                                pdTRUE,
                                portMAX_DELAY);

    if ((uxBits & ALL_SYSTEMS_BITS) == ALL_SYSTEMS_BITS)
    {
        printf(">>> [SUCCESS] ALL SUBSYSTEMS READY! SYSTEM OPERATIONAL! <<<\r\n");
    }

    while (1)
    {
        // Main system operation runs here
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

// 5. Emergency Task Using TASK NOTIFICATIONS (Zero-RAM)
void vTaskFastAlert(void *pvParameters)
{
    while (1)
    {
        // Wait for Task Notification from ISR
        // pdTRUE: Automatically clear notification count to 0 after read
        if (ulTaskNotifyTake(pdTRUE, portMAX_DELAY) > 0)
        {
            printf(">> [ALERT] Instant Wakeup via Task Notification (Fastest IPC)!\r\n");
        }
    }
}

// External interrupt from PA0 button
void EXTI0_IRQHandler(void)
{
    if (EXTI->PR & (1 << 0))
    {
        EXTI->PR = (1 << 0);

        BaseType_t xHigherPriorityTaskWoken = pdFALSE;

        // SEND NOTIFICATION DIRECTLY TO TASK VIA HANDLE (No Semaphore overhead!)
        if (xAlertTaskHandle != NULL)
        {
            vTaskNotifyGiveFromISR(xAlertTaskHandle, &xHigherPriorityTaskWoken);
        }

        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }
}

int main(void)
{
    // Hardware initialization (LED PC13, UART1, EXTI0)
    // ...

    // 1. CREATE EVENT GROUP
    xSystemEventGroup = xEventGroupCreate();

    // 2. CREATE 500ms AUTO-RELOAD SOFTWARE TIMER (pdTRUE = Auto-reload)
    xLedTimer = xTimerCreate("LedTimer", pdMS_TO_TICKS(500), pdTRUE, (void *)0, vLedTimerCallback);
    
    // Start Software Timer
    xTimerStart(xLedTimer, 0);

    // 3. CREATE TASKS
    xTaskCreate(vTaskInitSensor,     "Init_Sensor", 128, NULL, 2, NULL);
    xTaskCreate(vTaskInitFlash,      "Init_Flash",  128, NULL, 2, NULL);
    xTaskCreate(vTaskSystemManager,  "Sys_Manager", 128, NULL, 1, NULL);
    
    // Save Task Handle for direct notification from ISR
    xTaskCreate(vTaskFastAlert, "Alert_Task", 128, NULL, 3, &xAlertTaskHandle);

    // Start operating system
    vTaskStartScheduler();

    while (1);
}
```

---

## 5. Những Lưu Ý Quan Trọng Khi Dùng Software Timers

> [!CAUTION]
> **Tuyệt đối không được gọi các hàm chặn (Blocking Calls) bên trong Timer Callback:**
> Hàm Callback của Software Timer được thực thi bên trong ngữ cảnh của **Timer Daemon Task (`prvTimerTask`)**.
> Nếu bạn gọi hàm `vTaskDelay()` hoặc chờ một Queue/Semaphore vô thời hạn bên trong hàm Callback của Timer, **toàn bộ hệ thống Software Timers của toàn bộ vi điều khiển sẽ bị đóng băng hoàn toàn**!

---

## 6. Bài Tập Thực Hành

1. **Bài tập 1 (Bộ hẹn giờ tự tắt One-Shot Timer)**: Tạo một One-shot Timer thời lượng **10 giây**. Khi người dùng bấm nút PA0, bật đèn LED và bắt đầu đếm. Sau đúng 10 giây, hàm Callback của Timer sẽ tự động tắt đèn LED (ứng dụng đèn cầu thang thông minh).
2. **Bài tập 2 (Đồng bộ hóa Barrier bằng Event Groups)**: Tạo 3 Task cùng thực hiện tính toán. Cả 3 Task phải hoàn thành xong công đoạn của mình thì mới được phép cùng nhau bước sang công đoạn tiếp theo (kỹ thuật Điểm hẹn Rendezvous / Task Synchronization).
3. **Bài tập 3 (Đo đạc tốc độ Task Notification vs Semaphore)**: Viết một chương trình đo xem mất bao nhiêu chu kỳ xung nhịp để đánh thức một Task bằng `xSemaphoreGive()` so với dùng `xTaskNotifyGive()`.
