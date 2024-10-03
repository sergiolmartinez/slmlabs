import platform
import os
from dotenv import load_dotenv

# Load environment variables from .env file

if platform.system() == 'Windows':
    load_dotenv('.env.dev')
else:
    load_dotenv()


class Config:
    DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_DEFAULT_SENDER = os.getenv('SENDGRID_DEFAULT_SENDER')
    SENDGRID_DEFAULT_RECEIVER = os.getenv('SENDGRID_DEFAULT_RECEIVER')
    RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
    GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
