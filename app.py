import os
import sys
from app import create_app
from config import Config as config

sys.path.insert(0, os.path.dirname(__file__))


app = create_app()
application = app
app.config['DEBUG'] = os.environ.get('DEBUG', '0') == '1'


if __name__ == "__main__":
    app.run()  # Change to False when deploying
