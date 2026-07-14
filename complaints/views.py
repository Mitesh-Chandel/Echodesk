from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Complaint, Category, ComplaintHistory, ComplaintReply, ComplaintAttachment
from .forms import ComplaintForm, ComplaintFilterForm, ComplaintReplyForm, ComplaintAttachmentForm

# ============================================================================
# COMPLAINT LIST VIEW (with filtering and pagination)
# ============================================================================

@login_required(login_url='auth:login')
def complaint_list(request):
    """
    Display list of complaints for the logged-in user.
    Supports filtering by status, priority, category.
    """
    
    # Get all complaints for user
    complaints = request.user.complaints.all().order_by('-created_at')
    
    # Initialize filter form
    filter_form = ComplaintFilterForm(request.GET or None)
    
    # Apply filters
    if filter_form.is_valid():
        # Status filter
        if filter_form.cleaned_data.get('status'):
            complaints = complaints.filter(status=filter_form.cleaned_data['status'])
        
        # Priority filter
        if filter_form.cleaned_data.get('priority'):
            complaints = complaints.filter(priority=filter_form.cleaned_data['priority'])
        
        # Category filter
        if filter_form.cleaned_data.get('category'):
            complaints = complaints.filter(category=filter_form.cleaned_data['category'])
        
        # Search filter
        search_query = filter_form.cleaned_data.get('search', '')
        if search_query:
            complaints = complaints.filter(
                Q(complaint_id__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
    
    # Pagination
    paginator = Paginator(complaints, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'page_title': 'My Complaints',
    }
    
    return render(request, 'complaints/complaint_list.html', context)


# ============================================================================
# COMPLAINT DETAIL VIEW
# ============================================================================

@login_required(login_url='auth:login')
def complaint_detail(request, complaint_id):
    """
    Display detailed view of a single complaint.
    Shows: Details, attachments, replies, history.
    """
    
    # Get complaint and ensure user owns it or is staff/admin
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Check permissions
    if complaint.user != request.user and not request.user.profile.is_staff_member():
        messages.error(request, 'You do not have permission to view this complaint.')
        return redirect('complaints:complaint_list')
    
    # Get related data
    attachments = complaint.attachments.all()
    replies = complaint.replies.all().order_by('created_at')
    history = complaint.history.all().order_by('-created_at')
    
    context = {
        'complaint': complaint,
        'attachments': attachments,
        'replies': replies,
        'history': history,
        'page_title': f'Complaint {complaint.complaint_id}',
    }
    
    return render(request, 'complaints/complaint_detail.html', context)


# ============================================================================
# CREATE COMPLAINT VIEW
# ============================================================================

@login_required(login_url='auth:login')
def complaint_create(request):
    """
    Handle complaint creation.
    GET: Display form
    POST: Create complaint and redirect
    """
    
    # Only regular users can create complaints
    if request.user.profile.role == 'admin':
        messages.error(request, 'Admins cannot create complaints.')
        return redirect('dashboard:admin_dashboard')
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        
        if form.is_valid():
            # Create complaint without saving
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            
            # Create history entry
            ComplaintHistory.objects.create(
                complaint=complaint,
                change_type='status_change',
                old_value='-',
                new_value='pending',
                changed_by=request.user,
                description='Complaint created'
            )
            
            messages.success(request, f'Complaint {complaint.complaint_id} created successfully!')
            return redirect('complaints:complaint_detail', complaint_id=complaint.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ComplaintForm()
    
    context = {
        'form': form,
        'page_title': 'Create Complaint',
    }
    
    return render(request, 'complaints/complaint_form.html', context)


# ============================================================================
# UPDATE COMPLAINT VIEW
# ============================================================================

@login_required(login_url='auth:login')
def complaint_update(request, complaint_id):
    """
    Handle complaint editing.
    Users can only edit their own pending complaints.
    """
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Permission check
    if complaint.user != request.user:
        messages.error(request, 'You can only edit your own complaints.')
        return redirect('complaints:complaint_list')
    
    # Can only edit pending complaints
    if complaint.status != 'pending':
        messages.error(request, 'You can only edit pending complaints.')
        return redirect('complaints:complaint_detail', complaint_id=complaint.id)
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        
        if form.is_valid():
            # Store old values for history
            old_values = {
                'category': complaint.category.name if complaint.category else '-',
                'title': complaint.title,
                'priority': complaint.get_priority_display(),
            }
            
            updated_complaint = form.save()
            
            # Create history entries for changes
            if old_values['category'] != updated_complaint.category.name:
                ComplaintHistory.objects.create(
                    complaint=updated_complaint,
                    change_type='category_change',
                    old_value=old_values['category'],
                    new_value=updated_complaint.category.name,
                    changed_by=request.user,
                    description='Category changed'
                )
            
            if old_values['title'] != updated_complaint.title:
                ComplaintHistory.objects.create(
                    complaint=updated_complaint,
                    change_type='status_change',
                    old_value='Title changed',
                    new_value=updated_complaint.title,
                    changed_by=request.user,
                    description='Complaint title updated'
                )
            
            if old_values['priority'] != updated_complaint.get_priority_display():
                ComplaintHistory.objects.create(
                    complaint=updated_complaint,
                    change_type='priority_change',
                    old_value=old_values['priority'],
                    new_value=updated_complaint.get_priority_display(),
                    changed_by=request.user,
                    description='Priority changed'
                )
            
            messages.success(request, 'Complaint updated successfully!')
            return redirect('complaints:complaint_detail', complaint_id=complaint.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ComplaintForm(instance=complaint)
    
    context = {
        'form': form,
        'complaint': complaint,
        'page_title': f'Edit Complaint {complaint.complaint_id}',
    }
    
    return render(request, 'complaints/complaint_form.html', context)


# ============================================================================
# DELETE COMPLAINT VIEW
# ============================================================================

@login_required(login_url='auth:login')
def complaint_delete(request, complaint_id):
    """
    Handle complaint deletion.
    Users can only delete their own pending complaints.
    """
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Permission check
    if complaint.user != request.user:
        messages.error(request, 'You can only delete your own complaints.')
        return redirect('complaints:complaint_list')
    
    # Can only delete pending complaints
    if complaint.status != 'pending':
        messages.error(request, 'You can only delete pending complaints.')
        return redirect('complaints:complaint_detail', complaint_id=complaint.id)
    
    if request.method == 'POST':
        complaint_id_str = complaint.complaint_id
        complaint.delete()
        messages.success(request, f'Complaint {complaint_id_str} deleted successfully!')
        return redirect('complaints:complaint_list')
    
    context = {
        'complaint': complaint,
        'page_title': f'Delete Complaint {complaint.complaint_id}',
    }
    
    return render(request, 'complaints/complaint_confirm_delete.html', context)


# ============================================================================
# ADD REPLY TO COMPLAINT VIEW (Phase 5)
# ============================================================================

@login_required(login_url='auth:login')
def add_reply(request, complaint_id):
    """
    Handle adding replies to complaints.
    Users and staff can add replies.
    """
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Permission check
    is_owner = complaint.user == request.user
    is_staff = request.user.profile.is_staff_member()
    
    if not is_owner and not is_staff:
        messages.error(request, 'You do not have permission to reply to this complaint.')
        return redirect('complaints:complaint_list')
    
    if request.method == 'POST':
        form = ComplaintReplyForm(request.POST)
        
        if form.is_valid():
            reply = form.save(commit=False)
            reply.complaint = complaint
            reply.replied_by = request.user
            
            # Force reply type based on user role
            if is_staff:
                reply.reply_type = 'staff'
            else:
                reply.reply_type = 'user'
            
            reply.save()
            
            # Create history entry
            ComplaintHistory.objects.create(
                complaint=complaint,
                change_type='reply_added',
                old_value='-',
                new_value=reply.message[:50],
                changed_by=request.user,
                description=f'Reply added by {request.user.username}'
            )
            
            messages.success(request, 'Your reply has been added successfully!')
            return redirect('complaints:complaint_detail', complaint_id=complaint.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ComplaintReplyForm()
    
    context = {
        'form': form,
        'complaint': complaint,
        'page_title': f'Reply to {complaint.complaint_id}',
    }
    
    return render(request, 'complaints/add_reply.html', context)


# ============================================================================
# UPLOAD ATTACHMENT VIEW (Phase 5)
# ============================================================================

@login_required(login_url='auth:login')
def upload_attachment(request, complaint_id):
    """
    Handle file attachment uploads.
    Only the complaint owner can upload attachments.
    """
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Permission check
    if complaint.user != request.user:
        messages.error(request, 'You can only upload attachments to your own complaints.')
        return redirect('complaints:complaint_list')
    
    if request.method == 'POST':
        form = ComplaintAttachmentForm(request.POST, request.FILES)
        
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.complaint = complaint
            attachment.save()
            
            # Create history entry
            ComplaintHistory.objects.create(
                complaint=complaint,
                change_type='attachment_added',
                old_value='-',
                new_value=attachment.file_name,
                changed_by=request.user,
                description=f'Attachment uploaded: {attachment.file_name}'
            )
            
            messages.success(request, f'File "{attachment.file_name}" uploaded successfully!')
            return redirect('complaints:complaint_detail', complaint_id=complaint.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ComplaintAttachmentForm()
    
    context = {
        'form': form,
        'complaint': complaint,
        'page_title': f'Upload Attachment to {complaint.complaint_id}',
    }
    
    return render(request, 'complaints/upload_attachment.html', context)

# ============================================================================
# COMPLAINT LIST VIEW (with filtering and pagination)
# ============================================================================

@login_required(login_url='auth:login')
def complaint_list(request):
    """
    Display list of complaints for the logged-in user.
    Supports filtering by status, priority, category.
    """
    
    # Get all complaints for user
    complaints = request.user.complaints.all().order_by('-created_at')
    
    # Initialize filter form
    filter_form = ComplaintFilterForm(request.GET or None)
    
    # Apply filters
    if filter_form.is_valid():
        # Status filter
        if filter_form.cleaned_data.get('status'):
            complaints = complaints.filter(status=filter_form.cleaned_data['status'])
        
        # Priority filter
        if filter_form.cleaned_data.get('priority'):
            complaints = complaints.filter(priority=filter_form.cleaned_data['priority'])
        
        # Category filter
        if filter_form.cleaned_data.get('category'):
            complaints = complaints.filter(category=filter_form.cleaned_data['category'])
        
        # Search filter
        search_query = filter_form.cleaned_data.get('search', '')
        if search_query:
            complaints = complaints.filter(
                Q(complaint_id__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
    
    # Pagination
    paginator = Paginator(complaints, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'page_title': 'My Complaints',
    }
    
    return render(request, 'complaints/complaint_list.html', context)


# ============================================================================
# COMPLAINT DETAIL VIEW
# ============================================================================

@login_required(login_url='auth:login')
def complaint_detail(request, complaint_id):
    """
    Display detailed view of a single complaint.
    Shows: Details, attachments, replies, history.
    """
    
    # Get complaint and ensure user owns it or is staff/admin
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Check permissions
    if complaint.user != request.user and not request.user.profile.is_staff_member():
        messages.error(request, 'You do not have permission to view this complaint.')
        return redirect('complaints:complaint_list')
    
    # Get related data
    attachments = complaint.attachments.all()
    replies = complaint.replies.all().order_by('created_at')
    history = complaint.history.all().order_by('-created_at')
    
    context = {
        'complaint': complaint,
        'attachments': attachments,
        'replies': replies,
        'history': history,
        'page_title': f'Complaint {complaint.complaint_id}',
    }
    
    return render(request, 'complaints/complaint_detail.html', context)


# ============================================================================
# CREATE COMPLAINT VIEW
# ============================================================================

@login_required(login_url='auth:login')
def complaint_create(request):
    """
    Handle complaint creation.
    GET: Display form
    POST: Create complaint and redirect
    """
    
    # Only regular users can create complaints
    if request.user.profile.role == 'admin':
        messages.error(request, 'Admins cannot create complaints.')
        return redirect('dashboard:admin_dashboard')
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        
        if form.is_valid():
            # Create complaint without saving
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            
            # Create history entry
            ComplaintHistory.objects.create(
                complaint=complaint,
                change_type='status_change',
                old_value='-',
                new_value='pending',
                changed_by=request.user,
                description='Complaint created'
            )
            
            messages.success(request, f'Complaint {complaint.complaint_id} created successfully!')
            return redirect('complaints:complaint_detail', complaint_id=complaint.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ComplaintForm()
    
    context = {
        'form': form,
        'page_title': 'Create Complaint',
    }
    
    return render(request, 'complaints/complaint_form.html', context)


# ============================================================================
# UPDATE COMPLAINT VIEW
# ============================================================================

@login_required(login_url='auth:login')
def complaint_update(request, complaint_id):
    """
    Handle complaint editing.
    Users can only edit their own pending complaints.
    """
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Permission check
    if complaint.user != request.user:
        messages.error(request, 'You can only edit your own complaints.')
        return redirect('complaints:complaint_list')
    
    # Can only edit pending complaints
    if complaint.status != 'pending':
        messages.error(request, 'You can only edit pending complaints.')
        return redirect('complaints:complaint_detail', complaint_id=complaint.id)
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        
        if form.is_valid():
            # Store old values for history
            old_values = {
                'category': complaint.category.name if complaint.category else '-',
                'title': complaint.title,
                'priority': complaint.get_priority_display(),
            }
            
            updated_complaint = form.save()
            
            # Create history entries for changes
            if old_values['category'] != updated_complaint.category.name:
                ComplaintHistory.objects.create(
                    complaint=updated_complaint,
                    change_type='category_change',
                    old_value=old_values['category'],
                    new_value=updated_complaint.category.name,
                    changed_by=request.user,
                    description='Category changed'
                )
            
            if old_values['title'] != updated_complaint.title:
                ComplaintHistory.objects.create(
                    complaint=updated_complaint,
                    change_type='status_change',
                    old_value='Title changed',
                    new_value=updated_complaint.title,
                    changed_by=request.user,
                    description='Complaint title updated'
                )
            
            if old_values['priority'] != updated_complaint.get_priority_display():
                ComplaintHistory.objects.create(
                    complaint=updated_complaint,
                    change_type='priority_change',
                    old_value=old_values['priority'],
                    new_value=updated_complaint.get_priority_display(),
                    changed_by=request.user,
                    description='Priority changed'
                )
            
            messages.success(request, 'Complaint updated successfully!')
            return redirect('complaints:complaint_detail', complaint_id=complaint.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ComplaintForm(instance=complaint)
    
    context = {
        'form': form,
        'complaint': complaint,
        'page_title': f'Edit Complaint {complaint.complaint_id}',
    }
    
    return render(request, 'complaints/complaint_form.html', context)


# ============================================================================
# DELETE COMPLAINT VIEW
# ============================================================================

@login_required(login_url='auth:login')
def complaint_delete(request, complaint_id):
    """
    Handle complaint deletion.
    Users can only delete their own pending complaints.
    """
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Permission check
    if complaint.user != request.user:
        messages.error(request, 'You can only delete your own complaints.')
        return redirect('complaints:complaint_list')
    
    # Can only delete pending complaints
    if complaint.status != 'pending':
        messages.error(request, 'You can only delete pending complaints.')
        return redirect('complaints:complaint_detail', complaint_id=complaint.id)
    
    if request.method == 'POST':
        complaint_id_str = complaint.complaint_id
        complaint.delete()
        messages.success(request, f'Complaint {complaint_id_str} deleted successfully!')
        return redirect('complaints:complaint_list')
    
    context = {
        'complaint': complaint,
        'page_title': f'Delete Complaint {complaint.complaint_id}',
    }
    
    return render(request, 'complaints/complaint_confirm_delete.html', context)

