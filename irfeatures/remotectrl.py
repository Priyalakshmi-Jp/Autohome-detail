import time
import atexit
import json
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request
from threading import Thread
import requests

# Initialize Flask app
app = Flask(__name__)

# Initialize IR sensor
IR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN)

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
        if GPIO.input(IR_PIN):
            # Motion detected, append timestamp to list
            recent_motion_list.append(time.time())
            # Notify user using Flask API
            send_notification()
        time.sleep(0.1)

# Route to get current motion detected by IR
@app.route('/current_motion', methods=['GET'])
def get_current_motion():
    if GPIO.input(IR_PIN):
        return jsonify({'motion': 'detected'})
    else:
        return jsonify({'motion': 'not detected'})

# Route to get recent motion list detected by IR
@app.route('/recent_motions', methods=['GET'])
def get_recent_motions():
    global recent_motion_list
    return jsonify({'recent_motions': recent_motion_list[-5:]})

# Function to send notification to user
def send_notification():
    data = {'notification': 'Motion detected at {}'.format(time.ctime())}
    response = requests.post('http://user.com/notifications', json=data)

# Run Flask app and start motion detection thread
if __name__ == '__main__':
    detect_motion_thread = Thread(target=detect_motion)
    detect_motion_thread.daemon = True
    detect_motion_thread.start()
    app.run(port=5000, debug=True, threaded=True)
