from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm, CustomPasswordChangeForm
from .models import UserProfile

# ============================================================================
# USER REGISTRATION VIEW
# ============================================================================
# Why Function-Based View?
# - Simpler for basic CRUD
# - Easier to understand for beginners
# - Less magical than Class-Based Views
# - Full control over request/response
# ============================================================================

def register(request):
    """
    Handle user registration.
    GET: Display registration form
    POST: Process form submission and create user
    """
    
    if request.user.is_authenticated:
        # Redirect if already logged in
        return redirect('complaints:complaint_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            # Create user (profile auto-created in form's save method)
            user = form.save()
            
            # Auto-login after registration
            login(request, user)
            
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
            return redirect('dashboard:user_dashboard')
        else:
            # Form has errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Register',
    }
    return render(request, 'auth/register.html', context)


# ============================================================================
# USER LOGIN VIEW
# ============================================================================

def login_view(request):
    """
    Handle user login.
    GET: Display login form
    POST: Authenticate and login user
    """
    
    if request.user.is_authenticated:
        # Redirect if already logged in
        return redirect('dashboard:user_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User exists and password is correct
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next page if specified, else dashboard
            next_page = request.GET.get('next', 'dashboard:user_dashboard')
            return redirect(next_page)
        else:
            # Wrong credentials
            messages.error(request, 'Invalid username or password.')
    
    context = {'page_title': 'Login'}
    return render(request, 'auth/login.html', context)


# ============================================================================
# USER LOGOUT VIEW
# ============================================================================

def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('auth:login')


# ============================================================================
# USER PROFILE VIEW
# ============================================================================
# @login_required decorator:
# - Redirects to login if user not authenticated
# - login_url specifies redirect target
# ============================================================================

@login_required(login_url='auth:login')
def profile(request):
    """
    Display user profile and related data.
    Shows: User info, complaints, notifications
    """
    
    profile = get_object_or_404(UserProfile, user=request.user)
    
    # Get user's complaints (last 5)
    recent_complaints = request.user.complaints.all()[:5]
    
    # Get unread notifications count
    unread_notifications = request.user.notifications.filter(is_read=False).count()
    
    context = {
        'profile': profile,
        'recent_complaints': recent_complaints,
        'unread_notifications': unread_notifications,
        'page_title': 'My Profile',
    }
    
    return render(request, 'auth/profile.html', context)


# ============================================================================
# EDIT PROFILE VIEW
# ============================================================================

@login_required(login_url='auth:login')
def edit_profile(request):
    """
    Handle profile editing.
    GET: Display profile edit form
    POST: Update profile
    """
    
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('auth:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'page_title': 'Edit Profile',
    }
    
    return render(request, 'auth/edit_profile.html', context)


# ============================================================================
# CHANGE PASSWORD VIEW
# ============================================================================

@login_required(login_url='auth:login')
def change_password(request):
    """
    Handle password change.
    GET: Display password change form
    POST: Process password change
    """
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        
        if form.is_valid():
            user = request.user
            
            # Check if old password is correct
            if not user.check_password(form.cleaned_data['old_password']):
                messages.error(request, 'Current password is incorrect.')
            else:
                # Update password
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                
                # Re-login with new password
                login(request, user)
                
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('auth:profile')
    else:
        form = CustomPasswordChangeForm()
    
    context = {
        'form': form,
        'page_title': 'Change Password',
    }
    
    return render(request, 'auth/change_password.html', context)

