Complete step-by-step documentation for building a Flask-based IoT Dashboard (Desktop + Mobile view) using:

    ✅ BeagleBone Black Wireless (BBBW)
    ✅ BMP280 (Temperature/Pressure)
    ✅ SSD1306 OLED (local display)
    ✅ Flask Web Dashboard (remote monitoring)

    For reference go through the below topics:
        BBB/Kernel/IIO
        BBB/Kernel/OLED

1. Objective

Build an end-to-end IoT system that:

    Reads temperature and pressure from BMP280
    Displays locally on OLED
    Hosts a Flask web dashboard
    Accessible via mobile & desktop browser

2. System Architecture

    BMP280
        ↓
     I2C-2
        ↓
     BBBW (Python)
     ├── OLED Display
     └── Flask Server
            ↓
     Web Browser (Mobile/Desktop)

3. Hardware Setup

📍 I2C-2 Pins on BBBW

    | Signal | Pin   |
    | ------ | ----- |
    | SDA    | P9_20 |
    | SCL    | P9_19 |
    | VCC    | 3.3V  |
    | GND    | GND   |

4. Verify Devices
    i2cdetect -y -r 2

Expected:

    0x76 → BMP280
    0x3C → OLED

5. Install Required Packages

    pip3 install flask

    Auto Refresh Chart (Advanced)
        pip3 install flask-socketio
    
    Add Graph (Chart.js)
        Real-time temperature graph

    ✅ Authentication
        Add login page

    ✅ Run as Service
        systemctl enable flask-dashboard

6. Project Directory Structure
    mkdir -p ~/IoT/templates
    cd ~/IoT

    IoT/
    ├── app.py
    ├── sensors.py
    └── templates/
        └── index.html

7. Sensor Code (sensors.py)

8. Flask Backend (app.py)

9. Dashboard UI (templates/index.html)

10. Run the Application
    cd ~/IoT
    python3 app.py

11. Access Dashboard

    Find BBBW IP:

        ip addr show

    Open in browser:

        http://<BBBW-IP>:5000

12. Mobile View
    
    Open same URL on mobile
    UI auto-adjusts (responsive)
    Add to home screen → works like an app

13. Auto Start on Boot (Systemd)

    Create service:

    sudo vi /etc/systemd/system/iot-dashboard.service
    
        [Unit]
        Description=IoT Flask Dashboard
        After=network.target

        [Service]
        ExecStart=/usr/bin/python3 /home/root/IoT/app.py
        WorkingDirectory=/home/root/IoT
        Restart=always
        User=root

        [Install]
        WantedBy=multi-user.target

    Enable:

        systemctl daemon-reexec
        systemctl enable iot-dashboard
        systemctl start iot-dashboard

16. Final Output

    ✔ OLED shows:

        BMP280 Dashboard
        Temp: 28.5C
        Press:1008
        Alt: 45.2m
