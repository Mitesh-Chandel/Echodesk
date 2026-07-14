from django import forms
from .models import Complaint, Category, ComplaintReply, ComplaintAttachment

# ============================================================================
# COMPLAINT REPLY FORM
# ============================================================================

class ComplaintReplyForm(forms.ModelForm):
    """
    Form for adding replies to complaints.
    """
    
    class Meta:
        model = ComplaintReply
        fields = ['message', 'reply_type']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your reply here...'
            }),
            'reply_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


# ============================================================================
# COMPLAINT ATTACHMENT FORM
# ============================================================================

class ComplaintAttachmentForm(forms.ModelForm):
    """
    Form for uploading file attachments to complaints.
    Validates file types and sizes.
    """
    
    class Meta:
        model = ComplaintAttachment
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png,.gif'
            }),
        }
    
    def clean_file(self):
        """Validate file type and size"""
        file = self.cleaned_data.get('file')
        
        if file:
            # Check file size (max 5MB)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must not exceed 5MB.")
            
            # Check file extension
            allowed_extensions = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif']
            file_extension = file.name.split('.')[-1].lower()
            
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(f"File type '.{file_extension}' is not allowed. Allowed types: {', '.join(allowed_extensions)}")
        
        return file


# ============================================================================
# COMPLAINT FORM
# ============================================================================

class ComplaintForm(forms.ModelForm):
    """
    Form for creating and updating complaints.
    """
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Complaint
        fields = ['category', 'title', 'description', 'priority', 'location']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of your complaint'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Provide detailed information about your complaint'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'location': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Location where the issue occurred (optional)'
            }),
        }


# ============================================================================
# COMPLAINT SEARCH/FILTER FORM
# ============================================================================

class ComplaintFilterForm(forms.Form):
    """
    Form for filtering complaints.
    """
    
    STATUS_CHOICES = [('', 'All Statuses')] + list(Complaint.STATUS_CHOICES)
    PRIORITY_CHOICES = [('', 'All Priorities')] + list(Complaint.PRIORITY_CHOICES)
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="All Categories",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by complaint ID or title...'
        })
    )
