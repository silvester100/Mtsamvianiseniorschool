from flask import Blueprint, render_template, request, session
from db import get_connection, get_timetable_by_class_and_stream, get_timetable_by_teacher

timetable_bp = Blueprint('timetable', __name__)

# === View Block Timetable (by Class + Stream) ===
@timetable_bp.route('/view_block_timetable', methods=['GET', 'POST'])
def view_block_timetable():
    if request.method == 'POST':
        class_name = request.form['class_name']
        stream = request.form['stream']
        timetable = get_timetable_by_class_and_stream(class_name, stream)
        return render_template('block_timetable.html',
                               timetable=timetable,
                               class_name=class_name,
                               stream=stream)
    
    # GET request fallback
    return render_template('block_timetable.html',
                           timetable=[],
                           class_name=None,
                           stream=None)

# === Personal Timetable (for Teachers) ===
@timetable_bp.route('/personal_timetable')
def personal_timetable():
    teacher_email = session.get('email')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (teacher_email,))
    teacher = cursor.fetchone()
    teacher_id = teacher[0] if teacher else None

    timetable = get_timetable_by_teacher(teacher_id)
    return render_template('personal_timetable.html',
                           timetable=timetable)
