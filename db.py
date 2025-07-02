from datetime import datetime, timedelta
from app import db
from models import User, OTP, ActivityLog, Message, Mark, Subject

# ========================
# USER & REGISTRATION HELPERS
# ========================

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_pin(pin):
    return User.query.filter_by(pin=pin).first()

def create_user(first_name, surname, last_name, email, phone, pin, role):
    new_user = User(
        first_name=first_name,
        surname=surname,
        last_name=last_name,
        email=email,
        phone=phone,
        pin=pin,
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

# ========================
# OTP HELPERS
# ========================

def add_otp(email, code, valid_minutes=5):
    expiry = datetime.utcnow() + timedelta(minutes=valid_minutes)
    otp = OTP(email=email, code=code, expiration=expiry)
    db.session.add(otp)
    db.session.commit()

def validate_otp(email, code):
    otp = OTP.query.filter_by(email=email, code=code).first()
    if otp and otp.expiration > datetime.utcnow():
        return True
    return False

def delete_expired_otps():
    now = datetime.utcnow()
    OTP.query.filter(OTP.expiration < now).delete()
    db.session.commit()

# ========================
# ACTIVITY LOG
# ========================

def log_activity(user_id, activity_description):
    log = ActivityLog(user_id=user_id, activity=activity_description)
    db.session.add(log)
    db.session.commit()

# ========================
# MESSAGING HELPERS
# ========================

def send_message(sender_id, receiver_id, content):
    msg = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(msg)
    db.session.commit()

def get_inbox(user_id):
    return Message.query.filter_by(receiver_id=user_id).order_by(Message.timestamp.desc()).all()

def get_sent_messages(user_id):
    return Message.query.filter_by(sender_id=user_id).order_by(Message.timestamp.desc()).all()

# ========================
# MARKS HELPERS
# ========================

def enter_mark(student_id, subject_id, term, exam_type, year, score):
    existing = Mark.query.filter_by(
        student_id=student_id,
        subject_id=subject_id,
        term=term,
        exam_type=exam_type,
        year=year
    ).first()
    if existing:
        return False  # Prevent duplicate
    mark = Mark(
        student_id=student_id,
        subject_id=subject_id,
        term=term,
        exam_type=exam_type,
        year=year,
        score=score
    )
    db.session.add(mark)
    db.session.commit()
    return True

def update_mark(mark_id, new_score):
    mark = Mark.query.get(mark_id)
    if mark:
        mark.score = new_score
        db.session.commit()
        return True
    return False

def delete_mark(mark_id):
    mark = Mark.query.get(mark_id)
    if mark:
        db.session.delete(mark)
        db.session.commit()
        return True
    return False

# ========================
# SUBJECT HELPERS
# ========================

def assign_teacher_to_subject(subject_code, teacher_id):
    subject = Subject.query.filter_by(code=subject_code).first()
    if subject:
        subject.teacher_id = teacher_id
        db.session.commit()
        return True
    return False
