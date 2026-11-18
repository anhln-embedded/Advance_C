# Advanced Android BSP Engineering on Raspberry Pi 4: From Linux Kernel to Stable AIDL HAL, Framework System Service & Java Application

> A comprehensive deep-dive curriculum on Android Board Support Package (BSP) engineering, guiding developers across the complete modern Android stack: Linux Kernel 6.18 LTS (GKI), Google Kleaf / Bazel build system, Device Tree Overlays, Linux LED Subsystem, Stable AIDL HAL (NDK Backend), SELinux security policies, Android Framework System Services, and production Java applications controlling real physical hardware.

---

## 1. Course Overview & Core Engineering Objectives

In the connected embedded systems industry (Android Automotive, Smart Cockpit, Industrial IoT Touchscreens, POS Terminals), developing hardware control features cannot rely on naive techniques like opening raw GPIO nodes and blasting bytes. Google's Android architecture demands strict compliance with Project Treble partitioning, mandatory SELinux access control boundaries, and multi-layered Binder IPC protocols:

<p align="center">
  <img src="images/bai01_android_bsp_end_to_end_architecture.svg" width="950" alt="End-to-End Android BSP Architecture on Raspberry Pi 4">
</p>

### Key Learning Outcomes:
1. **Master the Android OS Image**: Inspect and reverse-fingerprint running system images (build fingerprint, kernel release, runtime `.config`, SELinux enforcement) from the KonstaKANG AOSP 17 distribution (Linux 6.18 LTS).
2. **Harness Modern Build Toolchains (Google Kleaf / Bazel)**: Understand hermetic Clang toolchains, Bazel sandbox isolation, DDK modules (`ddk_module`), and definitively resolve `vermagic` / symbol CRC mismatches via SCM Stamping (`workspace_status.json`).
3. **Driver Development & Device Tree Overlays**: Author clean Device Tree overlays (`gpio-leds` binding) and interface with the Linux LED Class subsystem (`brightness`, `trigger=timer`) rather than performing unsanctioned direct register I/O.
4. **Develop Production-Grade Stable AIDL HALs**: Transition from legacy HIDL to Stable AIDL (`@VintfStability`), implement Native C++ Daemons utilizing the NDK Backend (`libbinder_ndk`), declare VINTF Manifests, and configure `init.rc` lifecycle management.
5. **Enforce Fine-Grained SELinux Policies**: Author Type Enforcement (`.te`) policy rules, assign labeling in `file_contexts` and `service_contexts`, and eliminate `avc: denied` audit violations to pass CTS/VTS compliance.
6. **Extend Android Framework Services**: Implement and publish custom `LedService` into `system_server`, manage worker threads, enforce caller permissions (`android.permission.CONTROL_LED`), register Binder death recipients, and expose an elegant Client SDK (`LedManager`).
7. **Ship Complete Hardware-Control Apps**: Develop `LedController.apk` in native Java with real-time ON, OFF, and dynamic BLINK duty-cycle controls.

---

## 2. Architectural Diagrams & Vector Schematics

This curriculum is backed by dual-theme vector SVG diagrams optimized for modern Web LMS and documentation platforms:

1. **End-to-End Architectural Hierarchy**: `images/bai01_android_bsp_end_to_end_architecture.svg`
2. **Kleaf / Bazel Build Flow & SCM Stamping Pipeline**: `images/bai02_kleaf_bazel_kernel_build_flow.svg`
3. **Stable AIDL IPC & SELinux Multi-Domain Security Model**: `images/bai03_stable_aidl_selinux_security_model.svg`
4. **Raspberry Pi 4 40-Pin Header & LED Protection Circuit**: `images/bai04_rpi4_gpio_led_circuit_schematic.svg`

<p align="center">
  <img src="images/bai01_android_bsp_end_to_end_architecture.svg" width="950" alt="End-to-End Android BSP Architecture on Raspberry Pi 4">
</p>

---

## 3. Comprehensive Curriculum Syllabus

The curriculum spans **6 Specialized Modules (21 Hands-On Lessons)**:

### Module 1: Raspberry Pi 4 Hardware Foundations & Android OS Analysis
- **Lesson 01**: Overview of modern Android BSP architecture, Raspberry Pi 4 GPIO expansion pinout, and hardware electrical safety.
- **Lesson 02**: Flashing KonstaKANG AOSP 17, configuring ADB over TCP/IP, and comprehensive OS / Kernel reverse-fingerprinting.

### Module 2: AOSP Kernel Build Pipeline: Google Kleaf, Bazel & Out-of-tree Modules
- **Lesson 03**: Synchronization strategy for compatible AOSP kernel repositories (`android_kernel_manifest`, `android_kernel_brcm_rpi`).
- **Lesson 04**: Demystifying Google Kleaf / Bazel: Hermetic Clang toolchains, sandbox isolation, and Raspberry Pi 4 defconfig tuning.
- **Lesson 05**: Practical Lab 1: Building your first Hello World Kernel Module via Bazel DDK (`ddk_module`) and resolving Broadcom firmware dependencies.
- **Lesson 06**: Unraveling `vermagic`, `CONFIG_MODVERSIONS`, 32-bit CRC symbol matching, SCM Stamping (`workspace_status.json`), and cryptographic module signing.
- **Lesson 07**: Runtime module management via ADB (`insmod`, `rmmod`), kernel ring buffer diagnostics (`dmesg`), and Kernel Taint analysis.

