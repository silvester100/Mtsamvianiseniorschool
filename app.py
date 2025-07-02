from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Init app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Enable CORS if mobile/web access is needed
CORS(app)

# Configure MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init DB and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models to register them with SQLAlchemy
from models import *

# Register Blueprints
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.teacher_routes import teacher_bp
from routes.guardian_routes import guardian_bp
from routes.bursar_routes import bursar_bp
from routes.principal_routes import principal_bp
from routes.deputy_routes import deputy_bp
from routes.developer_routes import developer_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(guardian_bp)
app.register_blueprint(bursar_bp)
app.register_blueprint(principal_bp)
app.register_blueprint(deputy_bp)
app.register_blueprint(developer_bp)

# Main entry point
if __name__ == '__main__':
    app.run()
