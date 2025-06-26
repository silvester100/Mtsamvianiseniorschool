# routes/auth_routes.py

from flask import Blueprint, render_template, request, redirect, session, jsonify
from db import add_otp, verify_otp, get_connection
from datetime import datetime, timedelta
import random, string

auth_bp = Blueprint('auth', __name__)

# === Home/Login ===
@auth_bp.route('/')
def home():
    return render_template('request_otp.html')

# === Generate OTP Code ===
def generate_otp_code():
    return ''.join(random.choices(string.digits, k=6))

@auth_bp.route('/request_otp', methods=['POST'])
def request_otp():
    email = request.form['email']
    otp_code = generate_otp_code()
    expiration = (datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
    add_otp(email, otp_code, expiration)
    return jsonify({"status": "sent", "otp": otp_code})

@auth_bp.route('/verify_otp', methods=['POST'])
def verify_otp_route():
    email = request.form['email']
    code = request.form['code']
    if verify_otp(email, code):
        session['email'] = email
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT role, first_name FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        if not user:
            return "User not found", 404
        session['role'] = user['role']
        session['first_name'] = user['first_name']
        return redirect(f"/{user['role']}_dashboard")
    return "OTP Invalid or Expired"

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
