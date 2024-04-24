import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Define a dictionary to store modes
modes = {
    'Away': 'Turns off all the appliances,locks all windows, doors and gates',
    'Ambient': 'Turns on ambient lights, a mood setter',
    'Guest': 'Monitor and track guest movements to provide them hospitality',
    'Child and Elder': 'Monitor and track movements to provide them supervision',
    'Emergency': 'Enable emergency and evacuation protocols',
    'Night': 'Prepare for a restful night and sound sleep',
    'Energy Saver': 'Save application from overusage and reduce electricity bill',
    'Vacay': 'Turns off all the appliances, locks all windows, doors and gates, ensuring safety for a long leave from home',
}

# Define a route to handle GET requests
@app.route('/api/data', methods=['GET'])
def get_modes():
    selected_mode = request.args.get('mode')
    if selected_mode:
        main(selected_mode)
    return jsonify(modes)

def main(selected_mode):
    # Implement the logic for each mode here
    if selected_mode == 'Away':
        print('Away mode enabled')
    if selected_mode == 'Ambient':
        print('Ambient mode enabled')
    if selected_mode == 'Guest':
        print('Guest mode enabled')
    if selected_mode == 'Child and Elder':
        print('Child and Elder mode enabled')
    if selected_mode == 'Emergency':
        print('Emergency mode enabled')
    if selected_mode == 'Night':
        print('Night mode enabled')
    if selected_mode == 'Energy Saver':
        print('Energy Saver mode enabled')
    if selected_mode == 'Vacay':
        print('Vacay mode enabled')

if __name__ == '__main__':
    app.run(debug=True)