import os
import sys
from app import create_app

sys.path.insert(0, os.path.dirname(__file__))


app = create_app()
application = app

if __name__ == "__main__":
    app.run(debug=False)  # Change to False when deploying
