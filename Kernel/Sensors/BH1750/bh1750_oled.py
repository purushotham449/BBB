import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# OLED setup (I2C2 → port=2)
serial = i2c(port=2, address=0x3C)
device = ssd1306(serial)

font = ImageFont.load_default()

# BH1750 sysfs paths
RAW_PATH = "/sys/bus/iio/devices/iio:device0/in_illuminance_raw"
SCALE_PATH = "/sys/bus/iio/devices/iio:device0/in_illuminance_scale"

def read_lux():
    try:
        with open(RAW_PATH) as f:
            raw = float(f.read().strip())
        with open(SCALE_PATH) as f:
            scale = float(f.read().strip())
        return raw * scale
    except:
        return -1

def draw_screen(lux):
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), "BH1750 LIGHT", font=font, fill=255)

    if lux >= 0:
        draw.text((0, 20), f"LUX: {lux:.1f}", font=font, fill=255)
    else:
        draw.text((0, 20), "Sensor Error", font=font, fill=255)

    # Status
    if lux < 10:
        status = "DARK"
    elif lux < 200:
        status = "DIM"
    elif lux < 1000:
        status = "NORMAL"
    else:
        status = "BRIGHT"

    draw.text((0, 40), f"STATUS: {status}", font=font, fill=255)

    device.display(image)

# Main loop
while True:
    lux = read_lux()
    print(f"Lux: {lux:.2f}")
    draw_screen(lux)
    time.sleep(1)