from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
from database import create_table, add_session_data, get_previous_sessions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
api = Api(app)

# Create the table when the application starts
create_table()

# Initialize current session data dictionary
current_session_data = {
    'jump_count': 0,
    'set_count': 0,
    'set_duration': 0
}

# Routes to HTML templates
@app.route('/')
def index():
    previous_sessions = get_previous_sessions()
    return render_template('index.html', current_session_data=current_session_data, previous_sessions=previous_sessions)



# Route for setting goals (not changed from the previous code)
@app.route('/set_goals', methods=['POST'])
def set_goals():
    jump_goal = int(request.form['jump_goal'])
    set_goal = int(request.form['set_goal'])
    # Store the goals in the database or use them for further processing (optional)
    return 'Goals set successfully'

# Create a new resource to handle data sent from Arduino

class ArduinoData(Resource):
    def post(self):
        # Parse data sent from the Arduino
        parser = reqparse.RequestParser()
    
        parser.add_argument('jump_count', type=int)
        parser.add_argument('set_count', type=int)
        parser.add_argument('set_duration', type=int)
        data = parser.parse_args()



        # Update the current session data with real-time data from the Arduino
        global current_session_data
        current_session_data['jump_count'] = data['jump_count']
        current_session_data['set_count'] = data['set_count']
        current_session_data['set_duration'] = data['set_duration']

        # Store the data in the database
        add_session_data(data['jump_count'], data['set_count'], data['set_duration'])

        return {'message': 'Data received successfully'}

# Add the resource to the API
api.add_resource(ArduinoData, '/data')

if __name__ == '__main__':
    app.run(host='192.168.113.100', port=5000)

