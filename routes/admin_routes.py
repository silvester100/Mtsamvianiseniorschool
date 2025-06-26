# routes/admin_routes.py

from flask import Blueprint, render_template, request, redirect, flash, session, jsonify
from db import *
from utils.report_card_generator import generate_report_card_pdf
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# === Admin Dashboard ===
@admin_bp.route('/dashboard')
def dashboard():
    students = get_all_students()
    return render_template('admin_dashboard.html',
        greeting=get_greeting(),
        first_name=session.get('first_name'),
        students=students
    )

# === Promote Students ===
@admin_bp.route('/promote_students')
def promote_students():
    migrate_students()
    flash("Students promoted successfully", "success")
    return redirect('/admin/dashboard')

# === View/Edit Timetable ===
@admin_bp.route('/edit_timetable', methods=['GET', 'POST'])
def edit_timetable():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        class_name = request.form['class_name']
        stream = request.form['stream']
        day = request.form['day']
        period = request.form['period']
        subject = request.form['subject']
        teacher = request.form['teacher']

        cursor.execute("""
            INSERT INTO timetable (day, period, subject, teacher, class_name, stream)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (day, period, subject, teacher, class_name, stream))
        conn.commit()
        flash('Timetable entry saved.', 'success')

    cursor.execute("SELECT name FROM classes")
    classes = [row['name'] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM streams")
    streams = [row['name'] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM subjects")
    subjects = [row['name'] for row in cursor.fetchall()]

    cursor.execute("SELECT CONCAT(first_name, ' ', last_name) AS name FROM users WHERE role = 'teacher'")
    teachers = [row['name'] for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM timetable ORDER BY day, period")
    timetable = cursor.fetchall()

    conn.close()

    return render_template("edit_timetable.html",
        classes=classes,
        streams=streams,
        subjects=subjects,
        teachers=teachers,
        timetable=timetable
    )

# === AJAX: Get Streams By Class ===
@admin_bp.route('/get_streams')
def get_streams_route():
    class_name = request.args.get('class_name')
    streams = get_streams_by_class(class_name)
    return jsonify(streams)

# === Report Card PDF ===
@admin_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.json
    student = data["student"]
    subjects = data["subjects"]
    stream_position = data["stream_position"]
    overall_position = data["overall_position"]

    pdf_path = generate_report_card_pdf(student, subjects, stream_position, overall_position)
    return send_file(pdf_path, as_attachment=True)

@admin_bp.route('/get_report_data', methods=['POST'])
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

# === Greeting Helper ===
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    return "Good evening"
