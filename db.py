import mysql.connector
from models import Student
from datetime import datetime

# === CONSTANTS ===
DEVELOPER_EMAIL = "silvestergeorge100@gmail.com"

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
    if email.strip().lower() != DEVELOPER_EMAIL:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT code, expiration FROM otp WHERE email = %s ORDER BY id DESC LIMIT 1", (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        db_code, exp = result
        try:
            valid = db_code == code and datetime.now() <= datetime.strptime(str(exp), '%Y-%m-%d %H:%M:%S')
            if valid:
                ensure_developer_account_exists()
            return valid
        except ValueError:
            return False
    return False

# === Ensure Developer Account ===
def ensure_developer_account_exists():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (DEVELOPER_EMAIL,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("""
            INSERT INTO users (first_name, surname, last_name, email, phone, role)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ("Silvester", "George", "Developer", DEVELOPER_EMAIL, "0700000000", "developer"))
        conn.commit()
    conn.close()

# === USERS ===
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_teachers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, first_name, surname, last_name FROM users WHERE role = 'teacher'")
    result = cursor.fetchall()
    conn.close()
    return result

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
    cursor.execute("SELECT DISTINCT class_name FROM students ORDER BY class_name")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result

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
    cursor.execute("SELECT DISTINCT stream FROM students ORDER BY stream")
    result = [r[0] for r in cursor.fetchall()]
    conn.close()
    return result

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
def insert_subject(subject_name, class_name, stream, teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO subjects (name, class_name, stream, teacher_id)
        VALUES (%s, %s, %s, %s)
    """, (subject_name, class_name, stream, teacher_id))
    conn.commit()
    conn.close()

def get_all_subjects():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT subjects.id, subjects.name, subjects.class_name, subjects.stream,
               users.first_name, users.surname, users.last_name
        FROM subjects
        JOIN users ON subjects.teacher_id = users.id
        ORDER BY class_name, stream, subjects.name
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def delete_subject_by_id(subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
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
    CREATE TABLE IF NOT EXISTS developer_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(100),
        action TEXT,
        filename VARCHAR(255),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

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
            name VARCHAR(50),
            class_name VARCHAR(20),
            stream VARCHAR(20),
            teacher_id INT,
            FOREIGN KEY (teacher_id) REFERENCES users(id)
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
