from flask import request, render_template, flash
from flask_login import login_required, current_user
from datetime import datetime
from .modules import *  # Import the necessary functions
from . import user  # Import the 'user' blueprint
from src.app import db  # Import database object from the app module
from src.models import *  # Import the required models (e.g., User, demande_conge, avance_salaire)

# Helper function to get the current user's full name and role
def fullname_role():
    """
    Retrieves the full name and role (Administrator/Employee) of the current user.

    Returns:
        tuple: A tuple containing the full name and role of the user.
    """
    fullname = current_user.first_name + " " + current_user.last_name
    is_admin = 'Administrator' if current_user.is_admin == 1 else 'Employee'
    return (fullname, is_admin)

# Function to handle leave request submission
def RequestLeave():
    """
    Handles the process of submitting a leave request for the current user.
    Validates the date inputs, checks if there's an existing pending request,
    and saves the new leave request to the database.

    Returns:
        Response: A response object rendering the leave request page, with appropriate flash messages.
    """
    employee_id = current_user.employee_id
    leave_type = request.form["leave-type"]
    reason = request.form["reason"]

    try:
        # Parse the start and end dates from the form
        date_start = request.form["date_start"].strip()
        date_start = datetime.strptime(date_start, '%d/%m/%Y')

        date_end = request.form["date_end"].strip()
        date_end = datetime.strptime(date_end, '%d/%m/%Y')
    except:
        flash("Wrong date format. Please use dd/mm/yyyy format.")
        return render_template("user/request_leave.html")

    # Check if there's a pending leave request
    existing_request = demande_conge.query.filter_by(employee_id=employee_id).first()
    if existing_request:
        flash("You have a leave request pending approval.")
        return render_template("user/request_leave.html")

    # Create a new leave request and save it to the database
    new_request = demande_conge(employee_id=employee_id, type_conge=leave_type, 
                                 date_deb=date_start, date_fin=date_end, motif=reason)
    db.session.add(new_request)
    db.session.commit()
    flash("Leave request successfully submitted.")
    return render_template("user/request_leave.html")

# Function to handle salary advance request submission
def RequestAdvance():
    """
    Handles the process of submitting a salary advance request for the current user.
    Checks if there's an existing pending request and saves the new request to the database.

    Returns:
        Response: A response object rendering the salary advance request page, with appropriate flash messages.
    """
    employee_id = current_user.employee_id
    requested_amount = request.form["requested_amount"]
    reason = request.form["reason"]

    # Check if there's a pending salary advance request
    existing_request = avance_salaire.query.filter_by(employee_id=employee_id).first()
    if existing_request:
        flash("You have a salary advance request pending approval.")
        return render_template("user/request_advance.html")

    # Create a new salary advance request and save it to the database
    new_request = avance_salaire(employee_id=employee_id, montant=requested_amount, motif=reason)
    db.session.add(new_request)
    db.session.commit()
    flash("Salary advance request successfully submitted.")
    return render_template("user/request_advance.html")

# Route for requesting leave
@user.route("/request_leave", methods=['POST', 'GET'])
@login_required
def request_leave():
    """
    Displays the leave request form or handles the form submission.
    If the request method is POST, it calls RequestLeave() to process the leave request.

    Returns:
        Response: A response object rendering the leave request page.
    """
    if request.method == 'POST':
        return RequestLeave()  # Call RequestLeave function to handle the request
    else:
        fullname, role = fullname_role()  # Get the user's full name and role
        return render_template('user/request_leave.html', fullname=fullname, role=role)  # Render the leave form

# Route for requesting a salary advance
@user.route("/request_advance", methods=['POST', 'GET'])
@login_required
def request_advance():
    """
    Displays the salary advance request form or handles the form submission.
    If the request method is POST, it calls RequestAdvance() to process the advance request.

    Returns:
        Response: A response object rendering the salary advance request page.
    """
    if request.method == 'POST':
        return RequestAdvance()  # Call RequestAdvance function to handle the request
    fullname, role = fullname_role()  # Get the user's full name and role
    return render_template('user/request_advance.html', fullname=fullname, role=role)  # Render the advance form

# Route for viewing the status of leave and salary advance requests
@user.route('/follow_up')
@login_required
def follow_up():
    """
    Displays the status of the current user's leave and salary advance requests.
    If there are pending requests, it shows the status (Pending, Accepted, Declined).

    Returns:
        Response: A response object rendering the follow-up page with the current user's requests.
    """
    fullname, role = fullname_role()  # Get the user's full name and role

    employee_id = current_user.employee_id  # Get the employee ID
    leave = demande_conge.query.filter_by(employee_id=employee_id).first()  # Check if the user has a pending leave request
    advance = avance_salaire.query.filter_by(employee_id=employee_id).first()  # Check if the user has a pending salary advance request

    leave_list = {}
    advance_list = {}

    if leave or advance:
        # Process leave request status
        if leave:
            leave_status = 'Pending'
            if leave.status == 1:
                leave_status = 'Accepted'
            elif leave.status == 0:
                leave_status = 'Declined'

            leave_list = {
                'employee_id': leave.employee_id,
                'nom': User.query.filter_by(employee_id=leave.employee_id).first().first_name,
                'type': leave.type_conge,
                'date_deb': leave.date_deb,
                'date_fin': leave.date_fin,
                'motif': leave.motif,
                'status': leave_status
            }

        # Process salary advance status
        if advance:
            advance_status = 'Pending'
            if advance.status == 1:
                advance_status = 'Accepted'
            elif advance.status == 0:
                advance_status = 'Declined'

            advance_list = {
                'employee_id': advance.employee_id,
                'nom': User.query.filter_by(employee_id=advance.employee_id).first().first_name,
                'montant': advance.montant,
                'motif': advance.motif,
                'status': advance_status
            }

        # Render the follow-up page with leave and advance request details
        return render_template('user/followup.html', leave=leave_list, advance=advance_list, fullname=fullname, role=role)
    else:
        # If no leave or salary advance requests, render an empty follow-up page
        return render_template('user/followup.html', leave=None, advance=None, fullname=fullname, role=role)
