# LESSON 04: DEMYSTIFYING VERMAGIC, MODVERSIONS AND LAB 1 HELLO WORLD KERNEL MODULE

> Summary: In-depth analysis of Linux kernel binary compatibility mechanisms (Vermagic & CONFIG_MODVERSIONS), mastering SCM Stamping to eliminate the '-maybe-dirty' suffix, and building, loading, and verifying your first out-of-tree Hello World Kernel Module on Android 17 / Raspberry Pi 4 using Google Kleaf Bazel.

---

## 1. Secrets of Kernel Binary Compatibility: Vermagic & SCM Stamping

When invoking `insmod` to load a kernel module binary (`.ko`) into Android, the Linux kernel does not immediately execute code. Instead, it activates a sequential pipeline of strict binary verification checks:

<p align="center">
  <img src="images/bai04_module_binary_verification_pipeline.svg" width="950" alt="Binary Compatibility Verification Pipeline for Loadable Kernel Modules">
</p>

### 1.1. Anatomizing the Vermagic (Version Magic) String
The `vermagic` string is an ASCII descriptor embedded within the `.modinfo` ELF section of a compiled `.ko` file. It is assembled from 4 key components:

```text
6.18.38-g7a9131c1065a-v8 SMP preempt mod_unload modversions aarch64
|______| |___________| |_| |_______________________________________|
   |           |        |                      |
Base Version  SCM-Hash LocalVer          Kernel Feature Flags
```

1. **Base Kernel Version**: `6.18.38` (Derived from top-level kernel `Makefile`: `VERSION`, `PATCHLEVEL`, `SUBLEVEL`).
2. **SCM Revision Tag**: `-g7a9131c1065a` (Identifies the authoritative Git commit hash).
3. **Local Version Suffix**: `-v8` (Configured in target architecture `CONFIG_LOCALVERSION`).
4. **Architectural & Feature Configuration Flags**:
   - `SMP`: Symmetric Multiprocessing enabled.
   - `preempt`: Real-time kernel preemption model active.
   - `mod_unload`: Dynamic runtime module unloading supported.
   - `modversions`: 32-bit CRC symbol versioning enforced.
   - `aarch64`: Target CPU architecture (64-bit ARMv8-A).

---

## 2. Classic Trap: The `-maybe-dirty` Suffix & SCM Stamping Engineering

When building external modules using Kleaf Bazel for the first time, engineers frequently encounter module rejection with the following kernel diagnostic:

```text
insmod: failed to load hello_android.ko: Exec format error
dmesg: version magic '6.18.38-maybe-dirty-v8' should be '6.18.38-g7a9131c1065a-v8'
```

