# Phase 1: Database Models & ORM - COMPLETE ✅

## Summary

Phase 1 is complete! We've successfully created all core database models for EchoDesk with proper relationships, fields, and constraints.

---

## Models Created

### 1. **UserProfile** (users/models.py)
Extended user model with role-based access control.

**Why it exists:**
- Django's built-in User model doesn't have a role field
- We need to distinguish between regular users, staff, and admins
- OneToOneField allows extending User without modifying Django's core

**Fields:**
- `user` - OneToOneField to Django's User model
- `role` - Choice field: 'user', 'staff', 'admin'
- `phone` - Contact information
- `address` - User's address
- `created_at`, `updated_at` - Timestamps

**Key Methods:**
- `is_staff_member()` - Check if user is staff
- `is_admin()` - Check if user is admin
- `is_regular_user()` - Check if user is regular user

---

### 2. **Category** (complaints/models.py)
Categories of complaints that users can submit.

**Why it exists:**
- Stores complaint categories in the database
- Allows admins to add/remove categories without code changes
- Examples: Electricity, Water, Road, Garbage, Internet, College, Hostel, Transport

**Fields:**
- `name` - Category name (unique)
- `slug` - URL-friendly version (for URLs and filtering)
- `description` - Explanation of the category
- `created_at`, `updated_at` - Timestamps

**Example:**
```python
Category.objects.create(
    name='Electricity',
    slug='electricity',
    description='Issues related to electricity supply and outages'
)
```

---

### 3. **Complaint** (complaints/models.py)
Main complaint model - the core of the application.

**Why it exists:**
- Stores all complaint information
- Tracks status through resolution process
- Links users, staff, and categories

