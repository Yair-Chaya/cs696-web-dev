# Import the Flask class from the flask module
from flask import Flask
from flask import render_template
import requests
from flask import request, jsonify
import time

# Create an instance of the Flask class. This instance will be our WSGI application.
app = Flask(__name__)

# Create a simple user data store
users = {
    'user1': {'username': 'user1', 'password': 'pass1', 'full_name': 'Daniel B'},
    'user2': {'username': 'user2', 'password': 'pass2', 'full_name': 'Jessica V'},
    'user3': {'username': 'user3', 'password': 'pass3', 'full_name': 'Julia G'}
}

@app.route('/')
def index():
    print("Index endpoint called")
    # Render the index.html template when the root URL is accessed
    return render_template('text_from_flask.html')

@app.route('/api/data')
def api_data():
    print("API data endpoint called")
    # Return a JSON response when the /api/data URL is accessed
    time.sleep(1)
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/login', methods=['POST'])
def login():
    print("Login endpoint called")
    print("Request data:", request.json)
    
    # Get the username and password from the request
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Check if the user exists in the user store and the password matches
    if username in users and users[username]['password'] == password:
        return jsonify({'authenticated': True, 'full_name': users[username]['full_name']})
    else:
        return jsonify({'authenticated': False, 'message': 'Invalid username or password'}), 401
    

@app.route('/register', methods=['POST'])
def register():
    print("Register endpoint called")
    print("Request data:", request.json)
    
    # Get the username and password from the request
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Check if the user already exists
    if username in users:
        return jsonify({'registered': False, 'message': 'Username already exists'}), 400
    
    # Register the new user
    users[username] = {'username': username, 'password': password, 'full_name': data.get('full_name', '')}
    return jsonify({'registered': True, 'message': 'User registered successfully'})


@app.route('/users', methods=['GET'])
def get_users():
    print("Get users endpoint called")
    
    # Return the list of users as JSON
    return jsonify(users)

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    print("Get user endpoint called")
    
    # Check if the user exists
    if username in users:
        return jsonify(users[username])
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/users/delete/<username>', methods=['DELETE'])
def delete_user(username):
    print("Delete user endpoint called")
    
    # Check if the user exists
    if username in users:
        del users[username]
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/users/delete', methods=['DELETE'])
def delete_user_from_payload():
    print("Delete user from payload endpoint called")
    
    # Get the username from the request
    data = request.json
    username = data.get('username')
    
    # Check if the user exists
    if username in users:
        del users[username]
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

 
# Check if the executed script is the main program and run the Flask application.
# The debug=True option enables Flask's debugger, showing detailed error pages when an error occurs.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)