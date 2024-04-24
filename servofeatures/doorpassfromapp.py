from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO pins for servo motors
DOOR_PIN = 18

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_PIN, GPIO.OUT)

# Function to control servo motors
def control_servo(pin, angle):
    pwm = GPIO.PWM(pin, 50)
    pwm.start(0)
    duty_cycle = angle / 18.0 + 2.5
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()

# Variable to hold the password
password = "default_password"

# Route to set or update the password
@app.route('/set_password', methods=['POST'])
def set_password():
    global password
    new_password = request.form.get('new_password')
    if new_password:
        password = new_password
        return 'Password updated successfully'
    else:
        return 'No new password provided'

# Route for opening the door
@app.route('/open_door', methods=['GET'])
def open_door():
    entered_password = request.args.get('password')
    if entered_password == password:
        control_servo(DOOR_PIN, 90)  # Open door
        return 'Door opened'
    else:
        return 'Incorrect password'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
