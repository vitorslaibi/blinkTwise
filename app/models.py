from datetime import datetime
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    age = db.Column(db.Integer)
    sessions = db.relationship('Session', backref='user', lazy=True)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    begin_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    total_blinks = db.Column(db.Integer, default=0)
    prompts_given = db.Column(db.Integer, default=0)
    alerts_given = db.Column(db.Integer, default=0)
    activity_type = db.Column(db.String(32))
    blink_records = db.relationship('BlinkRecord', backref='session', lazy=True)

class BlinkRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Float)