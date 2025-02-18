from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Session
from app.forms import LoginForm, RegistrationForm, AnalysisForm, CalibrationForm
from app import db  # Import the db object
import cv2

# Create blueprints
main_routes = Blueprint('main', __name__)
auth_routes = Blueprint('auth', __name__)

# Main Routes
@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/calibrate', methods=['POST'])
@login_required
def calibrate():
    # Add calibration logic here
    flash('Calibration completed.', 'success')
    return redirect(url_for('main.settings'))

@main_routes.route('/profile')
@login_required
def profile():
    analysis_form = AnalysisForm()  # Create an instance of the AnalysisForm
    blink_history = Session.query.filter_by(user_id=current_user.id).order_by(Session.begin_time.desc()).all()
    return render_template('profile.html', analysis_form=analysis_form, blink_history=blink_history)

@main_routes.route('/settings')
@login_required
def settings():
    calibration_form = CalibrationForm()  # Create an instance of CalibrationForm
    return render_template('settings.html', calibration_form=calibration_form)

@main_routes.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html')

# Auth Routes
@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login successful!', 'success')
            return redirect(url_for('main.profile'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

from flask import jsonify

@main_routes.route('/start_analysis', methods=['POST'])
@login_required
def start_analysis():
    data = request.get_json()  # Get JSON data from the request
    activity = data.get('activity')  # Get the selected activity
    print(f"Starting analysis for activity: {activity}")  # Debugging

    # Add your blink analysis logic here
    # For now, just return a success message
    return jsonify({
        'status': 'success',
        'message': f'Blink analysis started for activity: {activity}'
    })

def generate_frames():
    camera = cv2.VideoCapture(0)  # Use the default camera
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@main_routes.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')