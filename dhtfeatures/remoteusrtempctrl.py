import time
import atexit
import json
import board
import adafruit_dht
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request
from threading import Thread

app = Flask(__name__)

# Initialize DHT sensor
dht_sensor = adafruit_dht.DHT11(board.D18)

# GPIO pin for controlling temperature (example pin, change as per your setup)
temperature_control_pin = 17
GPIO.setup(temperature_control_pin, GPIO.OUT)
temperature_pwm = GPIO.PWM(temperature_control_pin, 100)
temperature_pwm.start(0)

# Cleanup GPIO on exit
def cleanup():
    GPIO.cleanup()

atexit.register(cleanup)

# Route to get current temperature
@app.route('/current_temperature', methods=['GET'])
def get_current_temperature():
    humidity = dht_sensor.humidity
    temperature = dht_sensor.temperature
    return jsonify({'temperature': temperature, 'humidity': humidity}), 200

# Route to set desired temperature
@app.route('/set_temperature', methods=['POST'])
def set_desired_temperature():
    data = request.json
    desired_temperature = data.get('temperature')
    if desired_temperature is not None:
        # Example: Adjust temperature based on desired temperature
        control_temperature(desired_temperature)
        return jsonify({'message': 'Desired temperature set successfully.'}), 200
    else:
        return jsonify({'error': 'Temperature data missing.'}), 400

# Control temperature based on desired temperature
def control_temperature(desired_temperature):
    # Example logic to control temperature based on desired temperature
    current_temperature = dht_sensor.temperature
    if desired_temperature > current_temperature:
        temperature_pwm.ChangeDutyCycle(50)  # Example: increase temperature
    elif desired_temperature < current_temperature:
        temperature_pwm.ChangeDutyCycle(0)   # Example: decrease temperature
    else:
        temperature_pwm.ChangeDutyCycle(25)  # Example: maintain temperature

# Background task to read DHT sensor
def read_dht_sensor():
    while True:
        try:
            # Reading data from DHT sensor can be moved to get_current_temperature route for real-time data
            # For demonstration purpose, I'm keeping it here
            humidity = dht_sensor.humidity
            data = {'humidity': humidity}
            # Post data to Flask API
            response = app.test_client().post('/current_temperature', json=data)
            if response.status_code != 200:
                print("Failed to post data:", response.text)
            time.sleep(5)  # Read data every 5 seconds
        except RuntimeError as e:
            print("Error reading DHT sensor:", e)
            time.sleep(2)

# Start background task
if __name__ == '__main__':
    # Start thread to read DHT sensor
    dht_thread = Thread(target=read_dht_sensor)
    dht_thread.daemon = True
    dht_thread.start()

    # Run Flask app
    app.run(port=5000)
