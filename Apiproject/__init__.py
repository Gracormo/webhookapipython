from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize the Flask application
app = Flask(__name__)

# Set the secret key for session management and CSRF protection
app.config['SECRET_KEY'] = 'vf439374578h4h78t'
# Set the URI for the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize the SQLAlchemy ORM for database interactions
database = SQLAlchemy(app)
# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)
# Initialize LoginManager for handling user sessions
login_manager = LoginManager(app)
# Specify the view function to handle logins
login_manager.login_view = 'login'

# Import the routes module to register the routes with the Flask application
from Apiproject import routes