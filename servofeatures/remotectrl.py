from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO pins for servo motors
DOOR_PIN = 18
GATE_PIN = 23
WINDOW_PIN = 24

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_PIN, GPIO.OUT)
GPIO.setup(GATE_PIN, GPIO.OUT)
GPIO.setup(WINDOW_PIN, GPIO.OUT)

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

# Routes for controlling doors, gates, and windows
@app.route('/control/door', methods=['GET', 'POST'])
def control_door():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'open':
            control_servo(DOOR_PIN, 90)  # Open door
            return 'Door opened'
        elif action == 'close':
            control_servo(DOOR_PIN, 0)  # Close door
            return 'Door closed'
        else:
            return 'Invalid action'
    elif request.method == 'GET':
        return 'Send POST request with action=open/close to control the door'

@app.route('/control/gate', methods=['GET', 'POST'])
def control_gate():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'open':
            control_servo(GATE_PIN, 90)  # Open gate
            return 'Gate opened'
        elif action == 'close':
            control_servo(GATE_PIN, 0)  # Close gate
            return 'Gate closed'
        else:
            return 'Invalid action'
    elif request.method == 'GET':
        return 'Send POST request with action=open/close to control the gate'

@app.route('/control/window', methods=['GET', 'POST'])
def control_window():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'open':
            control_servo(WINDOW_PIN, 90)  # Open window
            return 'Window opened'
        elif action == 'close':
            control_servo(WINDOW_PIN, 0)  # Close window
            return 'Window closed'
        else:
            return 'Invalid action'
    elif request.method == 'GET':
        return 'Send POST request with action=open/close to control the window'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
