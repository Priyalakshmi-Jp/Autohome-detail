import RPi.GPIO as GPIO
import time
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for MQ2 sensor
MQ2_PIN = 4  # Example pin, adjust according to your setup

# Function to initialize MQ2 sensor
def init_mq2():
    GPIO.setup(MQ2_PIN, GPIO.IN)

# Function to read analog value from MQ2 sensor
def read_mq2():
    return GPIO.input(MQ2_PIN)

# Function to read data from the MQ2 sensor
def read_sensor():
    # Read analog value from MQ2 sensor
    smoke_detected = read_mq2()
    location = "Living Room"  # Example location
    severity = "High"  # Example severity
    duration = 10  # Example duration in seconds
    date_time = datetime.now()  # Get current date and time
    return smoke_detected, location, severity, duration, date_time

# Temporary storage for smoke detection events
smoke_events = []

# Route to receive smoke detection events
@app.route('/smoke_detection_event', methods=['POST'])
def smoke_detection_event():
    # Read data from the MQ2 sensor
    smoke_detected, location, severity, duration, date_time = read_sensor()

    # If smoke is detected, store the event
    if smoke_detected:
        smoke_events.append({
            'location': location,
            'severity': severity,
            'duration': duration,
            'date_time': date_time.strftime("%Y-%m-%d %H:%M:%S")  # Format date and time as string
        })

    return jsonify({"message": "Smoke detection event received"}), 200

# Route to retrieve stored smoke detection events
@app.route('/smoke_events', methods=['GET'])
def get_smoke_events():
    return jsonify(smoke_events), 200

# Main function
def main():
    try:
        # Initialize MQ2 sensor
        init_mq2()

        # Run the Flask app
        app.run(debug=True)

    except KeyboardInterrupt:
        # Clean up GPIO on keyboard interrupt
        GPIO.cleanup()

if __name__ == "__main__":
    main()
