# EchoDesk – AI Development Master Prompt
**A Production-Quality Django Complaint & Review Management System**

---

## 📋 Project Overview

**EchoDesk** is a portfolio-quality backend project demonstrating professional Django development practices. It's a Complaint & Review Management System similar to government complaint portals, university complaint systems, or customer support ticket systems.

**Target Audience:** Internships and junior backend/full-stack roles

---

## 🎯 User Goals

### Regular Users
- ✅ Register & Login
- ✅ Submit complaints with attachments
- ✅ Track complaint status in real-time
- ✅ View complete complaint history
- ✅ Receive notifications on updates
- ✅ Review and rate resolved complaints

### Staff Members
- ✅ View assigned complaints
- ✅ Reply to complaints
- ✅ Update complaint status
- ✅ Add internal notes

### Admins
- ✅ Manage all users
- ✅ Manage all complaints
- ✅ Manage staff assignments
- ✅ Access system dashboards
- ✅ Generate reports

---

## 💾 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.x + Django 6.0 |
| **Database** | PostgreSQL |
| **Frontend** | Django Templates + HTML |
| **Frontend Status** | Pure HTML (no CSS, Bootstrap, Tailwind yet) |
| **JS** | None (no AJAX, Charts.js, DataTables) |

**Focus:** Backend architecture and Django fundamentals

---

## 📁 Project Structure

```
Echodesk/
├── config/                  # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Database, apps, middleware
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
│
├── users/                   # User management app
│   ├── migrations/
│   ├── models.py            # User-related models
│   ├── views.py             # Auth views (register, login, logout)
│   ├── urls.py              # User URLs
│   ├── forms.py             # User forms
│   ├── admin.py             # Admin configuration
│   ├── apps.py
│   ├── tests.py
│   └── __init__.py
│
├── complaints/              # Complaint management app
│   ├── migrations/
│   ├── models.py            # Complaint models
│   ├── views.py             # Complaint CRUD views
│   ├── urls.py              # Complaint URLs
│   ├── forms.py             # Complaint forms
│   ├── admin.py             # Admin configuration
│   ├── apps.py
│   ├── tests.py
│   └── __init__.py
│
├── dashboard/               # Dashboard app
│   ├── migrations/
│   ├── models.py            # Dashboard models (if needed)
│   ├── views.py             # Dashboard views
│   ├── urls.py              # Dashboard URLs
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   └── __init__.py
│
├── templates/               # Django templates
│   ├── base.html            # Base template
│   ├── auth/
│   │   ├── register.html
│   │   ├── login.html
│   │   └── profile.html
│   ├── complaints/
│   │   ├── complaint_list.html
│   │   ├── complaint_detail.html
│   │   ├── complaint_create.html
│   │   └── complaint_update.html
│   └── dashboard/
│       ├── user_dashboard.html
│       └── admin_dashboard.html
│
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                   # User uploads
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .gitignore               # Git ignore file
└── README.md               # This file

```

---

## 🗄️ Database Models (Phase 1)

### User Roles
- **User:** Regular user who submits complaints
- **Staff:** Staff member who processes complaints
- **Admin:** System administrator

### Core Models

#### 1. **Category**
Categories of complaints (Electricity, Water, Road, etc.)

#### 2. **Complaint**
Main complaint submission by users

**Fields:**
- `complaint_id` - Readable ID (CMP-20260001)
- `user` - FK to User
- `category` - FK to Category
- `title` - Complaint title
- `description` - Detailed description
- `priority` - Low, Medium, High, Urgent
- `status` - Pending, Assigned, In Progress, Waiting for User, Resolved, Closed, Rejected
- `assigned_staff` - FK to Staff User (nullable)
- `created_at` - Timestamp
- `updated_at` - Timestamp

#### 3. **ComplaintAttachment**
File uploads for complaints

#### 4. **ComplaintReply**
Responses from staff or user

#### 5. **ComplaintHistory**
Track status changes and events

#### 6. **Review**
User ratings after complaint resolution

#### 7. **Notification**
System notifications

---

## 📊 Complaint Status Workflow

```
Pending → Assigned → In Progress → Waiting for User → Resolved → Closed
   ↓                                                      ↓
   └──────────────────────→ Rejected ──────────────→ Closed
```

---

## 🔐 Security Features

- ✅ Django Authentication System (built-in)
- ✅ `@login_required` decorator
- ✅ Permission-based access control
- ✅ CSRF protection (default)
- ✅ Django Forms validation
- ✅ ORM only (no raw SQL)
- ✅ File type validation
- ✅ Never trust user input

---

