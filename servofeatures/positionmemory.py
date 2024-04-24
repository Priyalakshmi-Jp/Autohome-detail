import json

# Function to read positions from configuration file
def read_positions():
    try:
        with open('positions.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save positions to configuration file
def save_positions(positions):
    with open('positions.json', 'w') as file:
        json.dump(positions, file)

# Example usage
positions = read_positions()

# Set servo motor positions based on retrieved positions
door_position = positions.get('door', 0)
window_position = positions.get('window', 0)

# Control servo motors based on positions
# Example: set_servo_position(door_position)
# Example: set_servo_position(window_position)

# Update positions when user changes them
positions['door'] = new_door_position
positions['window'] = new_window_position
save_positions(positions)
