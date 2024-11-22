from flask import Blueprint

# Define the blueprint for the 'user' module
user = Blueprint('user', __name__)

# Import routes associated with this blueprint
from . import routes
