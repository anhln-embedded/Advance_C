# LESSON 18: ENGINEERING CHARACTER DEVICE DRIVERS: READ, WRITE, IOCTL, AND POLL

> Summary: Engineering the kernel-to-userspace boundary via a Linux Character Device interface (`/dev/lora0`), implementing standardized `read()`, `write()`, and hardware configuration `ioctl()` primitives, and facilitating event-driven non-blocking I/O multiplexing utilizing `poll()`.

---

## 1. The Linux VFS Paradigm: "Everything is a File"

To permit userspace telematics daemons (authored in C/C++, Rust, or Go) to manipulate physical LoRa transceivers without direct kernel memory privileges, the driver exposes a standard **Character Device Node** at `/dev/lora0`:

```mermaid
flowchart TD
    subgraph USERSPACE["Userspace Layer"]
        APP["LoRa Edge Daemon (C++ Event Loop)"]
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

## 2. Hardware Control Interface via `ioctl()`

Beyond reading raw payload buffers, userspace applications must configure RF physical layer parameters dynamically. We standardize IOCTL opcodes using official Linux kernel macros:

```c
#include <linux/ioctl.h>

#define LORA_IOC_MAGIC 'L'

// Standardized IOCTL Command Opcode Definitions
#define LORA_IOCTL_SET_FREQ    _IOW(LORA_IOC_MAGIC, 1, uint32_t) // Set RF carrier frequency in Hz
#define LORA_IOCTL_SET_SF      _IOW(LORA_IOC_MAGIC, 2, uint8_t)  // Configure Spreading Factor (7-12)
#define LORA_IOCTL_SET_BW      _IOW(LORA_IOC_MAGIC, 3, uint32_t) // Configure Bandwidth in Hz
#define LORA_IOCTL_SET_TXPOWER _IOW(LORA_IOC_MAGIC, 4, int8_t)   // Set radiated output power in dBm
#define LORA_IOCTL_GET_RSSI    _IOR(LORA_IOC_MAGIC, 5, int16_t)  // Query last packet RSSI
#define LORA_IOCTL_GET_SNR     _IOR(LORA_IOC_MAGIC, 6, int8_t)   // Query last packet SNR
```

---

## 3. High-Performance Non-Blocking I/O Multiplexing via `poll()`

> [!IMPORTANT]
> **Why `poll()` Support is Mandatory for Production Daemons:**
> Without a kernel `.poll` implementation, userspace daemons are forced into endless busy-wait polling loops continuously invoking `read()`, pegging host CPU cores at **100% utilization**.
> Implementing `.poll` integrates seamlessly with **`epoll_wait()`** and **`poll()`**. The operating system scheduler places the userspace thread into a deep sleep state (consuming 0% CPU), unblocking it instantaneously the exact microsecond an inbound packet is latched in kernel memory!

---

## 4. Production C Kernel Implementation: `file_operations`

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

// 1. Device Open Primitive
static int lora_fops_open(struct inode *inode, struct file *filp) {
    filp->private_data = &g_lora_dev;
    return 0;
}

// 2. Device Read Primitive
static ssize_t lora_fops_read(struct file *filp, char __user *buf, size_t count, loff_t *f_pos) {
    struct lora_chardev *dev = filp->private_data;
    ssize_t ret = 0;

    // Handle non-blocking descriptors immediately
    if (!dev->has_data && (filp->f_flags & O_NONBLOCK)) {
        return -EAGAIN;
    }

    // Sleep until the Threaded IRQ wakes the waitqueue
    if (wait_event_interruptible(dev->rx_wait, dev->has_data)) {
        return -ERESTARTSYS; // Unblocked by POSIX signal (e.g., SIGINT/Ctrl+C)
    }

    mutex_lock(&dev->lock);
    if (count > dev->rx_len) {
        count = dev->rx_len;
    }

    // Safe memory copy crossing Kernel-to-Userspace boundary
    if (copy_to_user(buf, dev->rx_buf, count)) {
        ret = -EFAULT;
    } else {
        ret = count;
        dev->has_data = false; // Packet successfully consumed
    }
    mutex_unlock(&dev->lock);

    return ret;
}

// 3. Device Write Primitive
static ssize_t lora_fops_write(struct file *filp, const char __user *buf, size_t count, loff_t *f_pos) {
    u8 kbuf[256];
    if (count > 255) return -EINVAL;

    // Copy outbound payload from userspace buffer
    if (copy_from_user(kbuf, buf, count)) {
        return -EFAULT;
    }

    // Trigger physical SPI transmission
    // sx1276_transmit_payload(kbuf, count);

    return count;
}

// 4. Multiplexed Event Polling Primitive
static __poll_t lora_fops_poll(struct file *filp, poll_table *wait) {
    struct lora_chardev *dev = filp->private_data;
    __poll_t mask = 0;

    // Register our kernel waitqueue with the VFS poll table
    poll_wait(filp, &dev->rx_wait, wait);

    // If packet data is staged in memory, assert readable flag
    if (dev->has_data) {
        mask |= EPOLLIN | EPOLLRDNORM;
    }

    // Transceiver hardware ready for outbound writes
    mask |= EPOLLOUT | EPOLLWRNORM;

    return mask;
}

// 5. Hardware Configuration Primitive
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
            return -ENOTTY; // Command unrecognized
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

## 5. Core Engineering Notes & Best Practices

> [!TIP]
> **Kernel Memory Isolation Interview Question:** *"Why is standard `memcpy()` strictly forbidden when transferring packet buffers between kernel memory and userspace pointers, necessitating `copy_to_user()` and `copy_from_user()`?"*
> 
> **Authoritative Technical Response:**
> "Userspace pointers (`__user *buf`) exist inside unprivileged virtual memory spaces.
> 1. The memory address could be corrupt, malicious, or reference restricted kernel space. Invoking raw `memcpy()` would trigger an unchecked MMU Page Fault, crashing the entire operating system in an unrecoverable **Kernel Panic**.
> 2. The targeted userspace memory page might be swapped out to disk or uncommitted. The `copy_to_user()` family incorporates defensive validation (`access_ok`) and graceful kernel page-fault handling to ensure system stability."

