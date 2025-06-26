from flask import Blueprint, render_template, session
from db import get_all_students, get_timetable_by_teacher, get_connection

dashboard_bp = Blueprint('dashboard', __name__)

# === Greeting Helper ===
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    return "Good evening"

# === Admin Dashboard ===
@dashboard_bp.route('/admin_dashboard')
def admin_dashboard():
    students = get_all_students()
    return render_template('admin_dashboard.html',
                           greeting=get_greeting(),
                           first_name=session.get('first_name'),
                           students=students)

# === Teacher Dashboard ===
@dashboard_bp.route('/teacher_dashboard')
def teacher_dashboard():
    teacher_email = session.get('email')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (teacher_email,))
    teacher = cursor.fetchone()
    teacher_id = teacher[0] if teacher else None
    timetable = get_timetable_by_teacher(teacher_id)
    return render_template('teacher_dashboard.html',
                           greeting=get_greeting(),
                           first_name=session.get('first_name'),
                           timetable=timetable)

# === Guardian Dashboard ===
@dashboard_bp.route('/guardian_dashboard')
def guardian_dashboard():
    return render_template('guardian_dashboard.html',
                           greeting=get_greeting(),
                           first_name=session.get('first_name'))

# === Bursar Dashboard ===
@dashboard_bp.route('/bursar_dashboard')
def bursar_dashboard():
    return render_template('bursar_dashboard.html',
                           greeting=get_greeting(),
                           first_name=session.get('first_name'))

# === Principal Dashboard ===
@dashboard_bp.route('/principal_dashboard')
def principal_dashboard():
    return render_template('principal_dashboard.html',
                           greeting=get_greeting(),
                           first_name=session.get('first_name'))

# === Deputy Principal Dashboard ===
@dashboard_bp.route('/deputy_dashboard')
def deputy_dashboard():
    return render_template('deputy_dashboard.html',
                           greeting=get_greeting(),
                           first_name=session.get('first_name'))

# === Developer Dashboard ===
@dashboard_bp.route('/developer_dashboard')
def developer_dashboard():
    return render_template('developer_dashboard.html',
                           greeting=get_greeting(),
                           first_name=session.get('first_name'))
