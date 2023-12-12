from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, current_user, logout_user, login_required

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
            #flash('Logged in successfully!', category='success')
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
        elif len(email) < 0 or len(password) < 0:
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
            return redirect(url_for('views.explore'))
    return render_template("sign_up.html", user=current_user)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def changePassword():
    if request.method == 'POST':
        old_password = request.form.get('oldPassword')
        new_password = request.form.get('newPassword')
        password_confirm = request.form.get('passwordConfirm')

        # Retrieve the current user
        user = User.query.get(current_user.id)

        # Check if the old password matches the user's password
        if not check_password_hash(user.password, old_password):
            flash('Incorrect old password.', category='error')
        elif len(new_password) < 1:
            flash('Please enter a new password.', category='error')
        elif new_password != password_confirm:
            flash('Passwords don\'t match.', category='error')
        else:
            # Update the user's password with the new one
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password updated successfully!', category='success')
            return redirect(url_for('views.manageAccount'))
 
    return render_template("manageAccount.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/manageAccount', methods=['GET', 'POST'])
@login_required
def manageAccount():
    return render_template("manageAccount.html")