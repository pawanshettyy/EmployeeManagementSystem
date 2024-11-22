from flask import flash, request, render_template, url_for, redirect
from flask_login import login_required
from src.app import db
from src.models import *
from .modules import *
from . import admin
from datetime import datetime

# Route for managing leave requests
@admin.route("/manage_leave", methods=['POST', 'GET'])
@login_required
def manage_leave():
    """
    Handles the management of employee leave requests. Only accessible by admins.

    - GET: Displays a list of pending leave requests.
    - POST: Accepts or declines a leave request.
    """
    result = AdminOnly()  # Check if the user is an admin
    if result == False:
        return redirect(url_for('home.home'))  # Redirect to home if not admin

    if request.method == 'POST':
        # Handle leave request approval or rejection
        employee_id = request.form["employee_id"]
        conge = demande_conge.query.filter_by(employee_id=employee_id).first()
        if request.form['submit_b'] == "Accept":
            conge.status = 1
            flash("Leave request is accepted")        
        if request.form['submit_b'] == 'Decline':
            conge.status = 0
            flash("Leave request is declined")        

        db.session.commit()
        return redirect(url_for('admin.manage_leave'))  # Reload the page after action
    
    else:          
        fullname, role = fullname_role()  # Get the admin's full name and role
        result = demande_conge.query.all()
        leave_list = []
        # Collect all pending leave requests
        for leave in result:
            if leave.status not in [1, 0]:
                leave_list.append({
                    'employee_id': leave.employee_id,
                    'firstname': User.query.filter_by(employee_id=leave.employee_id).first().first_name,
                    'type': leave.type_conge,
                    'start_date': leave.date_deb,
                    'end_date': leave.date_fin,
                    'reason': leave.motif
                })
        return render_template('admin/manage_leave.html', fullname=fullname, role=role, leave_list=leave_list)


# Route for managing salary advances
@admin.route("/manage_advances", methods=['POST', 'GET'])
@login_required
def manage_advances():
    """
    Handles the approval or rejection of salary advance requests. Only accessible by admins.

    - GET: Displays a list of pending salary advance requests.
    - POST: Accepts or declines a salary advance request.
    """
    result = AdminOnly()  # Check if the user is an admin
    if result == False:
        return redirect(url_for('home.home'))  # Redirect to home if not admin

    if request.method == 'POST':
        # Handle salary advance request approval or rejection
        employee_id = request.form["employee_id"]
        advance = avance_salaire.query.filter_by(employee_id=employee_id).first()
        if request.form['submit_b'] == "Accept":
            advance.status = 1
            flash("Salary advance request is accepted")        
        if request.form['submit_b'] == 'Decline':
            advance.status = 0
            flash("Salary advance request is declined")        

        db.session.commit()
        return redirect(url_for('admin.manage_advances'))  # Reload the page after action
    
    else:
        fullname, role = fullname_role()  # Get the admin's full name and role
        result = avance_salaire.query.all()
        advances_list = []
        # Collect all pending salary advance requests
        for advance in result:
            if advance.status not in [1, 0]:
                advances_list.append({
                    'employee_id': advance.employee_id,
                    'firstname': User.query.filter_by(employee_id=advance.employee_id).first().first_name,
                    'requested_amount': advance.montant,
                    'reason': advance.motif
                })
        return render_template('admin/manage_advances.html', fullname=fullname, role=role, advances_list=advances_list)


# Route for listing all employees
@admin.route("/list_employees", methods=['POST', 'GET'])
@login_required
def list_employees():
    """
    Displays a list of all employees in the system. Only accessible by admins.

    - GET: Lists all employees with details such as ID, name, department, and salary.
    - POST: Redirects to the employee's edit page if the edit button is clicked.
    """
    result = AdminOnly()  # Check if the user is an admin
    if result == False:
        return redirect(url_for('home.home'))  # Redirect to home if not admin

    if request.method == 'POST':
        return redirect(url_for('admin.edit_employee', employee_id=request.form["employee_id"]))  # Redirect to edit page
    
    fullname, role = fullname_role()  # Get the admin's full name and role
    users = User.query.all()
    list_users = []
    # Collect all employees for display
    for user in users:
        list_users.append({
            "employee_id": user.employee_id,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "dep": user.dep_name,
            "salary": user.salaire
        })
    return render_template('admin/list_employees.html', list_users=list_users, fullname=fullname, role=role)


# Route for editing an employee's details
@admin.route("/edit_employee/<employee_id>", methods=['POST', 'GET'])
@login_required
def edit_employee(employee_id):
    """
    Allows an admin to edit or delete an employee's details.

    - GET: Displays the employee's current details in an editable form.
    - POST: Updates or deletes the employee's details based on the form action.
    """
    result = AdminOnly()  # Check if the user is an admin
    if result == False:
        return redirect(url_for('home.home'))  # Redirect to home if not admin
    
    if request.method == 'POST':
        if request.form['submit_b'] == "Apply":
            # Update employee details
            first_name = request.form["firstname"]
            last_name = request.form["lastname"]
            email = request.form["email"]
            gender = request.form["gender"]
            date_of_birth_str = request.form["date_of_birth"]
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()  # Convert to Python date object
            address = request.form["address"]
            dep = request.form["dep"]
            phone = request.form["phone"]
            salary = request.form["salary"]

            user = User.query.filter_by(employee_id=employee_id).first()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.gender = gender
            user.date_of_birth = date_of_birth
            user.address = address
            user.dep_name = dep
            user.phone = phone
            user.salaire = salary
            db.session.commit()

            flash("Account details have been saved successfully")  # Notify the admin
            return redirect(url_for('admin.edit_employee', employee_id=employee_id))  # Reload the page

        if request.form['submit_b'] == "Delete":
            # Delete employee
            user = User.query.filter_by(employee_id=employee_id).first()
            db.session.delete(user)
            db.session.commit()
            flash("User account successfully deleted")  # Notify the admin
            return redirect(url_for('admin.list_employees'))  # Redirect to employee list page
    
    else:
        # Display employee details in form for editing
        user = User.query.filter_by(employee_id=employee_id).first()
        return render_template('admin/edit.html', 
                               employee_id=user.employee_id, 
                               fullname=f"{user.first_name} {user.last_name}", 
                               firstname=user.first_name, 
                               lastname=user.last_name, 
                               gender=user.gender, 
                               date_of_birth=user.date_of_birth, 
                               email=user.email, 
                               phone=user.phone, 
                               address=user.address, 
                               dep=user.dep_name, 
                               salary=user.salaire)


# Route for listing all departments and their employee count
@admin.route("/list_dep")
@login_required
def list_dep():
    """
    Displays a list of all departments and the number of employees in each department.
    Only accessible by admins.
    """
    result = AdminOnly()  # Check if the user is an admin
    if result == False:
        return redirect(url_for('home.home'))  # Redirect to home if not admin
    
    fullname, role = fullname_role()  # Get the admin's full name and role
    deps = Departements.query.all()
    list_dep = []
    # Collect departments and employee count
    for dep in deps:
        dep_emp_count = len(User.query.filter_by(dep_name=dep.name).all()) 
        list_dep.append({"name": dep.name, "count": dep_emp_count})
    
    return render_template('admin/list_dep.html', list_dep=list_dep, fullname=fullname, role=role)
