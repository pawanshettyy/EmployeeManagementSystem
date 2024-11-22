from flask import Blueprint

# Create a Blueprint for authentication-related routes
auth = Blueprint('auth', __name__)

# Import the routes for this Blueprint
from . import routes
