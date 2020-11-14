from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import Profile
from django.contrib.auth.signals import user_logged_in, user_logged_out


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating a new profile for user {instance}")
        fp = Profile.objects.create(user=instance)
        fp.save()


@receiver(user_logged_in)
def user_logged_in(sender, user, request, **kwargs):
    print(f"\n\n User {user} logged in ")


@receiver(user_logged_out)
def user_logged_out(sender, user, request, **kwargs):
    print(f"\n\n User  {user} logged out ")
