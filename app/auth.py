from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models import User
from app import db

# Create a Blueprint for authentication routes
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # In real apps, use password hashing!
        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('main.profile'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))