# LESSON 02: DEEP-DIVE GPIO ARCHITECTURE AND BIT-BANDING TECHNIQUE

Welcome to the second lesson in the **Deep-Dive STM32F103 Programming Masterclass**. In Lesson 01, we explored basic GPIO output control to toggle an LED. In this lesson, we will dissect the internal electronic architecture of the General Purpose I/O peripheral, understand its specialized operating modes, and leverage a core feature of the ARM Cortex-M3 processor: **Bit-Banding Addressing Technique (Atomic Bit Manipulation)**.

---

## 1. Internal Physical Architecture of STM32F103 GPIO Pin

To master GPIO at the embedded hardware engineer level, a pin cannot simply be treated as an abstract "Input" or "Output". You must understand the integrated transistor schematic inside the microcontroller silicon:

<p align="center">
  <img src="images/bai02_gpio_structure.svg" width="900" alt="Internal Electronic Structure of STM32F103 GPIO Pin">
</p>

### 1.1 Input Protection Diodes
Every I/O pin integrates two clamping diodes for Electrostatic Discharge (ESD) protection:
- One diode connects up to VDD (3.3V) and one diode connects down to VSS (GND).
- **5V-Tolerant (FT) Pin Considerations**: Pins marked as **FT** in the device datasheet (e.g., PA8, PB6, PB7...) do not feature the conventional upper diode tied to VDD 3.3V. Instead, they use a specialized protection structure that safely tolerates 5V logic inputs when configured in Input Floating or Open-Drain mode.

### 1.2 Output Driver Stage: Push-Pull vs Open-Drain

1. **Push-Pull Output Mode**:
   - Employs both **P-MOS** (pulling up to VDD) and **N-MOS** (pulling down to VSS) transistors in complementary configuration.
   - When driving logic `1`: P-MOS conducts, N-MOS is cut off → The pin **sources** current from VDD.
   - When driving logic `0`: N-MOS conducts, P-MOS is cut off → The pin **sinks** current into GND.
   - *Applications*: Direct LED driving, high-speed SPI clock generation, chip select (CS) pins, and general logic signals.

2. **Open-Drain Output Mode**:
   - The P-MOS transistor is permanently disabled; only the **N-MOS** transistor is active.
   - When driving logic `0`: N-MOS conducts → The pin pulls strongly down to GND.
   - When driving logic `1`: N-MOS is cut off → The pin floats in **High-Impedance (Hi-Z)** state. Generating a high level requires an external pull-up resistor.
   - *Applications*: Shared multi-drop bidirectional communication buses such as I2C (SDA, SCL), 1-Wire, and voltage level shifting (e.g., interfacing 3.3V logic to 5V systems).

### 1.3 Schmitt Trigger & Input Data Sampling
- External analog input signals pass through a Schmitt Trigger stage to eliminate noise and debounce slow-transitioning edges, converting them into clean digital `0` or `1` logic levels.
- The digital state is sampled and latched into the **`GPIOx_IDR`** register on every cycle of the APB2 peripheral clock.

---

## 2. GPIO Registers According to Reference Manual RM0008

Each GPIO port (from GPIOA to GPIOG) manages up to 16 physical pins (Pin 0 → Pin 15), controlled via seven dedicated 32-bit registers:

| Register | Full Name | Offset | Functional Description |
| :--- | :--- | :---: | :--- |
| **`GPIOx_CRL`** | Port Configuration Register Low | `0x00` | Configures Pin 0 through Pin 7 (4 bits / pin) |
| **`GPIOx_CRH`** | Port Configuration Register High | `0x04` | Configures Pin 8 through Pin 15 (4 bits / pin) |
| **`GPIOx_IDR`** | Input Data Register | `0x08` | Reads input logic states (Read-Only) |
| **`GPIOx_ODR`** | Output Data Register | `0x0C` | Reads/writes output logic states |
| **`GPIOx_BSRR`**| Bit Set/Reset Register | `0x10` | Atomically sets or clears pin states |
| **`GPIOx_BRR`** | Bit Reset Register | `0x14` | Atomically clears pin states |
| **`GPIOx_LCKR`**| Port Configuration Lock Register | `0x18` | Locks pin configuration until subsequent MCU reset |

