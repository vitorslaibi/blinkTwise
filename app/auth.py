# app/database.py
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app import db
from app.models import User, Session, BlinkRecord

class DatabaseManager:
    @staticmethod
    def create_user(username, password_hash, age=None):
        """Create a new user in the database."""
        try:
            user = User(
                username=username,
                password_hash=password_hash,
                age=age
            )
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_by_username(username):
        """Retrieve a user by their username."""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create_session(user_id, activity_type):
        """Create a new monitoring session."""
        try:
            session = Session(
                user_id=user_id,
                activity_type=activity_type,
                begin_time=datetime.utcnow(),
                total_blinks=0,
                prompts_given=0,
                alerts_given=0
            )
            db.session.add(session)
            db.session.commit()
            return session
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def end_session(session_id):
        """End a monitoring session."""
        try:
            session = Session.query.get(session_id)
            if session:
                session.end_time = datetime.utcnow()
                db.session.commit()
                return session
            return None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def record_blink(session_id, start_time, end_time=None, duration=None):
        """Record a blink event."""
        try:
            blink = BlinkRecord(
                session_id=session_id,
                start_time=start_time,
                end_time=end_time,
                duration=duration
            )
            db.session.add(blink)
            
            # Update session blink count
            session = Session.query.get(session_id)
            session.total_blinks += 1
            
            db.session.commit()
            return blink
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_statistics(user_id):
        """Get comprehensive statistics for a user."""
        try:
            # Get total sessions
            total_sessions = Session.query.filter_by(user_id=user_id).count()

            # Get total monitoring time
            total_time = db.session.query(
                func.sum(Session.end_time - Session.begin_time)
            ).filter_by(user_id=user_id).scalar()

            # Calculate average blinks per minute across all sessions
            sessions = Session.query.filter_by(user_id=user_id).all()
            total_bpm = 0
            valid_sessions = 0

            for session in sessions:
                if session.end_time and session.total_blinks > 0:
                    duration = (session.end_time - session.begin_time).total_seconds() / 60
                    if duration > 0:
                        total_bpm += session.total_blinks / duration
                        valid_sessions += 1

            avg_bpm = total_bpm / valid_sessions if valid_sessions > 0 else 0

            return {
                'total_sessions': total_sessions,
                'total_time': total_time,
                'avg_bpm': avg_bpm
            }
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return None

    @staticmethod
    def get_recent_sessions(user_id, limit=5):
        """Get recent sessions with detailed metrics."""
        try:
            return Session.query.filter_by(user_id=user_id)\
                .order_by(Session.begin_time.desc())\
                .limit(limit)\
                .all()
        except Exception as e:
            print(f"Error fetching recent sessions: {e}")
            return []

    @staticmethod
    def get_session_details(session_id):
        """Get detailed metrics for a specific session."""
        try:
            session = Session.query.get(session_id)
            if not session:
                return None

            # Calculate session duration
            duration = (session.end_time - session.begin_time).total_seconds() if session.end_time else 0
            
            # Calculate blinks per minute
            bpm = (session.total_blinks / (duration / 60)) if duration > 0 else 0

            # Get blink intervals
            blinks = BlinkRecord.query.filter_by(session_id=session_id)\
                .order_by(BlinkRecord.start_time).all()
            
            intervals = []
            for i in range(len(blinks) - 1):
                interval = (blinks[i+1].start_time - blinks[i].end_time).total_seconds()
                intervals.append(interval)

            avg_interval = sum(intervals) / len(intervals) if intervals else 0

            return {
                'session': session,
                'duration': duration,
                'bpm': bpm,
                'avg_blink_duration': sum(b.duration for b in blinks) / len(blinks) if blinks else 0,
                'avg_interval': avg_interval,
                'blink_records': blinks
            }
        except Exception as e:
            print(f"Error fetching session details: {e}")
            return None

    @staticmethod
    def get_activity_thresholds(activity_type):
        """Get blink rate thresholds for different activities."""
        thresholds = {
            'reading': {'min': 1.4, 'max': 14.4},
            'gaze': {'min': 8.0, 'max': 21.0},
            'conversational': {'min': 10.5, 'max': 32.5}
        }
        return thresholds.get(activity_type, {'min': -1, 'max': -1})

    @staticmethod
    def record_alert(session_id, alert_type):
        """Record when an alert is given to the user."""
        try:
            session = Session.query.get(session_id)
            if session:
                session.alerts_given += 1
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error recording alert: {e}")

    @staticmethod
    def get_user_trends(user_id, days=30):
        """Get blink rate trends over time."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            sessions = Session.query.filter(
                and_(
                    Session.user_id == user_id,
                    Session.begin_time >= start_date
                )
            ).all()

            trends = []
            for session in sessions:
                if session.end_time:
                    duration = (session.end_time - session.begin_time).total_seconds() / 60
                    if duration > 0:
                        trends.append({
                            'date': session.begin_time.date(),
                            'bpm': session.total_blinks / duration,
                            'activity_type': session.activity_type
                        })

            return trends
        except Exception as e:
            print(f"Error calculating trends: {e}")
            return []