### Module 3: GPIO Systems, Device Tree Overlays & Linux LED Class Subsystem
- **Lesson 08**: Linux GPIO architecture evolution: From legacy sysfs to GPIO Descriptor Core (`gpiod_*`) and the BCM2711 controller.
- **Lesson 09**: Device Tree anatomy and authoring Device Tree Overlays (`.dts` / `.dtbo`) with `gpio-leds` bindings for Raspberry Pi 4.
- **Lesson 10**: Practical Lab 2: Exporting GPIO17 to the Linux LED Class (`/sys/class/leds/user-led/`), setting `brightness`, and activating hardware `timer trigger`.

### Module 4: Android Hardware Abstraction Layer (Vendor HAL) with Stable AIDL
- **Lesson 11**: Architectural evolution of HALs: From Legacy HAL to HIDL (deprecated) to modern Stable AIDL (`@VintfStability`).
- **Lesson 12**: Defining `ILed.aidl`, configuring `Android.bp` for C++ NDK Backend generation, and linking `libbinder_ndk`.
- **Lesson 13**: Practical Lab 3: Developing the Native C++ HAL Daemon (`vendor.example.hardware.led-service`), safe file I/O, and concurrency management.
- **Lesson 14**: Configuring VINTF Manifests (`manifest.xml`) and daemon lifecycle management in `init.rc`.
- **Lesson 15**: Advanced SELinux policy engineering: Type Enforcement, `file_contexts`, `service_contexts`, and debugging `avc: denied` audit violations.

### Module 5: Android Framework System Service Integration & SDK Manager Pattern
- **Lesson 16**: Android System Service architecture: Role of `system_server`, service publication, and lookup via `ServiceManager`.
- **Lesson 17**: Building `LedService.java`: Managing Binder proxies to Vendor HAL, Death Recipient callbacks, and permission verification (`enforceCallingOrSelfPermission`).
- **Lesson 18**: Crafting the Client SDK (`LedManager.java`) using the standard `getSystemService(LedManager.class)` registry pattern.

### Module 6: Java APK Application Development, End-to-End Verification & Troubleshooting
- **Lesson 19**: Practical Lab 4: Developing `LedController.apk` in Java: Clean UI design, real-time ON/OFF toggling, and BLINK frequency adjustments.
- **Lesson 20**: End-to-End Build and Deployment Pipeline: Orchestrating Kernel, DTBO, Native HAL Daemon, Framework, and APK.
- **Lesson 21**: Comprehensive Test Matrix: Binder IPC latency benchmarking, CPU/RAM profiling, and real-world troubleshooting guide.

---

## 4. Architectural Comparison: Hack vs Production Engineering

| Evaluation Criteria | Unofficial / Hack Approach | Google Production BSP Standard |
| :--- | :--- | :--- |
| **Privilege Model** | Grants root (`su`) to APK, reckless `chmod 777` on device files | Strictly enforces multi-tier user identity (App UID $→$ Framework $→$ HAL) |
| **Hardware Access** | Java APK directly invokes `Runtime.exec("echo 1 > /sys/...")` | Traversing Stable AIDL IPC, Vendor HAL Daemon, and Linux LED subsystem |
| **SELinux Security** | Disables protection by setting SELinux to `permissive` | Rigorous Type Enforcement: domains, exec types, service labels, sysfs attributes |
| **HAL Interface** | Deprecated HIDL or hardcoded C++ JNI embedded directly into APK | Stable AIDL (`@VintfStability`), NDK Backend, full Treble compliance |
| **LED Blinking (Blink)** | `Thread.sleep()` loop in user-space freezing UI and consuming CPU | Hardware-driven `timer trigger` inside kernel or dedicated HAL worker thread |

---

## 5. Technical Authoring Standards

All contributions to this repository must adhere to the **Web Markdown Authoring Standard**:
1. **Summary Blocks**: Optional single-sentence summary formatted as `> Summary: ...` (or `> Tóm tắt: ...`) in plain text without nested formatting.
2. **Technical Symbols**: Always use native Unicode symbols (`→`, `⇒`, `≤`, `≥`, `µA`, `dBm`, `kHz`, `MHz`). Avoid inline LaTeX arrow formulas that break on web CMS engines.
3. **GFM Callouts**: Standardized to 5 tags: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`. Tag identifiers must occupy their own line.
4. **Diagrams**: Vector SVGs located in `images/`, centered using `<p align="center"><img src="images/..." width="950" alt="..."></p>`.
5. **Code Blocks**: Always include explicit syntax highlighting identifiers (`c`, `cpp`, `bash`, `powershell`, `xml`, `python`, `dts`, `aidl`, `java`). Mermaid flowcharts are prohibited in documentation files in favor of responsive, dual-theme vector SVGs.
