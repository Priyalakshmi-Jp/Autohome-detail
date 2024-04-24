import requests
import time
from mq2_sensor import MQ2Sensor  # Assuming you have a library for interfacing with the MQ2 sensor
from flask import Flask, jsonify, request

app = Flask(__name__)

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

# Function to retrieve user address and name from Flask API
def get_user_info():
    # Send GET request to Flask API to retrieve user's information
    response = requests.get("http://localhost:5000/user/info")

    # Extract user's information from the response JSON
    user_info = response.json()
    user_address = user_info.get("address")
    user_name = user_info.get("name")
    return user_address, user_name

# Route to send notification to the user
@app.route('/send_notification', methods=['POST'])
def send_notification():
    # Detect smoke and determine severity
    smoke_ppm, severity = detect_smoke()

    # Retrieve user's information from Flask API
    user_address, user_name = get_user_info()

    # Compose notification message
    message = f"Emergency alert: {severity} smoke detected at {user_name}'s residence, {user_address}."

    # Send notification to the user
    user_endpoint = "http://localhost:5000/user/notification"
    response = requests.post(user_endpoint, json={"message": message})

    if response.status_code == 200:
        return jsonify({"status": "Notification sent"}), 200
    else:
        return jsonify({"error": "Failed to send notification"}), 500

# Main function
def main():
    while True:
        # Detect smoke and determine severity
        smoke_ppm, severity = detect_smoke()

        # If smoke is detected
        if severity != "Moderate":
            # Send emergency alert
            response = requests.post("http://localhost:5000/emergency_alert", json={"severity": severity})
            if response.status_code == 200:
                print("Emergency alert sent successfully.")
            else:
                print("Failed to send emergency alert.")

            # Send notification to the user
            response = send_notification()
            if response.status_code == 200:
                print("Notification sent successfully.")
            else:
                print("Failed to send notification.")

        time.sleep(300)  # Check for smoke every 5 minutes

if __name__ == "__main__":
    main()

#the neighbour here, should actually get the message, not just through app, it also requires sms,
#after this process only we'll excute, this code in emergency mode    