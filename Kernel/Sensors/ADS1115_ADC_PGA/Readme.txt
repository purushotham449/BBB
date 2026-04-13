ADS1115 (16-bit, 4-channel I²C ADC) on your BeagleBone Black Wireless (BBBW) with Kernel + DTS + Python userspace.

1) Hardware Connections (BBBW)

    | ADS1115 | BBBW                     |
    | ------- | ------------------------ |
    | VDD     | 3.3V                     |
    | GND     | GND                      |
    | SDA     | P9_20 (I2C2 SDA)         |
    | SCL     | P9_19 (I2C2 SCL)         |
    | ADDR    | GND → **0x48** (default) |

Analog inputs:

    A0–A3 → your sensors (0–3.3V recommended)

    ⚠️ Keep input ≤ VDD. If your board is powered at 5V, ensure inputs never exceed the BBBW’s safe range (use dividers if needed).

2) Verify I²C
        i2cdetect -y 2

    Expected:

        48

    (Other options: 0x49/0x4A/0x4B depending on ADDR wiring)

3) Kernel Support (IIO)

ADS1115 is supported by IIO driver.

Kernel config

    CONFIG_IIO=y
    CONFIG_TI_ADS1015=y   # covers ADS1015/ADS1115

menuconfig path
    Device Drivers →
        Industrial I/O support →
            Analog to digital converters →
                TI ADS1015/ADS1115

4) Device Tree (DTS)

    Add to your BBBW DTS:

    &i2c2 {
        status = "okay";

        ads1115@48 {
            compatible = "ti,ads1115";
            reg = <0x48>;

            #address-cells = <1>;
            #size-cells = <0>;

            channel@0 {
                reg = <0>;
            };
            channel@1 {
                reg = <1>;
            };
            channel@2 {
                reg = <2>;
            };
            channel@3 {
                reg = <3>;
            };
        };
    };

5) Build & Boot
    bitbake -c clean virtual/kernel
    bitbake virtual/kernel

6) Verify Driver
    dmesg | grep ads1115

    Expected:

        ads1115 2-0048: registered

7) Sysfs (IIO)
    ls /sys/bus/iio/devices/

    Example:

        iio:device2

    Read channels
        cat /sys/bus/iio/devices/iio:device2/in_voltage0_raw
        cat /sys/bus/iio/devices/iio:device2/in_voltage1_raw
        cat /sys/bus/iio/devices/iio:device2/in_voltage2_raw
        cat /sys/bus/iio/devices/iio:device2/in_voltage3_raw
        Scale (important)
        cat /sys/bus/iio/devices/iio:device2/in_voltage_scale

    👉 Convert:

        Voltage = raw * scale

    Run
        sudo python3 ads1115_monitor.py

    Example Output
    
        ADS1115 Continuous Monitor
        ---------------------------
        CH0: RAW=12345  VOLT=1.5432 V
        CH1: RAW= 5321  VOLT=0.6651 V
        CH2: RAW= 1023  VOLT=0.1280 V
        CH3: RAW=16000  VOLT=2.0000 V
