from flask import Flask
from flask import request, render_template, url_for, redirect
from flask import jsonify, make_response
from flask import session, flash
import bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configure the SQLAlchemy part
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # Local SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    about_me = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}', '{self.about_me}')"

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    user = db.relationship('User', backref=db.backref('interests', lazy=True))
    # Foreign key to link interest to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Interest('{self.name}', Description: {self.description}, '{self.user_id}')"
    
@app.route('/')
def show_all_users():
    users = User.query.all()
    if not users:
        return "No users found!"
    return '<br>'.join([f'Username: {user.username}, Email: {user.email}, About Me: {user.about_me}' for user in users])

@app.route('/add_user/<username>/<email>/<password>/<about_me>')
def add_user(username, email, password, about_me):
    new_user = User(username=username, email=email, password=password, about_me=about_me)
    db.session.add(new_user)
    db.session.commit()
    return f"User {username} added!"

@app.route('/delete_user/<username>')
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return f"User {username} deleted!"
    else:
        return f"User {username} not found!"
    
@app.route('/register/<username>/<email>/<password>/<about_me>')
def register(username, email, password, about_me):
    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "Username already exists!"
    # Create new user
    if not username or not email or not password:
        return "Username, email, and password are required!"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, email=email, password=hashed_password, about_me=about_me)
    db.session.add(new_user)
    db.session.commit()
    return f"User {username} registered!"

@app.route('/login/<username>/<password>')
def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard', username=username))
    else:
        flash('Invalid credentials!', 'danger')
        return redirect(url_for('login_page'))
    
@app.route('/dashboard/<username>')
def dashboard(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return f"Welcome to your dashboard, {user.username}! About Me: {user.about_me}"
    else:
        return "User not found!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
    
