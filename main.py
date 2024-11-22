""" Tying it all together with 'main.py' """

from src.app import app  # Import the Flask app from the app module

if __name__ == '__main__':
    # Run the Flask app with debugging enabled
    app.run(debug=True)
