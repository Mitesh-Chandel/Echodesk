from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

# ============================================================================
# USER REGISTRATION FORM
# ============================================================================
# Why separate form?
# - Encapsulates validation logic
# - Clean separation from views
# - Reusable across different views
# - Better error handling
# ============================================================================

class UserRegistrationForm(UserCreationForm):
    """
    Custom registration form extending Django's UserCreationForm.
    Collects: username, email, first_name, last_name, password, password confirmation
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        # Clear help texts
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    
    def clean_email(self):
        """Check if email already exists"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        """Save user and create profile"""
        user = super().save(commit=False)
        if commit:
            user.save()
            # Auto-create UserProfile
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'user'})
        return user


# ============================================================================
# USER PROFILE FORM
# ============================================================================

class UserProfileForm(forms.ModelForm):
    """
    Form for users to edit their profile information.
    """
    
    # Additional fields from User model
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91-XXXXXXXXXX'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your address'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate User fields if instance exists
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        """Save profile and update User model"""
        profile = super().save(commit=False)
        
        # Update User fields
        profile.user.first_name = self.cleaned_data.get('first_name', '')
        profile.user.last_name = self.cleaned_data.get('last_name', '')
        profile.user.email = self.cleaned_data.get('email', '')
        
        if commit:
            profile.user.save()
            profile.save()
        
        return profile


# ============================================================================
# PASSWORD CHANGE FORM (extends Django's form)
# ============================================================================

class CustomPasswordChangeForm(forms.Form):
    """
    Form for users to change their password.
    """
    
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password'
        })
    )
    
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
    
    def clean_new_password2(self):
        """Check if passwords match"""
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match.")
        
        return new_password2
