# BÀI 21: FREERTOS - ĐỒNG BỘ HÓA VÀ GIAO TIẾP ĐA TASK (QUEUE, SEMAPHORE, MUTEX)

Chào mừng bạn đến với bài học thứ 21 trong chuỗi đào tạo **STM32F103 chuyên sâu**. Ở bài 20, chúng ta đã cho các Task chạy độc lập song song. Nhưng trong một sản phẩm hoàn chỉnh, các Task không thể hoạt động cô lập mà phải liên tục trao đổi dữ liệu với nhau: ví dụ Task đọc cảm biến phải chuyển dữ liệu sang Task xử lý thuật toán, Task thuật toán phải gửi kết quả sang Task hiển thị màn hình và Task truyền thông mạng.

Nếu bạn dùng một biến toàn cục thông thường (`global variable`) để truyền dữ liệu giữa các Task, thảm họa **Tranh chấp dữ liệu (Race Condition)** và **Xung đột tài nguyên chia sẻ** sẽ xuất hiện ngay lập tức. Bài học này sẽ trang bị cho bạn 3 "vũ khí" hạng nặng của FreeRTOS: **Queue (Hàng đợi)**, **Semaphore (Cờ hiệu đồng bộ)** và **Mutex (Khóa loại trừ tương hỗ)** kèm cơ chế chống nghịch đảo mức ưu tiên (**Priority Inheritance**).

---

## 1. Hàng Đợi (Queue): Truyền Dữ Liệu An Toàn Giữa Các Task

**Queue** là cơ chế giao tiếp liên tiến trình (Inter-Task Communication - IPC) quan trọng nhất trong FreeRTOS:
- Hoạt động theo nguyên lý **Vào trước - Ra trước (FIFO - First In First Out)**.
- **An toàn luồng (Thread-safe)**: Nhiều Task có thể cùng ghi vào một Queue hoặc nhiều Task cùng đọc từ một Queue mà không sợ bị xung đột.
- **Truyền theo bản sao (Pass by Value)**: Dữ liệu được copy nguyên vẹn từng byte vào Queue. Nhờ đó, Task gửi có thể tái sử dụng ngay biến của nó mà không làm sai lệch dữ liệu của Task nhận.

<p align="center">
  <img src="images/bai21_freertos_sync.svg" width="940" alt="Cơ chế đồng bộ hóa và truyền dữ liệu đa nhiệm FreeRTOS">
</p>

### 1.1 Cơ chế Blocked Timeout thông minh:
- Nếu Queue đang **rỗng**, Task đọc có thể tự động đi ngủ (Blocked) chờ cho đến khi có dữ liệu được đẩy vào.
- Nếu Queue đang **đầy**, Task ghi có thể tự động đi ngủ chờ cho đến khi có một Task khác lấy bớt dữ liệu ra.

---

## 2. Semaphore: Đồng Bộ Hóa Giữa Ngắt ISR Và Task

**Semaphore** hoạt động như một chiếc vé (Token). Một Task hoặc một ngắt sẽ "Cho vé" (**Give**), và một Task khác sẽ chờ "Lấy vé" (**Take**):

| Khối Thực Thi | Hành Động Gọi Hàm FreeRTOS | Trạng Thái Semaphore | Mục Đích |
| :--- | :--- | :---: | :--- |
| **Hàm phục vụ ngắt (ISR)** | `xSemaphoreGiveFromISR()` | Nhả Token (Give) | Báo hiệu sự kiện phần cứng hoàn tất siêu tốc (vài µs). |
| **Cờ hiệu Binary Semaphore** | Cơ chế hàng đợi Token | Sẵn sàng (Available) | Cầu nối trao đổi trạng thái giữa ngắt và luồng thực thi Task. |
| **Worker Task (Ứng dụng)** | `xSemaphoreTake()` | Lấy Token (Take) | Đang ngủ Blocked lập tức thức dậy nhận cờ và xử lý tính toán nặng. |

### 2.1 Kỹ thuật Trì hoãn xử lý ngắt (Deferred Interrupt Processing):
Một nguyên tắc vàng trong hệ thống nhúng: **Hàm phục vụ ngắt ISR phải chạy cực nhanh (vài micro-giây)**. 
- Khi có sự kiện phần cứng (bấm nút, nhận gói tin), hàm ISR chỉ làm một việc duy nhất là phát cờ hiệu `xSemaphoreGiveFromISR()`.
- Một Task chuyên trách (đang ngủ chờ Semaphore) sẽ lập tức thức dậy để thực hiện toàn bộ các tác vụ tính toán nặng nhọc ở tầng ứng dụng mà không làm nghẽn hệ thống ngắt!

---

## 3. Mutex: Bảo Vệ Tài Nguyên Chia Sẻ Duy Nhất

