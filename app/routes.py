from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User, Session, BlinkRecord
from datetime import datetime

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/start_session', methods=['POST'])
@login_required
def start_session():
    activity_type = request.form['activity_type']
    session = Session(user_id=current_user.id, activity_type=activity_type)
    db.session.add(session)
    db.session.commit()
    return jsonify({'session_id': session.id})

@app.route('/record_blink', methods=['POST'])
@login_required
def record_blink():
    data = request.get_json()
    blink_record = BlinkRecord(
        session_id=data['session_id'],
        start_time=datetime.fromtimestamp(data['start_time']),
        end_time=datetime.fromtimestamp(data['end_time']),
        duration=data['duration']
    )
    db.session.add(blink_record)
    db.session.commit()
    return jsonify({'status': 'success'})