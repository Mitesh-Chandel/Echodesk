


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from complaints.models import Complaint, Category
from users.models import UserProfile

# ============================================================================
# HOME VIEW - UNCHANGED
# ============================================================================

def home(request):
    """
    Landing page.
    Redirects to dashboard if authenticated, else to login.
    """
    if request.user.is_authenticated:
        profile = request.user.profile
        if profile.role == 'admin':
            return redirect('dashboard:admin_dashboard')
        elif profile.role == 'staff':
            return redirect('dashboard:staff_dashboard')
        else:
            return redirect('dashboard:user_dashboard')
    else:
        return redirect('auth:login')


# ============================================================================
# USER/STUDENT DASHBOARD VIEW
# ============================================================================
# Why this view:
# Regular users need to see their own complaints at a glance.
# Shows summary stats + recent activity.
#
# Optimization:
# - aggregate() computes ALL counts in ONE database query (not 5 separate)
# - select_related('category') joins Category table, prevents N+1 for each row
# - order_by('-created_at')[:5] limits to 5 newest (efficient with database)
#
# Interview Question:
# "Why not just loop and count statuses in Python?"
# Answer: That's slow! Database does it 1000x faster. Always let DB aggregate.
# ============================================================================

@login_required(login_url='auth:login')
def user_dashboard(request):
    """
    Student/User dashboard showing their own complaint statistics.
    
    Shows:
    - Total complaints count
    - Count by status (Pending, In Progress, Resolved, Rejected, Closed)
    - Recent 5 complaints with details
    - Unread notifications count
    """
    
    # Get current user's complaints ONLY
    user_complaints = request.user.complaints.all()
    
    # ---- Optimization 1: aggregate() ----
    # Computes all counts in ONE SQL query instead of 5 separate queries
    # Example SQL generated: 
    #   SELECT COUNT(*) as total, 
    #          COUNT(CASE WHEN status='pending' THEN 1 END) as pending, ...
    #   FROM complaints WHERE user_id = X
    stats = user_complaints.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status="pending")),
        in_progress=Count("id", filter=Q(status="in_progress")),
        resolved=Count("id", filter=Q(status="resolved")),
        rejected=Count("id", filter=Q(status="rejected")),
        closed=Count("id", filter=Q(status="closed")),
    )
    
    # ---- Optimization 2: select_related() ----
    # Joins the Category table in one query, prevents N+1 problem
    # Without select_related: 1 query for complaints + 5 queries for each category
    # With select_related: 1 query with JOIN to Category table
    recent_complaints = (
        user_complaints
        .select_related("category")  # JOIN Category table
        .order_by("-created_at")[:5]  # Get 5 newest
    )
    
    # Get unread notifications
    unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    
    context = {
        'page_title': 'User Dashboard',
        'stats': stats,
        'recent_complaints': recent_complaints,
        'unread_notifications_count': unread_notifications_count,
    }
    
    return render(request, 'dashboard/student_dashboard.html', context)


# ============================================================================
# STAFF DASHBOARD VIEW
# ============================================================================
# Why this view:
# Staff members need to see complaints ASSIGNED TO THEM.
# They track their workload and pending items.
#
# Key Difference from Admin:
# Staff sees ONLY complaints assigned to them (filter by assigned_staff)
# Admin sees ALL complaints (no filter)
# ============================================================================

@login_required(login_url='auth:login')
def staff_dashboard(request):
    """
    Staff member dashboard showing assigned complaints.
    
    Shows:
    - Total assigned complaints
    - Count by status
    - Recent assigned complaints
    """
    
    # Check if user is staff
    if not (request.user.is_staff or request.user.profile.role == 'staff'):
        return redirect('dashboard:user_dashboard')
    
    # Get ONLY complaints assigned to this staff member
    assigned_complaints = Complaint.objects.filter(assigned_staff=request.user)
    
    # Aggregate counts in ONE query
    stats = assigned_complaints.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status="pending")),
        assigned=Count("id", filter=Q(status="assigned")),
        in_progress=Count("id", filter=Q(status="in_progress")),
        waiting=Count("id", filter=Q(status="waiting")),
        resolved=Count("id", filter=Q(status="resolved")),
    )
    
    # Recent assigned complaints with user and category joins
    recent_complaints = (
        assigned_complaints
        .select_related("user", "category")  # JOIN User and Category tables
        .order_by("-created_at")[:5]
    )
    
    context = {
        'page_title': 'Staff Dashboard',
        'stats': stats,
        'recent_complaints': recent_complaints,
    }
    
    return render(request, 'dashboard/staff_dashboard.html', context)


