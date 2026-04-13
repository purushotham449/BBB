import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# ===============================
# OLED SETUP (SH1106)
# ===============================
serial = i2c(port=2, address=0x3C)
device = sh1106(serial)

font = ImageFont.load_default()

# ===============================
# VL53L0X SYSFS PATH
# ===============================
DIST_PATH = "/sys/bus/iio/devices/iio:device1/in_distance_raw"

# ===============================
# READ DISTANCE
# ===============================
def read_distance():
    try:
        with open(DIST_PATH) as f:
            return int(f.read().strip())  # mm
    except Exception as e:
        print("Read error:", e)
        return -1


# ===============================
# DRAW OLED
# ===============================
def draw_display(dist):
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), "VL53L0X SENSOR", font=font, fill=255)

    if dist >= 0:
        draw.text((0, 20), f"{dist} mm", font=font, fill=255)
        draw.text((0, 32), f"{dist/10:.1f} cm", font=font, fill=255)
    else:
        draw.text((0, 20), "Sensor Error", font=font, fill=255)

    # Status logic
    if dist < 0:
        status = "ERROR"
    elif dist < 200:
        status = "NEAR"
    elif dist < 800:
        status = "MID"
    else:
        status = "FAR"

    draw.text((0, 50), f"STATUS: {status}", font=font, fill=255)

    device.display(image)


# ===============================
# MAIN LOOP
# ===============================
print("Starting VL53L0X OLED Monitor...")

while True:
    dist = read_distance()

    print(f"Distance: {dist} mm")

    draw_display(dist)

    time.sleep(1)