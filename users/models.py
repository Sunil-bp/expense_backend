from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.auth.models import User

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Expense vue "),
        # message:
        email_plaintext_message,
        # from:
        "expense.vue@gmail.com",
        # to:
        [reset_password_token.user.email]
    )


##new model for profile
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="related place",
    )
    photo = models.FileField(upload_to='profile_pics/',default  = "profile_pics/user_default.png")
    place = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        print("CHanging photo dimension ")
        super().save(*args, **kwargs)  # Call the "real" save() method.
        print("Changed photo dimension ")