# ============================================================================
# ADMIN DASHBOARD VIEW
# ============================================================================
# Why this view:
# Admins manage the ENTIRE system.
# They see all users, all complaints, system-wide statistics.
#
# Chart Data Preparation:
# Backend prepares data as dictionaries (not yet rendering charts).
# This data can be used later with Chart.js or any charting library.
#
# Example:
# category_chart_data = {'Electricity': 20, 'Water': 15, 'Road': 9}
# This can be converted to JSON and passed to frontend chart library.
#
# Why prepare now?
# Makes it easy to add charts later without changing views.
# ============================================================================

@login_required(login_url='auth:login')
def admin_dashboard(request):
    """
    Admin dashboard with system-wide statistics.
    
    Shows:
    - Total users, complaints, categories
    - Complaints by status (all statuses)
    - User breakdown by role
    - Recent complaints (all)
    - Chart data (categories, status distribution)
    """
    
    # Check if user is admin
    if not request.user.is_superuser and request.user.profile.role != 'admin':
        return redirect('dashboard:user_dashboard')
    
    # ---- System Wide Statistics ----
    all_complaints = Complaint.objects.all()
    
    # Aggregate all complaint counts in ONE query
    complaint_stats = all_complaints.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status="pending")),
        assigned=Count("id", filter=Q(status="assigned")),
        in_progress=Count("id", filter=Q(status="in_progress")),
        waiting=Count("id", filter=Q(status="waiting")),
        resolved=Count("id", filter=Q(status="resolved")),
        closed=Count("id", filter=Q(status="closed")),
        rejected=Count("id", filter=Q(status="rejected")),
    )
    
    # User statistics
    total_users = UserProfile.objects.count()
    total_staff = UserProfile.objects.filter(role='staff').count()
    total_admins = UserProfile.objects.filter(role='admin').count()
    total_regular_users = UserProfile.objects.filter(role='user').count()
    
    total_categories = Category.objects.count()
    
    # ---- Chart Data Preparation ----
    # Backend prepares data as dictionaries for frontend charting
    
    # 1. Complaints per Category
    # Example output: {'Electricity': 20, 'Water': 15, 'Road': 9}
    # Query: Get complaint count grouped by category
    # values('category__name') → groups by category name
    # annotate(count=Count('id')) → adds a count field for each group
    category_data = (
        all_complaints
        .values("category__name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    # Convert queryset to dictionary
    category_chart_data = {row["category__name"]: row["count"] for row in category_data}
    
    # 2. Status Distribution
    # Example output: {'Pending': 10, 'Resolved': 15, 'Rejected': 2}
    status_data = (
        all_complaints
        .values("status")
        .annotate(count=Count("id"))
    )
    # Convert to readable format (convert 'pending' to 'Pending')
    status_chart_data = {}
    for row in status_data:
        # Get the display name from STATUS_CHOICES
        status_key = row["status"]
        status_display = dict(Complaint.STATUS_CHOICES).get(status_key, status_key)
        status_chart_data[status_display] = row["count"]
    
    # 3. Priority Distribution (bonus for future use)
    priority_data = (
        all_complaints
        .values("priority")
        .annotate(count=Count("id"))
    )
    priority_chart_data = {}
    for row in priority_data:
        priority_key = row["priority"]
        priority_display = dict(Complaint.PRIORITY_CHOICES).get(priority_key, priority_key)
        priority_chart_data[priority_display] = row["count"]
    
    # ---- Recent Complaints for Table ----
    recent_complaints = (
        all_complaints
        .select_related("user", "category", "assigned_staff")
        .order_by("-created_at")[:10]
    )
    
    context = {
        'page_title': 'Admin Dashboard',
        'complaint_stats': complaint_stats,
        'total_users': total_users,
        'total_staff': total_staff,
        'total_admins': total_admins,
        'total_regular_users': total_regular_users,
        'total_categories': total_categories,
        'recent_complaints': recent_complaints,
        
        # Chart data (prepared for frontend charting library)
        'category_chart_data': category_chart_data,
        'status_chart_data': status_chart_data,
        'priority_chart_data': priority_chart_data,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)