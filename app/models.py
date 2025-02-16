from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    disable_alarms = db.Column(db.Boolean, default=False)
    disable_activities = db.Column(db.Boolean, default=False)
    settings_id = db.Column(db.Integer, db.ForeignKey('settings.id'))
    sessions = db.relationship('Session', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Settings Model
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blink_threshold = db.Column(db.Float, nullable=False)
    alert_min = db.Column(db.Float)
    alert_max = db.Column(db.Float)
    system_mode = db.Column(db.String(32))
    users = db.relationship('User', backref='settings', lazy=True)

# Session Model
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    begin_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    total_blinks = db.Column(db.Integer, default=0)
    prompts_given = db.Column(db.Integer, default=0)
    alerts_given = db.Column(db.Integer, default=0)
    blink_records = db.relationship('BlinkRecord', backref='session', lazy=True)

# Blink Record Model
class BlinkRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)