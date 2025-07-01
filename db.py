from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, guardian, student, teacher, bursar, developer
    email = db.Column(db.String(100), unique=True, nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade_level = db.Column(db.Integer, nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    archived = db.Column(db.Boolean, default=False)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    subject = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    term = db.Column(db.String(20), nullable=False)

def init_db():
    db.create_all()
