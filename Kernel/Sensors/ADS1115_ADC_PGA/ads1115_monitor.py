import time

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

print("ADS1115 Continuous Monitor")

while True:
    values = []
    for ch in range(4):
        raw = read_raw(ch)
        volt = raw * scale
        values.append((raw, volt))

    print("---------------------------")
    for ch, (raw, volt) in enumerate(values):
        print(f"CH{ch}: RAW={raw:5d}  VOLT={volt:.4f} V")

    time.sleep(1)