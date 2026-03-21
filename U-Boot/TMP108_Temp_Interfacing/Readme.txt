Let’s go step-by-step from hardware Let’s go step-by-step from hardware → I2C → U-Boot test

TMP108 Pins

| TMP108 Pin | Connection           |
| ---------- | -------------------- |
| VCC        | 3.3V (P9_3 or P9_4)  |
| GND        | GND (P9_1 or P9_2)   |
| SDA        | P9_20 (I2C2_SDA)     |
| SCL        | P9_19 (I2C2_SCL)     |
| ADD0       | GND (address = 0x48) |

Important
    Use 3.3V ONLY (not 5V)
    Ensure pull-up resistors (4.7kΩ) on SDA/SCL
    (BBBW usually has onboard pull-ups, but external is safer)

I2C Address (TMP108)
    Default address = 0x48

Test in U-Boot (No coding needed)
    
    Step 1: Select I2C bus
        => i2c dev 0
    Step 2: Scan bus
        => i2c probe

    Expected:
        48

        👉 If you see 48 → sensor detected ✅

But U-Boot expects:

        chip address[.offset] count

        ✔ Correct syntax:
            => i2c md 0x48 0x00.1 2

        ✔ Example Output
            0000: 1A C0

Convert to Temperature

        Raw:
            1A C0 → 0x1AC0

        Shift:
            0x1AC0 >> 4 = 0x1AC = 428

        Convert:
            428 × 0.0625 = 26.75°C

        Bit-Level Breakdown
            TMP108 (16-bit register)

            |15      4|3     0|
            | Temp MSB | Fraction |

        Example:
            0001 1010 1100 0000

        After shift:
            0001 1010 1100 → 428

Register Map

| Register      | Address | Size   | Description         |
| ------------- | ------- | ------ | ------------------- |
| Temperature   | `0x00`  | 16-bit | Current temperature |
| Configuration | `0x01`  | 16-bit | Settings            |
| T_LOW         | `0x02`  | 16-bit | Low threshold       |
| T_HIGH        | `0x03`  | 16-bit | High threshold      |
| Device ID     | `0x0F`  | 16-bit | ID register         |

Temperature Register (IMPORTANT)

    Register:
        0x00 → 16-bit value

    Format:
        MSB      LSB
        [15:4]   [3:0]
        Temp     Fraction

    👉 12-bit resolution

1️⃣ Temperature Register (0x00)

    0000: 1C E0
    Step-by-step decode
    Raw = 0x1CE0
    Shift = 0x1CE0 >> 4 = 0x1CE = 462
    Temp = 462 × 0.0625 = 28.875°C

    ✅ Temperature ≈ 28.88°C

2️⃣ Configuration Register (0x01)

    0001: 60 A0 → 0x60A0
    Bit breakdown (important fields)
    [15:13] = Conversion rate
    [12]    = Shutdown mode
    [11:10] = Thermostat mode
    [9]     = Polarity
    [8]     = Alert
    Decode:
        0x60A0 = 0110 0000 1010 0000

    Conversion rate → 011 → 8 Hz (typical)
    Shutdown → 0 → Continuous mode
    Thermostat → comparator mode

    ✅ Device is running in continuous conversion mode

3️⃣ T_LOW Register (0x02)
    
    0002: 4B 00 → 0x4B00
    0x4B00 >> 4 = 0x4B0 = 1200
    1200 × 0.0625 = 75°C

    ✅ T_LOW = 75°C

4️⃣ T_HIGH Register (0x03)

    0003: 50 00 → 0x5000
    0x5000 >> 4 = 0x500 = 1280
    1280 × 0.0625 = 80°C

    ✅ T_HIGH = 80°C

5️⃣ Device ID Register (0x0F)

    000f: 00 00

    👉 This is interesting ⚠️

    Expected (from datasheet)

    TMP108 usually returns a non-zero ID