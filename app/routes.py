from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, AnalysisForm, CalibrationForm, AlarmSettingsForm, ActivitySettingsForm
from app.models import User, Session, BlinkRecord
from app.utils.detector import detect_blinks
from app.utils.helpers import validate_blink_rate, calculate_bpm
from datetime import datetime

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# User Profile Page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    analysis_form = AnalysisForm()
    blink_history = Session.query.filter_by(user_id=current_user.id).order_by(Session.begin_time.desc()).all()

    if analysis_form.validate_on_submit():
        # Start blink analysis based on selected activity
        activity = analysis_form.activity.data
        return redirect(url_for('analysis', activity=activity))

    return render_template('profile.html', analysis_form=analysis_form, blink_history=blink_history)

# Blink Analysis Page
@app.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    activity = request.args.get('activity', 'reading')  # Default to 'reading' if no activity is provided
    return render_template('analysis.html', activity=activity)

# Start Blink Analysis (AJAX/WebSocket endpoint)
@app.route('/start_analysis', methods=['POST'])
@login_required
def start_analysis():
    # Start blink detection process
    # This could involve starting a background thread or process
    return jsonify({'status': 'success', 'message': 'Blink analysis started'})

# Stop Blink Analysis (AJAX/WebSocket endpoint)
@app.route('/stop_analysis', methods=['POST'])
@login_required
def stop_analysis():
    # Stop blink detection process
    return jsonify({'status': 'success', 'message': 'Blink analysis stopped'})

# Get Real-Time Blink Data (AJAX/WebSocket endpoint)
@app.route('/get_blink_data')
@login_required
def get_blink_data():
    # Fetch real-time blink data (mock data for now)
    blink_count = 10
    closed_time = 0.5
    interval_time = 2.0
    bpm = calculate_bpm(blink_count, interval_time)

    return jsonify({
        'blink_count': blink_count,
        'closed_time': closed_time,
        'interval_time': interval_time,
        'bpm': bpm
    })

# Settings Page
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    calibration_form = CalibrationForm()
    alarm_form = AlarmSettingsForm()
    activity_form = ActivitySettingsForm()

    if calibration_form.validate_on_submit():
        # Handle calibration logic
        flash('Calibration started.', 'info')
        return redirect(url_for('settings'))

    if alarm_form.validate_on_submit():
        # Update alarm settings
        current_user.disable_alarms = alarm_form.disable_alarms.data
        db.session.commit()
        flash('Alarm settings updated.', 'success')
        return redirect(url_for('settings'))

    if activity_form.validate_on_submit():
        # Update activity settings
        current_user.disable_activities = activity_form.disable_activities.data
        db.session.commit()
        flash('Activity settings updated.', 'success')
        return redirect(url_for('settings'))

    return render_template('settings.html', calibration_form=calibration_form, alarm_form=alarm_form, activity_form=activity_form)

# Video Feed for Blink Analysis
@app.route('/video_feed')
@login_required
def video_feed():
    # Stream video feed for blink analysis
    # This would involve integrating OpenCV and Flask's streaming capabilities
    return "Video feed placeholder"

# Calibration Endpoint
@app.route('/calibrate', methods=['POST'])
@login_required
def calibrate():
    # Handle calibration logic
    flash('Calibration completed.', 'success')
    return redirect(url_for('settings'))