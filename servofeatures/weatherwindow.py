import requests
import time
import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Function to fetch weather forecast data
def get_weather_forecast(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

# Function to control servo motor for windows
def control_windows(action):
    # Define servo motor positions for open and close actions
    if action == "open":
        # Set servo motor position to open the windows
        pass
    elif action == "close":
        # Set servo motor position to close the windows
        pass

# Function to send notification to Flask API
def send_notification(message):
    import requests

def send_notification(message):
    # Define the URL of the Flask API endpoint
    api_url = "http://localhost:5000/notification"  # Update with your API endpoint URL

    # Define the data to be sent in the POST request
    data = {
        "message": message  # Message indicating whether the window has been closed or opened
    }

    try:
        # Send POST request to the API
        response = requests.post(api_url, json=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print("Failed to send notification:", response.text)
    except Exception as e:
        print("An error occurred while sending notification:", str(e))

# Example usage:
# send_notification("Window closed")
# send_notification("Window opened")

    # Send POST request to Flask API
    pass

# Main function to check weather forecast and control windows
def main():
    while True:
        # Fetch weather forecast data
        weather_data = get_weather_forecast(API_KEY, CITY)
        
        # Extract relevant information from weather data
        weather_condition = weather_data.get('weather')[0].get('main')
        temperature = weather_data.get('main').get('temp')

        # Determine window control actions based on weather conditions
        if weather_condition in ["Rain", "Thunderstorm"]:
            # Close windows 10 minutes before rain or storm
            send_notification("Closing windows due to impending rain or storm")
            time.sleep(600)  # Wait 10 minutes before the forecasted event
            control_windows("close")
        elif weather_condition == "Clear" and temperature < 37:
            # Open windows if clear weather and temperature is below 37°C
            control_windows("open")
            send_notification("Opening windows due to clear weather")
        else:
            # No action needed for windows
            send_notification("No action needed for windows")

        # Wait for some time before checking weather forecast again
        time.sleep(3600)  # Check weather every hour

if __name__ == "__main__":
    main()