Khi có từ 2 Task trở lên cùng ghi dữ liệu ra **một cổng UART duy nhất** hoặc cùng điều khiển **một bus I2C/SPI**:
- Nếu không có cơ chế bảo vệ, Task 1 đang in dở một nửa chuỗi thì bị Task 2 chiếm quyền và in đè chuỗi của nó vào giữa → Bản tin trên màn hình bị xé nát và rách chữ!
- **Mutex (Mutual Exclusion)** hoạt động như một chiếc chìa khóa phòng vệ sinh duy nhất: Task nào muốn dùng tài nguyên phải lấy chìa khóa (`xSemaphoreTake`). Các Task khác muốn dùng phải xếp hàng chờ cho đến khi Task đang giữ trả lại chìa khóa (`xSemaphoreGive`).

### 3.1 Hiện tượng Nghịch đảo mức ưu tiên (Priority Inversion) & Cách giải quyết:
Nếu một Task ưu tiên thấp (Task L) đang giữ Mutex, Task ưu tiên cao (Task H) bị chặn phải chờ. Đúng lúc đó, một Task ưu tiên trung bình (Task M - không dùng Mutex) xuất hiện và chiếm quyền của Task L → Vô tình làm Task H phải chờ cả Task M! Đây là thảm họa đã từng suýt phá hủy tàu thám hiểm Sao Hỏa Mars Pathfinder năm 1997 của NASA!

> [!IMPORTANT]
> **Cơ chế Kế thừa mức ưu tiên (Priority Inheritance) của Mutex:**
> FreeRTOS Mutex tích hợp sẵn thuật toán phần mềm: Khi Task H bị chặn bởi Task L đang giữ Mutex, nhân hệ điều hành sẽ **tạm thời nâng mức ưu tiên của Task L lên bằng với Task H** để Task L hoàn thành nhanh nhất công việc và nhả Mutex ra ngay lập tức, triệt tiêu hoàn toàn hiện tượng nghịch đảo mức ưu tiên!

---

## 4. Triển Khai Mã Nguồn Thực Chiến

### Kịch bản thực hành:
1. **Task 1 (Producer)**: Đọc điện áp biến trở (giả lập hoặc từ ADC) định kỳ mỗi 500ms, đóng gói vào cấu trúc dữ liệu `SensorData_t` và đẩy vào **Queue**.
2. **Task 2 (Consumer)**: Chờ đọc dữ liệu từ **Queue**, lấy **Mutex** bảo vệ UART và in kết quả ra màn hình.
3. **Ngắt ngoài EXTI0 (Nút nhấn PA0)**: Khi có cạnh xuống, phát cờ **Binary Semaphore** đánh thức **Task 3 (Alarm Task)** để nháy còi/LED cảnh báo khẩn cấp.

---

File: `freertos_ipc.c`

```c
#include "stm32f10x.h"
#include <stdio.h>
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"

// Data packet struct passed via Queue
typedef struct {
    uint16_t raw_adc;
    float    voltage;
    uint32_t timestamp;
} SensorData_t;

// Declare FreeRTOS IPC handles
QueueHandle_t     xSensorQueue;
SemaphoreHandle_t xUartMutex;
SemaphoreHandle_t xButtonSemaphore;

// Mutex-protected printf retargeting function
void Safe_Printf(const char *format, ...)
{
    // ... [Implement vsnprintf if formatted printing is needed]
}

// 1. Sensor Reader & Queue Producer Task
void vTaskSensorProducer(void *pvParameters)
{
    SensorData_t sensor_data;
    uint16_t simulated_adc = 1000;

    while (1)
    {
        // Data acquisition
        sensor_data.raw_adc   = simulated_adc;
        sensor_data.voltage   = (simulated_adc * 3.3f) / 4095.0f;
        sensor_data.timestamp = xTaskGetTickCount();

        // Post to Queue, wait up to 100ms if Queue is full
        if (xQueueSend(xSensorQueue, &sensor_data, pdMS_TO_TICKS(100)) == pdPASS)
        {
            // Sent to Queue successfully
        }

        simulated_adc = (simulated_adc + 250) % 4096;
        vTaskDelay(pdMS_TO_TICKS(500)); // Sample every 500ms
    }
}

// 2. Queue Consumer & UART Print Task
void vTaskDisplayConsumer(void *pvParameters)
{
    SensorData_t received_data;

    while (1)
    {
        // Block on Queue indefinitely (portMAX_DELAY)
        if (xQueueReceive(xSensorQueue, &received_data, portMAX_DELAY) == pdPASS)
        {
            // Acquire Mutex to guard UART port before printing
            if (xSemaphoreTake(xUartMutex, portMAX_DELAY) == pdTRUE)
            {
                printf("[TIME %lu] Sensor Voltage: %.2f V (RAW: %u)\r\n", 
                       received_data.timestamp, 
                       received_data.voltage, 
                       received_data.raw_adc);

                // MANDATORY: Release Mutex after transmission completes
                xSemaphoreGive(xUartMutex);
            }
        }
    }
}

// 3. Emergency Task Woken by Button Interrupt
void vTaskEmergencyAlarm(void *pvParameters)
{
    while (1)
    {
        // Block waiting for Semaphore given by ISR
        if (xSemaphoreTake(xButtonSemaphore, portMAX_DELAY) == pdTRUE)
        {
            // Upon wakeup: Take Mutex to print emergency alert
            if (xSemaphoreTake(xUartMutex, portMAX_DELAY) == pdTRUE)
            {
                printf(">>> [EMERGENCY ALERT] Button Pressed! Interrupted from ISR <<<\r\n");
                xSemaphoreGive(xUartMutex);
            }

            // Fast blink LED PC13 alarm
            for (int i = 0; i < 4; i++)
            {
                GPIOC->ODR ^= (1 << 13);
                vTaskDelay(pdMS_TO_TICKS(80));
            }
        }
    }
}

// EXTI0 interrupt service routine (PA0 Button)
void EXTI0_IRQHandler(void)
{
    if (EXTI->PR & (1 << 0))
    {
        EXTI->PR = (1 << 0); // Clear interrupt flag

        BaseType_t xHigherPriorityTaskWoken = pdFALSE;

        // SIGNAL TASK FROM WITHIN INTERRUPT SERVICE ROUTINE
        xSemaphoreGiveFromISR(xButtonSemaphore, &xHigherPriorityTaskWoken);

        // Yield immediately if woken task has higher priority than current task
        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }
}

int main(void)
{
    // Hardware initialization (GPIO, UART1, EXTI0)
    // ...

    // 1. CREATE QUEUE: Max 5 items, item size sizeof(SensorData_t)
    xSensorQueue = xQueueCreate(5, sizeof(SensorData_t));

    // 2. CREATE MUTEX TO PROTECT UART COMMUNICATIONS
    xUartMutex = xSemaphoreCreateMutex();

    // 3. CREATE BINARY SEMAPHORE FOR HARDWARE ISR SYNC
    vSemaphoreCreateBinary(xButtonSemaphore);

    // Verify memory resource allocation
    if (xSensorQueue != NULL && xUartMutex != NULL && xButtonSemaphore != NULL)
    {
        // Create tasks with distinct priority levels
        xTaskCreate(vTaskSensorProducer, "Sensor_Task", 128, NULL, 1, NULL);
        xTaskCreate(vTaskDisplayConsumer, "Display_Task", 128, NULL, 1, NULL);
        xTaskCreate(vTaskEmergencyAlarm,  "Alarm_Task",  128, NULL, 3, NULL); // Highest priority

        // Start FreeRTOS operating system
        vTaskStartScheduler();
    }

    while (1);
}
```

