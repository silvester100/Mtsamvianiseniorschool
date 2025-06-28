from flask import Blueprint, render_template, request, session, redirect, url_for, flash, send_from_directory
import os

developer_bp = Blueprint('developer', __name__)

# === Ensure only developer can access ===
def is_developer():
    return session.get('role') == 'developer'

# === Developer Dashboard ===
@developer_bp.route('/developer_dashboard')
def developer_dashboard():
    if not is_developer():
        return redirect('/')
    return render_template('developer_dashboard.html', greeting="Welcome back", first_name=session.get('first_name'))

# === File Browser ===
@developer_bp.route('/developer/files')
def list_files():
    if not is_developer():
        return redirect('/')
    base_dir = os.getcwd()
    files = []
    for filename in os.listdir(base_dir):
        if filename.endswith('.py') or filename.endswith('.html'):
            files.append(filename)
    return render_template('developer_files.html', files=files)

# === Edit File ===
@developer_bp.route('/developer/edit/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    if not is_developer():
        return redirect('/')
    filepath = os.path.join(os.getcwd(), filename)
    if request.method == 'POST':
        content = request.form['content']
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        flash(f'{filename} updated successfully.', 'success')
        return redirect(url_for('developer.list_files'))
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('developer_edit_file.html', filename=filename, content=content)
