# admin.py - Blueprint for the admin section

from flask import Blueprint

# Define the blueprint for the 'admin' section
admin = Blueprint('admin', __name__)

# Import routes associated with the admin blueprint
from . import routes
