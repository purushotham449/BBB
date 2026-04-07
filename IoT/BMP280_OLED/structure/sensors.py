import glob

def find_bmp280():
    for dev in glob.glob("/sys/bus/iio/devices/iio:device*"):
        try:
            with open(dev + "/name") as f:
                if "bmp280" in f.read():
                    return dev
        except:
            pass
    return None

bmp = find_bmp280()

def read_file(path):
    try:
        with open(path) as f:
            return float(f.read().strip())
    except:
        return None

def read_bmp280():
    if not bmp:
        return None

    temp = read_file(bmp + "/in_temp_input")
    press = read_file(bmp + "/in_pressure_input")

    if temp and press:
        temp_c = temp / 1000.0
        pressure = press / 100.0
        altitude = 44330 * (1 - (pressure / 1013.25) ** 0.1903)

        return {
            "temp": temp_c,
            "pressure": pressure,
            "alt": altitude
        }

    return None