### 2.1 4-bit Configuration Matrix: `CNF[1:0]` and `MODE[1:0]`
To configure any given pin, 4 bits in either `CRL` or `CRH` must be specified:

| MODE[1:0] (Direction / Speed) | CNF[1:0] when MODE = 00 (Input) | CNF[1:0] when MODE > 00 (Output) |
| :---: | :--- | :--- |
| `00`: Input mode (Reset default) | `00`: Analog mode | `00`: General Purpose Output Push-Pull |
| `01`: Output mode, max speed 10MHz | `01`: Floating input | `01`: General Purpose Output Open-Drain |
| `10`: Output mode, max speed 2MHz | `10`: Input with Pull-up / Pull-down | `10`: Alternate Function Output Push-Pull |
| `11`: Output mode, max speed 50MHz | `11`: Reserved | `11`: Alternate Function Output Open-Drain |

> [!NOTE]
> **Distinguishing Internal Pull-Up vs Pull-Down in Input Mode:**
> When selecting `MODE = 00` and `CNF = 10` (Input with pull-up/pull-down):
> - Writing `ODR = 1`: Activates the internal **Pull-Up** resistor (weak tie to 3.3V).
> - Writing `ODR = 0`: Activates the internal **Pull-Down** resistor (weak tie to 0V).

---

## 3. Bit-Banding Technique in ARM Cortex-M3 Architecture

In real-time multitasking or single-core systems, traditional Read-Modify-Write bit operations on peripheral registers require multiple instructions:
```c
GPIOC->ODR |= (1 << 13); // 1. Read ODR -> 2. Bitwise OR -> 3. Write back to ODR
```
This sequence costs **3 assembly instruction cycles (`LDR`, `ORR`, `STR`)**. If an interrupt arrives between `LDR` and `STR`, the register value can be corrupted, triggering a critical race condition.

To eliminate this overhead at the hardware level, ARM Cortex-M3 integrates a **Bit-Banding Memory Architecture**:
- Each **single individual bit** in the standard memory region (Bit-Band Region) is mapped directly to an **entire 32-bit word** in the alias memory region (Bit-Band Alias Region).
- Writing `0` or `1` to this 32-bit alias address causes the memory bus logic to modify that single target bit in the original register **within a single atomic CPU cycle**!

<p align="center">
  <img src="images/bai02_bit_banding.svg" width="850" alt="ARM Cortex-M3 Bit-Banding Memory Mapping Mechanism">
</p>

### 3.1 Bit-Banding Address Calculation Formula

Cortex-M3 specifies two bit-band regions:
1. **SRAM Bit-band Region**: `0x2000 0000` → `0x200F FFFF` (1MB RAM) mapped to Alias: `0x2200 0000` → `0x23FF FFFF` (32MB).
2. **Peripheral Bit-band Region**: `0x4000 0000` → `0x400F FFFF` (1MB Peripherals) mapped to Alias: `0x4200 0000` → `0x43FF FFFF` (32MB).

The general mathematical formula is:
`Alias_Address = Alias_Base + (Byte_Offset × 32) + (Bit_Number × 4)`

Where:
- For STM32 peripherals (GPIO, Timers, USART...): `Alias_Base = 0x42000000`.
- `Byte_Offset = Peripheral_Register_Address - 0x40000000`.
- `Bit_Number = 0 → 31`.

### 3.2 Standard C Bit-Banding Macro
```c
#define BITBAND_PERI_BASE  0x40000000
#define BITBAND_ALIAS_BASE 0x42000000

#define BITBAND_PERI(RegAddr, Bit) \
    ((volatile uint32_t *)(BITBAND_ALIAS_BASE + (((uint32_t)(RegAddr) - BITBAND_PERI_BASE) * 32) + ((Bit) * 4)))
```

Calculation example for output pin PC13 on register `GPIOC_ODR` (`0x4001100C`):
- Byte Offset = `0x4001100C` - `0x40000000` = `0x1100C` = 69,644 bytes.
- Bit = 13.
- `Alias_Address` = `0x42000000` + (69644 × 32) + (13 × 4) = `0x42000000` + `0x220180` + `0x34` = `0x422201B4`.

