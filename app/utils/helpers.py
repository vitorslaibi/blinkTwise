from flask import flash

def show_alert(message, category="info"):
    """
    Display an alert message to the user using Flask's flash system.
    """
    flash(message, category)

def validate_blink_rate(blink_rate, activity):
    """
    Validate the user's blink rate based on their current activity.
    Returns a message if the blink rate is outside the recommended range.
    """
    activity_thresholds = {
        "reading": (12, 20),  # (min_blinks, max_blinks) per minute
        "gaze": (15, 25),
        "conversational": (10, 18)
    }

    if activity not in activity_thresholds:
        return "Invalid activity."

    min_blinks, max_blinks = activity_thresholds[activity]

    if blink_rate < min_blinks:
        return f"Your blink rate is low ({blink_rate} blinks/min). Consider taking a break."
    elif blink_rate > max_blinks:
        return f"Your blink rate is high ({blink_rate} blinks/min). Consider resting your eyes."

    return None

def calculate_bpm(blink_count, session_duration):
    """
    Calculate blinks per minute (BPM) based on blink count and session duration.
    """
    if session_duration == 0:
        return 0
    return (blink_count / session_duration) * 60