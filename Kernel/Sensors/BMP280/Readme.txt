What BMP280 Provides

    Parameter	            Description
    🌡 Temperature	        ±1°C accuracy
    🌬 Pressure	            High precision
    ⛰ Altitude	           Derived from pressure

Hardware Connections (BBBW I2C2)

    | BMP280 | BBBW    |
    | ------ | ------- |
    | VCC    | 3.3V ⚠️ |
    | GND    | GND     |
    | SDA    | P9_20   |
    | SCL    | P9_19   |

IMPORTANT

👉 Use 3.3V only
👉 BMP280 is NOT 5V tolerant

Step 1 — Detect Device
    i2cdetect -y -r 2

    Expected:

        76 or 77

    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- 76 --

🥈 Step 2 — Kernel Support (Already OK in most cases)

    Check:

        zcat /proc/config.gz | grep BMP

    Should include:

        CONFIG_BMP280=y or m
        CONFIG_IIO=y

Step 3 — Device Tree (If needed)

    Add under I2C2:

        bmp280@76 {
            compatible = "bosch,bmp280";
            reg = <0x76>;
        };

🧪 Step 4 — Verify in sysfs (IIO)
    ls /sys/bus/iio/devices/

    Expected:

        iio:deviceX
        Check device
        cat /sys/bus/iio/devices/iio:deviceX/name

    👉 Should show:

        bmp280

📊 Step 5 — Read Values
    Temperature
        cat in_temp_input

    👉 Example:

        28500   (→ 28.5°C)

    Pressure
        cat in_pressure_input

    👉 Example:

        101325   (Pa)

    Altitude Calculation (Optional)

        Add:

            altitude = 44330 * (1 - (pressure_hpa / 1013.25) ** 0.1903)

        Expected Output
            Temp: 28.45 °C | Pressure: 1008.32 hPa
            Altitude: 45.2 m

Step 6 — Test Raw I2C (IMPORTANT)

    Run:

        i2cget -y 2 0x76 0xD0

    👉 Expected:

        0x58  (BMP280)
        or
        0x60  (BME280)

Step 7 — Reset Device Manually

    i2cset -y 2 0x76 0xE0 0xB6
    sleep 1
    i2cget -y 2 0x76 0xD0

Step 8 — Reboot & Verify

    dmesg | grep bmp

    👉 Expected:

        bmp280 2-0076: registered
            
    ls /sys/bus/iio/devices/

    👉 Should show:

        iio:device0

    Check name
        cat /sys/bus/iio/devices/iio:device0/name

    👉 Should be:

        bmp280

