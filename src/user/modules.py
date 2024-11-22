from flask import request, render_template, flash
from flask_login import current_user
from src.app import db
from src.models import *
from datetime import datetime

# Helper function to get the user's full name and role
def fullname_role():
    # Get the full name of the user
    fullname = current_user.first_name + " " + current_user.last_name
    # Determine if the user is an Administrator or Employee
    is_admin = 'Administrator' if current_user.is_admin == 1 else 'Employee'
    return (fullname, is_admin)

# Function to handle the leave request
def RequestLeave():
    employee_id = current_user.employee_id
    leave_type = request.form["leave-type"]
    reason = request.form["reason"] 
    
    try:
        # Convert start date and end date from string to datetime object
        date_start = request.form["date_start"].strip()
        date_start = datetime.strptime(date_start, '%d/%m/%Y')   
        
        date_end = request.form["date_end"].strip()
        date_end = datetime.strptime(date_end, '%d/%m/%Y')   
    except:
        # If dates are invalid, show a flash message and return to the form
        flash("Wrong date format, please use dd/mm/yyyy")
        return render_template("user/request_leave.html")    
    
    # Check if the employee has a pending leave request
    row = demande_conge.query.filter_by(employee_id=employee_id).first()
    if row:
        flash("You have a leave request pending")
        return render_template("user/request_leave.html")
    
    # Create a new leave request if no pending request
    new_leave = demande_conge(employee_id=employee_id, type_conge=leave_type, date_deb=date_start, date_fin=date_end, motif=reason)
    db.session.add(new_leave)
    db.session.commit()
    flash("Leave request applied successfully")
    
    # Return to the leave request form after submission
    return render_template("user/request_leave.html")

# Function to handle the salary advance request
def RequestAdvance():
    employee_id = current_user.employee_id
    requested_amount = request.form["requested_amount"]
    reason = request.form["reason"] 
    
    # Check if the employee has a pending salary advance request
    row = avance_salaire.query.filter_by(employee_id=employee_id).first()
    if row:
        flash("You have a salary advance request pending")
        return render_template("user/request_advance.html")
    
    # Create a new salary advance request if no pending request
    new_advance = avance_salaire(employee_id=employee_id, montant=requested_amount, motif=reason)
    db.session.add(new_advance)
    db.session.commit()
    flash("Salary advance request applied successfully")
    
    # Return to the salary advance request form after submission
    return render_template("user/request_advance.html")
