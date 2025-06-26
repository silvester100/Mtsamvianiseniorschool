# utils/report_card_generator.py

from fpdf import FPDF

def generate_report_card_pdf(student, subjects, stream_position, overall_position):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Report Card", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Name: {student['name']}", ln=2)
    pdf.cell(200, 10, txt=f"Class: {student['grade']}", ln=3)
    pdf.cell(200, 10, txt=f"Stream Position: {stream_position}", ln=4)
    pdf.cell(200, 10, txt=f"Overall Position: {overall_position}", ln=5)

    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    for sub in subjects:
        pdf.cell(200, 10, txt=f"{sub['subject']}: {sub['score']}", ln=1)

    output_path = "report_card.pdf"
    pdf.output(output_path)
    return output_path
