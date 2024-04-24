import RPi.GPIO as GPIO
import time
import requests
from keypad import Keypad  # Make sure the Keypad class is imported correctly

# Initialize the GPIO library
GPIO.setmode(GPIO.BCM)

# Set up the pins for the servo motor
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)

# Set up the pins for the keypad
row_pins = [1, 2, 3, 4]
col_pins = [5, 6, 7, 8]
keys = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

keypad = Keypad(keys, row_pins, col_pins)

# Initialize the servo motor to the closed position
GPIO.output(servo_pin, GPIO.LOW)

# Set up the password
password = "1234"

# Initialize the variable to store the entered password
entered_password = ""

try:
    while True:
        # Get the key press from the keypad
        key = keypad.getKey()

        # If a key was pressed
        if key:
            # If the key is a number or the asterisk key
            if key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*"]:
                # Add the key to the entered password
                entered_password += key
                print(entered_password)

            # If the key is the hash key
            elif key == "#":
                # Check if the entered password is correct
                if entered_password == password:
                    # Send a request to the Flask API to indicate that the door has been opened
                    response = requests.post("http://localhost:5000/door/open")

                    # Open the door
                    GPIO.output(servo_pin, GPIO.HIGH)

                    # Wait for the door to open
                    time.sleep(1)

                    # Close the door
                    GPIO.output(servo_pin, GPIO.LOW)
                    
                    # Wait for the door to close
                    time.sleep(10)

                # Clear the entered password
                entered_password = ""

except KeyboardInterrupt:
    # Clean up GPIO on program exit
    GPIO.cleanup()
