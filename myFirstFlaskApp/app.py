# Import the Flask class from the flask module
from flask import Flask
from flask import render_template

# Create an instance of the Flask class. This instance will be our WSGI application.
app = Flask(__name__)

# Define a route for the root URL ("/"). Flask uses Python decorators to associate
# URLs with functions. This route is the "home" route.
@app.route('/')
def hello_world():
    # This function is called when the root URL is accessed. It returns the string
    # "Hello, World!" which is displayed in the client's web browser.
    return render_template('index.html')

@app.route('/users/<username>')
def hello_username(username):
    # This function is called when a URL matching "/users/<username>" is accessed.
    return render_template('hello_name.html', name=username)

@app.route('/users/<username>/<age>')
def hello_username_Age(username, age):
    # This function is called when a URL matching "/users/<username>" is accessed.
    return render_template('hello_name_age.html', name=username, age=age)
 
# Check if the executed script is the main program and run the Flask application.
# The debug=True option enables Flask's debugger, showing detailed error pages when an error occurs.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)