from Apiproject import app, database, bcrypt
from flask import render_template, url_for, request, redirect, jsonify
from Apiproject.forms import FormLogin, FormCreateAccount, FormSearch
from Apiproject.models import User, Webhookinfo
from flask_login import login_user, logout_user, current_user, login_required
import json

# Route to handle the main dashboard page
@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    form_search = FormSearch()
    # Handle search form submission
    if form_search.validate_on_submit() and 'button_submit_search' in request.form:
        email_query = form_search.email.data
        webhookinfos = Webhookinfo.query.filter_by(webhook_user=current_user.webhook_adress, email=email_query).order_by(Webhookinfo.id.desc()).all()
    # Handle search form reset
    elif form_search.validate_on_submit() and 'button_submit_clean' in request.form:
        webhookinfos = Webhookinfo.query.filter_by(webhook_user=current_user.webhook_adress).order_by(Webhookinfo.id.desc()).all()
    # Default case to display all webhook information
    else:
        webhookinfos = Webhookinfo.query.filter_by(webhook_user=current_user.webhook_adress).order_by(Webhookinfo.id.desc()).all()

    return render_template('main.html', webhookinfos=webhookinfos, form_search=form_search)

# Route to handle user login
@app.route('/', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    # Validate login form submission
    if form_login.validate_on_submit() and 'button_submit_login' in request.form:
        user = User.query.filter_by(email=form_login.email.data).first()
        # Check if user exists and password matches
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=False)
            return redirect(url_for('main'))

    return render_template('login.html', form_login=form_login)

# Route to handle user account creation
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form_createaccount = FormCreateAccount()
    # Validate account creation form submission
    if form_createaccount.validate_on_submit() and 'button_submit_createaccount' in request.form:
        # Encrypt password
        password_crypted = bcrypt.generate_password_hash(form_createaccount.password.data)
        # Create a new user instance
        user = User(email=form_createaccount.email.data, password=password_crypted)
        # Add new user to the database
        database.session.add(user)
        # Commit the transaction
        database.session.commit()
        return redirect(url_for('login'))

    return render_template('create_account.html', form_createaccount=form_createaccount)

# Route to handle user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Route to handle incoming webhook data
@app.route('/<webhook_adress>', methods=['POST'])
def receive_data(webhook_adress):
    user = User.query.filter_by(webhook_adress=webhook_adress).first()
    if not user:
        return jsonify({'error': 'Invalid webhook token'}), 404

    # Initialize the data variable
    data = {}

    # Check if the request content type is JSON
    if request.is_json:
        data = request.get_json()
    # Check if the request content type is form-data or x-www-form-urlencoded
    elif request.form:
        data = request.form.to_dict()
    # Fallback to treating the data as plain text
    elif request.data:
        try:
            data = json.loads(request.data.decode('utf-8'))
            if isinstance(data, str):
                return jsonify({'error': 'Unsupported content type or invalid JSON'}), 415
        except ValueError:
            return jsonify({'error': 'Unsupported content type or invalid JSON'}), 415
    else:
        return jsonify({'error': 'Unsupported content type'}), 415

    # Ensure data is a dictionary before proceeding
    if not isinstance(data, dict):
        return jsonify({'error': 'Data format is invalid'}), 400

    # Extract data from the dictionary
    name = data.get('nome')
    email = data.get('email')
    status = data.get('status')
    value = data.get('valor')
    payment_term = data.get('forma_pagamento')
    installments = data.get('parcelas')

    if not all([name, email, status, value, payment_term, installments]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Determine action based on status
    if status == 'aprovado':
        action = "grant him access to the course"
    elif status == 'reembolsado':
        action = "revoke his access to the course"
    elif status == 'recusado':
        action = "send payment declined message"
    else:
        action = ''

    webhook_user = user.webhook_adress

    # Create a new instance of Webhookinfo
    new_entry = Webhookinfo(
        name=name,
        email=email,
        status=status,
        value=value,
        payment_term=payment_term,
        installments=installments,
        action=action,
        webhook_user=webhook_user
    )

    # Add the new entry to the database
    database.session.add(new_entry)
    # Commit the transaction
    database.session.commit()

    return jsonify({'message': 'Data received and stored successfully'}), 201
