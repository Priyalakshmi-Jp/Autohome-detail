import requests
import RPi.GPIO as GPIO
import time

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Function to control servo motor
def control_servo(pin, speed, wait_time):
    # Set up servo motor with specified pin
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin, 50)  # 50 Hz PWM frequency

    # Start PWM with initial duty cycle (0 degree position)
    servo.start(0)

    # Set speed of servo motor
    servo.ChangeDutyCycle(speed)

    # Wait for the specified time
    time.sleep(wait_time)

    # Stop servo motor
    servo.stop()

# Function to retrieve customization settings from Flask API
def get_customization_settings(area):
    # Send GET request to Flask API endpoint
    response = requests.get(f"http://localhost:5000/customization/{area}")

    # Parse JSON response
    customization_settings = response.json()

    # Return customization settings
    return customization_settings

# Main function
def main():
    # Get customization settings for doors
    door_settings = get_customization_settings("doors")
    door_speed = door_settings.get("speed", 50)  # Default speed is 50%
    door_wait_time = door_settings.get("wait_time", 1)  # Default wait time is 1 second

    # Control door servo motor with customization settings
    control_servo(door_pin, door_speed, door_wait_time)

    # Similar steps for gates and windows

if __name__ == "__main__":
    main()
