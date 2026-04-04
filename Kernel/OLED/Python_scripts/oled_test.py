from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import time

# Init
serial = i2c(port=2, address=0x3C)
device = ssd1306(serial)

# Load big font
font = ImageFont.truetype("/usr/share/fonts/DejaVuSans-Bold.ttf", 20)

while True:
    text = "POOJA"

    with canvas(device) as draw:
        # Get text size
        w, h = draw.textbbox((0, 0), text, font=font)[2:]

        # Center position
        x = (128 - w) // 2
        y = (64 - h) // 2

        # Draw text
        draw.text((x, y), text, font=font, fill=255)

    time.sleep(1)
