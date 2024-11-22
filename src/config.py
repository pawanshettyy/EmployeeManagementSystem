"""Flask configuration."""

import os

# Secret key for securely signing session cookies and other cryptographic operations
SECRET_KEY = os.urandom(24)

# URI for the database connection (SQLite in this case)
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
