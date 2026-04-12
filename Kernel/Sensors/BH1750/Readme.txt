| BH1750 | BBBW             |
| ------ | ---------------- |
| VCC    | 3.3V             |
| GND    | GND              |
| SDA    | I2C2 SDA (P9_20) |
| SCL    | I2C2 SCL (P9_19) |

Default I2C address:

    0x23 (ADDR pin LOW)
    0x5C (ADDR HIGH)

2. Verify Detection

    i2cdetect -y 2

Expected:

        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:                         -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- 23 -- -- -- -- -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- --

3. Device Tree (DTS)

    Add to your board DTS:

        &i2c2 {
            status = "okay";

            bh1750@23 {
                compatible = "rohm,bh1750";
                reg = <0x23>;
            };
        };

4. Kernel Config

    BH1750 uses IIO (Industrial I/O) subsystem.

    Enable:

        CONFIG_IIO=y
        CONFIG_BH1750=y

    If using menuconfig:
        bitbake -c menuconfig virtual/kernel

    Navigate:

        Device Drivers →
        Industrial I/O support →
            Light sensors →
            BH1750 ambient light sensor

5. Build & Boot
    bitbake virtual/kernel

Boot and verify:

    dmesg | grep bh1750

    Expected:

        bh1750 2-0023: registered

6. Sysfs Interface (Userspace)

Check device name
    cat /sys/bus/iio/devices/iio:device0/name

    Expected:

        bh1750

Read RAW value
    cat /sys/bus/iio/devices/iio:device0/in_illuminance_raw

Read scale
    cat /sys/bus/iio/devices/iio:device0/in_illuminance_scale

👉 Value = lux

Convert to lux
    lux = raw * scale

Quick one-liner:
    awk '{r=$1} NR==2{printf "Lux: %.2f\n", r*$1}' \
    /sys/bus/iio/devices/iio:device0/in_illuminance_raw \
    /sys/bus/iio/devices/iio:device0/in_illuminance_scale
    
    Example Output
        raw = 120
        scale = 1.200000

    Lux = 144.00

Expected Values

    Environment	    Lux
    Dark room	    0–10
    Indoor	        100–500
    Office	        300–1000
    Sunlight	    10,000+

