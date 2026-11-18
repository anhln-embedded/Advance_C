# BÀI 18: XÂY DỰNG CHARACTER DEVICE DRIVER: READ, WRITE, IOCTL VÀ POLL

> Tóm tắt: Thiết kế tầng giao tiếp giữa nhân Linux và không gian người dùng thông qua Character Device Driver (`/dev/lora0`), hiện thực các thao tác file chuẩn `read()`, `write()`, giao tiếp điều khiển cấu hình tham số RF qua `ioctl()`, và hỗ trợ cơ chế vào ra phi đồng bộ không nghẽn với `poll()`.

---

## 1. Triết Lý VFS Của Linux: "Mọi Thứ Đều Là Tệp Tin"

Để một ứng dụng người dùng (như LoRa Daemon viết bằng C/C++ hoặc Go/Rust) có thể điều khiển được chip LoRa mà không cần quyền can thiệp trực tiếp vào bộ nhớ kernel, driver phải cung cấp một cổng giao tiếp dưới dạng **Character Device (Thiết bị ký tự)** nằm tại đường dẫn `/dev/lora0`.

```mermaid
flowchart TD
    subgraph USERSPACE["Không Gian Người Dùng (Userspace)"]
        APP["LoRa Daemon (C++ Event Loop)"]
    end

    subgraph VFS["Virtual Filesystem Switch (VFS)"]
        SYS_OPEN["open(\"/dev/lora0\", O_RDWR)"]
        SYS_WRITE["write(fd, payload, len)"]
        SYS_READ["read(fd, buffer, sizeof(buf))"]
        SYS_POLL["epoll_wait() / poll()"]
        SYS_IOCTL["ioctl(fd, LORA_SET_SF, 7)"]
    end

    subgraph DRIVER["LoRa Character Driver (Kernel Space)"]
        FOPS["struct file_operations lora_fops"]
        DRV_OPEN[".open = lora_dev_open"]
        DRV_WRITE[".write = lora_dev_write"]
        DRV_READ[".read = lora_dev_read"]
        DRV_POLL[".poll = lora_dev_poll"]
        DRV_IOCTL[".unlocked_ioctl = lora_dev_ioctl"]
    end

    APP --> SYS_OPEN & SYS_WRITE & SYS_READ & SYS_POLL & SYS_IOCTL
    SYS_OPEN --> DRV_OPEN
    SYS_WRITE --> DRV_WRITE
    SYS_READ --> DRV_READ
    SYS_POLL --> DRV_POLL
    SYS_IOCTL --> DRV_IOCTL
    FOPS --- DRV_OPEN & DRV_WRITE & DRV_READ & DRV_POLL & DRV_IOCTL
```

---

## 2. Định Nghĩa Giao Diện Điều Khiển `ioctl()`

Ngoài việc truyền nhận byte thô, người dùng cần thay đổi cấu hình vô tuyến (như đổi tần số, đổi Spreading Factor). Ta thiết lập các mã lệnh `ioctl` độc nhất sử dụng macro chuẩn của Linux:

```c
#include <linux/ioctl.h>

#define LORA_IOC_MAGIC 'L'

// Định nghĩa các lệnh IOCTL có truyền dữ liệu an toàn
#define LORA_IOCTL_SET_FREQ    _IOW(LORA_IOC_MAGIC, 1, uint32_t) // Đặt tần số Hz
#define LORA_IOCTL_SET_SF      _IOW(LORA_IOC_MAGIC, 2, uint8_t)  // Đặt Spreading Factor
#define LORA_IOCTL_SET_BW      _IOW(LORA_IOC_MAGIC, 3, uint32_t) // Đặt Bandwidth Hz
#define LORA_IOCTL_SET_TXPOWER _IOW(LORA_IOC_MAGIC, 4, int8_t)   // Đặt công suất phát dBm
#define LORA_IOCTL_GET_RSSI    _IOR(LORA_IOC_MAGIC, 5, int16_t)  // Lấy RSSI gói tin vừa nhận
#define LORA_IOCTL_GET_SNR     _IOR(LORA_IOC_MAGIC, 6, int8_t)   // Lấy SNR gói tin vừa nhận
```

---

## 3. Hiện Thực Cơ Chế Non-Blocking I/O Với `poll()`

> [!IMPORTANT]
> **Tại sao bắt buộc phải hỗ trợ hàm `poll()`?**
> Nếu không có `poll()`, ứng dụng tầng người dùng muốn biết khi nào có gói tin đến sẽ phải liên tục gọi hàm `read()` trong một vòng lặp vô tận (Busy Polling), khiến mức sử dụng CPU của tiến trình vọt lên **100%**.
> Khi có hàm `poll()`, ứng dụng có thể sử dụng các hàm gom sự kiện hiện đại như **`epoll_wait()`** hoặc **`poll()`**. Tiến trình Userspace sẽ được kernel đưa vào trạng thái ngủ sâu (0% CPU), và chỉ được đánh thức dậy ngay thời điểm có gói tin vô tuyến đáp xuống anten!

---

