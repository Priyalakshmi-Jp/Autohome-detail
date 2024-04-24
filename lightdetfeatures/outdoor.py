#pip install astral
import RPi.GPIO as GPIO
import time
from astral.sun import sun
from datetime import datetime, timedelta
from flask import Flask, jsonify, request

app = Flask(__name__)

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# GPIO pins for controlling lights
PATHWAY_LIGHT_PIN = 4  # GPIO pin for pathway light, adjust as needed
DRIVEWAY_LIGHT_PIN = 17  # GPIO pin for driveway light, adjust as needed
GARDEN_LIGHT_PIN = 27  # GPIO pin for garden light, adjust as needed
GATE_LIGHT_PIN = 22  # GPIO pin for gate light, adjust as needed

# LDR sensor pin
LDR_PIN = 18  # GPIO pin for LDR sensor, adjust as needed

# Define thresholds for lightness and darkness
LIGHT_THRESHOLD = 70  # Lightness threshold (adjust as needed)
DARKNESS_THRESHOLD = 30  # Darkness threshold (adjust as needed)

# Temporary storage for light status
light_status = {
    'pathway_light': False,
    'driveway_light': False,
    'garden_light': False,
    'gate_light': False
}

# Function to initialize GPIO pins
def init_gpio():
    GPIO.setup(PATHWAY_LIGHT_PIN, GPIO.OUT)
    GPIO.setup(DRIVEWAY_LIGHT_PIN, GPIO.OUT)
    GPIO.setup(GARDEN_LIGHT_PIN, GPIO.OUT)
    GPIO.setup(GATE_LIGHT_PIN, GPIO.OUT)

# Function to read LDR sensor value
def read_ldr():
    try:
        # Read analog value from LDR sensor
        ldr_value = GPIO.input(LDR_PIN)
        # Map the analog value from the LDR to the desired range (0 to 1032)
        # Assuming the LDR outputs values between 0 and 1023
        ldr_mapped_value = int((ldr_value / 1023) * 1032)
        return ldr_mapped_value
    except Exception as e:
        print("Error reading LDR sensor:", e)
        return None
    # Simulated function for reading LDR sensor value
    # Replace this with actual code to read from LDR sensor
    # Example: return 50  # Dummy value for demonstration
    pass

# Function to control pathway light
def control_pathway_light():
    ldr_value = read_ldr()
    if ldr_value <= DARKNESS_THRESHOLD:
        GPIO.output(PATHWAY_LIGHT_PIN, GPIO.HIGH)
        light_status['pathway_light'] = True
        post_light_status('pathway_light', ldr_value)
    elif ldr_value >= LIGHT_THRESHOLD:
        GPIO.output(PATHWAY_LIGHT_PIN, GPIO.LOW)
        light_status['pathway_light'] = False
        post_light_status('pathway_light', ldr_value)

# Function to control driveway light
def control_driveway_light():
    ldr_value = read_ldr()
    if ldr_value <= DARKNESS_THRESHOLD:
        GPIO.output(DRIVEWAY_LIGHT_PIN, GPIO.HIGH)
        light_status['driveway_light'] = True
        post_light_status('driveway_light', ldr_value)
    elif ldr_value >= LIGHT_THRESHOLD:
        GPIO.output(DRIVEWAY_LIGHT_PIN, GPIO.LOW)
        light_status['driveway_light'] = False
        post_light_status('driveway_light', ldr_value)

# Function to control garden light
def control_garden_light():
    ldr_value = read_ldr()
    if ldr_value <= DARKNESS_THRESHOLD:
        GPIO.output(GARDEN_LIGHT_PIN, GPIO.HIGH)
        light_status['garden_light'] = True
        post_light_status('garden_light', ldr_value)
    elif ldr_value >= LIGHT_THRESHOLD:
        GPIO.output(GARDEN_LIGHT_PIN, GPIO.LOW)
        light_status['garden_light'] = False
        post_light_status('garden_light', ldr_value)

# Function to control gate light
def control_gate_light():
    ldr_value = read_ldr()
    if ldr_value <= DARKNESS_THRESHOLD:
        GPIO.output(GATE_LIGHT_PIN, GPIO.HIGH)
        light_status['gate_light'] = True
        post_light_status('gate_light', ldr_value)
    elif ldr_value >= LIGHT_THRESHOLD:
        GPIO.output(GATE_LIGHT_PIN, GPIO.LOW)
        light_status['gate_light'] = False
        post_light_status('gate_light', ldr_value)

# Function to get sunrise and sunset times
def get_sunrise_sunset(latitude, longitude):
    city = astral.Location()
    city.latitude = latitude
    city.longitude = longitude
    city.timezone = 'UTC'  # Adjust timezone as needed
    s = sun(city.observer, date=datetime.now())
    sunrise_time = s['sunrise'].strftime('%H:%M:%S')
    sunset_time = s['sunset'].strftime('%H:%M:%S')
    return sunrise_time, sunset_time

# Function to post light status to Flask API
def post_light_status(light_name, ldr_value):
    status = "ON" if light_status[light_name] else "OFF"
    message = f"The {light_name.replace('_', ' ')} light is {status} at LDR value {ldr_value}"
    print(message)
    # Post message to Flask API
    requests.post("http://localhost:5000/light_status", json={"message": message})

# Route to retrieve light status
@app.route('/light_status', methods=['POST'])
def light_status():
    request_data = request.json
    message = request_data.get("message")
    print("Light status:", message)
    return jsonify({"status": "Received"}), 200

# Route to receive user's location
@app.route('/user/location', methods=['GET'])
def get_user_location():
    # Example request: http://localhost:5000/user/location?latitude=51.5074&longitude=0.1278
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if latitude is None or longitude is None:
        return jsonify({"error": "Latitude or longitude is missing in the request"}), 400

    # Convert latitude and longitude to float values
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return jsonify({"error": "Latitude and longitude must be numeric values"}), 400

    # Process the location data further as required

    return jsonify
    {"message": "User location received", "latitude": latitude, "longitude": longitude}, 200


# Main function
def main():
    try:
        init_gpio()
        
        sunrise_time, sunset_time = get_sunrise_sunset(latitude, longitude)
        if sunrise_time is None or sunset_time is None:
            print("Error: Unable to retrieve sunrise/sunset times. Exiting...")
            return
        
        print("Sunrise time:", sunrise_time)
        print("Sunset time:", sunset_time)
        
        while True:
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # Check if it's daytime
            if sunrise_time < current_time < sunset_time:
                control_pathway_light()
                control_driveway_light()
                control_garden_light()
                control_gate_light()
            else:
                # It's nighttime, turn off all lights
                GPIO.output(PATHWAY_LIGHT_PIN, GPIO.LOW)
                GPIO.output(DRIVEWAY_LIGHT_PIN, GPIO.LOW)
                GPIO.output(GARDEN_LIGHT_PIN, GPIO.LOW)
                GPIO.output(GATE_LIGHT_PIN, GPIO.LOW)
                light_status['pathway_light'] = False
                light_status['driveway_light'] = False
                light_status['garden_light'] = False
                light_status['gate_light'] = False
                print("All lights turned off at nighttime")
                post_light_status('pathway_light', 0)
                post_light_status('driveway_light', 0)
                post_light_status('garden_light', 0)
                post_light_status('gate_light', 0)
            
            time.sleep(60)  # Check every minute
    
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()



