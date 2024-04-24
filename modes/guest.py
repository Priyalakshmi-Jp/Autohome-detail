import RPi.GPIO as GPIO
import time
import requests
from flask import Flask, request

app = Flask(__name__)

# GPIO pins connected to the signal pins of the IR sensors at the door and gate
DOOR_SENSOR_PIN = 17
GATE_SENSOR_PIN = 18

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN)
GPIO.setup(GATE_SENSOR_PIN, GPIO.IN)

# Dictionary to track the last known state of each entry point (door/gate)
last_state = {
    DOOR_SENSOR_PIN: GPIO.input(DOOR_SENSOR_PIN),
    GATE_SENSOR_PIN: GPIO.input(GATE_SENSOR_PIN)
}

# Function to monitor movement and determine direction
def monitor_movement():
    while True:
        door_motion = GPIO.input(DOOR_SENSOR_PIN)
        gate_motion = GPIO.input(GATE_SENSOR_PIN)
        
        if door_motion != last_state[DOOR_SENSOR_PIN]:
            entry_point = "Door"
            direction = "arrived" if door_motion else "left"
            message = f"Guest {direction} through {entry_point} at {time.ctime()}"
            send_notification(message)
            last_state[DOOR_SENSOR_PIN] = door_motion
        
        if gate_motion != last_state[GATE_SENSOR_PIN]:
            entry_point = "Gate"
            direction = "arrived" if gate_motion else "left"
            message = f"Guest {direction} through {entry_point} at {time.ctime()}"
            send_notification(message)
            last_state[GATE_SENSOR_PIN] = gate_motion
        
        time.sleep(0.1)

# Function to send notification
def send_notification(message):
    data = {'notification': message}
    response = requests.post('http://localhost:5000/alerts', json=data)
    if response.status_code != 200:
        print('Failed to send notification:', response.text)

#add feature to override energy consumption mode
# Flag to indicate whether energy consumption mode is active
energy_saver_mode = False


# Function to override energy consumption mode
def override_energy_consumption():
    global energy_consumption_mode
    energy_saver_mode = False
    print("Energy consumption mode overridden.")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    try:
        monitor_movement()
    except KeyboardInterrupt:
        GPIO.cleanup()

#need to add multiple features on the basis
        

        