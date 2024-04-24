import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Define a dictionary to store modes
rooms = {
    'Living room': 'Turns off all the appliances,locks all windows, doors and gates',
    'Kitchen': 'Turns on ambient lights, a mood setter',
    'Guest room': 'Monitor and track guest movements to provide them hospitality',
    'Child and Elder room': 'Monitor and track movements to provide them supervision',
    'Bedroom': 'Enable emergency and evacuation protocols',
}

# Define a route to handle GET requests
@app.route('/api/data', methods=['GET'])
def get_rooms():
    selected_mode = request.args.get('mode')
    if selected_mode:
        main(selected_mode)
    return jsonify(modes)

def main(selected_room):
    # Implement the logic for each mode here
    if selected_room == 'Living room':
        print('Living room enabled')
    if selected_room == 'Kitchen':
        print(' Kitchen room enabled')
    if selected_room == 'Guest room':
        print('Guest room enabled')
    if selected_room == 'Child and Elder room':
        print('Child and Elder room enabled')
    if selected_room == 'Bedroom':
        print('Bedroom enabled')


if __name__ == '__main__':
    app.run(debug=True)