Controlling the pin requires only a direct pointer write:
```c
*((volatile uint32_t *)0x422201B4) = 0; // PC13 = 0 -> Turns ON Active-Low LED
*((volatile uint32_t *)0x422201B4) = 1; // PC13 = 1 -> Turns OFF Active-Low LED
```

---

## 4. Push Button Interfacing & Debouncing Algorithm

When a mechanical button is pressed or released, the physical spring contacts bounce repeatedly, generating rapid erratic voltage spikes over a window of 5ms to 20ms before settling:

<p align="center">
  <img src="images/bai02_button_debounce.svg" width="850" alt="Mechanical Push Button Bouncing and Software Debounce Filter">
</p>

Without debounce filtering, a 72MHz microcontroller will interpret those oscillations as dozens of independent key presses.

### Time-Sampling Software Debounce Algorithm:
1. Sample current button logic state.
2. If state transition is detected, wait for a stabilization interval (15ms - 20ms).
3. Sample the pin again: if the logic level is maintained, confirm the key press as valid.

---

## 5. Practical Hands-On Source Code Implementation

### Experimental Setup:
- On-board User LED connected to pin **PC13** (Active-Low).
- External Push Button connected to pin **PA0**: One terminal to PA0, one terminal to GND.
- Configure PA0 in **Input Pull-Up** mode (released = 1, pressed = 0).
- Each valid button press toggles the state of LED PC13.

---

### METHOD 1: BARE-METAL REGISTER PROGRAMMING WITH BIT-BANDING

File: `main.c`

```c
#include "stm32f10x.h"

// Peripheral bit-band alias base addresses
#define BITBAND_PERI_BASE  0x40000000
#define BITBAND_ALIAS_BASE 0x42000000

#define BITBAND_PERI(RegAddr, Bit) \
    ((volatile uint32_t *)(BITBAND_ALIAS_BASE + (((uint32_t)(RegAddr) - BITBAND_PERI_BASE) * 32) + ((Bit) * 4)))

// Atomic bit-band pointers for GPIO pins
#define PC13_OUT  (*BITBAND_PERI(&GPIOC->ODR, 13))
#define PA0_IN    (*BITBAND_PERI(&GPIOA->IDR, 0))

void delay_ms(volatile uint32_t ms)
{
    volatile uint32_t i;
    for (; ms > 0; ms--)
    {
        for (i = 0; i < 7200; i++)
        {
            __NOP();
        }
    }
}

void GPIO_Init_Register(void)
{
    // 1. Enable peripheral bus clocks for PORT A and PORT C via RCC_APB2ENR
    RCC->APB2ENR |= (1 << 2) | (1 << 4); // Bit 2: IOPAEN, Bit 4: IOPCEN

    // 2. Configure PC13: General Purpose Output Push-Pull at 2MHz maximum speed
    GPIOC->CRH &= ~(0x0F << 20); // Clear bits [23:20]
    GPIOC->CRH |= (0x02 << 20);  // MODE13 = 10 (Output 2MHz), CNF13 = 00 (Push-Pull)

    // Initial state: turn off LED (write HIGH)
    PC13_OUT = 1;

    // 3. Configure PA0: Input with Pull-Up
    GPIOA->CRL &= ~(0x0F << 0);  // Clear bits [3:0]
    GPIOA->CRL |= (0x08 << 0);   // MODE0 = 00 (Input), CNF0 = 10 (Input Pull-up/down)
    GPIOA->ODR |= (1 << 0);      // ODR0 = 1 -> Select internal PULL-UP resistor
}

int main(void)
{
    GPIO_Init_Register();

    while (1)
    {
        // Check button state on PA0 (Active-Low when pressed to GND)
        if (PA0_IN == 0)
        {
            delay_ms(20); // Key debounce delay
            if (PA0_IN == 0) // Confirm button is still held down
            {
                // Toggle LED PC13 atomically using Bit-Banding
                PC13_OUT = !PC13_OUT;

                // Wait for button release to prevent continuous toggling
                while (PA0_IN == 0);
                delay_ms(20); // Button release debounce delay
            }
        }
    }
}
```

---

### METHOD 2: STANDARD PERIPHERAL LIBRARY (SPL)

File: `main.c`

