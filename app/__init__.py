from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.blueprints.home import home
    from app.blueprints.blog import blog
    from app.blueprints.about import about
    from app.blueprints.contact import contact

    app.register_blueprint(home)
    app.register_blueprint(blog)
    app.register_blueprint(about)
    app.register_blueprint(contact)

    return app
