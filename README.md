# 🎯 EchoDesk - Complaint & Review Management System

A full-stack **Complaint & Review Management System (CRMS)** built with Django and PostgreSQL. EchoDesk provides a centralized platform for users to submit complaints, track progress in real-time, communicate with support staff, and provide feedback—all with role-based access control and comprehensive dashboards.

> 📌 **Portfolio-quality application** demonstrating Django best practices, scalable architecture, and production-ready code.

---

## ✨ Key Features

### 👤 User Features
- **Secure Authentication** – Registration, login with email verification
- **Submit Complaints** – Easy-to-use form with category selection
- **File Attachments** – Upload supporting documents and images
- **Real-time Tracking** – Monitor complaint status at every step
- **Complaint History** – View all past complaints and resolutions
- **Review & Rating** – Rate service quality after resolution
- **Notifications** – Stay updated on complaint progress
- **Smart Search & Filter** – Find complaints by status, category, date

### 👨‍💼 Staff Features
- **Assigned Complaints Dashboard** – View complaints assigned to you
- **Status Management** – Update complaint progress seamlessly
- **Reply System** – Communicate directly with users
- **Internal Notes** – Add notes for team reference
- **Bulk Operations** – Handle multiple complaints efficiently

### 🔐 Admin Features
- **User Management** – Manage user accounts and roles
- **Category Management** – Add/edit complaint categories
- **Staff Assignment** – Assign complaints to team members
- **Admin Dashboard** – Analytics and system overview
- **Reports & Insights** – Track metrics and performance
- **System Settings** – Configure platform behavior

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js |
| **Backend** | Python 3, Django 6 |
| **Database** | PostgreSQL |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```
EchoDesk/
├── complaints/              # Complaint models, views, URLs
├── users/                   # User authentication & profile
├── dashboard/               # Analytics & dashboards
├── config/                  # Django settings & configuration
├── templates/               # HTML templates
├── static/
│   ├── css/                 # Custom styles (39% of codebase)
│   ├── js/                  # JavaScript interactions
│   └── images/              # Assets
├── media/                   # User uploads (attachments)
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🔄 Complaint Workflow

```
Pending → Assigned → In Progress → Waiting for User → Resolved → Closed
                                                    ↓
                                            (Rejected) → Closed
```

Each status reflects real-world complaint handling, with automatic history tracking and user notifications.

---

## 🗄️ Database Schema

- **User** – User profiles with role-based access (user/staff/admin)
- **Category** – Complaint categories and types
- **Complaint** – Main complaint records with metadata
- **ComplaintAttachment** – File uploads linked to complaints
- **ComplaintReply** – Communication between users and staff
- **ComplaintHistory** – Audit trail of all changes
- **Review** – User ratings and feedback post-resolution
- **Notification** – Real-time alerts for users

---

## 🔒 Security Features

✅ Django Authentication & Authorization  
✅ Login-Required Protection on all views  
✅ Role-Based Access Control (RBAC)  
✅ CSRF & XSS Protection  
✅ Form Validation & Sanitization  
✅ Secure File Upload Validation  
✅ Django ORM (No Raw SQL Injection Risk)  
✅ Password Hashing with Django's default algorithm  

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip & virtualenv

### Installation

**1. Clone the Repository**
```bash
git clone https://github.com/Mitesh-Chandel/EchoDesk.git
cd EchoDesk
```

**2. Create & Activate Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables**

Create a `.env` file in the root directory:
```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
DB_NAME=echodesk
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

**5. Apply Database Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Create Superuser (Admin Account)**
```bash
python manage.py createsuperuser
```

**7. Run Development Server**
```bash
python manage.py runserver
```

**8. Access the Application**
- 🌐 User Dashboard: `http://127.0.0.1:8000/`
- 🔑 Admin Panel: `http://127.0.0.1:8000/admin/`

---

## 📊 Project Status

| Feature | Status |
|---------|--------|
| Database Models | ✅ Complete |
| Authentication System | ✅ Complete |
| Complaint CRUD | ✅ Complete |
| User Dashboard | ✅ Complete |
| Staff Dashboard | ✅ Complete |
| Admin Panel | ✅ Complete |
| Search & Filtering | ✅ Complete |
| Notifications | 🚧 In Progress |
| Review System | 🚧 In Progress |
| Reports & Analytics | 🚧 In Progress |
| Deployment | 📋 Planned |

---

## 🎓 What This Project Demonstrates

This portfolio project showcases:

- **Django Architecture** – MVT (Model-View-Template) pattern
- **Database Design** – Normalized PostgreSQL schemas with proper relationships
- **Authentication & Authorization** – Role-based access control implementation
- **CRUD Operations** – Full Create, Read, Update, Delete workflows
- **Django ORM** – Query optimization and model relationships
- **File Handling** – Secure file upload and validation
- **Search & Filtering** – Complex queries with Django ORM
- **Pagination** – Efficient data display for large datasets
- **Dashboard Analytics** – Real-time charts and metrics
- **Clean Code Practices** – Well-organized, maintainable codebase
- **Git Workflow** – Proper branching and commit history
- **Production-Ready Code** – Security, scalability, and best practices

---

## 🔮 Future Enhancements

- 📧 **Email Notifications** – Automated alerts to users and staff
- 🔌 **REST API** – JSON API for mobile app integration
- 🔐 **JWT Authentication** – Token-based auth for API
- ⚡ **Real-time Updates** – WebSocket support for live notifications
- 🐳 **Docker Support** – Containerized deployment
- 🧪 **Unit Testing** – Comprehensive test coverage
- 🔄 **CI/CD Pipeline** – GitHub Actions automation
- ☁️ **Cloud Deployment** – AWS/Heroku ready
- 🤖 **AI Integration** – Smart complaint categorization
- 📱 **Mobile Responsive UI** – Enhanced mobile experience

---

## 📝 Usage Examples

### For Users
1. Sign up with email and password
2. Create a new complaint with category, description, and attachments
3. Track status in your dashboard
4. Receive notifications on updates
5. Rate and review after resolution

### For Admin
1. Log into admin panel
2. View all complaints and assign to staff
3. Monitor system analytics
4. Manage categories and users
5. Generate reports

---

## 📂 Key Files

- `requirements.txt` – All Python dependencies
- `manage.py` – Django management command interface
- `config/settings.py` – Django configuration
- `cssGuide.md` – CSS class documentation
- `QUICK_START.md` – Fast setup guide
- `DOCUMENTATION_INDEX.md` – Full documentation index

---

## 🤝 Contributing

This is a personal portfolio project. For feedback or suggestions:
- Open an issue for bugs
- Create a pull request for improvements
- Contact: [Your Contact Info]

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Mitesh Chandel**  
Computer Engineering Student | Full-Stack Developer  
🔗 [GitHub](https://github.com/Mitesh-Chandel) | [Portfolio](#)

---

## 📞 Support

For issues, questions, or feature requests:
- 🐛 [Open an Issue](https://github.com/Mitesh-Chandel/EchoDesk/issues)
- 💬 Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- 📖 Read [QUICK_START.md](QUICK_START.md)

---

**Last Updated:** October 2026  
**Status:** Active Development 🚀
