import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app creation function
from app import create_app

# Initialize the Flask app
application = create_app()
