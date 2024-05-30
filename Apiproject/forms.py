from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Apiproject.models import User


# Form for creating a new account, includes email, password, password confirmation, and a token
class FormCreateAccount(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8,14)])
    password_confirmation = PasswordField('Password Confirmation', validators=[DataRequired(), EqualTo('password')])
    token = StringField('Token', validators=[DataRequired()])
    button_submit_createaccount = SubmitField('Create account')

    # Custom validator to check if the email already exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Register with another email or log in to continue')

    # Custom validator to check if the provided token is correct
    def validate_token(self, token):
        mytoken = 'uhdfaAADF123'
        if mytoken != token.data:
            raise ValidationError('Incorrect token, try again!')


# Form for user login, includes email and password fields
class FormLogin (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 14)])
    button_submit_login = SubmitField('Login')


# Form for searching webhook information by email, includes email field and submit buttons
class FormSearch (FlaskForm):
    email = StringField('Email')
    button_submit_search = SubmitField('Search')
    button_submit_clean = SubmitField('Clean')