```c
#include "stm32f10x.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_gpio.h"

void delay_ms(volatile uint32_t ms)
{
    volatile uint32_t i;
    for (; ms > 0; ms--)
    {
        for (i = 0; i < 7200; i++)
        {
            __NOP();
        }
    }
}

void GPIO_Configuration(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;

    // 1. Enable peripheral clocks for GPIOA and GPIOC
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_GPIOC, ENABLE);

    // 2. Configure PC13 pin: Output Push-Pull 2MHz
    GPIO_InitStructure.GPIO_Pin   = GPIO_Pin_13;
    GPIO_InitStructure.GPIO_Mode  = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_2MHz;
    GPIO_Init(GPIOC, &GPIO_InitStructure);

    // Default: turn off LED
    GPIO_SetBits(GPIOC, GPIO_Pin_13);

    // 3. Configure PA0 pin: Input Pull-Up
    GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_0;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; // Input Pull-Up
    GPIO_Init(GPIOA, &GPIO_InitStructure);
}

int main(void)
{
    GPIO_Configuration();

    while (1)
    {
        // Read PA0 input state
        if (GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_0) == Bit_RESET)
        {
            delay_ms(20); // Button debounce filter
            if (GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_0) == Bit_RESET)
            {
                // Toggle PC13 by reading ODR and writing inverted state
                if (GPIO_ReadOutputDataBit(GPIOC, GPIO_Pin_13) == Bit_SET)
                {
                    GPIO_ResetBits(GPIOC, GPIO_Pin_13); // Turn on LED
                }
                else
                {
                    GPIO_SetBits(GPIOC, GPIO_Pin_13);   // Turn off LED
                }

                // Wait for key release
                while (GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_0) == Bit_RESET);
                delay_ms(20);
            }
        }
    }
}
```

---

## 6. Common Pitfalls and Hardware Warnings

> [!WARNING]
> **1. Forgetting to Enable the APB2 Bus Clock:**
> If you fail to set bit `IOPAEN` or `IOPCEN` in the `RCC->APB2ENR` register, writes to `CRL`, `CRH`, and `ODR` will be discarded by the peripheral bus controller, leaving the pins inactive.

> [!IMPORTANT]
> **2. Accidentally Reconfiguring JTAG / SWD Pins (PA13, PA14, PA15, PB3, PB4):**
> Following system reset, these pins are assigned by hardware to JTAG/SWD debug functionality:
> - **PA13**: JTMS / SWDIO
> - **PA14**: JTCK / SWCLK
> - **PB3**: JTDO (requires AFIO remap to release for GPIO use)
> - **PB4**: JNTRST
> If PA13 or PA14 is reconfigured as general GPIO without keeping SWD enabled, communication with the ST-Link V2 probe will be lost. Recovering requires pulling the BOOT0 jumper HIGH or holding the hardware RESET button during flash programming.

---

## 7. Debugging in Keil MDK

1. Press `Ctrl + F5` to launch a Debug Session.
2. Open **Watch 1** (`View -> Watch Windows -> Watch 1`).
3. Add bit-banding expressions: `PA0_IN` and `PC13_OUT`.
4. Open the peripheral register viewer: **Peripherals -> General Purpose I/O -> GPIOA** and **GPIOC**.
5. Press `F10` to step over instructions:
   - When grounding PA0, observe bit `IDR0` toggle from `1` to `0`.
   - Observe bit `ODR13` change state accordingly on GPIOC.

---

## 8. Practical Exercises

1. **Exercise 1 (SRAM Bit-Banding)**: Declare a 32-bit state flag in RAM `uint32_t system_flags = 0;`. Write a Bit-Banding macro expression to access and set bit 7 to `1` without affecting any other bits.
2. **Exercise 2 (Multi-Mode Push Button)**: Using PA0 as a single push button, write a program distinguishing between:
   - **Short Press (< 500ms)**: LED PC13 blinks once.
   - **Long Press (> 1000ms)**: LED PC13 blinks continuously at 5Hz frequency.
3. **Exercise 3 (Open-Drain & Level Shifting)**: Configure PB7 in Open-Drain output mode at 10MHz speed. Connect PB7 to an external 5V supply through a 4.7kΩ pull-up resistor. Use a multimeter or oscilloscope to measure PB7 when outputting logic `0` and `1` to verify clean 5V level translation.
