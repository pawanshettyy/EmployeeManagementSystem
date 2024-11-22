from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user
from src.app import db
from src.models import User
from datetime import datetime

# Function to handle login
def LoginAccount():
    # Retrieve the employee_id and password from the form
    employee_id = request.form["employee_id"]
    password = request.form["password"]
    
    # Query the database for the user with the given employee_id
    user = User.query.filter_by(employee_id=employee_id).first()

    # Check if the user exists and if the password matches
    if not user or user.password != password:
        # If invalid, flash a message and render the login page again
        flash('Please verify your information and try again.')
        return render_template('auth/login.html')
    
    # If valid, log the user in and redirect to the home page
    login_user(user, remember=False)
    return redirect(url_for('home.home'))

# Function to handle user registration
def RegisterAccount():
    # Retrieve data from the registration form
    employee_id = request.form["employee_id"]
    first_name = request.form["inputFirstName"]
    last_name = request.form["inputLastName"]
    gender = request.form["inputGender"]
    date_of_birth_str = request.form["inputDOB"]
    date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()  # Convert to Python date object
    email = request.form["inputEmail"]
    password = request.form["inputPassword"]
    address = request.form["address"]
    dep = request.form["dep"]
    is_admin = request.form["is_admin"]
    phone = request.form["phone"]

    # Check if a user already exists with the given employee_id
    existing_user = User.query.filter_by(employee_id=employee_id).first()
    if existing_user:
        # If the user already exists, flash a message and render the registration page
        flash("This employee ID is already registered.")
        return render_template("auth/register.html")
    
    # Create a new user object with the data from the form
    new_user = User(
        employee_id=employee_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        date_of_birth=date_of_birth,
        email=email,
        password=password,
        phone=phone,
        address=address,
        dep_name=dep,
        salaire=None,  # Assuming salary is handled separately
        is_admin=True if "Yes" in is_admin else False
    )

    # Add the new user to the database and commit the changes
    db.session.add(new_user)
    db.session.commit()
    
    # Flash a success message and render the registration page
    flash("Your account has been successfully created!")
    return render_template("auth/register.html")
