import mysql.connector
from models import Student
from datetime import datetime

# === CONNECT TO DB ===
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="school_db"
    )

# === OTP ===
def add_otp(email, code, expiration):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO otp (email, code, expiration) VALUES (%s, %s, %s)", (email, code, expiration))
    conn.commit()
    conn.close()

def verify_otp(email, code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT code, expiration FROM otp WHERE email = %s ORDER BY id DESC LIMIT 1", (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        db_code, exp = result
        return db_code == code and datetime.now() <= datetime.strptime(str(exp), '%Y-%m-%d %H:%M:%S')
    return False

# === USERS ===
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# === STUDENTS ===
def add_student(student: Student):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (first_name, surname, last_name, pin, class_name, stream, guardian_email, date_of_birth, photo_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (student.first_name, student.surname, student.last_name, student.pin, student.class_name, student.stream,
          student.guardian_email, student.date_of_birth, student.photo_url))
    conn.commit()
    conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student

# === CLASSES / STREAMS ===
def get_all_classes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM classes")
    result = cursor.fetchall()
    conn.close()
    return [r[0] for r in result]

def add_class(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO classes (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

def delete_class(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classes WHERE name = %s", (name,))
    conn.commit()
    conn.close()

def get_all_streams():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM streams")
    result = cursor.fetchall()
    conn.close()
    return [r[0] for r in result]

def add_stream(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO streams (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

def delete_stream(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM streams WHERE name = %s", (name,))
    conn.commit()
    conn.close()

def count_streams():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM streams")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_streams_by_class(class_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stream FROM class_streams WHERE class_name = %s", (class_name,))
    result = cursor.fetchall()
    conn.close()
    return [r[0] for r in result]

# === SUBJECTS ===
def get_all_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM subjects")
    result = cursor.fetchall()
    conn.close()
    return [r[0] for r in result]

def add_subject(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subjects (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

def delete_subject(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subjects WHERE name = %s", (name,))
    conn.commit()
    conn.close()

# === TIMETABLE ===
def get_timetable_by_class_and_stream(class_name, stream):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT day, period, subject, teacher
        FROM timetable
        WHERE class_name = %s AND stream = %s
        ORDER BY day, period
    """, (class_name, stream))
    results = cursor.fetchall()
    conn.close()
    return results

def get_timetable_by_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT day, period, subject, class_name, stream
        FROM timetable
        WHERE teacher_id = %s
        ORDER BY day, period
    """, (teacher_id,))
    results = cursor.fetchall()
    conn.close()
    return results

# === MARKS / REPORT DATA ===
def get_student_marks(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT subject, score, exam_type, term, year
        FROM marks
        WHERE student_id = %s
    """, (student_id,))
    results = cursor.fetchall()
    conn.close()
    return results

# === PROMOTION ===
def migrate_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET class_name = class_name + 1 WHERE class_name REGEXP '^[0-9]+$'")
    conn.commit()
    conn.close()

# === INITIALIZE DB ===
def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            surname VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(20),
            role VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS otp (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(100),
            code VARCHAR(10),
            expiration DATETIME
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            surname VARCHAR(50),
            last_name VARCHAR(50),
            pin VARCHAR(20),
            class_name VARCHAR(20),
            stream VARCHAR(20),
            guardian_email VARCHAR(100),
            date_of_birth DATE,
            photo_url TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(20) UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streams (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(20) UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS class_streams (
            id INT AUTO_INCREMENT PRIMARY KEY,
            class_name VARCHAR(20),
            stream VARCHAR(20)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INT AUTO_INCREMENT PRIMARY KEY,
            day VARCHAR(20),
            period VARCHAR(20),
            subject VARCHAR(50),
            teacher VARCHAR(100),
            teacher_id INT,
            class_name VARCHAR(20),
            stream VARCHAR(20)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject VARCHAR(50),
            score DECIMAL(5,2),
            exam_type VARCHAR(30),
            term VARCHAR(20),
            year INT
        )
    """)

    conn.commit()
    conn.close()
