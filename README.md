# Employee Management System (EMS)

EMS is a web-based application provides a basic, beautiful, and modern solution for managing various aspects of human resources within an organization. With a user-friendly interface and robust functionalities, EMS simplifies HR-related tasks and enhances efficiency.

`<b>`Please kindly note `</b>` that EMS is currently in its early stages of development. Your valuable feedback and contributions play a crucial role in shaping the future of the app. We sincerely appreciate your willingness to be a part of this journey and thank you in advance for your valuable contributions! :)

## Technologies Used

- Python: A powerful programming language used for the backend development of HRMS.
- Flask Framework: A lightweight and flexible web framework for building web applications in Python.
- Flask SQLAlchemy: An extension for Flask that provides an easy-to-use interface for interacting with SQL databases.
- Bootstrap: A popular CSS framework for creating responsive and appealing frontend designs.
- SQLite3: A lightweight, serverless database engine used for storing HRMS data.

## Project Structure

The repository has the following structure:

```
.
├── CHANGELOG.md
├── configure-python3.10.txt
├── images
├── instance
│   ├── db.sqlite3
│   └── insert.sql
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
├── src
│   ├── admin
│   │   ├── __init__.py
│   │   ├── modules.py
│   │   └── routes.py
│   ├── app.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── modules.py
│   │   └── routes.py
│   ├── config.py
│   ├── home
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models.py
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       ├── datatables-simple-demo.js
│   │       └── scripts.js
│   ├── templates
│   │   ├── admin
│   │   │   ├── edit.html
│   │   │   ├── list_dep.html
│   │   │   ├── list_employees.html
│   │   │   ├── manage_advances.html
│   │   │   └── manage_leave.html
│   │   ├── auth
│   │   │   ├── login.html
│   │   │   ├── password.html
│   │   │   └── register.html
│   │   ├── base.html
│   │   ├── errors
│   │   │   ├── 401.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── home
│   │   │   └── home.html
│   │   └── user
│   │       ├── followup.html
│   │       ├── request_advance.html
│   │       └── request_leave.html
│   └── user
│       ├── __init__.py
│       ├── modules.py
│       └── routes.py
└── TODO.md

16 directories, 42 files

```

## Getting Started

To get started with EMS on your local machine, follow these steps:

1. Navigate to the project directory: `cd hrms`
2. Install the project dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Access HRMS in your browser at `ttp://127.0.0.1:5000/`
