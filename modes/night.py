import RPi.GPIO as GPIO
import time
import requests
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)
# Define GPIO pin for LDR sensor
LDR_PIN = 18  # Example pin for LDR sensor, adjust as needed

# Define the GPIO pin for LED sensor
LED_PIN = 25

# Define GPIO pin for DHT11 sensor
DHT11_PIN = 11

# Define GPIO pin for PIR sensor
PIR_PIN = 11

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(DHT11_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.IN)
GPIO.setup(PIR_PIN, GPIO.IN)

# Function to read light intensity from LDR sensor
def read_ldr():
    return GPIO.input(LDR_PIN)


def read_dht():
    return GPIO.input(DHT11_pin)
# Function to adjust lights for sleep based on user-defined sleep timings
def adjust_lights_for_sleep(ldr_value):
    # Get user-defined sleep timings from Flask API
    response = requests.get('http://localhost:5000/sleep-timings')

    if response.status_code == 200:
        sleep_timings = response.json()
        sleep_start = datetime.strptime(sleep_timings['sleep_start'], '%H:%M:%S').time()
        sleep_end = datetime.strptime(sleep_timings['sleep_end'], '%H:%M:%S').time()

        # Check if it's nighttime and if the current time is within sleep timings
        current_time = datetime.now().time()
        nighttime = not (datetime.strptime("06:00:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("18:00:00", "%H:%M:%S").time())
        if nighttime and sleep_start <= current_time <= sleep_end:

            ldr_value = read_ldr()
             # Adjust LED based on LDR value
            if ldr_value > 800:  # High light intensity
                GPIO.output(LED_PIN, GPIO.LOW)  # Dim the LED
            elif ldr_value > 400:  # Moderate light intensity
                GPIO.output(LED_PIN, GPIO.LOW)  # Dim the LED
            else:  # Low light intensity
                GPIO.output(LED_PIN, GPIO.HIGH)  # Turn off the LED
            # Code to reduce or dim the lights or turn off the lights goes here
            print("Adjusting lights for sleep...")
        else:
            print("Not adjusting lights for sleep.")
    else:
        print('Failed to retrieve sleep timings:', response.text)



# Function to adjust temperature
def adjust_temp_for_sleep(dht_value):
    # Get user-defined sleep timings from Flask API
    response = requests.get('http://localhost:5000/sleep-timings')

    if response.status_code == 200:
        sleep_timings = response.json()
        sleep_start = datetime.strptime(sleep_timings['sleep_start'], '%H:%M:%S').time()
        sleep_end = datetime.strptime(sleep_timings['sleep_end'], '%H:%M:%S').time()

        # Check if it's nighttime and if the current time is within sleep timings
        current_time = datetime.now().time()
        nighttime = not (datetime.strptime("06:00:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("18:00:00", "%H:%M:%S").time())
        if nighttime and sleep_start <= current_time <= sleep_end:
            # Code to reduce or dim the lights or turn off the lights goes here
            print("Adjusting temperature and humidity for sleep...")
        else:
            print("Not adjusting temperature and humidity for sleep.")
    else:
        print('Failed to retrieve sleep timings:', response.text)

# Code for movement in sleep
def detect_sleep():
    # Initialize variables
    motion_count = 0
    sleep_threshold = 3  # Number of consecutive readings with no motion to detect sleep

    while True:
        if read_pir() == GPIO.LOW:
            motion_count = 0  # Reset motion count if motion is detected
        else:
            motion_count += 1  # Increment motion count if no motion is detected

        # If motion count exceeds the sleep threshold, consider occupants to have gone to sleep
        if motion_count >= sleep_threshold:
            return True
        else:
            return False

# Function to control servo motor to close door
def close_door():
    # Check if the door is open
    door_status = GPIO.input(DOOR_SERVO_PIN)
    if door_status == GPIO.LOW:  # If door is open, close it
        GPIO.output(DOOR_SERVO_PIN, GPIO.HIGH)
        print("Door closed")
    else:
        print("Door is already closed")

# Function to control servo motor to close window
def close_window():
    # Check if the window is open
    window_status = GPIO.input(WINDOW_SERVO_PIN)
    if window_status == GPIO.LOW:  # If window is open, close it
        GPIO.output(WINDOW_SERVO_PIN, GPIO.HIGH)
        print("Window closed")
    else:
        print("Window is already closed")

# Function to control servo motor to close gate
def close_gate():
    # Check if the gate is open
    gate_status = GPIO.input(GATE_SERVO_PIN)
    if gate_status == GPIO.LOW:  # If gate is open, close it
        GPIO.output(GATE_SERVO_PIN, GPIO.HIGH)
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

# Main function
def main():
    try:
        while True:
            # Closing, windows, gates and doors
            close_elements()

            # Detecting whether occupants have went to sleep or not
            if detect_sleep():
                print("Occupants have gone to sleep.")
            else:
                print("Occupants are awake.")

            # Read light intensity from LDR sensor
            ldr_value = read_ldr()

            # Control lights based on night time
            adjust_lights_for_sleep(ldr_value)

            time.sleep(10)  # Read LDR sensor every 10 seconds

    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on keyboard interrupt

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    main()
