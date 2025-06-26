from flask import Blueprint, request, jsonify, send_file
from utils.report_card_generator import generate_report_card_pdf
from db import get_student_by_id, get_student_marks

report_bp = Blueprint('report', __name__)

# === Generate Report PDF ===
@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.json
    student = data["student"]
    subjects = data["subjects"]
    stream_position = data["stream_position"]
    overall_position = data["overall_position"]

    pdf_path = generate_report_card_pdf(student, subjects, stream_position, overall_position)
    return send_file(pdf_path, as_attachment=True)

# === Provide Report Data (JSON API) ===
@report_bp.route('/get_report_data', methods=['POST'])
def get_report_data():
    student_id = request.json.get('student_id')
    student = get_student_by_id(student_id)
    subjects = get_student_marks(student_id)

    # These could be calculated in future
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
