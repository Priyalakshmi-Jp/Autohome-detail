    import RPi.GPIO as GPIO
    import time
    import requests
    from datetime import datetime, timedelta
    import json
    import schedule
    import board
    import adafruit_dht
    from flask import jsonify, request

    app = Flask(__name__)

    # Define GPIO pins for servo motor control
    DOOR_SERVO_PIN = 18  # Example pin for controlling door with servo motor, adjust as needed
    WINDOW_SERVO_PIN = 23  # Example pin for controlling window with servo motor, adjust as needed
    GATE_SERVO_PIN = 24  # Example pin for controlling gate with servo motor, adjust as needed
    IR_SENSOR_PIN = 23  # Example pin for IR sensor, adjust as needed
    LDR_PIN = 24  # Example pin for LDR sensor, adjust as needed
    LIGHT_PIN = 11 # pin for controlling light
    FAN_pin = 23 #pin for fan controlling
    AC_pin = 24 #pin for ac controlling
    DHT11_PIN = 25 # Set up DHT11 sensor


    # Flask API endpoint
    API_ENDPOINT = "http://localhost:5000"

    # Initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOOR_SERVO_PIN, GPIO.OUT)
    GPIO.setup(WINDOW_SERVO_PIN, GPIO.OUT)
    GPIO.setup(GATE_SERVO_PIN, GPIO.OUT)
    GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
    GPIO.setup(LDR_PIN, GPIO.IN)
    GPIO.setup(FAN_pin, GPIO.OUT)
    GPIO.setup(AC_pin, GPIO.OUT)

    # Read data from DHT11 sensor and change the values# Adding predefined temp & humidity, HVAC system turned on to minimuize heating/cooling suitable conditions maintained to prevent mold or freezing pipes

    def read_dht11_data():
        dht_device = adafruit_dht.DHT11(board.D4)
    while True:
        try:
            temperature_c = dht_device.temperature
            temperature_f = temperature_c * (9 / 5) + 32

            humidity = dht_device.humidity

            print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))
        except RuntimeError as err:
            print(err.args[0])

        time.sleep(2.0)
        if humidity is not None and temperature is not None:
            # Check temperature thresholds
            if temperature <= 0:
                # Temperature too low, turn on fan
                fan_status('on')
            elif temperature >= 55:
                # Temperature too high, turn on AC
                ac_status('on')
        
            # Check humidity threshold
            if humidity >= 80:
                # Humidity too high, turn on AC
                ac_status('on')

            result = {'temperature': temperature, 'humidity': humidity}
        else:
            result = {'temperature': None, 'humidity': None}

        return result

    #--------scheduling ac and fan-------------
    import schedule
    import time

    def schedule_ac_and_fan():
        # Define intervals and durations for turning on the AC and fan
        AC_INTERVAL = 9  # Interval in hours
        FAN_INTERVAL = 9  # Interval in hours
        DURATION = 5  # Duration in minutes

        # Define functions to turn on/off the AC and fan
        def turn_on(device):
            device('on')

        def turn_off(device):
            device('off')

        # Function to schedule AC and fan operations
        def schedule_ac_and_fan():
            devices = {'AC': ac_status, 'Fan': fan_status}

            for device, status in devices.items():
                schedule.every(AC_INTERVAL if device == 'AC' else FAN_INTERVAL).hours.do(turn_on, status)
                schedule.every(AC_INTERVAL if device == 'AC' else FAN_INTERVAL).hours.do(turn_off, status).after(DURATION).minutes

            # Main loop to execute scheduled tasks
            while True:
                schedule.run_pending()
                time.sleep(1)
def close_door():
    # Check if the door is open (assuming 90-degree angle corresponds to open)
    door_angle = get_servo_angle(DOOR_SERVO_PIN)
    if door_angle == 90:
        # Close the door by setting the servo angle to 0 degrees
        set_servo_angle(DOOR_SERVO_PIN, 0)
        print("Door closed")
    else:
        print("Door is already closed")

def close_window():
    # Check if the window is open (assuming 90-degree angle corresponds to open)
    window_angle = get_servo_angle(WINDOW_SERVO_PIN)
    if window_angle == 90:
        # Close the window by setting the servo angle to 0 degrees
        set_servo_angle(WINDOW_SERVO_PIN, 0)
        print("Window closed")
    else:
        print("Window is already closed")

def close_gate():
    # Check if the gate is open (assuming 90-degree angle corresponds to open)
    gate_angle = get_servo_angle(GATE_SERVO_PIN)
    if gate_angle == 90:
        # Close the gate by setting the servo angle to 0 degrees
        set_servo_angle(GATE_SERVO_PIN, 0)
        print("Gate closed")
    else:
        print("Gate is already closed")

    # Function to close all elements using servo motors
    def close_elements():
        close_door()
        close_window()
        close_gate()

        # Post data to Flask API after closing elements
        data = {
            "door_status": "closed",
            "window_status": "closed",
            "gate_status": "closed"
        }
        requests.post(API_ENDPOINT + "/close_elements", json=data)


    # Function to turn off all power appliances
    def turn_off_power_appliances():
        # Code to turn off all power appliances
        print("Turning off all power appliances")

    # Function to check for intrusion or movement using IR sensor
    def check_intrusion():
        if GPIO.input(IR_SENSOR_PIN):
            print("Intrusion or movement detected")
            # Post message to Flask API
            message = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       "event": "Intrusion or movement detected"}
            requests.post(API_ENDPOINT + "/intrusion_detection", json=message)

    # Function to monitor light levels using LDR sensor
    def monitor_light_levels():
        while True:
            light_value = GPIO.input(LDR_PIN)
            # Check if light level is unusual (adjust threshold as needed)
            if light_value < 100:  # Example threshold for unusual light level
                print("Unusual light level detected")
                # Post message to Flask API
                message = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           "event": "Unusual light level detected",
                           "light_value": light_value}
                requests.post(API_ENDPOINT + "/unusual_light_detection", json=message)
            time.sleep(60)  # Check light level every minute
 
    # To deter potential theft and robbery

    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(11, GPIO.OUT)

    # Define function to handle light status
    def light_status():
        data = json.loads(request.data)
        light_status_bool = data.get('light_status')
        print(f"Light is {'on' if light_status_bool == '1' else 'off'}")
        GPIO.output(11, GPIO.HIGH if light_status_bool == '1' else GPIO.LOW)
        # Schedule turning off the light after 30 minutes
        if light_status_bool == '1':
            schedule.every(9).hours.do(lambda: GPIO.output(11, GPIO.LOW)).tag('light_off')
        return jsonify({'msg': 'success.'}), 201

    @app.route('/api/light_status', methods=['POST'])
    def handle_light_status():
        return light_status()

    # Start the scheduler loop
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)


    # Main function
    def main():
        try:
        
            # Call the scheduling function
            schedule_ac_and_fan()
            # Reading temp and humid 
            read_dht_data()

            # Check light status
            light_status()
        
            # Close elements using servo motor
            close_elements()

            # Turn off power appliances
            turn_off_power_appliances()

            # Start monitoring for intrusion using IR sensor
            GPIO.add_event_detect(IR_SENSOR_PIN, GPIO.RISING, callback=check_intrusion)

            # Start monitoring light levels using LDR sensor
            monitor_light_levels()

        except KeyboardInterrupt:
            GPIO.cleanup()

    if __name__ == "__main__":
        main()
        # Start the scheduler loop in a separate thread
        import threading
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.start()
        app.run(debug=True, host='0.0.0.0', port=8000)
    #during the vacay mode, some of the lights should be turned on or off