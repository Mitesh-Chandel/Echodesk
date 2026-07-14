from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from complaints.models import Complaint, Category
from users.models import UserProfile

# ============================================================================
# HOME VIEW
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
# USER DASHBOARD VIEW
# ============================================================================

@login_required(login_url='auth:login')
def user_dashboard(request):
    """
    User dashboard showing complaint statistics and recent activity.
    """
    
    # Get user's complaints
    total_complaints = request.user.complaints.count()
    pending = request.user.complaints.filter(status='pending').count()
    in_progress = request.user.complaints.filter(status='in_progress').count()
    resolved = request.user.complaints.filter(status='resolved').count()
    closed = request.user.complaints.filter(status='closed').count()
    rejected = request.user.complaints.filter(status='rejected').count()
    
    # Recent complaints
    recent_complaints = request.user.complaints.all()[:5]
    
    # Unread notifications
    unread_notifications = request.user.notifications.filter(is_read=False)
    
    context = {
        'page_title': 'User Dashboard',
        'total_complaints': total_complaints,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'closed': closed,
        'rejected': rejected,
        'recent_complaints': recent_complaints,
        'unread_notifications': unread_notifications,
    }
    
    return render(request, 'dashboard/user_dashboard.html', context)


# ============================================================================
# STAFF DASHBOARD VIEW
# ============================================================================

@login_required(login_url='auth:login')
def staff_dashboard(request):
    """
    Staff member dashboard showing assigned complaints.
    """
    
    # Check if user is staff
    if request.user.profile.role not in ['staff', 'admin']:
        return redirect('dashboard:user_dashboard')
    
    # Get assigned complaints
    assigned_complaints = Complaint.objects.filter(assigned_staff=request.user)
    
    # Statistics
    total_assigned = assigned_complaints.count()
    pending = assigned_complaints.filter(status='pending').count()
    in_progress = assigned_complaints.filter(status='in_progress').count()
    waiting = assigned_complaints.filter(status='waiting').count()
    resolved = assigned_complaints.filter(status='resolved').count()
    
    # Recent complaints
    recent_complaints = assigned_complaints.order_by('-created_at')[:5]
    
    context = {
        'page_title': 'Staff Dashboard',
        'total_assigned': total_assigned,
        'pending': pending,
        'in_progress': in_progress,
        'waiting': waiting,
        'resolved': resolved,
        'recent_complaints': recent_complaints,
    }
    
    return render(request, 'dashboard/staff_dashboard.html', context)


# ============================================================================
# ADMIN DASHBOARD VIEW
# ============================================================================

@login_required(login_url='auth:login')
def admin_dashboard(request):
    """
    Admin dashboard with system-wide statistics.
    """
    
    # Check if user is admin
    if request.user.profile.role != 'admin':
        return redirect('dashboard:user_dashboard')
    
    # System statistics
    total_complaints = Complaint.objects.count()
    total_users = UserProfile.objects.count()
    total_categories = Category.objects.count()
    
    # Complaint statistics
    pending = Complaint.objects.filter(status='pending').count()
    assigned = Complaint.objects.filter(status='assigned').count()
    in_progress = Complaint.objects.filter(status='in_progress').count()
    waiting = Complaint.objects.filter(status='waiting').count()
    resolved = Complaint.objects.filter(status='resolved').count()
    closed = Complaint.objects.filter(status='closed').count()
    rejected = Complaint.objects.filter(status='rejected').count()
    
    # User role breakdown
    total_regular_users = UserProfile.objects.filter(role='user').count()
    total_staff = UserProfile.objects.filter(role='staff').count()
    total_admins = UserProfile.objects.filter(role='admin').count()
    
    # Category breakdown
    categories = Category.objects.annotate(complaint_count=Count('complaints')).order_by('-complaint_count')[:5]
    
    # Recent complaints
    recent_complaints = Complaint.objects.all().order_by('-created_at')[:5]
    
    context = {
        'page_title': 'Admin Dashboard',
        'total_complaints': total_complaints,
        'total_users': total_users,
        'total_categories': total_categories,
        'pending': pending,
        'assigned': assigned,
        'in_progress': in_progress,
        'waiting': waiting,
        'resolved': resolved,
        'closed': closed,
        'rejected': rejected,
        'total_regular_users': total_regular_users,
        'total_staff': total_staff,
        'total_admins': total_admins,
        'recent_complaints': recent_complaints,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)


# Import Count for annotations
from django.db.models import Count

