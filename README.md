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
│       ├── detector.py       # Updated blink detection logic
│       └── helpers.py        # Helper functions (e.g., alerts, prompts)
│
├── config.py                 # Configuration file (e.g., Flask settings, database URI)
├── requirements.txt          # Python dependencies
├── run.py                    # Entry point to run the Flask app
└── README.md                 # Project documentation