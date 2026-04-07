from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

serial = i2c(port=2, address=0x3C)
device = ssd1306(serial)
font = ImageFont.load_default()

def update_oled(data):
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), "BMP280 Dashboard", font=font, fill=255)

    if data:
        draw.text((0, 16), f"Temp: {data['temp']:.1f}C", font=font, fill=255)
        draw.text((0, 32), f"Press:{data['pressure']:.0f}", font=font, fill=255)
        draw.text((0, 48), f"Alt:  {data['alt']:.1f}m", font=font, fill=255)

    device.display(image)
