Complete VL53L0X (laser ToF distance sensor) + BBBW setup: Kernel + DTS + Python userspace

1. Hardware Connection (BBBW)

    | VL53L0X | BBBW             |
    | ------- | ---------------- |
    | VCC     | 3.3V             |
    | GND     | GND              |
    | SDA     | P9_20 (I2C2 SDA) |
    | SCL     | P9_19 (I2C2 SCL) |

👉 Default I2C address: 0x29

2. Verify Detection

    i2cdetect -y 2

    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- 29 -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --

3. Kernel Support

    VL53L0X is supported via IIO subsystem.

Kernel Config
    CONFIG_IIO=y
    CONFIG_VL53L0X_I2C=y

menuconfig path

    Device Drivers →
        Industrial I/O support →
            Distance sensors →
                VL53L0X laser ranger

4. Device Tree (DTS)

Add to your BBBW DTS:

&i2c2 {
    status = "okay";

    vl53l0x@29 {
        compatible = "st,vl53l0x";
        reg = <0x29>;
    };
};

5. Build & Boot
    bitbake -c clean virtual/kernel
    bitbake virtual/kernel

6. Verify Driver
    dmesg | grep vl53

Expected:

    vl53l0x 2-0029: registered

7. Sysfs Interface
    ls /sys/bus/iio/devices/

    Example:

        iio:device1

    Read Distance
        cat /sys/bus/iio/devices/iio:device1/in_distance_raw

    👉 Output in millimeters

