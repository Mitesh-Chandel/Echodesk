from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Complaint, ComplaintAttachment, 
    ComplaintReply, ComplaintHistory, Review, Notification
)

# ============================================================================
# CATEGORY ADMIN
# ============================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for complaint categories."""
    
    list_display = ['name', 'slug', 'get_complaint_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'slug', 'description']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate slug from name
    ordering = ['name']
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_complaint_count(self, obj):
        """Show how many complaints in this category"""
        count = obj.complaints.count()
        return format_html(
            '<span style="background-color: #e3f2fd; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    get_complaint_count.short_description = 'Complaints'


# ============================================================================
# COMPLAINT ATTACHMENT INLINE
# ============================================================================

class ComplaintAttachmentInline(admin.TabularInline):
    """
    Inline admin for attachments.
    Allows viewing/editing attachments directly in complaint form.
    """
    model = ComplaintAttachment
    extra = 1
    readonly_fields = ['uploaded_at', 'file_type']
    fields = ['file', 'file_name', 'file_type', 'uploaded_at']


# ============================================================================
# COMPLAINT REPLY INLINE
# ============================================================================

class ComplaintReplyInline(admin.TabularInline):
    """
    Inline admin for replies.
    Allows viewing all replies in the complaint form.
    """
    model = ComplaintReply
    extra = 0
    readonly_fields = ['replied_by', 'created_at', 'updated_at', 'message']
    fields = ['replied_by', 'reply_type', 'message', 'created_at']
    can_delete = False


# ============================================================================
# COMPLAINT HISTORY INLINE
# ============================================================================

class ComplaintHistoryInline(admin.TabularInline):
    """
    Inline admin for complaint history.
    Shows all changes made to the complaint.
    """
    model = ComplaintHistory
    extra = 0
    readonly_fields = ['change_type', 'old_value', 'new_value', 'changed_by', 'created_at', 'description']
    fields = ['change_type', 'old_value', 'new_value', 'changed_by', 'created_at', 'description']
    can_delete = False


# ============================================================================
# COMPLAINT ADMIN (MAIN)
# ============================================================================

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    """
    Main admin interface for complaints.
    Shows overview and allows editing complaint details.
    """
    
    # Columns in list view
    list_display = [
        'complaint_id', 'get_title', 'user', 'category', 
        'priority_badge', 'status_badge', 'assigned_staff', 'created_at'
    ]
    
    # Filters
    list_filter = [
        'status', 'priority', 'category', 'created_at', 'assigned_staff'
    ]
    
    # Search
    search_fields = ['complaint_id', 'title', 'user__username', 'category__name']
    
    # Read-only fields
    readonly_fields = [
        'complaint_id', 'created_at', 'updated_at', 
        'resolved_at', 'get_user_link', 'get_attachments_count',
        'get_replies_count', 'get_history_count'
    ]
    
    # Inline editing for related models
    inlines = [ComplaintAttachmentInline, ComplaintReplyInline, ComplaintHistoryInline]
    
    # Field grouping
    fieldsets = (
        ('Complaint ID & Status', {
            'fields': ('complaint_id', 'status', 'priority')
        }),
        ('Complaint Details', {
            'fields': ('user', 'get_user_link', 'category', 'title', 'description', 'location')
        }),
        ('Assignment', {
            'fields': ('assigned_staff',)
        }),
        ('Timestamps & Counts', {
            'fields': (
                'created_at', 'updated_at', 'resolved_at',
                'get_attachments_count', 'get_replies_count', 'get_history_count'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Default sorting
    ordering = ['-created_at']
    
    # Actions
    actions = ['mark_as_resolved', 'mark_as_closed', 'mark_as_rejected']
    
    def get_title(self, obj):
        """Truncate long titles"""
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    get_title.short_description = 'Title'
    get_title.admin_order_field = 'title'
    
    def priority_badge(self, obj):
        """Display priority as colored badge"""
        colors = {
            'low': '#90EE90',
            'medium': '#FFD700',
            'high': '#FF6347',
            'urgent': '#FF0000'
        }
        color = colors.get(obj.priority, '#808080')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    priority_badge.admin_order_field = 'priority'
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'pending': '#FFA500',
            'assigned': '#1E90FF',
            'in_progress': '#4169E1',
            'waiting': '#9370DB',
            'resolved': '#228B22',
            'closed': '#808080',
            'rejected': '#DC143C'
        }
        color = colors.get(obj.status, '#808080')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def get_user_link(self, obj):
        """Link to User admin"""
        from django.urls import reverse
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    get_user_link.short_description = 'User Profile'
    
    def get_attachments_count(self, obj):
        """Show attachment count"""
        count = obj.attachments.count()
        return format_html(
            '<span style="background-color: #f0f0f0; padding: 3px 8px; border-radius: 3px;">{} files</span>',
            count
        )
    get_attachments_count.short_description = 'Attachments'
    
    def get_replies_count(self, obj):
        """Show reply count"""
        count = obj.replies.count()
        return format_html(
            '<span style="background-color: #f0f0f0; padding: 3px 8px; border-radius: 3px;">{} replies</span>',
            count
        )
    get_replies_count.short_description = 'Replies'
    
    def get_history_count(self, obj):
        """Show history count"""
        count = obj.history.count()
        return format_html(
            '<span style="background-color: #f0f0f0; padding: 3px 8px; border-radius: 3px;">{} changes</span>',
            count
        )
    get_history_count.short_description = 'History'
    
    # Admin actions
    def mark_as_resolved(self, request, queryset):
        """Bulk action to mark complaints as resolved"""
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} complaint(s) marked as resolved.')
    mark_as_resolved.short_description = "Mark selected as Resolved"
    
    def mark_as_closed(self, request, queryset):
        """Bulk action to mark complaints as closed"""
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} complaint(s) marked as closed.')
    mark_as_closed.short_description = "Mark selected as Closed"
    
    def mark_as_rejected(self, request, queryset):
        """Bulk action to mark complaints as rejected"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} complaint(s) marked as rejected.')
    mark_as_rejected.short_description = "Mark selected as Rejected"


# ============================================================================
# COMPLAINT ATTACHMENT ADMIN
# ============================================================================

@admin.register(ComplaintAttachment)
class ComplaintAttachmentAdmin(admin.ModelAdmin):
    """Admin interface for complaint attachments."""
    
    list_display = ['file_name', 'get_complaint_id', 'file_type', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['file_name', 'complaint__complaint_id']
    readonly_fields = ['uploaded_at', 'file_type']
    ordering = ['-uploaded_at']
    
    def get_complaint_id(self, obj):
        """Link to complaint"""
        from django.urls import reverse
        url = reverse('admin:complaints_complaint_change', args=[obj.complaint.id])
        return format_html('<a href="{}">{}</a>', url, obj.complaint.complaint_id)
    get_complaint_id.short_description = 'Complaint'


# ============================================================================
# COMPLAINT REPLY ADMIN
# ============================================================================

@admin.register(ComplaintReply)
class ComplaintReplyAdmin(admin.ModelAdmin):
    """Admin interface for complaint replies."""
    
    list_display = ['get_complaint_id', 'replied_by', 'reply_type', 'created_at']
    list_filter = ['reply_type', 'created_at']
    search_fields = ['complaint__complaint_id', 'replied_by__username', 'message']
    readonly_fields = ['created_at', 'updated_at', 'message']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Reply Information', {
            'fields': ('complaint', 'replied_by', 'reply_type', 'message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_complaint_id(self, obj):
        """Link to complaint"""
        from django.urls import reverse
        url = reverse('admin:complaints_complaint_change', args=[obj.complaint.id])
        return format_html('<a href="{}">{}</a>', url, obj.complaint.complaint_id)
    get_complaint_id.short_description = 'Complaint'


# ============================================================================
# COMPLAINT HISTORY ADMIN
# ============================================================================

@admin.register(ComplaintHistory)
class ComplaintHistoryAdmin(admin.ModelAdmin):
    """Admin interface for complaint history (audit trail)."""
    
    list_display = [
        'get_complaint_id', 'change_type', 'old_value_short',
        'new_value_short', 'changed_by', 'created_at'
    ]
    list_filter = ['change_type', 'created_at']
    search_fields = ['complaint__complaint_id', 'changed_by__username', 'description']
    readonly_fields = [
        'complaint', 'change_type', 'old_value', 'new_value',
        'changed_by', 'description', 'created_at'
    ]
    ordering = ['-created_at']
    can_delete = False
    
    fieldsets = (
        ('Change Information', {
            'fields': ('complaint', 'change_type', 'old_value', 'new_value')
        }),
        ('Additional Details', {
            'fields': ('changed_by', 'description', 'created_at')
        }),
    )
    
    def get_complaint_id(self, obj):
        """Link to complaint"""
        from django.urls import reverse
        url = reverse('admin:complaints_complaint_change', args=[obj.complaint.id])
        return format_html('<a href="{}">{}</a>', url, obj.complaint.complaint_id)
    get_complaint_id.short_description = 'Complaint'
    
    def old_value_short(self, obj):
        """Truncate old value"""
        val = obj.old_value or '-'
        return val[:30] + '...' if len(str(val)) > 30 else val
    old_value_short.short_description = 'Old Value'
    
    def new_value_short(self, obj):
        """Truncate new value"""
        val = obj.new_value or '-'
        return val[:30] + '...' if len(str(val)) > 30 else val
    new_value_short.short_description = 'New Value'


# ============================================================================
# REVIEW ADMIN
# ============================================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for complaint reviews."""
    
    list_display = ['get_complaint_id', 'reviewed_by', 'rating_stars', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['complaint__complaint_id', 'reviewed_by__username', 'feedback']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('complaint', 'reviewed_by', 'rating', 'feedback')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_complaint_id(self, obj):
        """Link to complaint"""
        from django.urls import reverse
        url = reverse('admin:complaints_complaint_change', args=[obj.complaint.id])
        return format_html('<a href="{}">{}</a>', url, obj.complaint.complaint_id)
    get_complaint_id.short_description = 'Complaint'
    
    def rating_stars(self, obj):
        """Display rating as stars"""
        stars = '⭐' * obj.rating
        return format_html(
            '<span style="font-size: 18px;">{}</span> <span style="color: #666;">({}/5)</span>',
            stars, obj.rating
        )
    rating_stars.short_description = 'Rating'
    rating_stars.admin_order_field = 'rating'


# ============================================================================
# NOTIFICATION ADMIN
# ============================================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for notifications."""
    
    list_display = [
        'user', 'notification_type', 'is_read_badge',
        'get_complaint_id', 'created_at'
    ]
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'message', 'complaint__complaint_id']
    readonly_fields = ['created_at', 'read_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('user', 'complaint', 'notification_type', 'message', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def is_read_badge(self, obj):
        """Display read status as badge"""
        if obj.is_read:
            return format_html(
                '<span style="background-color: #90EE90; padding: 3px 8px; border-radius: 3px; color: white;">✓ Read</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #FFD700; padding: 3px 8px; border-radius: 3px; color: black;">✉ Unread</span>'
            )
    is_read_badge.short_description = 'Status'
    is_read_badge.admin_order_field = 'is_read'
    
    def get_complaint_id(self, obj):
        """Link to related complaint if exists"""
        if obj.complaint:
            from django.urls import reverse
            url = reverse('admin:complaints_complaint_change', args=[obj.complaint.id])
            return format_html('<a href="{}">{}</a>', url, obj.complaint.complaint_id)
        return '-'
    get_complaint_id.short_description = 'Complaint'
    
    def mark_as_read(self, request, queryset):
        """Bulk action to mark notifications as read"""
        from django.utils import timezone
        updated = queryset.update(is_read=True, read_at=timezone.now())
        self.message_user(request, f'{updated} notification(s) marked as read.')
    mark_as_read.short_description = "Mark selected as Read"
    
    def mark_as_unread(self, request, queryset):
        """Bulk action to mark notifications as unread"""
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{updated} notification(s) marked as unread.')
    mark_as_unread.short_description = "Mark selected as Unread"

