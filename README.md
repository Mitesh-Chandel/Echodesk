# EchoDesk - Complaint & Review Management System

EchoDesk is a full-stack **Complaint & Review Management System (CRMS)** built with **Django** and **PostgreSQL**. It provides a centralized platform where users can submit complaints, track their progress, communicate with staff, and provide feedback after resolution.

This project is being developed as a portfolio-quality application following Django best practices and real-world software architecture.

---

## Features

### User
- User Registration & Login
- Secure Authentication
- Dashboard
- Create Complaints
- Upload Attachments
- Track Complaint Status
- View Complaint History
- Notifications
- Review & Rating System

### Staff
- View Assigned Complaints
- Update Complaint Status
- Reply to Complaints
- Internal Notes

### Admin
- Manage Users
- Manage Complaints
- Manage Categories
- Assign Staff
- Dashboard & Analytics
- Reports

---

## Tech Stack

| Technology | Usage |
|------------|------|
| Python 3 | Backend |
| Django 6 | Web Framework |
| PostgreSQL | Database |
| HTML5 | Templates |
| CSS3 | Custom Styling |
| JavaScript | Client-side Interactions |
| Chart.js | Dashboard Analytics |
| Git & GitHub | Version Control |

---

## Project Structure

```
EchoDesk/
│
├── complaints/
├── users/
├── dashboard/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
├── config/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Main Modules

- Authentication System
- Complaint Management
- Category Management
- Complaint Status Tracking
- Complaint History
- File Attachments
- Review & Rating
- Notifications
- Dashboard & Analytics
- Search & Filtering
- Pagination
- Reports

---

## Complaint Workflow

```
Pending
   │
Assigned
   │
In Progress
   │
Waiting for User
   │
Resolved
   │
Closed
```

Rejected complaints can be closed directly.

---

## Database Models

- User
- Category
- Complaint
- ComplaintAttachment
- ComplaintReply
- ComplaintHistory
- Review
- Notification

---

## Security Features

- Django Authentication
- Login Required Protection
- Role-Based Authorization
- CSRF Protection
- Form Validation
- Secure File Upload Validation
- Django ORM (No Raw SQL)

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/EchoDesk.git

cd EchoDesk
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and add your PostgreSQL credentials.

Example:

```
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=echodesk

DB_USER=postgres

DB_PASSWORD=yourpassword

DB_HOST=localhost

DB_PORT=5432
```

### Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

Admin Panel:

```
http://127.0.0.1:8000/admin/
```

---

## Project Status

Current Development Progress

- ✅ Database Models
- ✅ Authentication
- ✅ Complaint CRUD
- ✅ Dashboard
- ✅ Search & Filtering
- 🚧 Notifications
- 🚧 Review System
- 🚧 Reports & Analytics
- 🚧 Deployment

---

## Learning Objectives

This project demonstrates:

- Django Project Architecture
- PostgreSQL Integration
- Authentication & Authorization
- CRUD Operations
- Django ORM
- File Upload Handling
- Search & Filtering
- Pagination
- Dashboard Analytics
- Clean Code Practices
- MVC (MVT) Architecture
- Git Workflow

---

## Future Improvements

- Email Notifications
- REST API
- JWT Authentication
- Real-time Notifications
- Docker Support
- Unit Testing
- CI/CD Pipeline
- Cloud Deployment
- AI-Based Complaint Categorization
- Mobile Responsive UI

---

## Screenshots

Add project screenshots here.

```
/screenshots

login.png

dashboard.png

complaints.png

admin.png
```

---

## Author

**Mitesh Chandel**

Computer Engineering Student

---

```
Echodesk
├─ complaints
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─ __init__.py
├─ COMPLETION_SUMMARY.md
├─ config
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ __init__.py
├─ cssGuide.md
├─ dashboard
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─ __init__.py
├─ data.json
├─ DEPLOYMENT_READY.md
├─ DOCUMENTATION_INDEX.md
├─ FILE_MANIFEST.md
├─ manage.py
├─ PHASES_2_5_COMPLETE.md
├─ PHASE_1_COMPLETE.md
├─ QUICK_START.md
├─ README.md
├─ requirements.txt
├─ setup_data.py
├─ static
│  ├─ admin
│  │  └─ css
│  │     └─ admin.css
│  ├─ css
│  │  ├─ auth.css
│  │  ├─ complaints.css
│  │  ├─ components.css
│  │  ├─ dashboard.css
│  │  ├─ forms.css
│  │  ├─ layout.css
│  │  ├─ main.css
│  │  ├─ responsive.css
│  │  └─ utilities.css
│  ├─ images
│  └─ js
│     └─ layout.js
├─ structure.md
├─ templates
│  ├─ admin
│  │  └─ base_site.html
│  ├─ auth
│  │  ├─ base_auth.html
│  │  ├─ change_password.html
│  │  ├─ edit_profile.html
│  │  ├─ login.html
│  │  ├─ profile.html
│  │  └─ register.html
│  ├─ base.html
│  ├─ complaints
│  │  ├─ add_reply.html
│  │  ├─ complaint_confirm_delete.html
│  │  ├─ complaint_detail.html
│  │  ├─ complaint_form.html
│  │  ├─ complaint_list.html
│  │  └─ upload_attachment.html
│  ├─ dashboard
│  │  ├─ admin_dashboard.html
│  │  ├─ staff_dashboard.html
│  │  ├─ student_dashboard.html
│  │  └─ user_dashboard.html
│  └─ partials
│     ├─ footer.html
│     ├─ messages.html
│     ├─ sidebar.html
│     └─ topbar.html
└─ users
   ├─ admin.py
   ├─ apps.py
   ├─ forms.py
   ├─ migrations
   │  ├─ 0001_initial.py
   │  └─ __init__.py
   ├─ models.py
   ├─ signals.py
   ├─ tests.py
   ├─ urls.py
   ├─ views.py
   └─ __init__.py

```