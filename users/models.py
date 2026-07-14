from django.db import models
from django.contrib.auth.models import User

# ============================================================================
# USER ROLE MODEL
# ============================================================================
# Why this exists:
# Django's built-in User model doesn't have a role/user_type field.
# We create a UserProfile model with a OneToOneField to extend the User model.
# This allows us to add custom fields like role without modifying Django's core.
#
# Django Concept:
# OneToOneField creates a 1:1 relationship between User and UserProfile.
# This is more efficient than adding fields directly to User model.
# ============================================================================

class UserProfile(models.Model):
    """
    Extended user profile with role-based access control.
    
    Roles:
    - user: Regular user who submits complaints (default)
    - staff: Staff member who processes complaints
    - admin: System administrator
    """
    
    ROLE_CHOICES = [
        ('user', 'Regular User'),
        ('staff', 'Staff Member'),
        ('admin', 'Administrator'),
    ]
    
    # OneToOneField ensures each User has exactly one UserProfile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Role field to determine permissions
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    # Contact information
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    
    def is_staff_member(self):
        """Check if user is staff"""
        return self.role == 'staff'
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_regular_user(self):
        """Check if user is regular user"""
        return self.role == 'user'
