import time
import atexit
import json
import board
import adafruit_dht
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialize DHT sensor
dht_sensor = adafruit_dht.DHT11(board.D18)

# Cleanup GPIO on exit
def cleanup():
    GPIO.cleanup()

atexit.register(cleanup)

# Route to post DHT data
@app.route('/dht_room', methods=['POST'])
def post_dht_data():
    data = request.json
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    if temperature is not None and humidity is not None:
        print("Received Temperature: {:.1f}°C, Humidity: {}%".format(temperature, humidity))
        # Perform further processing here if needed
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
            response = requests.post('http://localhost:5000/dht_room', json=data)
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
    from threading import Thread
    import requests
    dht_thread = Thread(target=read_and_post_dht_data)
    dht_thread.daemon = True
    dht_thread.start()

    app.run(port=5000)
