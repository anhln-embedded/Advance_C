# LESSON 02: SETTING UP AOSP OS AND SYSTEM REVERSE FINGERPRINTING TECHNIQUES

> Summary: Guide to downloading and verifying the integrity of the KonstaKANG AOSP 17 build for Raspberry Pi 4, establishing remote ADB connectivity, and executing a rigorous system reverse engineering and OS fingerprinting workflow to extract kernel configurations, SELinux policies, and peripheral states for source tree matching.

---

## 1. Build Provenance & Cryptographic Integrity Verification

In commercial BSP engineering, developers frequently begin from an existing manufacturer reference OS image deployed on target silicon. The initial engineering checkpoint is **verifying the origin and cryptographic integrity** of the compressed operating system image before flashing it onto physical storage media.

<p align="center">
  <img src="images/bai02_image_integrity_flash_workflow.svg" width="950" alt="SHA-256 Hash Verification Workflow and AOSP Flashing Process">
</p>

### Reference Baseline Release Specifications:
- **Archive Filename**: `AOSP17-20261030-KonstaKANG-rpi4.zip`
- **Official Distribution Portal**: [KonstaKANG Raspberry Pi 4 AOSP 17](https://konstakang.com/devices/rpi4/AOSP17/)
- **Authoritative SHA-256 Hash**:
  ```text
  9c02408206053b8bcbf7591a02d8d28d09becf17cfa522f52a945c5f87deb709
  ```

### Computing the Cryptographic Hash on Host Workstations:

* **Windows (PowerShell)**:
  ```powershell
  Get-FileHash .\AOSP17-20261030-KonstaKANG-rpi4.zip -Algorithm SHA256
  ```

* **Linux / macOS (Bash)**:
  ```bash
  sha256sum AOSP17-20261030-KonstaKANG-rpi4.zip
  ```

> [!WARNING]
> **Copyright & Licensing Notice:**
> - KonstaKANG builds incorporate components governed by the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.
> - Commercial redistribution and unauthorized public re-uploading (mirroring) are prohibited by the author. All distribution links must point directly to the project's official portal.

---

## 2. Flashing Workflow & First Boot

1. Launch **Raspberry Pi Imager** (or BalenaEtcher / native Linux `dd`).
2. Select the extracted target image file (`.img`).
3. Select the target microSD storage card (recommended capacity $\ge 16\text{ GB}$, rated Class 10 U3 A2 to ensure adequate random 4K read/write IOPS for Android ART runtime operations).
4. Click **Write** and verify the written data blocks before removing the card.
5. Insert the microSD card into the Raspberry Pi 4 slot, connect USB peripherals, connect a micro-HDMI display cable, and apply power via a certified USB-C power supply ($5\text{V} / 3\text{A}$).
6. Once the Android desktop initializes:
   - Navigate to **Settings** $→$ **About tablet** $→$ Tap **Build number** 7 consecutive times to unlock **Developer options**.
   - Navigate to **System** $→$ **Developer options**: Enable **USB debugging** and **Network ADB debugging** (allowing remote shell access over the local IP network).

---

## 3. Establishing the Android Debug Bridge (ADB Over TCP/IP)

On your development host workstation, ensure the Android SDK Platform-Tools are accessible in the system path:

```bash
# Verify ADB host tool version
adb version

# Connect to Raspberry Pi 4 over LAN (replace with actual target IP address)
adb connect 192.168.1.150:5555

# Verify device attachment state
adb devices
```

Expected terminal response:
```text
List of devices attached
192.168.1.150:5555    device
```

---

## 4. OS & Kernel Reverse Fingerprinting Techniques

To compile custom drivers that are 100% binary-compatible with a running Android device, engineers must extract **5 core categories of system technical fingerprints**:

<p align="center">
  <img src="images/bai02_os_reverse_fingerprinting_tree.svg" width="950" alt="Android OS and Kernel Reverse Fingerprinting Decision Tree">
</p>

### 4.1. Extracting Android Build Properties
Execute the following property queries to inspect the system framework baseline:

```bash
adb shell getprop ro.build.fingerprint
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.type
adb shell getprop ro.product.device
```

* **Baseline Findings**:
  - `ro.build.version.release`: `17` (Android 17 / AOSP Preview)
  - `ro.build.version.sdk`: `36`
  - `ro.product.device`: `rpi4`
  - `ro.build.type`: `userdebug` (Permits privilege escalation to root on the ADB shell via `adb root`)

### 4.2. Extracting Linux Kernel Identity
This data dictates the exact **`vermagic`** string required for all loadable kernel modules:

```bash
adb shell uname -a
adb shell uname -r
adb shell cat /proc/version
adb shell cat /proc/cmdline
```

* **Detailed Technical Breakdown**:
  ```text
  Linux localhost 6.18.38-g7a9131c1065a-v8 #1 SMP PREEMPT Thu Oct 30 14:15:20 UTC 2026 aarch64
  ```
  - **Base Kernel Version**: `6.18.38` (Linux Long Term Support - LTS release).
  - **SCM Commit Suffix**: `-g7a9131c1065a`.
    - The prefix `g` designates Git source control.
    - The alphanumeric token `7a9131c1065a` represents the **first 12 characters of the Git Commit SHA-1** in the kernel branch used to build this release.
  - **Local Version Suffix**: `-v8` (Configured in the Raspberry Pi defconfig to designate the 64-bit ARMv8-A architecture).

### 4.3. Extracting and Analyzing Kernel Configuration (`/proc/config.gz`)
Android kernels are typically built with `CONFIG_IKCONFIG_PROC=y`, enabling direct extraction of the active runtime `.config` file from system memory:

```bash
# Pull the runtime compressed config archive to the host workstation
adb pull /proc/config.gz ./device_config.gz
zcat ./device_config.gz > ./device_kernel.config

# Inspect kernel flags that govern loadable module compatibility:
grep -E 'CONFIG_MODULES|CONFIG_MODVERSIONS|CONFIG_MODULE_SIG|CONFIG_LEDS|CONFIG_GPIO' ./device_kernel.config
```

* **Critical Architectural Parameters Discovered**:
  ```ini
  CONFIG_MODULES=y                  # Enables dynamic kernel module loading (insmod/modprobe)
  CONFIG_MODULE_UNLOAD=y           # Enables runtime module unloading (rmmod)
  CONFIG_MODVERSIONS=y             # Enforces 32-bit CRC symbol version hashing
  CONFIG_MODULE_SIG=y              # Supports cryptographic module signature verification
  CONFIG_MODULE_SIG_ALL=y          # Automatically signs internal kernel modules during build
  CONFIG_LEDS_CLASS=y              # Enables Linux LED Subsystem
  CONFIG_LEDS_GPIO=y               # Enables GPIO-driven LED class driver
  CONFIG_OF=y                      # Enables Open Firmware / Device Tree runtime resolution
  ```

> [!IMPORTANT]
> **Implications of `CONFIG_MODVERSIONS=y`:**
> When this feature is active, the Linux kernel does not merely compare ASCII version strings; it verifies the **32-bit CRC checksum** of every kernel symbol referenced by the module (e.g., `printk`, `module_layout`). Any mismatch in kernel internal data structures (`struct`) between the module build headers and running kernel image will cause `insmod` to fail with `disagrees about version of symbol`.

### 4.4. Auditing Security Policies & Module Signing Enforcement
```bash
# Check SELinux operational mode (Enforcing vs Permissive)
adb shell getenforce

# Check if dynamic module loading is globally locked down
adb shell cat /proc/sys/kernel/modules_disabled

# Check if the kernel strictly enforces valid cryptographic signatures
adb shell cat /sys/module/module/parameters/sig_enforce
```

* **Observed Runtime Values**:
  - `modules_disabled`: `0` (Dynamic module loading is permitted).
  - `sig_enforce`: `N` (Module signature verification is supported but **not strictly enforced**. When loading unsigned out-of-tree modules, the kernel generates an audit log and applies a *Kernel Taint* flag rather than triggering a kernel panic).

### 4.5. Surveying Active Peripheral Sysfs Nodes
```bash
# Audit registered LED class devices
adb shell ls -la /sys/class/leds/

# Audit GPIO subsystem interfaces
adb shell ls -la /sys/class/gpio/
adb shell ls -la /dev/gpiochip*
```

---

## 5. Generating the Comprehensive System Baseline Profile (`device-baseline.txt`)

Following the investigation, consolidate all extracted parameters into an authoritative baseline technical specification:

```text
==================================================================
DEVICE BASELINE AUDIT SPECIFICATION
Project: Raspberry Pi 4 Model B - Android BSP Mastery
Audit Timestamp: 2026-10-30
==================================================================

[1. HARDWARE SPECIFICATION]
- Board Target: Raspberry Pi 4 Model B Rev 1.5 (4GB LPDDR4)
- Processor: Broadcom BCM2711 SoC (Quad-core Cortex-A72 @ 1.5 GHz)
- Target Control Pin: BCM GPIO17 (Physical Header Pin 11)
- Circuit Reference Ground: GND (Physical Header Pin 6)

[2. ANDROID PLATFORM RELEASE]
- Distribution: KonstaKANG AOSP 17
- Release Date: 2026-10-30
- Android Release: 17 (SDK Level 36)
- Build Flavor: userdebug
- Build Fingerprint: raspberry/rpi4/rpi4:17/...:userdebug/test-keys

[3. LINUX KERNEL IDENTITY]
- Release String: 6.18.38-g7a9131c1065a-v8
- Base Version: 6.18.38
- Git SCM Commit SHA-1: 7a9131c1065a28544c1b6592152981b4c4102367
- Local Version: -v8
- Vermagic Signature: SMP preempt mod_unload modversions aarch64

[4. SECURITY & MODULE ENFORCEMENT POLICIES]
- SELinux Mode: Enforcing
- modules_disabled: 0 (Dynamic module loading permitted)
- sig_enforce: N (Taint flag logged on unsigned module, non-fatal)
- Modversions: Enabled (Strict 32-bit CRC symbol matching enforced)

[5. PERIPHERAL SUBSYSTEM STATES]
- LED Class Subsystem: Active at /sys/class/leds/
- GPIO Subsystem: Character device (/dev/gpiochipX) and Device Tree gpio-leds supported
==================================================================
```

---

## 6. Self-Assessment & Engineering Exercises

1. **Analyzing SCM Hashes**: Suppose `uname -r` on a target board yields `6.18.38-v8` without the `-g<hash>` component. What does this reveal about the ROM developer's kernel build environment? Which Kbuild configuration flag controls this behavior?
2. **Recovering Missing `config.gz`**: If an uncharacterized Android board returns `No such file or directory` when attempting `adb shell ls /proc/config.gz`, what alternative reverse engineering techniques can be used to extract or reconstruct the kernel `.config` file?
3. **Automated Auditing Script**: Write a portable Bash shell script (`audit_device.sh`) that connects via ADB, executes all verification commands listed above, and outputs a formatted Markdown summary table.