**Fields:**
- `complaint_id` - Auto-generated readable ID (CMP-2026010100001)
- `user` - FK to User (who submitted)
- `category` - FK to Category
- `title` - Complaint title
- `description` - Detailed description
- `priority` - Low, Medium, High, Urgent
- `status` - Pending, Assigned, In Progress, Waiting, Resolved, Closed, Rejected
- `assigned_staff` - FK to User (who's assigned, nullable)
- `location` - Where the issue is
- `created_at`, `updated_at`, `resolved_at` - Timestamps

**Status Workflow:**
```
Pending → Assigned → In Progress → Waiting for User → Resolved → Closed
   ↓
Rejected → Closed
```

**Key Feature - Auto-generated ID:**
```python
def save(self, *args, **kwargs):
    if not self.complaint_id:
        today = timezone.now().strftime('%Y%m%d')
        today_count = Complaint.objects.filter(
            created_at__date=timezone.now().date()
        ).count() + 1
        self.complaint_id = f"CMP-{today}{today_count:04d}"
    super().save(*args, **kwargs)
```

---

### 4. **ComplaintAttachment** (complaints/models.py)
File uploads attached to complaints.

**Why separate model?**
- A complaint can have MULTIPLE attachments
- OneToMany relationship requires separate model
- One-to-one would limit to one file only

**Fields:**
- `complaint` - FK to Complaint
- `file` - FileField for upload (stored in media/complaints/YYYY/MM/DD/)
- `file_name` - Original filename
- `file_type` - Extension (pdf, jpg, png, doc, etc.)
- `uploaded_at` - Timestamp

**Example Usage:**
```python
complaint = Complaint.objects.get(id=1)
complaint.attachments.all()  # All files for this complaint
```

---

### 5. **ComplaintReply** (complaints/models.py)
Communication thread - replies from user or staff.

**Why it exists:**
- Tracks conversation between user and staff
- Each reply is a separate database record
- Creates a timeline of communication
- Supports internal notes (visible to staff only)

**Fields:**
- `complaint` - FK to Complaint
- `replied_by` - FK to User (who replied)
- `reply_type` - 'user', 'staff', or 'internal' (internal notes)
- `message` - The reply text
- `created_at`, `updated_at` - Timestamps

**Example - Get all replies:**
```python
complaint = Complaint.objects.get(id=1)
for reply in complaint.replies.all():
    print(f"{reply.replied_by.username}: {reply.message}")
```

---

### 6. **ComplaintHistory** (complaints/models.py)
Audit trail of all changes to a complaint.

**Why it exists:**
- Maintains complete history for accountability
- Shows who changed what and when
- Useful for debugging and auditing
- Creates transparency for users

**Fields:**
- `complaint` - FK to Complaint
- `change_type` - Type of change (status_change, staff_assigned, etc.)
- `old_value` - Previous value
- `new_value` - New value
- `changed_by` - User who made the change
- `description` - Description of change
- `created_at` - Timestamp

**Example:**
When complaint status changes from "Pending" to "Assigned", a record is created:
```python
ComplaintHistory.objects.create(
    complaint=complaint,
    change_type='status_change',
    old_value='pending',
    new_value='assigned',
    changed_by=request.user,
    description='Assigned to staff member'
)
```

---

### 7. **Review** (complaints/models.py)
User ratings and feedback after complaint resolution.

**Why OneToOneField?**
- Each complaint can have only ONE review
- Prevents duplicate reviews
- Simple mapping between Complaint and Review

**Fields:**
- `complaint` - OneToOneField to Complaint
- `reviewed_by` - FK to User (who gave review)
- `rating` - 1-5 stars
- `feedback` - Text review
- `created_at`, `updated_at` - Timestamps

**Example:**
```python
# Check if complaint has a review
if hasattr(complaint, 'review'):
    print(f"Rating: {complaint.review.rating}/5")
    print(f"Feedback: {complaint.review.feedback}")
```

---

### 8. **Notification** (complaints/models.py)
System notifications for important events.

**Why it exists:**
- Alerts users to complaint updates
- Database notifications (emails come later)
- Tracks read/unread status
- Can be delivered to multiple users

**Fields:**
- `user` - FK to User (who gets notified)
- `complaint` - FK to Complaint (nullable for system notifications)
- `notification_type` - complaint_submitted, assigned, status_changed, reply_received, resolved, etc.
- `message` - Notification text
- `is_read` - Boolean
- `created_at`, `read_at` - Timestamps

**Example:**
```python
# Get unread notifications for user
unread = request.user.notifications.filter(is_read=False)
unread_count = unread.count()
```

---

## Database Relationships Explained

### ForeignKey vs OneToOneField

**ForeignKey (One-to-Many):**
- One category has many complaints
- One user has many complaints
- One complaint has many replies/attachments
- Multiple rows can reference the same parent

```python
category = models.ForeignKey(Category, on_delete=models.CASCADE, ...)
# One category → Many complaints ✓
```

**OneToOneField (One-to-One):**
- One user has one profile
- One complaint has one review (max)
- Unique relationship - no duplicates

```python
complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, ...)
# One complaint → One review only ✓
```

---

## on_delete Options Explained

### CASCADE
When parent is deleted, all related records are deleted too.

```python
user = models.ForeignKey(User, on_delete=models.CASCADE, ...)
# If user is deleted, all their complaints are deleted
```

### SET_NULL
When parent is deleted, the field is set to NULL.

```python
assigned_staff = models.ForeignKey(
    User, 
    on_delete=models.SET_NULL,
    null=True
)
# If staff member is deleted, field becomes NULL (complaint remains)
```

---

## related_name Explained

`related_name` allows reverse queries from parent to child.

**Without related_name:**
```python
# Get all complaints for a user
complaints = Complaint.objects.filter(user=user)
```

**With related_name='complaints':**
```python
# Much cleaner!
complaints = user.complaints.all()
```

**Other examples:**
```python
# From category
complaints = category.complaints.all()

# From user (notifications)
notifications = user.notifications.all()

# From complaint (replies)
replies = complaint.replies.all()
```

---

## Django ORM Concepts

### Django ORM (Object-Relational Mapping)
Django ORM translates Python code to SQL automatically.

**Key Advantage:** Write Python, not SQL!

### What Happens Behind the Scenes

**When you write:**
```python
complaint = Complaint.objects.create(
    user=request.user,
    category=category,
    title="Power outage in sector 5",
    priority='urgent'
)
```

**Django translates to SQL:**
```sql
INSERT INTO complaints_complaint 
(user_id, category_id, title, priority, status, created_at)
VALUES (1, 1, 'Power outage in sector 5', 'urgent', 'pending', '2026-01-01 10:30:00')
```

### Why Use ORM?

✅ **Automatically handles SQL injection prevention**
✅ **Works with any database (MySQL, PostgreSQL, SQLite)**
✅ **Readable Python code**
✅ **Type hints and autocomplete**
✅ **Migrations handle schema changes**

---

## Migrations Explained

**What are migrations?**
Files that describe database schema changes in Python code.

**Why they matter:**
- Track changes over time
- Reproducible database setup
- Team collaboration (version control)
- Easy rollback

### How They Work

**1. Create migration:**
```bash
python manage.py makemigrations
# Creates: complaints/migrations/0001_initial.py
```

**2. Apply migration:**
```bash
python manage.py migrate
# Executes SQL to create tables
```

### Migration File Structure

```python
# complaints/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(...)),
                ('name', models.CharField(max_length=100, unique=True)),
                ...
            ],
        ),
    ]
```

---

## Common Interview Questions & Answers

### Q1: What is ForeignKey and how does it work?
**Answer:**
ForeignKey creates a many-to-one relationship in Django ORM.
- One category → Many complaints
- Automatically creates database constraint
- Prevents referencing non-existent categories
- `on_delete` parameter determines what happens when parent is deleted

**Example:**
```python
category = models.ForeignKey(Category, on_delete=models.CASCADE)
```

---

### Q2: What's the difference between ForeignKey and OneToOneField?
**Answer:**
- **ForeignKey:** Many-to-one (multiple children can have same parent)
- **OneToOneField:** One-to-one (each child linked to exactly one parent, no duplicates)

**When to use:**
- `ForeignKey`: Complaint → Category (many complaints per category)
- `OneToOneField`: Complaint → Review (one review per complaint)

---

### Q3: What does related_name do?
**Answer:**
`related_name` allows reverse queries from parent to child without raw Python loops.

**Without:**
```python
complaints = Complaint.objects.filter(category=category)
```

**With `related_name='complaints'`:**
```python
complaints = category.complaints.all()
```

---

### Q4: Why use Django ORM instead of raw SQL?
**Answer:**
- **Security:** Built-in SQL injection prevention
- **Portability:** Works with any database
- **Readability:** Python code is clearer than SQL
- **Maintainability:** Easy to refactor relationships
- **Speed:** Django optimizes queries automatically

---

### Q5: What happens when I run `python manage.py migrate`?
**Answer:**
Django:
1. Reads all migration files
2. Checks which migrations are already applied (from django_migrations table)
3. Generates SQL for unapplied migrations
4. Executes SQL against the database
5. Records completed migrations

---

### Q6: What does `on_delete=models.CASCADE` mean?
**Answer:**
When the parent record is deleted, all child records are deleted too.

**Example:**
```python
user = models.ForeignKey(User, on_delete=models.CASCADE)
# If user is deleted, all their complaints are deleted
```

**Other options:**
- `SET_NULL`: Set field to NULL (parent deleted, child remains)
- `PROTECT`: Prevent deletion if children exist
- `SET_DEFAULT`: Set to default value

---

## Common Beginner Mistakes

### ❌ Mistake 1: Forgetting on_delete parameter
```python
# WRONG - will cause error
user = models.ForeignKey(User)

# CORRECT
user = models.ForeignKey(User, on_delete=models.CASCADE)
```

### ❌ Mistake 2: Using wrong relationship type
```python
# WRONG - allows multiple reviews per complaint
review = models.ForeignKey(Review, on_delete=models.CASCADE)

# CORRECT
review = models.OneToOneField(Review, on_delete=models.CASCADE)
```

### ❌ Mistake 3: Forgetting to run migrations
```bash
# WRONG - changed model but didn't create migration
python manage.py runserver

# CORRECT
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply to database
python manage.py runserver       # Now run server
```

### ❌ Mistake 4: Querying non-existent relationships
```python
# WRONG - if related_name is 'complaints'
category.complaint_set.all()  # Error!

# CORRECT
category.complaints.all()
```

### ❌ Mistake 5: Modifying without CASCADE
```python
# If staff member is assigned to complaints
assigned_staff = models.ForeignKey(User, on_delete=models.CASCADE)
# Deleting staff deletes all assigned complaints!

# BETTER
assigned_staff = models.ForeignKey(
    User, 
    on_delete=models.SET_NULL,
    null=True
)
# Deleting staff just unassigns complaints
```

---

## Database Schema Overview

### Auto-created Fields
Django automatically adds:
- `id` (BigAutoField) - Primary key
- `created_at`, `updated_at` - Auto timestamps

### Indexes Created
Indexes speed up queries:
```
- user, -created_at (on Complaint) - Fast user complaint queries
- status (on Complaint) - Fast status filtering
- category (on Complaint) - Fast category filtering
- user, is_read (on Notification) - Fast unread notifications
```

---

## How to Query the Models

### Create
```python
category = Category.objects.create(
    name='Electricity',
    slug='electricity'
)

complaint = Complaint.objects.create(
    user=request.user,
    category=category,
    title='No power supply',
    priority='high'
)
```

### Read
```python
# Single object
complaint = Complaint.objects.get(id=1)

# Multiple objects
complaints = Complaint.objects.all()
complaints = Complaint.objects.filter(status='pending')
complaints = Complaint.objects.filter(user=request.user)
```

### Update
```python
complaint.status = 'assigned'
complaint.assigned_staff = staff_user
complaint.save()
```

### Delete
```python
complaint.delete()
```

### Complex Queries
```python
# All pending complaints for a user
user_pending = request.user.complaints.filter(status='pending')

# All high priority urgent complaints
urgent = Complaint.objects.filter(
    priority__in=['high', 'urgent'],
    status='pending'
)

# Complaints with replies
complained_with_replies = Complaint.objects.filter(
    replies__isnull=False
).distinct()
```

---

## What's Next - Phase 2

In Phase 2, we will:
- Register all models in Django admin
- Configure list_display, list_filter, search_fields
- Test models via admin interface
- Set up proper admin organization

**Preparation for Phase 2:**
✅ All models created
✅ Migrations applied
✅ Database tables ready

---

## Files Modified/Created in Phase 1

| File | Status | Changes |
|------|--------|---------|
| [users/models.py](users/models.py) | ✅ Created | UserProfile model |
| [complaints/models.py](complaints/models.py) | ✅ Created | 7 core models |
| [complaints/migrations/0001_initial.py](complaints/migrations/0001_initial.py) | ✅ Created | Migration file |
| [users/migrations/0001_initial.py](users/migrations/0001_initial.py) | ✅ Created | Migration file |
| [config/settings.py](config/settings.py) | ✅ Updated | SQLite database |
| [requirements.txt](requirements.txt) | ✅ Created | Dependencies |

---

## Verification

✅ Models created with proper relationships
✅ Migrations generated without errors
✅ Migrations applied to database
✅ Database schema created
✅ All 8 models ready

**Database Tables Created:**
- auth_user
- complaints_category
- complaints_complaint
- complaints_complaintattachment
- complaints_complainthistory
- complaints_complaintreply
- complaints_review
- complaints_notification
- users_userprofile

---

## Phase 1 Status

**✅ COMPLETE**

All database models have been created with:
- Proper relationships (ForeignKey, OneToOneField)
- Appropriate fields and data types
- Timestamps and metadata
- Database constraints and indexes
- Migration files generated
- Database schema applied

**Ready for Phase 2: Django Admin Configuration**

---

*Phase 1 Completion Date: 2026-01-13*
*Next: Phase 2 - Admin Configuration*

