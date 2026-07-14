from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# ============================================================================
# CATEGORY MODEL
# ============================================================================
# Why this exists:
# Complaints need to be categorized (Electricity, Water, Road, etc.).
# Storing categories in DB allows admins to add/remove/modify categories
# without changing code.
#
# Key Points:
# - CharField for category name (max_length=100)
# - slug field for URL-friendly names
# - description to explain the category
# ============================================================================

class Category(models.Model):
    """
    Complaint categories.
    Examples: Electricity, Water, Road, Garbage, Internet, College, Hostel, Transport, Other
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # slug: URL-friendly version of the name (e.g., "electricity-issues")
    # Used in URLs and filtering
    slug = models.SlugField(max_length=100, unique=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


# ============================================================================
# COMPLAINT MODEL
# ============================================================================
# Why this exists:
# This is the core model. Users submit complaints that staff processes.
# It tracks all complaint details: title, description, status, priority, etc.
#
# Key Relationships:
# - ForeignKey(User): The user who submitted the complaint
# - ForeignKey(Category): What category is this complaint?
# - ForeignKey(User, staff_member): Which staff member is assigned?
#
# Status Flow:
# Pending → Assigned → In Progress → (Waiting for User) → Resolved → Closed
#                   ↓
#              Rejected → Closed
# ============================================================================

class Complaint(models.Model):
    """
    Main complaint model for tracking user complaints.
    """
    
    # Priority levels
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Complaint status
    STATUS_CHOICES = [
        ('pending', 'Pending'),           # Just submitted
        ('assigned', 'Assigned'),         # Assigned to staff
        ('in_progress', 'In Progress'),   # Staff working on it
        ('waiting', 'Waiting for User'),  # Waiting for user response
        ('resolved', 'Resolved'),         # Issue resolved
        ('closed', 'Closed'),             # Complaint closed
        ('rejected', 'Rejected'),         # Complaint rejected
    ]
    
    # Auto-generated unique complaint ID (e.g., CMP-20260001)
    complaint_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # User who submitted complaint
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    
    # Category of complaint
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='complaints')
    
    # Complaint details
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Priority and status
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Staff member assigned to this complaint (nullable - not assigned initially)
    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )
    
    # Location/details
    location = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.complaint_id} - {self.title}"
    
    def save(self, *args, **kwargs):
        """
        Override save to auto-generate complaint_id if not exists.
        complaint_id format: CMP-YYYYMMDD0001
        """
        if not self.complaint_id:
            today = timezone.now().strftime('%Y%m%d')
            # Count complaints created today
            today_count = Complaint.objects.filter(
                created_at__date=timezone.now().date()
            ).count() + 1
            self.complaint_id = f"CMP-{today}{today_count:04d}"
        
        super().save(*args, **kwargs)


# ============================================================================
# COMPLAINT ATTACHMENT MODEL
# ============================================================================
# Why this exists:
# Users may want to attach files (images, documents) with their complaints.
# This model stores file information separately for better organization.
#
# Why separate model?
# A complaint can have multiple attachments (one-to-many relationship).
# This is why we use ForeignKey(Complaint), not a simple FileField.
#
# File validation happens when files are uploaded (in forms/views).
# ============================================================================

class ComplaintAttachment(models.Model):
    """
    File attachments for complaints.
    Supports images and documents.
    """
    
    ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif']
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='attachments')
    
    # File upload with custom storage path
    file = models.FileField(upload_to='complaints/%Y/%m/%d/')
    
    # Original filename for display
    file_name = models.CharField(max_length=255)
    
    # File type for validation
    file_type = models.CharField(max_length=10, blank=True)
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Complaint Attachment'
        verbose_name_plural = 'Complaint Attachments'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.complaint.complaint_id} - {self.file_name}"
    
    def save(self, *args, **kwargs):
        """Extract file type and name"""
        if self.file:
            self.file_name = self.file.name
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)


# ============================================================================
# COMPLAINT REPLY MODEL
# ============================================================================
# Why this exists:
# Communication between user and staff happens through replies.
# This model tracks each message in the conversation.
#
# replied_by can be either user or staff.
# We determine who replied by checking the user's role.
# ============================================================================

class ComplaintReply(models.Model):
    """
    Replies to complaints from user or staff.
    Creates a conversation thread.
    """
    
    REPLY_TYPE_CHOICES = [
        ('user', 'User Reply'),
        ('staff', 'Staff Reply'),
        ('internal', 'Internal Note'),  # Internal notes only visible to staff
    ]
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='replies')
    
    # User who replied
    replied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='complaint_replies')
    
    # Type of reply
    reply_type = models.CharField(max_length=10, choices=REPLY_TYPE_CHOICES, default='user')
    
    # Reply message
    message = models.TextField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Complaint Reply'
        verbose_name_plural = 'Complaint Replies'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Reply to {self.complaint.complaint_id} by {self.replied_by.username}"


# ============================================================================
# COMPLAINT HISTORY MODEL
# ============================================================================
# Why this exists:
# Track all changes to a complaint (status changes, staff assignment, etc.)
# This creates an audit trail for accountability and transparency.
#
# Key Information:
# - What changed (status, assigned_staff, etc.)
# - What was the old value and new value
# - Who made the change and when
# ============================================================================

class ComplaintHistory(models.Model):
    """
    Audit trail for all complaint changes.
    Tracks status changes, staff assignments, etc.
    """
    
    CHANGE_TYPE_CHOICES = [
        ('status_change', 'Status Changed'),
        ('staff_assigned', 'Staff Assigned'),
        ('priority_change', 'Priority Changed'),
        ('category_change', 'Category Changed'),
        ('attachment_added', 'Attachment Added'),
        ('reply_added', 'Reply Added'),
    ]
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='history')
    
    # What changed
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    
    # Store old and new values
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    
    # Who made the change
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='complaint_history_changes')
    
    # Description of change
    description = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Complaint History'
        verbose_name_plural = 'Complaint Histories'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.complaint.complaint_id} - {self.get_change_type_display()}"


# ============================================================================
# REVIEW MODEL
# ============================================================================
# Why this exists:
# After a complaint is resolved, users can rate and review the resolution.
# This provides feedback on staff performance and service quality.
#
# OneToOneField: A complaint can have only ONE review.
# This prevents duplicate reviews for the same complaint.
# ============================================================================

class Review(models.Model):
    """
    User reviews for resolved complaints.
    Only allows reviews for resolved complaints.
    """
    
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    # OneToOneField ensures each complaint has max one review
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='review')
    
    # User who submitted the review
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')
    
    # Rating (1-5)
    rating = models.IntegerField(choices=RATING_CHOICES)
    
    # Textual feedback
    feedback = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.complaint.complaint_id} - {self.get_rating_display()}"


# ============================================================================
# NOTIFICATION MODEL
# ============================================================================
# Why this exists:
# Users need to be notified of important events:
# - Complaint submitted
# - Complaint assigned
# - Status changed
# - Reply received
# - Complaint resolved
#
# Database notifications allow tracking read/unread status.
# Email notifications can be added later.
# ============================================================================

class Notification(models.Model):
    """
    System notifications for users.
    Triggered by complaint events.
    """
    
    NOTIFICATION_TYPE_CHOICES = [
        ('complaint_submitted', 'Complaint Submitted'),
        ('complaint_assigned', 'Complaint Assigned'),
        ('status_changed', 'Status Changed'),
        ('reply_received', 'Reply Received'),
        ('complaint_resolved', 'Complaint Resolved'),
        ('review_requested', 'Review Requested'),
    ]
    
    # User who receives notification
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    # Related complaint (nullable for system-wide notifications)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    # Type of notification
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    
    # Notification message
    message = models.TextField()
    
    # Read status
    is_read = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_notification_type_display()}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

