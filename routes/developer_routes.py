import os
from flask import Blueprint, render_template, request, redirect, session, abort
from datetime import datetime
from shutil import copy2
from db import get_connection

developer_bp = Blueprint('developer', __name__)

DEVELOPER_EMAIL = "silvestergeorge100@gmail.com"
BASE_FOLDERS = ["routes", "templates", "static"]


# === Helpers ===
def is_developer():
    return session.get("email") == DEVELOPER_EMAIL


def log_dev_action(email, action, filename):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO developer_logs (email, action, filename) VALUES (%s, %s, %s)",
        (email, action, filename)
    )
    conn.commit()
    conn.close()


def backup_file(filepath):
    if not os.path.exists("backups"):
        os.makedirs("backups")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(filepath)
    backup_path = f"backups/{timestamp}_{filename}"
    copy2(filepath, backup_path)


# === Developer Dashboard ===
@developer_bp.route('/developer_dashboard')
def developer_dashboard():
    if not is_developer():
        abort(403)
    return render_template("developer_dashboard.html", greeting="Welcome back", first_name="Developer")


# === File Browser ===
@developer_bp.route('/developer/files')
def list_files():
    if not is_developer():
        abort(403)

    file_tree = {}
    for folder in BASE_FOLDERS:
        folder_path = os.path.join(os.getcwd(), folder)
        if os.path.exists(folder_path):
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            file_tree[folder] = files

    return render_template("developer_file.html", file_tree=file_tree)


# === View/Edit File ===
@developer_bp.route('/developer/edit/<folder>/<filename>', methods=['GET', 'POST'])
def edit_file(folder, filename):
    if not is_developer():
        abort(403)

    filepath = os.path.join(os.getcwd(), folder, filename)

    if request.method == 'POST':
        new_content = request.form['content']
        if os.path.exists(filepath):
            backup_file(filepath)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            log_dev_action(session['email'], "Edited file", f"{folder}/{filename}")
        return redirect('/developer/files')

    # GET
    if not os.path.exists(filepath):
        return "File not found", 404

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    return render_template("developer_editor.html", folder=folder, filename=filename, content=content)


# === Developer Logs ===
@developer_bp.route('/developer/logs')
def developer_logs():
    if not is_developer():
        abort(403)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM developer_logs ORDER BY timestamp DESC LIMIT 100")
    logs = cursor.fetchall()
    conn.close()

    return render_template("developer_logs.html", logs=logs)
