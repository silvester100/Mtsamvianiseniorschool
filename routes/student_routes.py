from flask import Blueprint, render_template, request, redirect, jsonify
from db import add_student, get_streams_by_class
from models import Student

student_bp = Blueprint('student', __name__)

# === Register a New Student ===
@student_bp.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        student = Student(
            id=0,
            first_name=request.form['first_name'],
            surname=request.form['surname'],
            last_name=request.form['last_name'],
            pin=request.form['pin'],
            class_name=request.form['class_name'],
            stream=request.form['stream'],
            guardian_email=request.form['guardian_email'],
            date_of_birth=request.form['date_of_birth'],
            photo_url=request.form['photo_url']
        )
        add_student(student)
        return redirect('/admin_dashboard')
    
    return render_template('register_student.html')

# === Get Streams Dynamically by Class (AJAX) ===
@student_bp.route('/get_streams')
def get_streams():
    class_name = request.args.get('class_name')
    streams = get_streams_by_class(class_name)
    return jsonify(streams)
