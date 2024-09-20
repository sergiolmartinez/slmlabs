from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config
import logging
from logging.handlers import RotatingFileHandler

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
    from app.blueprints.sitemap import sitemap  # Add sitemap blueprint

    app.register_blueprint(home)
    app.register_blueprint(blog)
    app.register_blueprint(about)
    app.register_blueprint(contact)
    app.register_blueprint(sitemap)  # Register sitemap blueprint

    # Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Logging configuration for production
    if not app.debug:
        file_handler = RotatingFileHandler(
            'logs/slmlabs.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('SLM Labs startup')

    return app
