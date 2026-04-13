import time

DIST_PATH = "/sys/bus/iio/devices/iio:device1/in_distance_raw"

def read_distance():
    try:
        with open(DIST_PATH) as f:
            return int(f.read().strip())
    except:
        return -1

print("VL53L0X Distance Monitor")

while True:
    dist = read_distance()

    if dist < 0:
        print("Sensor Error")
    else:
        print(f"Distance: {dist} mm ({dist/10:.1f} cm)")

    time.sleep(1)