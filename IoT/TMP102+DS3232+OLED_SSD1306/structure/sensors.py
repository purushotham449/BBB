import smbus2

bus = smbus2.SMBus(2)

DS3231_ADDR = 0x68
TMP102_ADDR = 0x48

def bcd_to_dec(bcd):
    return (bcd // 16) * 10 + (bcd % 16)

def read_time():
    data = bus.read_i2c_block_data(DS3231_ADDR, 0x00, 7)

    sec = bcd_to_dec(data[0])
    minute = bcd_to_dec(data[1])
    hour = bcd_to_dec(data[2])
    date = bcd_to_dec(data[4])
    month = bcd_to_dec(data[5])
    year = bcd_to_dec(data[6]) + 2000

    return f"{date:02d}-{month:02d}-{year}", f"{hour:02d}:{minute:02d}:{sec:02d}"

def read_temp():
    raw = bus.read_word_data(TMP102_ADDR, 0x00)
    raw = ((raw << 8) & 0xFF00) | (raw >> 8)
    temp = (raw >> 4) * 0.0625
    return round(temp, 2)