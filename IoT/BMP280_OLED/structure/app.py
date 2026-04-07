from flask import Flask, render_template, jsonify
import time
from sensors import read_bmp280
from oled import update_oled

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    bmp = read_bmp280()

    if bmp:
        data = {
            "temp": bmp["temp"],
            "pressure": bmp["pressure"],
            "alt": bmp["alt"],
            "time": time.strftime("%H:%M:%S")
        }
    else:
        data = {
            "temp": 0,
            "pressure": 0,
            "alt": 0,
            "time": "N/A"
        }

    update_oled(data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
