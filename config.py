import os
from dotenv import load_dotenv

# Load environment variables from .env file (if running locally)
load_dotenv()

class Config:
    # Secret Key (Used for sessions, OTP security, etc.)
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

    # PostgreSQL connection URI (for Railway or local)
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: Flask-Mail or other configs (if using email OTP)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # Optional: Logging, Debug, etc.
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
