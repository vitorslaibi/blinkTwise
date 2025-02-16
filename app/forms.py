from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

# Analysis Form
class AnalysisForm(FlaskForm):
    activity = SelectField('Activity', choices=[
        ('reading', 'Reading'),
        ('gaze', 'Gaze'),
        ('conversational', 'Conversational')
    ], validators=[DataRequired()])
    submit = SubmitField('Start Analysis')

# Calibration Form
class CalibrationForm(FlaskForm):
    submit = SubmitField('Start Calibration')

# Alarm Settings Form
class AlarmSettingsForm(FlaskForm):
    disable_alarms = BooleanField('Disable Alarms')
    submit = SubmitField('Save Settings')

# Activity Settings Form
class ActivitySettingsForm(FlaskForm):
    disable_activities = BooleanField('Disable Activities')
    submit = SubmitField('Save Settings')