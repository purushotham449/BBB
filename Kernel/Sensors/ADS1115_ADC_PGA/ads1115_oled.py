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
# ADS1115 SYSFS PATH
# ===============================
BASE = "/sys/bus/iio/devices/iio:device1"

def read_raw(ch):
    try:
        with open(f"{BASE}/in_voltage{ch}_raw") as f:
            return int(f.read().strip())
    except:
        return -1

def read_scale():
    try:
        with open(f"{BASE}/in_voltage_scale") as f:
            return float(f.read().strip())
    except:
        return 0.0

scale = read_scale()

# ===============================
# DRAW OLED
# ===============================
def draw_display(values):
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), "ADS1115 ADC", font=font, fill=255)

    for i, (raw, volt) in enumerate(values):
        draw.text((0, 12 + i*12),
                  f"CH{i}:{volt:.2f}V",
                  font=font,
                  fill=255)

    device.display(image)

# ===============================
# MAIN LOOP
# ===============================
print("ADS1115 OLED Monitor Started")

while True:
    values = []

    for ch in range(4):
        raw = read_raw(ch)
        volt = raw * scale
        values.append((raw, volt))

    # Console output
    for i, (raw, volt) in enumerate(values):
        print(f"CH{i}: {volt:.3f} V")

    print("----------------------")

    draw_display(values)

    time.sleep(1)