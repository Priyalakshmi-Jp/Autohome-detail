import RPi.GPIO as GPIO
import time
from flask import Flask, jsonify

app = Flask(__name__)

# GPIO pin for the LDR sensor
LDR_PIN = 18  # Example pin for LDR sensor, adjust as needed

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)

# Function to read data from the LDR sensor
def read_ldr():
    return GPIO.input(LDR_PIN)

# Function to calculate energy usage
def calculate_energy_usage(ldr_value):
    # Assuming a linear relationship between light intensity and energy usage
    # You can replace this with a more accurate model based on your specific setup
    energy_usage = 100 - ldr_value  # Example formula, adjust as needed
    return energy_usage

# Route to retrieve energy usage information
@app.route('/energy_usage', methods=['GET'])
def get_energy_usage():
    ldr_value = read_ldr()
    energy_usage = calculate_energy_usage(ldr_value)
    insights = "Consider using energy-efficient LED bulbs or installing motion sensors to reduce energy usage."
    return jsonify({"ldr_value": ldr_value, "energy_usage": energy_usage, "insights": insights}), 200

# Main function
def main():
    try:
        app.run(debug=True, host='0.0.0.0')  # Run the Flask app

    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on keyboard interrupt

if __name__ == "__main__":
    main()
