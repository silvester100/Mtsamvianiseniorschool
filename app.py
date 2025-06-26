from flask import Flask, render_template, request, redirect, session, jsonify, send_file, flash
from db import initialize_db, add_otp, verify_otp, get_connection, get_all_students, get_timetable_by_teacher, get_streams_by_class, get_student_by_id, get_student_marks, migrate_students
from utils.report_card_generator import generate_report_card_pdf
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
# from routes.teacher_routes import teacher_bp # (optional)

from datetime import datetime, timedelta
import random, string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# === BLUEPRINTS ===
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
# app.register_blueprint(teacher_bp)

# === OTP Routes (in case you want fallback login inline) ===
@app.route('/')
def home():
    return render_template('request_otp.html')

def generate_otp_code():
    return ''.join(random.choices(string.digits, k=6))

@app.route('/request_otp', methods=['POST'])
def request_otp():
    email = request.form['email']
    otp_code = generate_otp_code()
    expiration = (datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
    add_otp(email, otp_code, expiration)
    return jsonify({"status": "sent", "otp": otp_code})

@app.route('/verify_otp', methods=['POST'])
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# === DASHBOARD ROUTES ===
@app.route('/admin_dashboard')
def admin_dashboard():
    students = get_all_students()
    return render_template('admin_dashboard.html', greeting=get_greeting(), first_name=session.get('first_name'), students=students)

@app.route('/teacher_dashboard')
def teacher_dashboard():
    teacher_email = session.get('email')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (teacher_email,))
    teacher = cursor.fetchone()
    teacher_id = teacher[0] if teacher else None
    timetable = get_timetable_by_teacher(teacher_id)
    return render_template('teacher_dashboard.html', greeting=get_greeting(), first_name=session.get('first_name'), timetable=timetable)

@app.route('/guardian_dashboard')
def guardian_dashboard():
    return render_template('guardian_dashboard.html', greeting=get_greeting(), first_name=session.get('first_name'))

@app.route('/bursar_dashboard')
def bursar_dashboard():
    return render_template('bursar_dashboard.html', greeting=get_greeting(), first_name=session.get('first_name'))

@app.route('/principal_dashboard')
def principal_dashboard():
    return render_template('principal_dashboard.html', greeting=get_greeting(), first_name=session.get('first_name'))

@app.route('/deputy_dashboard')
def deputy_dashboard():
    return render_template('deputy_dashboard.html', greeting=get_greeting(), first_name=session.get('first_name'))

@app.route('/developer_dashboard')
def developer_dashboard():
    return render_template('developer_dashboard.html', greeting=get_greeting(), first_name=session.get('first_name'))

# === STUDENT PROMOTION ===
@app.route('/promote_students')
def promote_students():
    migrate_students()
    flash("Students promoted successfully", "success")
    return redirect('/admin_dashboard')

# === STREAM OPTIONS AJAX ===
@app.route('/get_streams')
def get_streams():
    class_name = request.args.get('class_name')
    streams = get_streams_by_class(class_name)
    return jsonify(streams)

# === BLOCK TIMETABLE ===
@app.route('/view_block_timetable', methods=['GET', 'POST'])
def view_block_timetable():
    if request.method == 'POST':
        class_name = request.form['class_name']
        stream = request.form['stream']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM timetable WHERE class_name = %s AND stream = %s", (class_name, stream))
        timetable = cursor.fetchall()
        return render_template('block_timetable.html', timetable=timetable, class_name=class_name, stream=stream)
    return render_template('block_timetable.html', timetable=[], class_name=None, stream=None)

# === PERSONAL TIMETABLE ===
@app.route('/personal_timetable')
def personal_timetable():
    teacher_email = session.get('email')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (teacher_email,))
    teacher = cursor.fetchone()
    teacher_id = teacher[0] if teacher else None
    timetable = get_timetable_by_teacher(teacher_id)
    return render_template('personal_timetable.html', timetable=timetable)

# === REPORT CARD GENERATION ===
@app.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.json
    student = data["student"]
    subjects = data["subjects"]
    stream_position = data["stream_position"]
    overall_position = data["overall_position"]

    pdf_path = generate_report_card_pdf(student, subjects, stream_position, overall_position)
    return send_file(pdf_path, as_attachment=True)

@app.route('/get_report_data', methods=['POST'])
def get_report_data():
    student_id = request.json.get('student_id')
    student = get_student_by_id(student_id)
    subjects = get_student_marks(student_id)
    stream_position = "15/45"
    overall_position = "33/120"
    return jsonify({
        "student": {
            "name": f"{student['first_name']} {student['surname']} {student['last_name']}",
            "grade": f"{student['class_name']} {student['stream']}"
        },
        "stream_position": stream_position,
        "overall_position": overall_position,
        "subjects": subjects
    })

# === HELPER ===
def get_greeting():
    now = datetime.now().hour
    if now < 12:
        return "Good morning"
    elif now < 17:
        return "Good afternoon"
    return "Good evening"

# === BOOTSTRAP APP ===
if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
