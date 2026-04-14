1. MPU6050 Overview

MPU6050 =

    📦 3-axis Accelerometer
    🔄 3-axis Gyroscope
    🌡 Temperature sensor (internal)
    📡 I2C interface

    Default I2C address:

        0x68  (AD0 = GND)

2. Hardware Connections (BBBW ↔ MPU6050)
    
    MPU6050 Pin	BBBW Pin
        VCC	3.3V ⚠️
        GND	GND
        SDA	I2C2_SDA (P9_20)
        SCL	I2C2_SCL (P9_19)
        AD0	GND (for 0x68)

    ⚠️ Important:

        Use 3.3V only (NOT 5V)
        BBBW already has I2C pull-ups

🧪 3. Verify Device Detection
    
    i2cdetect -y -r 2

    Expected:

        68  ← MPU6050

4. Initialize MPU6050 (Wake Up)

    By default, MPU6050 is in sleep mode.

        i2cset -y 2 0x68 0x6B 0x00

    👉 Register:

        0x6B → Power Management

📊 5. Read Raw Sensor Data

    Register Map

        | Function | Register |
        | -------- | -------- |
        | Accel X  | 0x3B     |
        | Accel Y  | 0x3D     |
        | Accel Z  | 0x3F     |
        | Temp     | 0x41     |
        | Gyro X   | 0x43     |
        | Gyro Y   | 0x45     |
        | Gyro Z   | 0x47     |

    Example (Read Accel X High Byte)
        i2cget -y 2 0x68 0x3B

    i2cget -y 2 0x68 0x75
    
        What It SHOULD Be

            Device	    WHO_AM_I

            MPU6050	    0x68
            MPU6500	    0x70
            MPU9250	    0x71

7. Convert to Real Units (Important)
    
    Accelerometer (default ±2g)
        value / 16384.0 → g
    Gyroscope (default ±250°/s)
        value / 131.0 → °/sec

Verify
    i2cdetect -y -r 2                                     

    Expected:
    
            0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f                            
        00:                         -- -- -- -- -- -- -- --                            
        10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                            
        20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                            
        30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --                            
        40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                            
        50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                            
        60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --                            
        70: -- -- -- -- -- -- -- --       

3. Kernel Support

    MPU6500 is supported via IIO subsystem.

    Kernel Config
        CONFIG_IIO=y
        CONFIG_INV_MPU6050_IIO=y
        CONFIG_INV_MPU6050_I2C=y
        CONFIG_INV_MPU6050_SPI=y

    menuconfig path

        Device Drivers →
            Industrial I/O support →
                Inertial Measurement Units →
                    InvenSense MPU6050/6500/9250

4. Device Tree (DTS)

    Add to your BBBW DTS:

    &i2c2 {
        status = "okay";

        mpu@68 {
            compatible = "invensense,mpu6500";   // ✅ FIXED
            reg = <0x68>;
        };
    };

5. Build & Boot
    bitbake -c clean virtual/kernel
    bitbake virtual/kernel

6. Verify Driver
    
    cat /sys/bus/iio/devices/iio:device0/name

    Expected:
        mpu6500
    
    dmesg | grep mpu

    Expected:

        mpu6500 2-0068: registered

    Bind Device to Driver (Important)

        If auto-detection doesn’t happen:

            echo mpu6050 0x68 > /sys/bus/i2c/devices/i2c-2/new_device

    Then:

        ls /sys/bus/iio/devices/

        You should see:

            iio:device0

    Check channels
        ls /sys/bus/iio/devices/iio:device0

    Expected:

        in_accel_x_raw
        in_accel_y_raw
        in_accel_z_raw
        in_anglvel_x_raw
        in_anglvel_y_raw
        in_anglvel_z_raw
        in_temp_raw