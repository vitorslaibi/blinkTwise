from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Settings, Session, BlinkRecord
from datetime import datetime

# Create a Blueprint for main routes
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html', session={"begin_time": datetime.now()})

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # In real apps, use password hashing!
            login_user(user)
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main_routes.route('/profile')
@login_required  # Use the login_required decorator from Flask-Login
def profile():
    return render_template('profile.html', user=current_user)

@main_routes.route('/settings')
@login_required  # Use the login_required decorator from Flask-Login
def settings():
    return render_template('settings.html', user=current_user)

@main_routes.route('/logout')
@login_required  # Use the login_required decorator from Flask-Login
def logout():
    logout_user()
    return redirect(url_for('main.index'))