# LESSON 03: KERNEL SOURCE SYNCHRONIZATION STRATEGY AND KLEAF BAZEL BUILD PIPELINE

> Summary: Differentiating Android Platform and Kernel source trees, establishing a production build environment on Ubuntu 22.04 LTS, synchronizing Raspberry Pi 4 kernel repositories via Google Repo, and mastering modern hermetic kernel compilation using Google Kleaf and Bazel sandbox isolation.

---

## 1. Delineating Architectural Boundaries: Android Platform Source vs Android Kernel Source

A common conceptual pitfall encountered by engineers transitioning into Android BSP development is conflating the **Android Platform Tree** with the **Android Kernel Tree**.

In modern AOSP architecture, these two codebases are decoupled and maintained via separate repository manifests:
- **Android Platform Tree**: Encompasses the Android Framework (Java/Kotlin), System Services, Native Daemons, ART Runtime, Soong Build System (`Android.bp`), core applications, and hardware integration definitions in `device/`. A typical shallow checkout demands between $250\text{ GB} → 400\text{ GB}$ of disk space.
- **Android Kernel Tree**: Encompasses the Linux kernel source, device drivers, Device Tree source files (`.dts`), and Google's specialized build orchestration ruleset known as **Kleaf / Bazel**. A typical kernel checkout requires approximately $30\text{ GB} → 50\text{ GB}$.

<p align="center">
  <img src="images/bai03_platform_vs_kernel_source_trees.svg" width="950" alt="Separation of Android Platform Tree and Kernel Source Tree">
</p>

> [!IMPORTANT]
> **Source Alignment Realities in Production:**
> Compiling a Linux kernel that matches commit hash `7a9131c1065a` **does not mean your entire Android platform tree matches the prebuilt KonstaKANG ROM**.
> The KonstaKANG distribution builds on top of the upstream **Raspberry Vanilla** project but incorporates proprietary BSP patches (Mesa GPU hardware acceleration, touchscreen touch event filters, advanced settings menus). To ensure full reproducibility, engineers must lock manifests for both repositories independently.

---

## 2. Setting Up the Production Build Environment

Compiling the Android Common Kernel with Google Kleaf requires a host workstation meeting specific architectural baselines:

