# 🏫 School Management System

A comprehensive, modern, and mobile-friendly **School Management System** built using **Flask** and **MySQL** (or SQLite), with full support for OTP login, dashboards for all roles, automated student promotion, report cards, timetable management, archives, and much more.

---

## 📦 Features

### 🎓 User Roles
- **Student** – View marks, download files, access report cards, chat
- **Guardian** – View student results, performance, fees, login via PIN
- **Teacher** – Enter/edit marks, access private/public archives, messaging
- **Admin** – Manage subjects, teachers, classes, streams, and timetable
- **Bursar** – Manage and view student fees and payment status
- **Principal & Deputy Principal** – View school-wide performance reports
- **Developer** – Remote code editing, debug access, full system control

---

### ⚙️ Core Modules

| Module           | Description |
|------------------|-------------|
| ✅ **OTP Login**       | Secure email-based one-time password login |
| ✅ **Student Promotion** | Automatic year-end promotion and graduation |
| ✅ **Subjects/Streams** | Setup with class and stream split (min 4 streams) |
| ✅ **Timetable**       | Block + personal view, printable, teacher-limited to 2 subjects |
| ✅ **Report Cards**    | PDF/CSV export, charts and school branding |
| ✅ **Archive System**  | Teacher: public/private; Student: public-only |
| ✅ **Messaging**       | Internal chat by role |
| ✅ **Activity Logging**| Tracks user operations for audit trail |

---

## 🛠️ Technologies

- **Backend**: Flask (Python)
- **Database**: MySQL or SQLite
- **Frontend**: HTML5, CSS3, Bootstrap, Font Awesome
- **PDF Reports**: fpdf2
- **Charts**: matplotlib (student performance)
- **OTP**: Email-based secure codes

---

## 🚀 Installation Guide

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/school-management-system.git
   cd school-management-system

school-management-system/
│
├── app.py
├── db.py
├── models.py
├── config.py
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── register_user.html
│   ├── admin_dashboard.html
│   ├── setup_subject.html
│   └── (all other dashboards)
│
├── static/
│   └── css/, js/, images/
│
├── routes/
│   ├── auth_routes.py
│   ├
