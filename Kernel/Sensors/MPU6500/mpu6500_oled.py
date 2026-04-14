import time
from smbus2 import SMBus
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# ===============================
# I2C CONFIG
# ===============================
MPU_ADDR = 0x68
bus = SMBus(2)

# ===============================
# OLED CONFIG (SH1106)
# ===============================
serial = i2c(port=2, address=0x3C)
device = sh1106(serial)

font = ImageFont.load_default()

# ===============================
# MPU REGISTERS
# ===============================
PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C
ACCEL_CONFIG = 0x1C
GYRO_CONFIG  = 0x1B
INT_PIN_CFG  = 0x37

ACCEL_XOUT = 0x3B
GYRO_XOUT  = 0x43

# ===============================
# INIT MPU (FIXED VERSION)
# ===============================
def mpu_init():
    try:
        # Reset device
        bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0x80)
        time.sleep(0.1)

        # Wake up + set clock
        bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0x01)

        # Enable all sensors
        bus.write_byte_data(MPU_ADDR, PWR_MGMT_2, 0x00)

        # Accel ±2g
        bus.write_byte_data(MPU_ADDR, ACCEL_CONFIG, 0x00)

        # Gyro ±250 dps
        bus.write_byte_data(MPU_ADDR, GYRO_CONFIG, 0x00)

        # Enable bypass (MPU9250 support)
        bus.write_byte_data(MPU_ADDR, INT_PIN_CFG, 0x02)

        time.sleep(0.1)

        # Debug WHO_AM_I
        who = bus.read_byte_data(MPU_ADDR, 0x75)
        print(f"WHO_AM_I: {hex(who)}")

    except Exception as e:
        print("MPU INIT ERROR:", e)


# ===============================
# READ 16-bit VALUE
# ===============================
def read_word(reg):
    high = bus.read_byte_data(MPU_ADDR, reg)
    low  = bus.read_byte_data(MPU_ADDR, reg + 1)

    val = (high << 8) | low
    if val > 32767:
        val -= 65536

    return val


# ===============================
# READ SENSOR DATA
# ===============================
def read_mpu():
    try:
        ax = read_word(ACCEL_XOUT)
        ay = read_word(ACCEL_XOUT + 2)
        az = read_word(ACCEL_XOUT + 4)

        gx = read_word(GYRO_XOUT)
        gy = read_word(GYRO_XOUT + 2)
        gz = read_word(GYRO_XOUT + 4)

        # Convert to units
        ax /= 16384.0
        ay /= 16384.0
        az /= 16384.0

        gx /= 131.0
        gy /= 131.0
        gz /= 131.0

        return ax, ay, az, gx, gy, gz

    except Exception as e:
        print("READ ERROR:", e)
        return 0, 0, 0, 0, 0, 0


# ===============================
# DRAW OLED
# ===============================
def draw_display(ax, ay, az, gx, gy, gz):
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), "MPU SENSOR", font=font, fill=255)

    draw.text((0, 12), f"A:{ax:.2f},{ay:.2f},{az:.2f}", font=font, fill=255)
    draw.text((0, 26), f"G:{gx:.1f},{gy:.1f},{gz:.1f}", font=font, fill=255)

    # Orientation logic
    if az > 0.8:
        orient = "FLAT"
    elif ax > 0.5:
        orient = "TILT X"
    elif ay > 0.5:
        orient = "TILT Y"
    else:
        orient = "MOVING"

    draw.text((0, 48), orient, font=font, fill=255)

    device.display(image)


# ===============================
# MAIN
# ===============================
print("MPU OLED Monitor Started")

mpu_init()

while True:
    ax, ay, az, gx, gy, gz = read_mpu()

    print("----------------------")
    print(f"ACCEL: {ax:.2f} {ay:.2f} {az:.2f}")
    print(f"GYRO : {gx:.1f} {gy:.1f} {gz:.1f}")

    draw_display(ax, ay, az, gx, gy, gz)

    time.sleep(0.5)