### Why Does `-maybe-dirty` Appear?
The Linux kernel Kbuild infrastructure relies on the `scripts/setlocalversion` script. When this script detects uncommitted changes in Git or detects that source files are being built outside a conventional Git tree (which is precisely the case inside Bazel's hermetic sandbox), it appends `-dirty` or `-maybe-dirty` to signal an untracked engineering build.

### Production Solution: Kleaf SCM Stamping Override
To eliminate this discrepancy and achieve bit-for-bit synchronization with the running target kernel, we leverage Google Kleaf's official **SCM Stamping Override** mechanism:

Create the file `common/workspace_status.json`:
```json
{
    "SCMVERSION": "-g7a9131c1065a"
}
```

When invoking the Bazel build command, pass the `--config=stamp` flag paired with the locked manifest reference:
```bash
tools/bazel build \
  --config=stamp \
  --repo_manifest="$(realpath .):$(realpath locked-manifest.xml)" \
  //labs/hello_android:hello_android
```

> [!CAUTION]
> **Engineering Rigor & System Safety Warning:**
> Never attempt to hex-edit the `vermagic` string inside a compiled `.ko` binary to bypass version checks. Forcing the kernel to load a module compiled against mismatched headers causes struct padding alignment divergence, leading to fatal memory corruption and sudden kernel panics!

---

## 3. Symbol CRC Hash Verification Mechanism (`CONFIG_MODVERSIONS`)

When `CONFIG_MODVERSIONS=y` is set, the toolchain generates a mathematical **32-bit CRC checksum** for every function prototype and data structure exported by the kernel and consumed by the module (e.g., `_printk`, `module_layout`). These hashes are stored inside the `__versions` section of the `.ko` ELF binary.

```bash
# Inspect symbol version dependencies embedded in the module
llvm-readelf -s bazel-bin/labs/hello_android/hello_android/hello_android.ko | grep -E 'printk|module_layout'
```

During `insmod`, the kernel matches these CRC hashes against its active runtime symbol table (`/proc/kallsyms` and `Module.symvers`). Only if all symbol signatures match with 100% mathematical fidelity is the module permitted into kernel memory space (Ring 0 / EL1).

---

## 4. Lab 1: Building Hello World Kernel Module with Bazel DDK

### Step 1: Authoring the Module C Source Code
Create the directory `labs/hello_android` within your kernel workspace:

```bash
mkdir -p labs/hello_android
```

Create `labs/hello_android/hello_android.c`:

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

// Initialization entry point - Executed when module is loaded via insmod
static int __init hello_android_init(void)
{
    pr_info("hello_android: ========================================\n");
    pr_info("hello_android: Hello Android Kernel! SoC BCM2711 RPi4\n");
    pr_info("hello_android: Module running on Linux 6.18 AOSP 17\n");
    pr_info("hello_android: ========================================\n");
    return 0; // Return 0 signals successful initialization
}

// Exit cleanup point - Executed when module is unloaded via rmmod
static void __exit hello_android_exit(void)
{
    pr_info("hello_android: Goodbye Android Kernel! Cleaned up successfully.\n");
}

// Register lifecycle entry points with Linux kernel core
module_init(hello_android_init);
module_exit(hello_android_exit);

// Mandatory module metadata declarations
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Embedded-AIoT Lab PTIT");
MODULE_DESCRIPTION("First Out-of-tree Android Kernel Module built with Bazel Kleaf");
MODULE_VERSION("1.0.0");
```

### Step 2: Defining the `BUILD.bazel` Build Target
Create `labs/hello_android/BUILD.bazel`:

```python
load("@kleaf//build/kernel/kleaf:kernel.bzl", "ddk_module")

ddk_module(
    name = "hello_android",
    srcs = ["hello_android.c"],
    out = "hello_android.ko",
    kernel_build = "//common:rpi4",
    deps = [
        # Include full 64-bit ARM architecture headers to avoid missing compiler-version.h
        "//common:all_headers_aarch64",
    ],
)
```

### Step 3: Compiling the Module
Execute the build command from the root of your kernel workspace:

```bash
tools/bazel build \
  --config=stamp \
  --repo_manifest="$(realpath .):$(realpath locked-manifest.xml)" \
  //labs/hello_android:hello_android
```

* **Inspect the Generated Binary**:
  ```bash
  ls -lh bazel-bin/labs/hello_android/hello_android/hello_android.ko
  file bazel-bin/labs/hello_android/hello_android/hello_android.ko
  ```

* **Verify the Vermagic String Prior to Deployment**:
  ```bash
  strings bazel-bin/labs/hello_android/hello_android/hello_android.ko | grep '^vermagic='
  ```
  Expected output:
  ```text
  vermagic=6.18.38-g7a9131c1065a-v8 SMP preempt mod_unload modversions aarch64
  ```

---

## 5. Deploying, Loading, and Unloading the Module via ADB

### Step 1: Push the Binary to the Target Device
On an Android `userdebug` build, `/data/local/tmp` provides read, write, and execute permissions suitable for developer staging:

```bash
adb push bazel-bin/labs/hello_android/hello_android/hello_android.ko /data/local/tmp/
```

### Step 2: Load the Module into Kernel Space
Spawn an authenticated root shell on the target:

```bash
adb root
adb shell

# Inside the Android root shell:
cd /data/local/tmp
insmod hello_android.ko
```

### Step 3: Inspect Module Registry and Kernel Ring Buffer (`dmesg`)
```bash
# Verify presence in kernel loaded modules table
lsmod | grep hello_android

# Inspect kernel ring buffer output
dmesg | grep hello_android
```

* **Observed Target System Kernel Log**:
  ```text
  hello_android: loading out-of-tree module taints kernel.
  hello_android: module verification failed: signature and/or required key missing - tainting kernel
  hello_android: ========================================
  hello_android: Hello Android Kernel! SoC BCM2711 RPi4
  hello_android: Module running on Linux 6.18 AOSP 17
  hello_android: ========================================
  ```

### 5.1. Analyzing Kernel Diagnostic Messages:
1. `loading out-of-tree module taints kernel`:
   - This diagnostic is **completely expected**. The Linux kernel sets a taint flag (`O` - Out-of-tree) recording that the module was built outside the mainline source repository.
2. `module verification failed: signature and/or required key missing`:
   - Signals that the module was not signed with the distribution vendor's private cryptographic key. Because `sig_enforce=N`, the kernel logs an unsigned taint flag (`E`) without blocking module initialization.
3. `Hello Android Kernel!`:
   - Confirms that `hello_android_init()` executed in privileged kernel space (Ring 0 / EL1) on the Raspberry Pi 4.

### Step 4: Unloading the Module from Kernel Memory
```bash
# Unload module
rmmod hello_android

# Confirm removal from active module list
lsmod | grep hello_android

# Verify cleanup log message
dmesg | tail -n 20 | grep hello_android
```

* **Expected Confirmation**:
  ```text
  hello_android: Goodbye Android Kernel! Cleaned up successfully.
  ```

---

## 6. Self-Assessment & Engineering Exercises

1. **Intentional Vermagic Discrepancy Experiment**: Modify `common/workspace_status.json` with an incorrect commit hash (e.g., `-g111122223333`), recompile the module, and attempt to load it on the Raspberry Pi 4 via `insmod`. What specific error code does `insmod` return, and what diagnostic appears in `dmesg`?
2. **Module Parameters Implementation**: Extend `hello_android.c` using the macro `module_param(led_pin, int, 0644)` to accept a target GPIO pin number as a parameter at load time (`insmod hello_android.ko led_pin=17`).
3. **Kernel Memory Footprint Analysis**: Use `adb shell cat /proc/modules` to determine the exact memory footprint (in bytes) and the base virtual address allocated to `hello_android` while loaded in memory.
