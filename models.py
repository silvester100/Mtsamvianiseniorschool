from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# === USERS ===
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pin = db.Column(db.String(6), nullable=False)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)
    subjects = db.Column(db.String(50))  # Max 2 subjects, comma-separated
    pin = db.Column(db.String(6), nullable=False)

class Guardian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    otp_code = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)

class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    access_token = db.Column(db.String(256))  # For remote code edit

# === STUDENTS & ACADEMICS ===
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    class_name = db.Column(db.String(20))
    pin = db.Column(db.String(6), nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey('guardian.id'))

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    year = db.Column(db.Integer)
    term = db.Column(db.String(10))
    exam_type = db.Column(db.String(20))  # CAT, Midterm, Final
    score = db.Column(db.Float)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

class ArchivedStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    archived_on = db.Column(db.DateTime, default=datetime.utcnow)

# === ARCHIVE SYSTEM ===
class ArchiveFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    path = db.Column(db.String(200))
    file_type = db.Column(db.String(20))  # pdf, video, docx
    is_public = db.Column(db.Boolean, default=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# === TIMETABLE ===
class TimetableEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    class_name = db.Column(db.String(20))
    stream = db.Column(db.String(20))
    day = db.Column(db.String(20))
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)

# === OTP LOGS ===
class OTPLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    otp = db.Column(db.String(6))
    expires_at = db.Column(db.DateTime)

# === MESSAGING ===
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100))
    recipient = db.Column(db.String(100))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# === ACTIVITY LOG ===
class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120))
    action = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
