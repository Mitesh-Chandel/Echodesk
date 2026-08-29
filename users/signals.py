from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def sync_user_profile(sender, instance, **kwargs):
    """
    Keep the custom UserProfile role in sync with Django's auth flags.
    This ensures admins/staff are routed to the correct dashboard.
    """
    profile, _ = UserProfile.objects.get_or_create(user=instance)

    if instance.is_superuser:
        profile.role = 'admin'
    elif instance.is_staff:
        profile.role = 'staff'
    else:
        profile.role = 'user'

    profile.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Backward-compatible profile creation hook.
    """
    if created:
        sync_user_profile(sender, instance, **kwargs)