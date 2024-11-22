from flask import flash
from flask_login import current_user
from src.models import *  # Assuming necessary models are imported

def AdminOnly():
    employee_id = current_user.employee_id  # Retrieve the current user's employee ID
    if current_user.is_admin == 0:  # If the current user is not an admin
        flash("Administrative access only")  # Flash an error message
    return True if current_user.is_admin == 1 else False  # Return True if the user is an admin, otherwise False
