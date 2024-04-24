import RPi.GPIO as GPIO
import time
import requests
import adafruit_dht
from datetime import datetime, timedelta
import json
import board
from flask import Flask, request

app = Flask(__name__)
# Define GPIO pins for servo motor control

DOOR_SERVO_PIN = 11  # Example pin for controlling door with servo motor, adjust as needed
WINDOW_SERVO_PIN = 13  # Example pin for controlling window with servo motor, adjust as needed
GATE_SERVO_PIN = 15  # Example pin for controlling gate with servo motor, adjust as needed
IR_SENSOR_PIN = 23  # Example pin for IR sensor, adjust as needed
LDR_PIN = 24  # Example pin for LDR sensor, adjust as needed
LIGHT_PIN = 11 #pin for checking status of light

#DHT11_PIN =  #pin for checking temp/humid status

# Flask API endpoint
API_ENDPOINT = "http://localhost:5000"

# Initialize GPIO
GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)

GPIO.setup(DOOR_SERVO_PIN, GPIO.OUT)
GPIO.setup(WINDOW_SERVO_PIN, GPIO.OUT)
GPIO.setup(GATE_SERVO_PIN, GPIO.OUT)

GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
GPIO.setup(LDR_PIN, GPIO.IN)

dht_device = adafruit_dht.DHT11(board.D4)
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


def close_door():
    # Check if the door is open (assuming 90-degree angle corresponds to open)
    door_angle = get_servo_angle(DOOR_SERVO_PIN)
    if door_angle == 90:
        # Close the door by setting the servo angle to 0 degrees
        set_servo_angle(DOOR_SERVO_PIN, 0)
        print("Door closed")
    else:
        print("Door is already closed")

def close_window():
    # Check if the window is open (assuming 90-degree angle corresponds to open)
    window_angle = get_servo_angle(WINDOW_SERVO_PIN)
    if window_angle == 90:
        # Close the window by setting the servo angle to 0 degrees
        set_servo_angle(WINDOW_SERVO_PIN, 0)
        print("Window closed")
    else:
        print("Window is already closed")

def close_gate():
    # Check if the gate is open (assuming 90-degree angle corresponds to open)
    gate_angle = get_servo_angle(GATE_SERVO_PIN)
    if gate_angle == 90:
        # Close the gate by setting the servo angle to 0 degrees
        set_servo_angle(GATE_SERVO_PIN, 0)
        print("Gate closed")
    else:
        print("Gate is already closed")

# Function to close all elements using servo motors
def close_elements():
    close_door()
    close_window()
    close_gate()

    # Post data to Flask API after closing elements
    data = {
        "door_status": "closed",
        "window_status": "closed",
        "gate_status": "closed"
    }
    requests.post(API_ENDPOINT + "/close_elements", json=data)


# Function to turn off all power appliances
def turn_off_power_appliances():
    # Code to turn off all power appliances
    print("Turning off all power appliances")

# Function to check for intrusion or movement using IR sensor
def check_intrusion():
    if GPIO.input(IR_SENSOR_PIN):
        print("Intrusion or movement detected")
        # Post message to Flask API
        message = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   "event": "Intrusion or movement detected"}
        requests.post(API_ENDPOINT + "/intrusion_detection", json=message)

# Function to monitor light levels using LDR sensor
def monitor_light_levels():
    while True:
        light_value = GPIO.input(LDR_PIN)
        # Check if light level is unusual (adjust threshold as needed)
        if light_value < 100:  # Example threshold for unusual light level
            print("Unusual light level detected")
            # Post message to Flask API
            message = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       "event": "Unusual light level detected",
                       "light_value": light_value}
            requests.post(API_ENDPOINT + "/unusual_light_detection", json=message)
        time.sleep(60)  # Check light level every minute
 
#
def light_status():
    light_status = json.loads(request.data)
    light_status_bool = light_status['light_status']
    print(light_status_bool)
    #setting GPIO pin 11 to output
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)

    if light_status_bool == "1":
        # light is on
        print('light is on')
        GPIO.output(11,GPIO.HIGH)
    else:
        # ligh is off
        print('light is off')
        GPIO.output(11,GPIO.LOW)


    return jsonify({ 'msg': 'success.' }), 201 

# Main function
def main():
    try:

        # Reading temp/humidity
        read_dht11_data()
               
        # Check light status
        light_status()
        """
        # Close elements using servo motor
        close_elements()
        """
        # Turn off power appliances
        turn_off_power_appliances()

        # Start monitoring for intrusion using IR sensor
        GPIO.add_event_detect(IR_SENSOR_PIN, GPIO.RISING, callback=check_intrusion)

        # Start monitoring light levels using LDR sensor
        monitor_light_levels()
        
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    main()