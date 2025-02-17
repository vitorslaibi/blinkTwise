# BlinkTwise

BlinkTwise is a Python-based application that monitors a user's blink rate and duration using computer vision techniques. It leverages **OpenCV** and **MediaPipe** for blink detection and **Flask** for the web interface. The application helps users stay alert by providing real-time feedback on their blink patterns.

## Features

- **User Authentication**: Users can register, log in, and manage their profiles.
- **Blink Analysis**: Real-time blink detection and analysis based on selected activities (e.g., reading, conversational).
- **Activity-Based Thresholds**: Different blink rate thresholds for various activities.
- **Blink History**: View past blink analysis sessions.
- **Settings**: Customize alarm and activity settings.
- **Live Video Feed**: Display a live video feed for blink analysis (optional).

## Technologies Used

- **Python**: Core programming language.
- **Flask**: Web framework for building the application.
- **OpenCV**: Computer vision library for video processing.
- **MediaPipe**: Facial landmark detection for blink detection.
- **SQLAlchemy**: Database management for storing user data and blink records.
- **Bootstrap**: Front-end framework for responsive design.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/BlinkTwise.git
   cd BlinkTwise
Create a Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

pip install -r requirements.txt

Set Up the Database:

Initialize the database:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Run the Application:

python run.py

Access the Application:
Open your browser and navigate to http://127.0.0.1:5000.

Usage
Register or Log In:

Create a new account or log in with existing credentials.

Start Blink Analysis:

Go to the Profile page.

Select an activity (e.g., reading, conversational).

Click Start Analysis to begin monitoring your blink rate.

View Blink History:

Check the Blink History section on the Profile page to view past sessions.

Customize Settings:

Navigate to the Settings page to enable/disable alarms and activities.

Live Video Feed (Optional):

If enabled, the live video feed will display on the Profile page during blink analysis.

Project Structure
Copy
BlinkTwise/
│
├── app/                      # Flask application
│   ├── __init__.py           # Flask app initialization
│   ├── routes.py             # Flask routes (views)
│   ├── models.py             # Database models (SQLAlchemy)
│   ├── forms.py              # Flask-WTF forms for user input
│   ├── templates/            # HTML templates (Jinja2)
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Home page
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration page
│   │   ├── profile.html      # User profile page
│   │   ├── settings.html     # Settings page
│   │   └── analysis.html     # Blink analysis page
│   ├── static/               # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/                # Utility functions
│       ├── detector.py       # Blink detection logic
│       └── helpers.py        # Helper functions (e.g., alerts, prompts)
│
├── migrations/               # Database migrations (Flask-Migrate)
├── requirements.txt          # Python dependencies
├── run.py                    # Entry point to run the Flask app
└── README.md                 # Project documentation
Contributing
Contributions are welcome! If you'd like to contribute to BlinkTwise, please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeatureName).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeatureName).

Open a pull request.