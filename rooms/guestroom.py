import os
import sys
import RPi.GPIO as GPIO
import requests
import json
from datetime import datetime
import Adafruit_DHT
from flask import Flask, request, make_response, jsonify
import io

# Setup GPIO pins
light_pin = 18
fan_pin = 23
ac_pin = 24

# Set up DHT11 sensor
DHT11_PIN = 25

# Set up Window and door
window_pin = 11
door_pin = 16

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(light_pin, GPIO.OUT)
GPIO.setup(fan_pin, GPIO.OUT)
GPIO.setup(ac_pin, GPIO.OUT)
GPIO.setup(door_pin, GPIO.OUT)
GPIO.setup(window_pin, GPIO.OUT)
dht_device = adafruit_dht.DHT11(board.D4)

app = Flask(__name__)

# Read data from DHT11 sensor
def read_dht11_data():
    while True:
        try:
            temperature_c = dht_device.temperature
            temperature_f = temperature_c*(9 / 5) + 32
            humidity = dht_device.humidity
            print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))
        except RuntimeError as err:
            print(err.args[0])

        time.sleep(1)
# Light status management
def light_status(status):
    if status == 'on':
        GPIO.output(light_pin, GPIO.HIGH)
    elif status == 'off':
        GPIO.output(light_pin, GPIO.LOW)

# Fan status management
def fan_status(status):
    if status == 'on':
        GPIO.output(fan_pin, GPIO.HIGH)
    elif status == 'off':
        GPIO.output(fan_pin, GPIO.LOW)

# AC status management
def ac_status(status):
    if status == 'on':
        GPIO.output(ac_pin, GPIO.HIGH)
    elif status == 'off':
        GPIO.output(ac_pin, GPIO.LOW)

# Function to get status of the door
def door_status():
    if status == 'open':
        GPIO.input(door_pin, GPIO.HIGH)
    elif status == 'closed':
        GPIO.input(door_pin, GPIO.LOW)
        

# Function to get status of the window
def window_status():
    if status == 'open':
        GPIO.input(window_pin, GPIO.HIGH)
    elif status == 'closed':
        GPIO.input(window_pin, GPIO.LOW)
 
 
def read_image(guest_room):
    #filename = 'uploads\\123.jpg'
    #---------------or---------------
    """image_path = f'uploads/{pid}.jpg'  # Adjust the path based on your file structure
    try:
        with open(image_path, 'rb') as image_file:
            return image_file.read()
    except FileNotFoundError:
        return None
    """
    #---------------or----------------
    image_url = f'https://res.cloudinary.com/dmfwpz555/image/upload/rooms/guest_room.jpg'  # Replace with the actual URL

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        return response.content
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
        print(f"Error: {err}")
        return None
    # Implement this function to read the image file based on the provided PID
    # Example: Read image from file system or database
    # Return image data as bytes or None if PID is invalid
    

@app.route('/images/guest_room.jpg', methods=['GET'])
def get_image(guest_room):
    image_binary = read_image(guest_room)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % guest_room)
    return response, send_file(
    io.BytesIO(image_binary),
    mimetype='image/jpeg',
    as_attachment=True,
    download_name='%s.jpg' % guest_room)
    
 # Create the /status endpoint
@app.route('/api/status', methods=['GET'])
def status():
    light = GPIO.input(light_pin)
    fan = GPIO.input(fan_pin)
    ac = GPIO.input(ac_pin)
    dh11_data = read_dht11_data()
    door = door_status()
    window = window_status()

    status = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'light': 'on' if light == GPIO.HIGH else 'off',
        'fan': 'on' if fan == GPIO.HIGH else 'off',
        'ac': 'on' if ac == GPIO.HIGH else 'off',
        'temperature': dh11_data['temperature'],
        'humidity': dh11_data['humidity'],
        'door_status': 'open' if door == GPIO.HIGH else 'closed',
        'window': 'open' if window == GPIO.HIGH else 'closed',
    }

    return jsonify(status)

# Define a route to handle GET requests for counting active devices
@app.route('/api/device_count', methods=['GET'])
def device_count():
    devices = {
        'light': GPIO.input(light_pin),
        'fan': GPIO.input(fan_pin),
        'ac': GPIO.input(ac_pin),
        'door': GPIO.input(door_pin),
        'window': GPIO.input(window_pin),
    }

    active_devices = sum(devices.values())

    return jsonify({'active_devices': active_devices})
# Define a route to handle POST requests for controlling the devices
@app.route('/api/control', methods=['POST'])
def control_devices():
    req_data = request.get_json()

    if 'devices' in req_data:
        devices = req_data['devices']

        for device_name, status in devices.items():
            if device_name == 'light':
                light_status(status)
            elif device_name == 'fan':
                fan_status(status)
            elif device_name == 'ac':
                ac_status(status)
            elif device_name == 'door':
                door_status(status)
                # Update the door status after setting its value
                status_dict = {'door_status': 'open' if GPIO.input(door_pin) else 'closed'}
            elif device_name == 'window':
                window_status(status)
                # Update the window status after setting its value
                status_dict = {'window': 'open' if GPIO.input(window_pin) else 'closed'}

            if device_name in ['light', 'fan', 'ac']:
                # Update the status of the controllable device
                status_dict[device_name] = 'on' if status == 'true' else 'off'

        # Return the updated status in the response
        return jsonify(status_dict)

    else:
        return jsonify({'error': 'No devices specified in the request'}), 400

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(light_pin, GPIO.OUT)
    GPIO.setup(fan_pin, GPIO.OUT)
    GPIO.setup(ac_pin, GPIO.OUT)
    GPIO.setup(door_pin, GPIO.OUT)
    GPIO.setup(window_pin, GPIO.OUT)
    app.run(debug=True, host='0.0.0.0', port=8000)
