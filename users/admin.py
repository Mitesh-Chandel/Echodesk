from django.contrib import admin
from .models import UserProfile

# ============================================================================
# USER PROFILE ADMIN
# ============================================================================
# Why we configure admin:
# - Makes user management easy without writing views/forms
# - Admins can see all users and their roles at a glance
# - Quick way to assign roles and permissions
# 
# Admin features:
# - list_display: Columns shown in list view
# - list_filter: Filters on the right sidebar
# - search_fields: Search bar at top
# - readonly_fields: Fields that can't be edited
# - ordering: Default sort order
# ============================================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for user profiles.
    Allows admins to manage user roles and information.
    """
    
    # Columns displayed in the list view
    list_display = ['get_username', 'get_email', 'role', 'phone', 'created_at']
    
    # Filters on the right sidebar
    list_filter = ['role', 'created_at']
    
    # Search functionality
    search_fields = ['user__username', 'user__email', 'phone']
    
    # Read-only fields (can be viewed but not edited)
    readonly_fields = ['created_at', 'updated_at', 'get_user_link']
    
    # Group fields in sections
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'get_user_link', 'created_at', 'updated_at')
        }),
        ('Role & Permissions', {
            'fields': ('role',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address')
        }),
    )
    
    # Default sort order
    ordering = ['-created_at']
    
    def get_username(self, obj):
        """Display username from related User model"""
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'
    
    def get_email(self, obj):
        """Display email from related User model"""
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'
    
    def get_user_link(self, obj):
        """Link to User admin page"""
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name() or obj.user.username)
    get_user_link.short_description = 'Full User Profile'
