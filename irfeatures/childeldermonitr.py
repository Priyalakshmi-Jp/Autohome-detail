import RPi.GPIO as GPIO
import time
import requests
from flask import Flask, jsonify, request

# GPIO pins connected to the signal pins of the IR sensors at the door and gate
DOOR_SENSOR_PIN = 17
GATE_SENSOR_PIN = 18

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN)
GPIO.setup(GATE_SENSOR_PIN, GPIO.IN)

# Function to monitor movement and send alerts
def monitor_movement():
    while True:
        door_motion = GPIO.input(DOOR_SENSOR_PIN)
        gate_motion = GPIO.input(GATE_SENSOR_PIN)
        
        if door_motion or gate_motion:
            entry_point = "Door" if door_motion else "Gate"
            message = f"Child/Elder Motion detected at {entry_point} at {time.ctime()}"
            send_notification(message)
        
        time.sleep(0.1)

# Function to send notification
def send_notification(message):
    data = {'notification': message}
    response = requests.post('http://localhost:5000/alerts', json=data)
    if response.status_code != 200:
        print('Failed to send notification:', response.text)

if __name__ == "__main__":
    try:
        monitor_movement()
    except KeyboardInterrupt:
        GPIO.cleanup()


##intializing flask app
        
app = Flask(__name__)

@app.route('/alerts', methods=['POST'])
def receive_alert():
    data = request.json
    print('Received alert:', data)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
