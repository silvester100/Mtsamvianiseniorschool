from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables (.env for local; use Render Dashboard in production)
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Sample model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# ✅ Create tables at startup using app context (Flask 3+ compatible)
with app.app_context():
    db.create_all()

# Homepage route with HTML
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>School App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding-top: 80px;
                background: #f0f2f5;
            }
            h1 {
                color: #333;
            }
            p {
                font-size: 18px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <h1>🎓 School Management System</h1>
        <p>✅ Flask + PostgreSQL is working on Render!</p>
    </body>
    </html>
    """

# Simple ping route
@app.route('/ping')
def ping():
    return "✅ Pong — app is alive!"

# Local development only
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
