from flask import Blueprint  # Import Blueprint class from Flask

home = Blueprint('home', __name__)  # Create a blueprint named 'home', using the current module (__name__) as its context.

from . import routes  # Import routes (or views) for the 'home' blueprint from the routes file in the same package
