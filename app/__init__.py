from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from datetime import datetime  # Add this import

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from app.routes import main  # Import the Blueprint
    app.register_blueprint(main)  # Register it
    
    # Add a custom Jinja filter for datetime formatting
    @app.template_filter('datetime')
    def format_datetime(value, format="%Y-%m-%d %H:%M:%S"):
        if value is None:
            return ""
        return value.strftime(format)

    # Register Blueprints
    from app.routes import main_routes
    from app.auth import auth
    app.register_blueprint(main_routes)
    app.register_blueprint(auth)

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app