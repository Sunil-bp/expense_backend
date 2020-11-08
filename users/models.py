from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.auth.models import User
from PIL import Image
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

#new manger
class ProfileManager(models.Manager):
    def with_counts(self):
        result_list = self.filter(user__username__contains="sunil")
        return result_list
    def with_counts_test(self):
        result_list = self.filter(user__username__contains="te")
        return result_list




##new model for profile
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="User name",
    )

    avialble = models.BooleanField(default = False)
    photo = models.ImageField(upload_to='profile_pics/',default  = "profile_pics/user_default.png")
    place = models.CharField(max_length=30,default="karnataka")


    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        img_path = self.photo.path
        foo = Image.open(img_path)
        foo = foo.resize((160, 300), Image.ANTIALIAS)
        foo.save(img_path, quality=95)

