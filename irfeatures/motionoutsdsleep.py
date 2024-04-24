import RPi.GPIO as GPIO
import time
import requests

# GPIO pin connected to the signal pin of the IR sensor
SENSOR_PIN = 17

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Flask API URL to get user's wake-up time and bedtime parameters
FLASK_API_URL = 'http://localhost:5000/user_parameters'

# Function to get user's wake-up time and bedtime parameters from the Flask API
def get_user_parameters():
    response = requests.get(FLASK_API_URL)
    if response.status_code == 200:
        data = response.json()
        wakeup_time = data.get('wakeup_time')
        bedtime = data.get('bedtime')
        return wakeup_time, bedtime
    else:
        print('Failed to fetch user parameters')
        return None, None

# Function to monitor movement and activate heightened security mode at night
def monitor_movement():
    while True:
        current_time = time.localtime()
        wakeup_time, bedtime = get_user_parameters()
        if wakeup_time and bedtime:
            if current_time.tm_hour < wakeup_time or current_time.tm_hour >= bedtime:
                # Nighttime - activate heightened security mode
                if GPIO.input(SENSOR_PIN) == GPIO.HIGH:
                    send_notification("Motion detected outside sleeping hours!")
        time.sleep(0.1)

# Function to send notification
def send_notification(message):
    data = {'notification': message}
    response = requests.post('http://localhost:5000/alerts', json=data)
    if response.status_code != 200:
        print('Failed to send notification:', response.text)

if __name__ == "__main__":
    try:
        monitor_movement()
    except KeyboardInterrupt:
        GPIO.cleanup()
