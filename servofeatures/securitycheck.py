import requests
import RPi.GPIO as GPIO
import time

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Function to control servo motor for locking
def lock_servo(pin):
    # Set up servo motor with specified pin
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin, 50)  # 50 Hz PWM frequency

    # Start PWM with initial duty cycle (0 degree position)
    servo.start(0)

    # Rotate servo motor to lock position
    servo.ChangeDutyCycle(10)  # Adjust duty cycle for lock position

    # Wait for the lock to engage
    time.sleep(1)

    # Stop servo motor
    servo.stop()

# Function to control servo motor for unlocking
def unlock_servo(pin):
    # Set up servo motor with specified pin
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin, 50)  # 50 Hz PWM frequency

    # Start PWM with initial duty cycle (0 degree position)
    servo.start(0)

    # Rotate servo motor to unlock position
    servo.ChangeDutyCycle(5)  # Adjust duty cycle for unlock position

    # Wait for the unlock to complete
    time.sleep(1)

    # Stop servo motor
    servo.stop()

# Function to retrieve security mode from Flask API
def get_security_mode():
    # Send GET request to Flask API endpoint
    response = requests.get("http://localhost:5000/security_mode")

    # Parse JSON response
    security_mode = response.json()

    # Return security mode
    return security_mode

# Main function
def main():
    while True:
        # Retrieve security mode
        security_mode = get_security_mode()

        # Check if security mode is away mode or it's nighttime
        if security_mode == "away_mode" or is_nighttime():
            # Lock all doors and gates
            lock_servo(door_pin)
            lock_servo(gate_pin)

        # Wait for some time before checking again (e.g., every 1 hour)
        time.sleep(3600)

# Function to check if it's nighttime
def is_nighttime():
    # Implement logic to determine if it's nighttime
    # You can use datetime.datetime.now() to get the current time
    # and compare it with the nighttime period
    return False  # Placeholder logic

if __name__ == "__main__":
    main()
