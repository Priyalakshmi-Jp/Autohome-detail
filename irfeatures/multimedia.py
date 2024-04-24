import RPi.GPIO as GPIO
import time
from flask import Flask, request

IR_PIN = 17

# Function to perform WiFi scanning
def scan_wifi_devices():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.scan()
    available_networks = [n[0] for n in wlan.scan()]
    return available_networks

# Function to detect motion using IR sensor
def detect_motion():
    # Initialize GPIO and IR sensor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_PIN, GPIO.IN)

    while True:
        if GPIO.input(IR_PIN) == GPIO.HIGH:
            return True  # Motion detected
        time.sleep(0.1)

# Flask app initialization
app = Flask(__name__)

# Define endpoints for controlling multimedia system
@app.route('/pause', methods=['POST'])
def pause_media():
    # Code to pause media playback
    return 'Media paused'

@app.route('/resume', methods=['POST'])
def resume_media():
    # Code to resume media playback
    return 'Media resumed'

# Define endpoint for PIR sensor events
@app.route('/pir', methods=['POST'])
def pir_event():
    motion_detected = request.json.get('motion_detected')
    if motion_detected:
        # Code to trigger multimedia actions when motion is detected
        # Example: pause_media()
        return 'Motion detected'
    return 'No motion detected'

if __name__ == '__main__':
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    # Main function for motion detection
    while True:
        connected_devices = scan_wifi_devices()
        
        # Check if any device is playing media
        media_playing = any(device_is_playing_media(device) for device in connected_devices)
        
        if media_playing:
            # Motion detection
            motion_detected = detect_motion()
            if motion_detected:
                # Pause media playback
                pause_media()
                time.sleep(5)  # Wait for motion to settle
                
                # Resume playback when motion is detected again
                while detect_motion():
                    resume_media()
                    time.sleep(0.1)

        time.sleep(1)
