from flask import Flask, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO pins for servo motors and position sensors
DOOR_PIN = 18
DOOR_SENSOR_PIN = 21
WINDOW_PIN = 23
WINDOW_SENSOR_PIN = 24
GATE_PIN = 25
GATE_SENSOR_PIN = 26

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_PIN, GPIO.OUT)
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN)
GPIO.setup(WINDOW_PIN, GPIO.OUT)
GPIO.setup(WINDOW_SENSOR_PIN, GPIO.IN)
GPIO.setup(GATE_PIN, GPIO.OUT)
GPIO.setup(GATE_SENSOR_PIN, GPIO.IN)

# Function to read position of servo motor
def read_position(sensor_pin):
    # Logic to read position from the sensor
    # Example: For a potentiometer, read analog value; For a rotary encoder, count pulses
    return GPIO.input(sensor_pin)

# Route to get position feedback for door
@app.route('/door_position', methods=['GET'])
def get_door_position():
    position = read_position(DOOR_SENSOR_PIN)
    return jsonify({'position': position})

# Route to get position feedback for window
@app.route('/window_position', methods=['GET'])
def get_window_position():
    position = read_position(WINDOW_SENSOR_PIN)
    return jsonify({'position': position})

# Route to get position feedback for gate
@app.route('/gate_position', methods=['GET'])
def get_gate_position():
    position = read_position(GATE_SENSOR_PIN)
    return jsonify({'position': position})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
