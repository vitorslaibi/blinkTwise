BlinkTwise/
│
├── app/
│   ├── __init__.py
│   ├── models.py          # Database models (SQLAlchemy)
│   ├── routes.py          # Flask routes
│   ├── auth.py            # Authentication logic
│   ├── detector.py        # Blink detection logic
│   ├── templates/         # HTML templates for Flask
│   │   ├── base.html      # Base template
│   │   ├── index.html     # Home page
│   │   ├── login.html     # Login page
│   │   ├── register.html  # Register page
│   │   ├── profile.html   # User profile page
│   │   ├── settings.html  # Settings page
│   └── static/            # Static files (CSS, JS, images)
│       ├── styles.css
│       └── logo_light.png
│
├── requirements.txt       # Python dependencies
├── config.py              # Configuration file
└── run.py                 # Entry point for the Flask app