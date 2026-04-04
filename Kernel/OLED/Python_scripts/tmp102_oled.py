from smbus2 import SMBus
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import time

# -----------------------
# TMP102 Config
# -----------------------
I2C_BUS = 2
TMP102_ADDR = 0x48

# -----------------------
# OLED Config
# -----------------------
serial = i2c(port=2, address=0x3C)
device = ssd1306(serial)

# Load big font
font_large = ImageFont.truetype("/usr/share/fonts/DejaVuSans-Bold.ttf", 20)
font_small = ImageFont.load_default()

# -----------------------
# Read TMP102
# -----------------------
def read_temp():
    try:
        with SMBus(I2C_BUS) as bus:
            raw = bus.read_word_data(TMP102_ADDR, 0x00)

            # Swap bytes
            raw = ((raw << 8) & 0xFF00) | (raw >> 8)

            # Convert
            temp = raw >> 4
            if temp & 0x800:
                temp -= 1 << 12

            return temp * 0.0625

    except Exception as e:
        return None


# -----------------------
# Main Loop
# -----------------------
while True:
    temp = read_temp()

    with canvas(device) as draw:

        if temp is None:
            msg = "Sensor Err"
            w, h = draw.textbbox((0,0), msg, font=font_small)[2:]
            draw.text(((128-w)//2, (64-h)//2), msg, font=font_small, fill=255)

        else:
            temp_str = f"{temp:.1f} C"

            # Title
            title = "TEMP"
            w1, h1 = draw.textbbox((0,0), title, font=font_small)[2:]
            draw.text(((128-w1)//2, 5), title, font=font_small, fill=255)

            # Temperature (big, centered)
            w2, h2 = draw.textbbox((0,0), temp_str, font=font_large)[2:]
            draw.text(((128-w2)//2, (64-h2)//2 + 10), temp_str, font=font_large, fill=255)

    time.sleep(1)
