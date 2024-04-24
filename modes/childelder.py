import RPi.GPIO as GPIO
import time
import requests
from flask import Flask, jsonify, request
import json
import threading  # Add import statement for threading module

# GPIO pins connected to the signal pins of the IR sensors at the door and gate
DOOR_SENSOR_PIN = 17
GATE_SENSOR_PIN = 18

# GPIO pin connected to the HVAC system
HVAC_PIN = 23

# GPIO pin connected to the LIGHT system
LIGHT_PIN = 11

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN)
GPIO.setup(GATE_SENSOR_PIN, GPIO.IN)
GPIO.setup(HVAC_PIN, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)

# Function for light status to turn on/off
def light_status():
    light_status = json.loads(request.data)
    light_status_bool = light_status['light_status']
    print(light_status_bool)

    if light_status_bool == "1":
        # light is on
        print('light is on')
        GPIO.output(LIGHT_PIN, GPIO.HIGH)  # Correct GPIO pin number
    else:
        # light is off
        print('light is off')
        GPIO.output(LIGHT_PIN, GPIO.LOW)  # Correct GPIO pin number

    return jsonify({ 'msg': 'success.' }), 201 

# Function to monitor movement and send alerts
def monitor_movement():
    while True:
        door_motion = GPIO.input(DOOR_SENSOR_PIN)
        gate_motion = GPIO.input(GATE_SENSOR_PIN)
        
        if door_motion or gate_motion:
            entry_point = "Door" if door_motion else "Gate"
            message = f"Child/Elder Motion detected at {entry_point} at {time.ctime()}"
            send_notification(message)
            # Turn on HVAC when movement is detected
            control_hvac(True)
        else:
            # Turn off HVAC when no movement is detected
            control_hvac(False)
        
        time.sleep(0.1)

# Function to send notification
def send_notification(message):
    data = {'notification': message}
    response = requests.post('http://localhost:5000/alerts', json=data)
    if response.status_code != 200:
        print('Failed to send notification:', response.text)

# Function to control HVAC system
def control_hvac(state):
    GPIO.output(HVAC_PIN, state)

# Initialize Flask app
app = Flask(__name__)

# Route to receive alerts
@app.route('/alerts', methods=['POST'])
def receive_alert():
    data = request.json
    print('Received alert:', data)
    return jsonify({'status': 'success'})

# Route to control light
@app.route('/light_status', methods=['POST'])
def light_status_info():
    light_status()
    return jsonify({'status': 'success'})

# Route to control HVAC
@app.route('/control_hvac', methods=['POST'])
def control_hvac_route():
    data = request.json
    hvac_state = data.get('state')
    if hvac_state is not None:
        control_hvac(hvac_state)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

if __name__ == '__main__':
    try:
        # Start monitoring movement in a separate thread
        movement_thread = threading.Thread(target=monitor_movement)
        movement_thread.start()
        
        # Run the Flask app
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()



# need to add different codes for multiple features, the above code only mentions ir sensor