---

## 5. Những Lỗi Thường Gặp Khi Dùng Queue Và Mutex

> [!CAUTION]
> **1. Sử dụng sai API bên trong hàm ngắt ISR:**
> Các hàm thông thường như `xQueueSend()`, `xSemaphoreGive()`, `xSemaphoreTake()` **tuyệt đối không được gọi bên trong hàm phục vụ ngắt ISR**!
> Nếu gọi các hàm này trong ISR, vi điều khiển sẽ bị sập treo ngay lập tức do cơ chế chặn Blocked không được phép tồn tại trong ngữ cảnh ngắt.
> **Bắt buộc dùng các hàm có đuôi `...FromISR`**: ví dụ `xQueueSendFromISR()`, `xSemaphoreGiveFromISR()`.

> [!WARNING]
> **2. Quên trả Mutex (`xSemaphoreGive`):**
> Nếu một Task lấy Mutex (`xSemaphoreTake`) nhưng do một câu lệnh `return` giữa chừng hoặc gặp lỗi mà quên không trả lại Mutex, tất cả các Task khác trên hệ thống cùng cần tài nguyên đó sẽ bị kẹt vĩnh viễn trong trạng thái ngủ (**Deadlock**)!

---

## 6. Bài Tập Thực Hành

1. **Bài tập 1 (Hàng đợi truyền chuỗi String Queue)**: Tạo một Queue truyền trực tiếp con trỏ chuỗi ký tự (`char *`). Ba Task khác nhau cùng gửi các thông điệp cảnh báo `"SYSTEM_BOOT"`, `"MOTOR_RUNNING"`, `"OVERHEAT"` vào Queue để một Task duy nhất in ra UART mà không hề bị trùng lặp dòng.
2. **Bài tập 2 (Counting Semaphore quản lý bãi đỗ xe)**: Tạo một Counting Semaphore có giá trị ban đầu là `3` (tượng trưng cho bãi đỗ xe có đúng 3 chỗ). Viết 5 Task giả lập 5 chiếc xe muốn vào bãi. Khi bãi đã đủ 3 xe, các Task xe tiếp theo phải chờ cho đến khi có một xe rời bãi (`Give`).
3. **Bài tập 3 (Deadlock và cơ chế phòng ngừa)**: Viết một chương trình cố tình tạo lỗi Deadlock (Task A giữ Mutex 1 chờ Mutex 2, Task B giữ Mutex 2 chờ Mutex 1). Sử dụng tham số thời gian chờ hữu hạn `ticksToWait` (ví dụ 100ms) thay vì `portMAX_DELAY` để giải thoát hệ thống khi xảy ra kẹt chéo Mutex.
