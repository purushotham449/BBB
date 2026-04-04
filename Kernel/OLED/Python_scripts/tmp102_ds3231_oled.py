from smbus2 import SMBus
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import time

# -----------------------
# CONFIG
# -----------------------
I2C_BUS = 2
TMP102_ADDR = 0x48
DS3231_ADDR = 0x68

# OLED init
serial = i2c(port=2, address=0x3C)
device = ssd1306(serial)

font = ImageFont.load_default()

# -----------------------
# TMP102 READ
# -----------------------
def read_temp():
    try:
        with SMBus(I2C_BUS) as bus:
            raw = bus.read_word_data(TMP102_ADDR, 0x00)
            raw = ((raw << 8) & 0xFF00) | (raw >> 8)

            temp = raw >> 4
            if temp & 0x800:
                temp -= 1 << 12

            return temp * 0.0625
    except:
        return None


# -----------------------
# DS3231 READ
# -----------------------
def bcd_to_dec(bcd):
    return (bcd >> 4) * 10 + (bcd & 0x0F)


def read_ds3231():
    try:
        with SMBus(I2C_BUS) as bus:
            sec = bcd_to_dec(bus.read_byte_data(DS3231_ADDR, 0x00))
            minute = bcd_to_dec(bus.read_byte_data(DS3231_ADDR, 0x01))
            hour = bcd_to_dec(bus.read_byte_data(DS3231_ADDR, 0x02) & 0x3F)

            day = bcd_to_dec(bus.read_byte_data(DS3231_ADDR, 0x04))
            month = bcd_to_dec(bus.read_byte_data(DS3231_ADDR, 0x05) & 0x1F)
            year = bcd_to_dec(bus.read_byte_data(DS3231_ADDR, 0x06)) + 2000

            time_str = f"{hour:02}:{minute:02}:{sec:02}"
            date_str = f"{day:02}-{month:02}-{year}"

            return time_str, date_str

    except Exception as e:
        return None, None


# -----------------------
# MAIN LOOP
# -----------------------
while True:
    temp = read_temp()
    time_str, date_str = read_ds3231()

    if temp is not None:
        temp_str = f"{temp:.1f}C"
    else:
        temp_str = "Err"

    if time_str is None:
        time_str = "RTC Err"
    if date_str is None:
        date_str = "RTC Err"

    with canvas(device) as draw:

        draw.text((0, 0), f"Date: {date_str}", font=font, fill=255)
        draw.text((0, 20), f"Time: {time_str}", font=font, fill=255)
        draw.text((0, 40), f"Temp: {temp_str}", font=font, fill=255)

    time.sleep(1)
