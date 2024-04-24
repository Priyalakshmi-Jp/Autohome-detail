from datetime import datetime
import RPi.GPIO as GPIO
import time

# Define GPIO pin for LDR sensor
LDR_PIN = 18  # Example pin for LDR sensor, adjust as needed

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)

# Function to read light intensity from LDR sensor
def read_ldr():
    return GPIO.input(LDR_PIN)

# Function to calculate color temperature based on light intensity and current time
def calculate_color_temperature(ldr_value):
    # Daytime vs. nighttime detection based on current time
    current_time = datetime.now().time()
    daytime = datetime.strptime("06:00:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("18:00:00", "%H:%M:%S").time()

    # Adjust color temperature based on light intensity and daytime/nighttime
    if daytime:
        if ldr_value > 800:  # High light intensity (bright sunlight)
            color_temperature = "Cool"  # Use cooler color temperature (e.g., bluish-white light)
        elif ldr_value > 400:  # Moderate light intensity (cloudy or shaded)
            color_temperature = "Neutral"  # Use neutral color temperature
        else:  # Low light intensity (dawn, dusk, or overcast conditions)
            color_temperature = "Warm"  # Use warm color temperature (e.g., yellowish-white light)
    else:  # Nighttime
        if ldr_value > 200:  # Moderate light intensity (streetlights or indoor lighting)
            color_temperature = "Neutral"  # Use neutral color temperature
        else:  # Low light intensity (darkness)
            color_temperature = "Warm"  # Use warm color temperature (e.g., yellowish-white light)

    return color_temperature

# Function to control lights based on color temperature
def control_lights(ldr_value):
    color_temperature = calculate_color_temperature(ldr_value)
    # Code to control lights based on color temperature goes here
    # This could involve adjusting LED brightness or color, or controlling smart bulbs
    print("Color Temperature:", color_temperature)

# Main function
def main():
    try:
        while True:
            # Read light intensity from LDR sensor
            ldr_value = read_ldr()

            # Control lights based on color temperature
            control_lights(ldr_value)

            time.sleep(10)  # Read LDR sensor every 10 seconds

    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on keyboard interrupt

if __name__ == "__main__":
    main()
