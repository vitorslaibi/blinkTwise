from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    settings_id = db.Column(db.Integer, db.ForeignKey('settings.id'))

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blink_threshold = db.Column(db.Float, nullable=False)
    alert_min = db.Column(db.Float)
    alert_max = db.Column(db.Float)
    system_mode = db.Column(db.String(32))

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    total_blinks = db.Column(db.Integer)
    prompts_given = db.Column(db.Integer)
    alerts_given = db.Column(db.Integer)

class BlinkRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)