from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_session import Session
from datetime import timedelta
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev_secret')

# === POSTGRESQL DATABASE CONFIG ===
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yourpassword@localhost/school_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# === SESSION CONFIG ===
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config['SESSION_TYPE'] = 'filesystem'

# === EMAIL CONFIG (OTP Support) ===
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS')

# === INIT EXTENSIONS ===
db = SQLAlchemy(app)
mail = Mail(app)
Session(app)

# === IMPORT BLUEPRINTS ===
from auth_routes import auth_bp
from admin_routes import admin_bp
from teacher_routes import teacher_bp
from guardian_routes import guardian_bp
from bursar_routes import bursar_bp
from principal_routes import principal_bp
from deputy_routes import deputy_bp
from developer_routes import developer_bp

# === REGISTER BLUEPRINTS ===
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(teacher_bp, url_prefix='/teacher')
app.register_blueprint(guardian_bp, url_prefix='/guardian')
app.register_blueprint(bursar_bp, url_prefix='/bursar')
app.register_blueprint(principal_bp, url_prefix='/principal')
app.register_blueprint(deputy_bp, url_prefix='/deputy')
app.register_blueprint(developer_bp, url_prefix='/developer')

# === CREATE TABLES ===
with app.app_context():
    db.create_all()

# === RUN SERVER ===
if __name__ == '__main__':
    app.run(debug=True)