## 4. Mã Nguồn Mẫu Hoàn Chỉnh Của Tầng `file_operations`

```c
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/poll.h>
#include <linux/slab.h>

struct lora_chardev {
    wait_queue_head_t rx_wait;
    bool              has_data;
    u8                rx_buf[256];
    size_t            rx_len;
    struct mutex      lock;
};

static struct lora_chardev g_lora_dev;

// 1. Thao tác Mở thiết bị (open)
static int lora_fops_open(struct inode *inode, struct file *filp) {
    filp->private_data = &g_lora_dev;
    return 0;
}

// 2. Thao tác Đọc dữ liệu (read)
static ssize_t lora_fops_read(struct file *filp, char __user *buf, size_t count, loff_t *f_pos) {
    struct lora_chardev *dev = filp->private_data;
    ssize_t ret = 0;

    // Nếu không có dữ liệu và file được mở ở chế độ Non-blocking (O_NONBLOCK)
    if (!dev->has_data && (filp->f_flags & O_NONBLOCK)) {
        return -EAGAIN;
    }

    // Chờ cho đến khi Threaded IRQ đánh thức hàng đợi waitqueue
    if (wait_event_interruptible(dev->rx_wait, dev->has_data)) {
        return -ERESTARTSYS; // Bị gián đoạn bởi tín hiệu Signal (ví dụ Ctrl+C)
    }

    mutex_lock(&dev->lock);
    if (count > dev->rx_len) {
        count = dev->rx_len;
    }

    // Sao chép an toàn dữ liệu từ Kernel Space sang Userspace
    if (copy_to_user(buf, dev->rx_buf, count)) {
        ret = -EFAULT;
    } else {
        ret = count;
        dev->has_data = false; // Đã đọc xong
    }
    mutex_unlock(&dev->lock);

    return ret;
}

// 3. Thao tác Ghi dữ liệu phát sóng (write)
static ssize_t lora_fops_write(struct file *filp, const char __user *buf, size_t count, loff_t *f_pos) {
    u8 kbuf[256];
    if (count > 255) return -EINVAL;

    // Sao chép payload từ Userspace vào Kernel
    if (copy_from_user(kbuf, buf, count)) {
        return -EFAULT;
    }

    // Kích hoạt phát sóng qua SPI
    // sx1276_transmit_payload(kbuf, count);

    return count;
}

// 4. Thao tác Poll phục vụ epoll_wait
static __poll_t lora_fops_poll(struct file *filp, poll_table *wait) {
    struct lora_chardev *dev = filp->private_data;
    __poll_t mask = 0;

    // Đăng ký waitqueue vào bảng poll của hệ điều hành
    poll_wait(filp, &dev->rx_wait, wait);

    // Nếu đã có dữ liệu trong buffer, báo cờ EPOLLIN sẵn sàng đọc
    if (dev->has_data) {
        mask |= EPOLLIN | EPOLLRDNORM;
    }

    // Luôn sẵn sàng ghi (EPOLLOUT)
    mask |= EPOLLOUT | EPOLLWRNORM;

    return mask;
}

// 5. Thao tác Điều khiển cấu hình (ioctl)
static long lora_fops_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
    switch (cmd) {
        case LORA_IOCTL_SET_SF: {
            uint8_t sf;
            if (copy_from_user(&sf, (void __user *)arg, sizeof(sf))) return -EFAULT;
            if (sf < 7 || sf > 12) return -EINVAL;
            // sx1276_set_sf(sf);
            break;
        }
        default:
            return -ENOTTY; // Lệnh không hỗ trợ
    }
    return 0;
}

static const struct file_operations lora_fops = {
    .owner          = THIS_MODULE,
    .open           = lora_fops_open,
    .read           = lora_fops_read,
    .write          = lora_fops_write,
    .poll           = lora_fops_poll,
    .unlocked_ioctl = lora_fops_ioctl,
};
```

---

## 5. Lưu Ý Kỹ Thuật & Best Practices Thực Chiến

> [!TIP]
> **Bài toán thiết kế thực chiến:** *"Tại sao ta không thể dùng `memcpy()` thông thường mà bắt buộc phải dùng `copy_to_user()` và `copy_from_user()` trong hàm read/write của Character Driver?"*
> 
> **Giải pháp kiến trúc chuẩn mực:**
> "con trỏ truyền vào từ người dùng (`__user *buf`) trỏ vào không gian địa chỉ ảo của tiến trình Userspace.
> 1. Con trỏ này có thể không hợp lệ (NULL hoặc trỏ vào vùng nhớ cấm của kernel), nếu dùng `memcpy` sẽ gây lỗi Page Fault làm **Panic sập toàn bộ Kernel**.
> 2. Vùng nhớ của Userspace có thể bị hệ điều hành tráo đổi ra đĩa (Swapped Out). Hàm `copy_to_user()` được tích hợp sẵn cơ chế kiểm tra tính hợp lệ của địa chỉ bộ nhớ (`access_ok`) và xử lý bắt trang an toàn nếu xảy ra Page Fault!"

