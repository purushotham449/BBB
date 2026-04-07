import time
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

    print("Using device:", dev)

    while True:
        temp = read_value(dev + "/in_temp_input")
        pressure = read_value(dev + "/in_pressure_input")

        if temp and pressure:
            temp_c = temp / 1000.0
            pressure_hpa = pressure / 100.0

            print(f"Temp: {temp_c:.2f} °C | Pressure: {pressure_hpa:.2f} hPa")

        time.sleep(1)

if __name__ == "__main__":
    main()