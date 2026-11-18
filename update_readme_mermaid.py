import re

path = 'f:/Advance_C/rpi4-android-bsp-mastery/README.md'
txt = open(path, encoding='utf-8').read()

# Replace block 1
old_b1 = """```mermaid
flowchart TD
    APP["Ứng dụng Java (LedController.apk)"]
    APP -->|Java API Call| SDK["Client SDK API (LedManager.java)"]
    SDK -->|IPC: ILedManager.aidl| FW["Framework System Service (LedService.java in system_server)"]
    FW -->|Treble Stable AIDL: ILed.aidl| HAL["Vendor HAL Daemon (vendor.example.hardware.led-service C++ NDK)"]
    HAL -->|POSIX File I/O: write()| SYSFS["Linux LED Class Subsystem (/sys/class/leds/user-led/)"]
    SYSFS -->|GPIO Descriptor Framework| DRV["Kernel Driver (drivers/leds/leds-gpio.c)"]
    DRV -->|MMIO Register Access| BCM["Broadcom BCM2711 GPIO Controller"]
    BCM -->|Physical Pin 11 (GPIO17)| LED["Mạch Đệm Điện Tử: Trở Hạn Dòng 330 Ω + Đèn LED Đỏ"]
```"""

new_b1 = """<p align="center">
  <img src="images/bai01_android_bsp_end_to_end_architecture.svg" width="950" alt="Kiến trúc toàn trình Android BSP trên Raspberry Pi 4">
</p>"""

txt = txt.replace(old_b1, new_b1)

# Remove empty mermaid block if any
txt = re.sub(r'```mermaid\s*```', '', txt)

# In section 2, the image was already bai01_android_bsp_end_to_end_architecture.svg.
# Let's show both bai01 and bai04 or bai03 in section 2:
txt = txt.replace(
"""<p align="center">
  <img src="images/bai01_android_bsp_end_to_end_architecture.svg" width="950" alt="Kiến trúc toàn trình Android BSP trên Raspberry Pi 4">
</p>""",
new_b1, 1
)

open(path, 'w', encoding='utf-8').write(txt)
print("Updated README.md: removed all mermaid flowcharts!")
