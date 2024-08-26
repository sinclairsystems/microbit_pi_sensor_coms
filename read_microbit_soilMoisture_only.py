from flask import Flask, render_template_string
import serial
import threading

app = Flask(__name__)

# Serial port setup (replace '/dev/ttyACM0' with your actual port)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

# Shared data structure
data = {"moisture": None}

# Function to read data from Micro:bit
def read_serial_data():
    global data
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Received: {line}")  # Debugging print to see the raw data
                if "Moisture Level:" in line:
                    data["moisture"] = line.split(": ")[1]
        except Exception as e:
            print(f"Error reading serial data: {e}")

# Start the data reading thread
threading.Thread(target=read_serial_data, daemon=True).start()

# Define the Flask route for the web panel
@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Soil Moisture Monitor</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>Soil Moisture Level</h1>
        <p>{{ moisture }}</p>
    </body>
    </html>
    ''', moisture=data["moisture"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
