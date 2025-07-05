from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load .env (works locally; Render uses dashboard for secrets)
load_dotenv()

app = Flask(__name__)

# Use DATABASE_URL from environment
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Sample model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return "✅ App is live! Flask + PostgreSQL on Render."

# Run app using Render's port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