## 🚀 Development Phases

### Phase 1: Database Models ✨ **CURRENT**
- Create all database models
- Set up relationships
- Generate migrations
- Explain ORM concepts

### Phase 2: Django Admin Configuration
- Register models in admin
- Configure list_display, list_filter, search_fields
- Test models via admin interface

### Phase 3: Authentication System
- User registration
- Login/logout
- User profiles
- Profile editing
- Password change

### Phase 4: Complaint CRUD Operations
- Create complaint
- View complaint detail
- Update complaint
- Delete complaint
- Complaint listing

### Phase 5: Replies, Attachments & History
- Complaint replies
- File attachments with validation
- Complaint history tracking
- Timeline view

### Phase 6: Dashboards
- User dashboard
- Admin dashboard
- Staff dashboard
- Display statistics

### Phase 7: Search & Filtering
- Search complaints
- Filter by status, priority, category, date
- Pagination

### Phase 8: Notifications
- Database notifications
- Notification triggers
- Notification display

### Phase 9: Review System
- Rate resolved complaints
- Textual feedback
- Review listings

### Phase 10: Code Cleanup & Optimization
- Code review
- Performance optimization
- Deployment preparation

---

## 🛠️ Development Rules

### Code Quality
- ✅ Always follow Django best practices
- ✅ Use meaningful variable names
- ✅ Keep code clean and organized
- ✅ Avoid duplicated logic
- ✅ Use Django ORM only

### File Organization
- ✅ Always separate: Models, Views, URLs, Forms, Templates, Admin
- ✅ Use Function-Based Views (FBV) initially
- ✅ Use Class-Based Views (CBV) only after project completion

### Explanation
- ✅ Explain why each file is created
- ✅ Explain how Django uses each component
- ✅ Explain database relationships
- ✅ Include common interview questions
- ✅ Highlight common beginner mistakes

### Development Workflow
- ✅ Never jump ahead to future phases
- ✅ Build feature by feature
- ✅ Generate complete, working code
- ✅ Never generate placeholder code
- ✅ Stop at end of each phase for confirmation

---

## 📚 Key Django Concepts

### Models
- Django ORM automatically creates tables
- ForeignKey creates relationships
- `related_name` allows reverse queries
- `created_at`, `updated_at` for tracking

### Migrations
- Track database schema changes
- `python manage.py makemigrations`
- `python manage.py migrate`

### Admin Interface
- Built-in CRUD interface
- Configure with `list_display`, `list_filter`
- Great for testing models

### Authentication
- Django's built-in User model
- `@login_required` decorator
- Permission system

### Templates
- Reusable HTML with variables
- Template inheritance with `{% extends %}`
- Context variables from views

---

## 🎓 Learning Outcomes

After completing EchoDesk, you'll understand:

- ✅ Complete Django project structure
- ✅ Database modeling and relationships
- ✅ Django ORM and migrations
- ✅ Authentication and permissions
- ✅ Form handling and validation
- ✅ Template rendering and inheritance
- ✅ Admin interface customization
- ✅ URL routing and views
- ✅ File uploads and media handling
- ✅ Search and filtering
- ✅ Notifications system
- ✅ Django best practices

---

## 🚦 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- Virtual Environment

### Setup
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with DATABASE_URL

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Access
- Admin Panel: http://localhost:8000/admin
- (More URLs will be added as we build)

---

## 📖 Phase Progress Checklist

- [ ] Phase 1: Database Models
- [ ] Phase 2: Admin Configuration
- [ ] Phase 3: Authentication
- [ ] Phase 4: Complaint CRUD
- [ ] Phase 5: Replies, Attachments, History
- [ ] Phase 6: Dashboards
- [ ] Phase 7: Search & Filtering
- [ ] Phase 8: Notifications
- [ ] Phase 9: Reviews
- [ ] Phase 10: Cleanup & Optimization

---

## 💡 Important Notes

1. **Never jump ahead:** Build exactly in the order specified
2. **Always explain:** Every file, every relationship, every concept
3. **Complete code only:** No placeholders, no TODOs
4. **Interview ready:** Include learning insights at each phase
5. **Production quality:** Follow Django best practices throughout

---

## 📞 Common Interview Questions

These will be answered throughout the project:

- What is Django ORM and why use it?
- How do ForeignKey relationships work?
- What's the difference between related_name and reverse queries?
- How does Django migration system work?
- Why separate models, views, and templates?
- How do permissions work in Django?
- What's CSRF protection?
- How to handle file uploads securely?

---

**Status:** Ready for Phase 1 🚀

*Next: Database Models & Django ORM*

