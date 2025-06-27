from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from db import (
    get_all_classes, get_all_streams, get_all_teachers,
    add_subject, get_all_subjects, delete_subject_by_id,
    get_subject_by_id, update_subject
)

admin_routes = Blueprint('admin_routes', __name__)

# === Setup Subjects Page ===
@admin_routes.route('/admin/setup-subjects', methods=['GET', 'POST'])
@login_required
def setup_subjects():
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        class_name = request.form['class']
        stream = request.form['stream']
        teacher_id = request.form['teacher_id']

        if subject_name and class_name and stream and teacher_id:
            add_subject(subject_name, class_name, stream, teacher_id)
            flash("✅ Subject added successfully!", "success")
        else:
            flash("⚠️ Please fill all fields.", "danger")

        return redirect(url_for('admin_routes.setup_subjects'))

    classes = get_all_classes()
    streams = get_all_streams()
    teachers = get_all_teachers()
    subjects = get_all_subjects()

    return render_template('setup_subject.html',
                           classes=classes,
                           streams=streams,
                           teachers=teachers,
                           subjects=subjects)

# === Delete Subject ===
@admin_routes.route('/admin/delete-subject/<int:subject_id>')
@login_required
def delete_subject(subject_id):
    delete_subject_by_id(subject_id)
    flash("🗑️ Subject deleted.", "info")
    return redirect(url_for('admin_routes.setup_subjects'))

# === Edit Subject ===
@admin_routes.route('/admin/edit-subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        class_name = request.form['class']
        stream = request.form['stream']
        teacher_id = request.form['teacher_id']

        update_subject(subject_id, subject_name, class_name, stream, teacher_id)
        flash("✏️ Subject updated.", "success")
        return redirect(url_for('admin_routes.setup_subjects'))

    subject = get_subject_by_id(subject_id)
    classes = get_all_classes()
    streams = get_all_streams()
    teachers = get_all_teachers()

    return render_template('edit_subject.html',
                           subject=subject,
                           classes=classes,
                           streams=streams,
                           teachers=teachers)
