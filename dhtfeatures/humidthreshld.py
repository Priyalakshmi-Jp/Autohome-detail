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

# Cleanup GPIO on exit
def cleanup():
    GPIO.cleanup()

atexit.register(cleanup)

# Threshold values for humidity
EXTREMELY_LOW_HUMIDITY_THRESHOLD = 20
LOW_HUMIDITY_THRESHOLD = 30
IDEAL_HUMIDITY_MIN = 30
IDEAL_HUMIDITY_MAX = 50
HIGH_HUMIDITY_THRESHOLD = 60
EXTREMELY_HIGH_HUMIDITY_THRESHOLD = 70

# Route to post DHT data
@app.route('/dht_room', methods=['POST'])
def post_dht_data():
    data = request.json
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    if temperature is not None and humidity is not None:
        print("Received Temperature: {:.1f}°C, Humidity: {}%".format(temperature, humidity))
        # Check humidity threshold
        if humidity < EXTREMELY_LOW_HUMIDITY_THRESHOLD:
            alert = "Extremely Low Humidity!"
        elif humidity < LOW_HUMIDITY_THRESHOLD:
            alert = "Low Humidity!"
        elif humidity >= IDEAL_HUMIDITY_MIN and humidity <= IDEAL_HUMIDITY_MAX:
            alert = "Ideal/Normal Humidity"
        elif humidity == HIGH_HUMIDITY_THRESHOLD:
            alert = "High Humidity!"
        elif humidity > EXTREMELY_HIGH_HUMIDITY_THRESHOLD:
            alert = "Extremely High Humidity!"
        else:
            alert = None
        
        if alert:
            # Post alert to Flask API
            response = app.test_client().post('/humidity_alert', json={'alert': alert})
            if response.status_code == 200:
                print("Alert posted successfully.")
            else:
                print("Failed to post alert:", response.text)
        return jsonify({'message': 'Data received successfully.'}), 200
    else:
        return jsonify({'error': 'Temperature or humidity data missing.'}), 400

# Background task to read DHT sensor and post data
def read_and_post_dht_data():
    while True:
        try:
            temperature = dht_sensor.temperature
            humidity = dht_sensor.humidity
            data = {'temperature': temperature, 'humidity': humidity}
            # Post data to Flask API
            response = app.test_client().post('/dht_room', json=data)
            if response.status_code == 200:
                print("Data posted successfully.")
            else:
                print("Failed to post data:", response.text)
            time.sleep(5)  # Read and post data every 5 seconds
        except RuntimeError as e:
            print("Error reading DHT sensor:", e)
            time.sleep(2)

# Start background task
if __name__ == '__main__':
    dht_thread = Thread(target=read_and_post_dht_data)
    dht_thread.daemon = True
    dht_thread.start()

    app.run(port=5000)
