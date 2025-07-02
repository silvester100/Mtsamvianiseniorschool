from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from app import db
from models import User
from db import add_otp, validate_otp, get_user_by_email, log_activity
import random
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# === Send OTP (simulate via console or real email API) ===
@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    email = request.form.get('email')
    user = get_user_by_email(email)

    if not user:
        flash("No account found with that email.", "danger")
        return redirect(url_for('auth.login'))

    code = str(random.randint(100000, 999999))
    add_otp(email=email, code=code)

    # Simulate sending email (real app should send via SMTP or SendGrid)
    print(f"OTP for {email} is {code}")

    session['email'] = email
    flash("OTP sent to your email.", "success")
    return redirect(url_for('auth.verify_otp'))

# === OTP Verification ===
@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        code = request.form.get('otp')
        email = session.get('email')

        if validate_otp(email, code):
            user = get_user_by_email(email)
            session['user_id'] = user.id
            session['role'] = user.role
            session.permanent = True
            session.modified = True

            log_activity(user.id, f"{user.role} logged in")

            # Redirect based on role
            if user.role == 'admin':
                return redirect('/admin/dashboard')
            elif user.role == 'teacher':
                return redirect('/teacher/dashboard')
            elif user.role == 'guardian':
                return redirect('/guardian/dashboard')
            elif user.role == 'student':
                return redirect('/guardian/student-dashboard')  # Student logs in via guardian
            elif user.role == 'bursar':
                return redirect('/bursar/dashboard')
            elif user.role == 'principal':
                return redirect('/principal/dashboard')
            elif user.role == 'deputy':
                return redirect('/deputy/dashboard')
            elif user.role == 'developer':
                return redirect('/developer/dashboard')
            else:
                flash("Unknown role.", "warning")
                return redirect(url_for('auth.login'))
        else:
            flash("Invalid or expired OTP.", "danger")
            return redirect(url_for('auth.verify_otp'))

    return render_template('auth/verify_otp.html')

# === Login page (email input) ===
@auth_bp.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')

# === Logout ===
@auth_bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        log_activity(user_id, "Logged out")
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))
