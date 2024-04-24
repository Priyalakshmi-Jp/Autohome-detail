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

# Threshold values for anomaly detection
HIGHTEMPERATURE_THRESHOLD = 60  # Example: Temperature threshold for fire detection
LOWTEMPERATURE_THRESHOLD = 60  # Example: Temperature threshold for pipe freeze detection
HUMIDITY_THRESHOLD = 70     # Example: Humidity threshold for water leak detection

# Route to post DHT data
@app.route('/dht_room', methods=['POST'])
def post_dht_data():
    data = request.json
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    if temperature is not None and humidity is not None:
        print("Received Temperature: {:.1f}°C, Humidity: {}%".format(temperature, humidity))
        # Check for anomalies
        check_anomalies(temperature, humidity)
        return jsonify({'message': 'Data received successfully.'}), 200
    else:
        return jsonify({'error': 'Temperature or humidity data missing.'}), 400

# Check for anomalies and post alerts if detected
def check_anomalies(temperature, humidity):
    if temperature > HIGHTEMPERATURE_THRESHOLD:
        post_alert("Fire detected! Temperature is too high: {:.1f}°C".format(temperature))
    elif temperature < LOWTEMPERATURE_THRESHOLD:
        post_alert("Pipes Freeing point reached! Temperature is too low: {:.1f}°C".format(temperature))
    elif humidity > HUMIDITY_THRESHOLD:
        post_alert("Water leak, flood detected! Possible mold growth. Humidity is too high: {}%".format(humidity))

# Post alert to Flask API
def post_alert(message):
    response = app.test_client().post('/alert', json={'message': message})
    if response.status_code == 200:
        print("Alert posted successfully.")
    else:
        print("Failed to post alert:", response.text)

# Background task to read DHT sensor
def read_dht_sensor():
    while True:
        try:
            humidity = dht_sensor.humidity
            temperature = dht_sensor.temperature
            data = {'temperature': temperature, 'humidity': humidity}
            # Post data to Flask API
            response = app.test_client().post('/dht_room', json=data)
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
    w