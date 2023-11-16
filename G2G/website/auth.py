from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, current_user

auth = Blueprint('auth', __name__)

# Handles user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieves email and password from form
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Logs user in if password matches
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.explore'))
        else:
            # Displays error messages for failed login attempts
            flash('Incorrect email or password.', category='error')
    return render_template("login.html")

# Handles user sign-up
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        user = User.query.filter_by(email=email).first()
        if user:
            # Checks for existing email
            flash('Email already exists.', category='error')
        elif len(email) < 4 or len(password) < 7:
            # Displays error messages for invalid inputs
            flash('Invalid email or password.', category='error')
        elif password != confirm_password:
            # Displays error message for password mismatch
            flash('Passwords don\'t match.', category='error')
        else:
            # Creates a new user and logs them in
            new_user = User(email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.explore'))
    return render_template("sign_up.html", user=current_user)
