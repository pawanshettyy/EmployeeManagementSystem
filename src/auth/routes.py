from flask import flash, request, render_template, url_for, redirect, send_from_directory, abort, after_this_request, session
from flask_login import login_user, logout_user, login_required, current_user

from .modules import *  # Import helper functions like LoginAccount and RegisterAccount
from . import auth  # Import the blueprint for the auth routes

# Route to handle user login
@auth.route("/login", methods=['POST', 'GET'])
def login():
    # If the request method is POST, handle the login logic
    if request.method == 'POST':
        response = LoginAccount()  # Call the function to handle the login
        return response  # Return the result from the login function
    else:
        # If the request method is GET, simply render the login page
        return render_template('auth/login.html')    

# Route to handle user registration
@auth.route("/register", methods=['POST', 'GET'])
def register():
    # TODO: Add form validation before processing
    if request.method == 'POST':
        response = RegisterAccount()  # Call the function to handle registration
        return response  # Return the result from the registration function
    else:
        # If the request method is GET, render the registration page
        return render_template('auth/register.html')     

# Route to handle user logout
@auth.route('/logout')
def logout():
    logout_user()  # Log out the current user
    return redirect(url_for('auth.login'))  # Redirect to the login page

# Route to handle password reset or password change page
@auth.route("/motdepass", methods=['POST', 'GET'])
def motdepass():
    return render_template('auth/password.html')  # Render the password change page
