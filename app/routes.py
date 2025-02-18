from flask import Blueprint, render_template, redirect, url_for, flash, request, Response, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Session
from app.forms import LoginForm, RegistrationForm, AnalysisForm, CalibrationForm, AlarmSettingsForm, ActivitySettingsForm
from app.detector import detect_blinks, blink_ratio, LEFT_EYE, RIGHT_EYE
from app import db
import cv2
import mediapipe as mp
import time
import datetime
from threading import Thread

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Create blueprints
main_routes = Blueprint('main', __name__)
auth_routes = Blueprint('auth', __name__)

# --------------------------
# Main Routes
# --------------------------

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/profile')
@login_required
def profile():
    analysis_form = AnalysisForm()
    blink_history = Session.query.filter_by(user_id=current_user.id).order_by(Session.begin_time.desc()).all()
    return render_template('profile.html', 
                         analysis_form=analysis_form,
                         blink_history=blink_history)

@main_routes.route('/settings')
@login_required
def settings():
    calibration_form = CalibrationForm()
    alarm_form = AlarmSettingsForm()
    activity_form = ActivitySettingsForm()
    return render_template('settings.html',
                         calibration_form=calibration_form,
                         alarm_form=alarm_form,
                         activity_form=activity_form)

@main_routes.route('/analysis/<int:session_id>')
@login_required
def analysis(session_id):
    return render_template('analysis.html', session_id=session_id)

@main_routes.route('/test_webcam')
def test_webcam():
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    camera.release()
    return f"Webcam accessible: {success}"
# --------------------------
# Video Streaming & Analysis
# --------------------------

def generate_frames(session_id):
    camera = cv2.VideoCapture(0)
    session = Session.query.get(session_id)
    
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Process frame with MediaPipe Face Mesh
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            landmarks = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) 
                       for lm in results.multi_face_landmarks[0].landmark]
            
            ratio = blink_ratio(landmarks, RIGHT_EYE, LEFT_EYE)
            if ratio > 3.8:
                session.total_blinks += 1
                db.session.commit()

            cv2.putText(frame, f"Blinks: {session.total_blinks}", (10, 50), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@main_routes.route('/video_feed/<int:session_id>')
@login_required
def video_feed(session_id):
    return Response(generate_frames(session_id),
                  mimetype='multipart/x-mixed-replace; boundary=frame')
# --------------------------
# Data Endpoints
# --------------------------

@main_routes.route('/blink_data')
@login_required
def blink_data():
    session = Session.query.filter_by(user_id=current_user.id).order_by(Session.begin_time.desc()).first()
    if not session:
        return jsonify({'error': 'No active session'}), 404
    
    duration = (datetime.datetime.utcnow() - session.begin_time).total_seconds() / 60
    bpm = (session.total_blinks / duration) if duration > 0 else 0
    
    return jsonify({
        'blink_count': session.total_blinks,
        'bpm': bpm
    })

# --------------------------
# Form Handlers
# --------------------------

@main_routes.route('/start_analysis', methods=['POST'])
@login_required
def start_analysis():
    session = Session(
        user_id=current_user.id,
        begin_time=datetime.datetime.utcnow(),
        total_blinks=0
    )
    db.session.add(session)
    db.session.commit()
    return redirect(url_for('main.analysis', session_id=session.id))  # Pass session_id

@main_routes.route('/calibrate', methods=['POST'])
@login_required
def calibrate():
    flash('Calibration completed', 'success')
    return redirect(url_for('main.settings'))

@main_routes.route('/update_alarm_settings', methods=['POST'])
@login_required
def update_alarm_settings():
    if request.form.get('disable_alarms'):
        current_user.disable_alarms = True
    else:
        current_user.disable_alarms = False
    
    db.session.commit()
    flash('Alarm settings updated', 'success')
    return redirect(url_for('main.settings'))

@main_routes.route('/update_activity_settings', methods=['POST'])
@login_required
def update_activity_settings():
    if request.form.get('disable_activities'):
        current_user.disable_activities = True
    else:
        current_user.disable_activities = False
    
    db.session.commit()
    flash('Activity settings updated', 'success')
    return redirect(url_for('main.settings'))

# --------------------------
# Authentication Routes
# --------------------------

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
        flash('Invalid credentials', 'danger')
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
        flash('Registration successful! Please login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('main.index'))