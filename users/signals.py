from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.shortcuts import get_object_or_404

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # user=instance
    if created:
        Profile.objects.create(
           user=instance
            )  # Create profile for new user

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):   # Only save if profile exists
        instance.profile.save()

# @receiver(post_save, sender=Profile)
# def update_user(sender, instance, created, **kwargs):
#     profile = instance
#     if created == False:
#         user = get_object_or_404(User, id=profile.user.id)
#         user.email = profile.email
#         user.save()
    