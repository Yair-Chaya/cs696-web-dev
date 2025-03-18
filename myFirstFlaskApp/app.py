# Import the Flask class from the flask module
from flask import Flask
from flask import render_template
import requests
from flask import request, jsonify
import time

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, ValidationError

import os
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
# Create an instance of the Flask class. This instance will be our WSGI application.

def my_length_check(form, field):
    if len(field.data) > 5:
        raise ValidationError('Field must be less than 50 characters')

class NameForm(FlaskForm):
    name = StringField('Name', [InputRequired(), my_length_check])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        return f'Hello, {name}!'
    return render_template('index.html', form=form)
 
# Check if the executed script is the main program and run the Flask application.
# The debug=True option enables Flask's debugger, showing detailed error pages when an error occurs.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)