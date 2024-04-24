import RPi.GPIO as GPIO
import time

# Define GPIO pin for LDR sensor
LDR_PIN = 18

def read_ldr_value():
    GPIO.setup(LDR_PIN, GPIO.OUT)
    GPIO.output(LDR_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(LDR_PIN, GPIO.IN)
    while GPIO.input(LDR_PIN) == GPIO.LOW:
        continue
    start_time = time.time()
    while GPIO.input(LDR_PIN) == GPIO.HIGH:
        continue
    end_time = time.time()
    return end_time - start_time

def map_ldr_value(ldr_value, ldr_min, ldr_max, brightness_min, brightness_max):
    return brightness_min + (ldr_value - ldr_min) * (brightness_max - brightness_min) / (ldr_max - ldr_min)

def main():
    # Calibration values for LDR sensor
    ldr_min = 0.1
    ldr_max = 1.0

    # Outdoor light intensity data (example)
    outdoor_light_intensity = 0.5  # Assuming outdoor light intensity is normalized between 0 and 1

    # Indoor lighting control parameters
    brightness_min = 0  # Minimum brightness (e.g., 0%)
    brightness_max = 100  # Maximum brightness (e.g., 100%)

    while True:
        ldr_value = read_ldr_value()
        indoor_brightness = map_ldr_value(ldr_value, ldr_min, ldr_max, brightness_min, brightness_max)

        # Adjust indoor lighting based on outdoor light intensity
        adjusted_brightness = indoor_brightness * outdoor_light_intensity
        print("Indoor brightness:", adjusted_brightness)

        # Set indoor lighting levels (e.g., using PWM or smart lighting controls)
        # Example: set_pwm_brightness(adjusted_brightness)

        time.sleep(1)  # Adjust sampling interval as needed

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        main()
    finally:
        GPIO.cleanup()
