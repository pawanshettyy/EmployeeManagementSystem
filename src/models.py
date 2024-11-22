from .app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User model for authentication and storing user information
class User(UserMixin, db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    dep_name = db.Column(db.Integer, db.ForeignKey('departements.name'))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(15))  # Changed to String to allow special characters
    salaire = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)

    def __init__(self, first_name, last_name, gender, date_of_birth, email, password, dep_name, address, phone, salaire, is_admin):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.email = email
        self.password = generate_password_hash(password)  # Store hashed password
        self.dep_name = dep_name
        self.address = address
        self.phone = phone
        self.salaire = salaire
        self.is_admin = is_admin

    # Override get_id function to return our custom user ID
    def get_id(self):
        return self.employee_id

    # Method to check the password against the hashed password stored
    def verify_password(self, password):
        return check_password_hash(self.password, password)

# Departements model for storing department data
class Departements(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    employee_count = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name

# Leave request model for storing leave requests
class demande_conge(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    type_conge = db.Column(db.String)
    date_deb = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    motif = db.Column(db.String)
    status = db.Column(db.Boolean)  # Status: 0=Declined, 1=Accepted, None=Pending

# Salary advance request model
class avance_salaire(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    montant = db.Column(db.Integer)
    motif = db.Column(db.String)
    status = db.Column(db.Boolean)  # Status: 0=Declined, 1=Accepted, None=Pending
