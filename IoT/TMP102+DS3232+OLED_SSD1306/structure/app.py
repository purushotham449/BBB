from flask import Flask, render_template, jsonify
from sensors import read_time, read_temp

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    date, time_now = read_time()
    temp = read_temp()

    return jsonify({
        "date": date,
        "time": time_now,
        "temperature": temp
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)