#code for dynamic adjust of temp/humid according to user preference
import Adafruit_DHT
from flask import Flask, jsonify, request

app = Flask(__name__)

# Default temperature and humidity values
DEFAULT_TEMPERATURE = 24  # Default temperature in Celsius
DEFAULT_HUMIDITY = 40  # Default humidity in percentage

# Variables to store user preferences
user_temperature = DEFAULT_TEMPERATURE
user_humidity = DEFAULT_HUMIDITY

# Endpoint to retrieve user preferences
@app.route('/user/preferences', methods=['GET'])
def get_user_preferences():
    global user_temperature, user_humidity
    return jsonify({
        'temperature': user_temperature,
        'humidity': user_humidity
    })

# Endpoint to update user preferences
@app.route('/user/preferences', methods=['POST'])
def update_user_preferences():
    global user_temperature, user_humidity
    request_data = request.json
    user_temperature = request_data.get('temperature', DEFAULT_TEMPERATURE)
    user_humidity = request_data.get('humidity', DEFAULT_HUMIDITY)
    return jsonify({'message': 'User preferences updated successfully'}), 200

# Function to read temperature and humidity from DHT11 sensor
def read_dht11_sensor():
    sensor = Adafruit_DHT.DHT11
    pin = 4  # GPIO pin for DHT11 sensor (adjust as needed)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return temperature, humidity

# Function to adjust temperature and humidity based on user preferences
def adjust_temperature_and_humidity(temperature, humidity):
    global user_temperature, user_humidity
    if user_temperature is not None:
        temperature = user_temperature
    if user_humidity is not None:
        humidity = user_humidity
    return temperature, humidity

# Main function
def main():
    while True:
        # Read temperature and humidity from DHT11 sensor
        temperature, humidity = read_dht11_sensor()

        # Adjust temperature and humidity based on user preferences
        adjusted_temperature, adjusted_humidity = adjust_temperature_and_humidity(temperature, humidity)

        # Post updated temperature and humidity to Flask API
        # Implement this part based on your Flask API setup

        # Print the adjusted values (for testing)
        print("Adjusted Temperature:", adjusted_temperature)
        print("Adjusted Humidity:", adjusted_humidity)

        # Sleep for some time before reading sensor again
        time.sleep(10)  # Adjust as needed

if __name__ == "__main__":
    main()