### 1. Host Hardware Prerequisites:
- **Operating System**: Ubuntu 22.04 LTS (Jammy Jellyfish) x86_64 (native bare-metal or high-performance Docker container).
- **Processor**: Minimum 8 physical CPU cores (16+ threads recommended for Bazel parallel action graph execution).
- **RAM**: Minimum 16 GB (32 GB strongly recommended, as linking 64-bit ARM Linux kernel images via `ld.lld` produces heavy peak memory consumption).
- **Storage**: Minimum 100 GB formatted with ext4 (NTFS over network shares is strictly unsupported due to Bazel's reliance on atomic symlink and hardlink operations).

### 2. Installing Required Host Toolchains:
Launch a shell on Ubuntu 22.04 and execute:

```bash
sudo apt update && sudo apt install -y \
  git git-lfs curl python3 python3-pip python3-setuptools \
  openjdk-17-jdk build-essential libncurses5 libssl-dev \
  bison flex rsync bc cpio libelf-dev zlib1g-dev

# Install Google Repo management utility
mkdir -p ~/.bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/.bin/repo
chmod a+rx ~/.bin/repo

# Export ~/.bin to user environment PATH
echo 'export PATH="$HOME/.bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify toolchain versions
git --version
python3 --version
repo version
```

---

## 3. Initializing and Synchronizing the Android Kernel Source Tree

### Step 1: Initialize Repo with Google's Common Kernel Manifest
Create a dedicated workspace and target the Android 17 LTS kernel release branch:

```bash
mkdir -p ~/android/kernel-rpi4
cd ~/android/kernel-rpi4

repo init \
  -u https://android.googlesource.com/kernel/manifest \
  -b common-android17-6.18-lts
```

### Step 2: Fetch the Raspberry Pi 4 Local Manifest
Retrieve the community device overlay manifest from the Raspberry Vanilla project to integrate BCM2711 SoC definitions:

```bash
curl -o .repo/local_manifests/manifest_brcm_rpi.xml \
  -L https://raw.githubusercontent.com/raspberry-vanilla/android_kernel_manifest/android-17.0/manifest_brcm_rpi.xml \
  --create-dirs
```

### Step 3: Refine Local Manifest Configuration for Lab Reproducibility
To ensure the kernel tree tracks the patched Raspberry Vanilla kernel branch and includes all required Broadcom Wi-Fi/Bluetooth firmware blobs, verify that `.repo/local_manifests/manifest_brcm_rpi.xml` aligns with the following structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <remote name="github" fetch="https://github.com/" />
    
    <!-- Replace Google generic kernel/common with Raspberry Pi patched kernel -->
    <remove-project name="kernel/common" />
    <project path="common"
             name="raspberry-vanilla/android_kernel_brcm_rpi"
             remote="github"
             revision="android-17.0" />
             
    <!-- Fetch proprietary Broadcom hardware firmware needed during packaging -->
    <project path="vendor/brcm"
             name="raspberry-vanilla/proprietary_vendor_brcm"
             remote="github"
             revision="android-17.0" />
</manifest>
```

### Step 4: Execute Repository Synchronization (Repo Sync)
```bash
# Synchronize repositories utilizing 4 concurrent network worker threads
repo sync -c -j4 --fail-fast
```

### Step 5: Lock the Manifest and Verify Git Commit Hashes
Immediately following synchronization, pin down the manifest (`locked-manifest.xml`) to record the exact commit revision of every dependent repository:

```bash
# Export frozen manifest
repo manifest -r -o locked-manifest.xml

# Inspect the HEAD commit of the common/ kernel repository
cd common
git log -1 --oneline
git rev-parse HEAD
cd ..
```

* **Verification Checkpoint**:
  ```text
  7a9131c1065a28544c1b6592152981b4c4102367
  ```
  This Git commit SHA-1 matches the exact SCM hash string `g7a9131c1065a` extracted from `uname -r` in Lesson 02.

---

## 4. Demystifying the Google Kleaf / Bazel Build System

Starting with Android 13, Google formally deprecated conventional `make`-based kernel compilation (`ARCH=arm64 CROSS_COMPILE=... make`) in favor of **Kleaf**.

Kleaf is a comprehensive set of build rules built on top of the **Bazel** multi-language build system, delivering 3 major engineering advancements:

<p align="center">
  <img src="images/bai02_kleaf_bazel_kernel_build_flow.svg" width="950" alt="Kleaf Bazel Hermetic Build Flow for Android Common Kernel">
</p>

### 1. Hermetic Clang Toolchain:
In traditional Embedded Linux, build outputs vary depending on host GCC or Clang packages installed on Ubuntu. With Kleaf, all Clang/LLVM compilers, `ld.lld`, and `llvm-objcopy` binaries are prebuilt dependencies checked directly into `prebuilts/clang/`. Bazel **never accesses the host system's compiler binaries**, ensuring 100% reproducible bit-for-bit builds across different workstations and CI/CD pipelines.

### 2. Hermetic Sandbox Isolation:
Every C compilation action is isolated inside an ephemeral directory known as the **Bazel Sandbox** (`/tmp/bazel-sandbox/...`).
- Inside the sandbox, source files can only access headers and libraries explicitly declared in the target's `BUILD.bazel` rule.
- Undeclared dependencies or attempts to read files outside the sandbox trigger an immediate build termination: `Action failed to make progress`.

### 3. Core Kleaf Build Rules:
- **`kernel_build`**: Orchestrates the entire kernel compilation pipeline, producing `vmlinux`, `Image`, Device Tree blobs (`.dtb`), and the critical symbol database `Module.symvers`.
- **`ddk_headers`**: Exports kernel internal header trees required for out-of-tree Device Driver Kit (DDK) modules.
- **`ddk_module`**: Compiles external `.c` sources into `.ko` loadable kernel modules.

---

## 5. Compiling the Raspberry Pi 4 Kernel with Kleaf

### 1. Resolving Broadcom Firmware Dependencies in Bazel Graph:
The `kernel_build` target for Raspberry Pi 4 packages the wireless regulatory database (`regulatory.db`). We declare this resource cleanly in `vendor/brcm/BUILD.bazel`:

```python
package(default_visibility = ["//visibility:public"])

filegroup(
    name = "rpi4_firmware",
    srcs = glob([
        "rpi4/proprietary/vendor/firmware/**",
    ]),
)
```

Ensure that `common/BUILD.bazel` references `//vendor/brcm:rpi4_firmware` within the `srcs` attribute of the `kernel_build(name = "rpi4")` target.

### 2. Invoking the Bazel Kernel Build Action:
Utilize the repository's bundled `tools/bazel` launcher:

```bash
# Build the complete kernel image and Device Tree blobs for Raspberry Pi 4
tools/bazel build \
  --config=fast \
  --config=stamp \
  //common:rpi4
```

* **Compilation Flag Analysis**:
  - `--config=fast`: Optimizes compilation throughput by skipping non-critical documentation checks.
  - `--config=stamp`: Activates Git SCM stamping to embed commit hash metadata into version descriptors.
  - `//common:rpi4`: Canonical target path within the Bazel workspace.

### 3. Inspecting Build Artifacts:
Upon completion (`Build completed successfully`), build outputs reside within the `bazel-bin/` symlink tree:

```bash
# Inspect generated kernel and Device Tree binaries
ls -lh bazel-bin/common/rpi4/arch/arm64/boot/Image
ls -lh bazel-bin/common/rpi4/arch/arm64/boot/dts/broadcom/bcm2711-rpi-4-b.dtb

# Inspect kernel symbol version database
ls -lh bazel-bin/common/rpi4/Module.symvers
```

The `Module.symvers` symbol database contains the 32-bit CRC hashes of all exported kernel functions, serving as the cornerstone for binary compatibility in Lesson 04!

---

## 6. Self-Assessment & Engineering Exercises

1. **Sandbox Dependency Analysis**: Why might a kernel module source `#include <linux/compiler-version.h>` build without issue when invoked through standalone host `make`, but fail abruptly under Kleaf Bazel if the rule lacks `//common:all_headers_aarch64`?
2. **Auditing `Module.symvers`**: View the first 20 lines of `bazel-bin/common/rpi4/Module.symvers` using `head -n 20`. What is the structural format and semantic meaning of each column in this file?
3. **Inspecting Target Defconfig**: Inspect `common/arch/arm64/configs/android_rpi4_defconfig`. Which string literal is assigned to `CONFIG_LOCALVERSION`, and how does it propagate into the final vermagic?
