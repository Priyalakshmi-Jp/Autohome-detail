import RPi.GPIO as GPIO
import time
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for MQ2 sensor and power management relay
MQ2_PIN = 4  # Example pin for MQ2 sensor, adjust according to your setup
POWER_RELAY_PIN = 17  # Example pin for power management relay, adjust according to your setup

# Function to initialize MQ2 sensor
def init_mq2():
    GPIO.setup(MQ2_PIN, GPIO.IN)

# Function to initialize power management relay
def init_power_management():
    GPIO.setup(POWER_RELAY_PIN, GPIO.OUT)
    GPIO.output(POWER_RELAY_PIN, GPIO.HIGH)  # Initially turn off power

# Function to read analog value from MQ2 sensor
def read_mq2():
    return GPIO.input(MQ2_PIN)

# Function to detect smoke and determine severity level
def detect_smoke():
    mq2_sensor = MQ2Sensor()  # Initialize the MQ2 sensor
    smoke_ppm = mq2_sensor.read_ppm()  # Read smoke concentration in ppm

    # Define severity levels based on ppm ranges
    if smoke_ppm < 200:
        severity = "Low"
    elif 200 <= smoke_ppm < 700:
        severity = "Moderately High"
    elif 700 <= smoke_ppm < 4000:
        severity = "High"
    else:
        severity = "Dangerous"

    return smoke_ppm, severity


# Function to activate power management
def activate_power_management():
    # Turn off all electrical appliances
    # Here, you can add code to control other GPIO pins to turn off appliances
    # For demonstration purposes, let's print a message
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"The power appliances are turned off as the smoke detected is moderately high at {time_now}"
    print("Activating power management:", message)

    # Switch electricity of home to backup generators or battery backups
    GPIO.output(POWER_RELAY_PIN, GPIO.LOW)

    # Post message to Flask API
    requests.post("http://localhost:5000/power_off", json={"message": message})

# Function to switch to backup generators or battery
def switch_to_backup():
    # Here, you can add code to switch to backup generators or battery
    # For demonstration purposes, let's print a message
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"The backup generators or battery have been switched on at {time_now}"
    print("Switching to backup generators or battery:", message)

    # Post message to Flask API
    requests.post("http://localhost:5000/switch_to_backup", json={"message": message})

# Route to retrieve stored smoke detection events
@app.route('/smoke_events', methods=['GET'])
def get_smoke_events():
    return jsonify(smoke_events), 200

# Route to handle power off event
@app.route('/power_off', methods=['POST'])
def power_off():
    request_data = request.json
    message = request_data.get("message")
    print("Received power off message:", message)
    # Perform any additional actions if required
    return jsonify({"status": "Received power off message"}), 200

# Route to handle switch to backup event
@app.route('/switch_to_backup', methods=['POST'])
def switch_to_backup():
    request_data = request.json
    message = request_data.get("message")
    print("Received switch to backup message:", message)
    # Perform any additional actions if required
    return jsonify({"status": "Received switch to backup message"}), 200

# Main function
def main():
    try:
        # Initialize MQ2 sensor and power management
        init_mq2()
        init_power_management()

        # Run the Flask app
        app.run(debug=True)

    except KeyboardInterrupt:
        # Clean up GPIO on keyboard interrupt
        GPIO.cleanup()

if __name__ == "__main__":
    main()
