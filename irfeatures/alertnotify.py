

##-----------------------------------------------------------------------------------------------------------------------------------
import time
import atexit
import json
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request
from threading import Thread
import requests

# Initialize Flask app
app = Flask(__name__)

"""
# Define the Flask API URL to send notifications
FLASK_API_URL = 'http://localhost:5000/notifications'"""

# Initialize IR sensor pins for entry points
DOOR_PIN = 17
GATE_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_PIN, GPIO.IN)
GPIO.setup(GATE_PIN, GPIO.IN)

# Initialize recent motion list
recent_motion_list = []

# Cleanup GPIO on exit
def cleanup():
    GPIO.cleanup()

atexit.register(cleanup)

# Start background task to check for motion
def detect_motion():
    global recent_motion_list
    while True:
        door_motion = GPIO.input(DOOR_PIN)
        gate_motion = GPIO.input(GATE_PIN)

        if door_motion or gate_motion:
            # Motion detected at door or gate
            entry_point = "Door" if door_motion else "Gate"
            message = "Motion detected at {} at {}".format(entry_point, time.ctime())
            recent_motion_list.append(message)
            # Notify user using Flask API
            send_notification(message)

        time.sleep(0.1)

# Function to trigger security measures for unauthorized access
def trigger_security_measures():
    last_door_time = 0
    last_gate_time = 0
    AUTHORIZED_ENTRY_THRESHOLD = 60  # Move this inside the function or pass as an argument
    while True:
        door_state = GPIO.input(DOOR_PIN)
        gate_state = GPIO.input(GATE_PIN)
        
        if door_state == GPIO.LOW:
            if time.time() - last_door_time > AUTHORIZED_ENTRY_THRESHOLD:
                message = 'Unauthorized access detected at the door!'
                send_notification(message)
                # Activate other security measures here, such as triggering alarms or sirens
                # ...
                last_door_time = time.time()

        if gate_state == GPIO.LOW:
            if time.time() - last_gate_time > AUTHORIZED_ENTRY_THRESHOLD:
                message = 'Unauthorized access detected at the gate!'
                send_notification(message)
                # Activate other security measures here, such as triggering alarms or sirens
                # ...
                last_gate_time = time.time()

        time.sleep(1)

# Route to get current motion detected by IR
@app.route('/current_motion', methods=['GET'])
def get_current_motion():
    door_motion = GPIO.input(DOOR_PIN)
    gate_motion = GPIO.input(GATE_PIN)
    if door_motion or gate_motion:
        return jsonify({'motion': 'detected'})
    else:
        return jsonify({'motion': 'not detected'})

# Route to get recent motion list detected by IR
@app.route('/recent_motions', methods=['GET'])
def get_recent_motions():
    global recent_motion_list
    return jsonify({'recent_motions': recent_motion_list[-5:]})

# Function to send notification to user
def send_notification(message):
    data = {'notification': message}
    response = requests.post('http://user.com/notifications', json=data)

# Run Flask app and start motion detection thread
if __name__ == '__main__':
    detect_motion_thread = Thread(target=detect_motion)
    detect_motion_thread.daemon = True
    detect_motion_thread.start()
    
    security_thread = Thread(target=trigger_security_measures)
    security_thread.daemon = True
    security_thread.start()
    
    app.run(port=5000, debug=True, threaded=True)
