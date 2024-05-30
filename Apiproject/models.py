from Apiproject import database, login_manager
from datetime import datetime
from flask_login import UserMixin
import secrets

# This function is used by Flask-Login to load a user by their user ID.
@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))

# The User class represents users in the application.
# It includes fields for the user's email, password, and a unique webhook adress.
# It also establishes a relationship with the Webhookinfo class.
class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    webhook_adress = database.Column(database.String, nullable=False, unique=True, default=secrets.token_hex(8))
    webhookinfos = database.relationship('Webhookinfo', backref='autor', lazy=True)

# The Webhookinfo class represents information received through webhooks.
# It includes fields for the name, email, status, value, payment term, number of installments, and action.
# It also includes a foreign key that links each entry to a user via their webhook adress.
class Webhookinfo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    name = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    status = database.Column(database.String, nullable=False)
    value = database.Column(database.Integer, nullable=False)
    payment_term = database.Column(database.String, nullable=False)
    installments = database.Column(database.Integer, nullable=False)
    action = database.Column(database.String, nullable=True)
    webhook_user = database.Column(database.Integer, database.ForeignKey('user.webhook_adress'), nullable=False)
