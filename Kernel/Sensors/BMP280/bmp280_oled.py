#Expected OLED Output
    # BMP280 Sensor
    # Temp: 28.45 C
    # Pres: 1008.32 hPa
    # Alt: 45.2 m

import time
import glob
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# OLED setup
serial = i2c(port=2, address=0x3C)
device = ssd1306(serial)

# Find BMP280 device
def find_bmp280():
    for dev in glob.glob("/sys/bus/iio/devices/iio:device*"):
        try:
            with open(dev + "/name") as f:
                if "bmp280" in f.read():
                    return dev
        except:
            pass
    return None

# Read sysfs value
def read_value(path):
    try:
        with open(path) as f:
            return float(f.read().strip())
    except:
        return None

def main():
    dev = find_bmp280()
    if not dev:
        print("BMP280 not found")
        return

    print("Using:", dev)

    font = ImageFont.load_default()

    while True:
        temp = read_value(dev + "/in_temp_input")
        pressure = read_value(dev + "/in_pressure_input")

        if temp and pressure:
            temp_c = temp / 1000.0
            pressure_hpa = pressure / 100.0
            altitude = 44330 * (1 - (pressure_hpa / 1013.25) ** 0.1903)

            # Create image
            image = Image.new("1", (128, 64))
            draw = ImageDraw.Draw(image)

            draw.text((0, 0), "BMP280 Sensor", font=font, fill=255)
            draw.text((0, 16), f"Temp: {temp_c:.2f} C", font=font, fill=255)
            draw.text((0, 32), f"Pres: {pressure_hpa:.2f} hPa", font=font, fill=255)
            draw.text((0, 48), f"Alt: {altitude:.1f} m", font=font, fill=255)

            device.display(image)

        time.sleep(1)

if __name__ == "__main__":
    main()