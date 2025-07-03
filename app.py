from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)

# Setup database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# === Register all blueprints ===
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.teacher_routes import teacher_bp
from routes.guardian_routes import guardian_bp
from routes.developer_routes import developer_bp
from routes.bursar_routes import bursar_bp
from routes.principal_routes import principal_bp
from routes.deputy_routes import deputy_bp
from routes.archive_routes import archive_bp
from routes.timetable_routes import timetable_bp
from routes.otp_routes import otp_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(guardian_bp)
app.register_blueprint(developer_bp)
app.register_blueprint(bursar_bp)
app.register_blueprint(principal_bp)
app.register_blueprint(deputy_bp)
app.register_blueprint(archive_bp)
app.register_blueprint(timetable_bp)
app.register_blueprint(otp_bp)

# === Main entry point ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
