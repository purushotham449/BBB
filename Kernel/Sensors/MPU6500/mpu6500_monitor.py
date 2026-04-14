#!/usr/bin/env python3

import smbus
import time

bus = smbus.SMBus(2)
addr = 0x68

# Wake up MPU6050
bus.write_byte_data(addr, 0x6B, 0)

def read_word(reg):
    high = bus.read_byte_data(addr, reg)
    low = bus.read_byte_data(addr, reg+1)
    val = (high << 8) + low
    if val > 32767:
        val -= 65536
    return val

def get_temp():
    temp_raw = read_word(0x41)
    return temp_raw / 340.0 + 36.53

while True:
    ax = read_word(0x3B)
    ay = read_word(0x3D)
    az = read_word(0x3F)

    gx = read_word(0x43)
    gy = read_word(0x45)
    gz = read_word(0x47)

    temp = get_temp()

    print(f"Accel: X={ax} Y={ay} Z={az}")
    print(f"Gyro : X={gx} Y={gy} Z={gz}")
    print(f"Temp : {temp:.2f} C")
    print("---------------------------")

    time.sleep(1)