from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)

# Configure the app with settings from the config file
app.config.from_pyfile('./config.py')

# Initialize SQLAlchemy (for database handling)
db = SQLAlchemy(app)

# Set up session management with SQLAlchemy
app.config['SESSION_SQLALCHEMY'] = db

# Import models (defined in the models.py file)
from .models import *

# Register blueprints for different sections of the app

# Auth blueprint for login, logout, registration, etc.
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Admin blueprint for the admin-related views
from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

# User blueprint for user-related views (e.g., requesting leave, salary advances, etc.)
from .user import user as user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

# Home blueprint for the homepage
from .home import home as home_blueprint
app.register_blueprint(home_blueprint)

# Initialize the LoginManager to manage user sessions
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # The endpoint for login page
login_manager.init_app(app)  # Initialize LoginManager with the app

# Define user loader function to load user from the database using their user_id
@login_manager.user_loader
def load_user(user_id):
    """
    This function is used by Flask-Login to load a user by their user_id.
    
    Args:
        user_id (int): The user ID of the logged-in user.
        
    Returns:
        User: The User object that corresponds to the user_id.
    """
    return User.query.get(int(user_id))  # Query the User model to get the user by their ID

# Initialize the database tables (only when app context is available)
with app.app_context():
    # Create all the database tables as defined in the models
    db.create_all()

# ERROR HANDLING ROUTES

@app.errorhandler(404)
def page_not_found(error):
    """
    Handles 404 errors (page not found). It renders a custom 404 error page.
    
    Args:
        error (Exception): The error that triggered the handler.
        
    Returns:
        Response: A response object rendering the 404 error page.
    """
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def server_error(error):
    """
    Handles 500 errors (server errors). It renders a custom 500 error page.
    
    Args:
        error (Exception): The error that triggered the handler.
        
    Returns:
        Response: A response object rendering the 500 error page.
    """
    return render_template("errors/500.html"), 500

@app.errorhandler(401)
def access_denied(error):
    """
    Handles 401 errors (unauthorized access). It renders a custom 401 error page.
    
    Args:
        error (Exception): The error that triggered the handler.
        
    Returns:
        Response: A response object rendering the 401 error page.
    """
    return render_template("errors/401.html"), 401

# Expose the Flask app to be run
if __name__ == "__main__":
    app.run(debug=True)
