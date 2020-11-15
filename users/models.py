from django.db import models
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.auth.models import User
from PIL import Image


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print(f"Password reset for user  {reset_password_token.user}")
    email_plaintext_message = "Hi {}, \n" \
                              "A password reset request was requested.\n" \
                              "Please copy the token at our password reset page \n\n" \
                              "token={}\n\n" \
                              "Regards, \n" \
                              "Expense.vue Team ".format(reset_password_token.user, reset_password_token.key)
    print(f"Emial being sent is  \n {email_plaintext_message}")
    send_mail(
        "Password Reset for {title}".format(title="Expense vue "),
        email_plaintext_message,
        "expense.vue@gmail.com",
        [reset_password_token.user.email]
    )

#new manger all test
class ProfileManager(models.Manager):
    def with_counts(self):
        result_list = self.filter(user__username__contains="sunil")
        return result_list
    def with_counts_test(self):
        result_list = self.filter(user__username__contains="te")
        return result_list

    def get_images(self,user_name):
        print(f" In method to get image url for user {user_name}")
        result_list = self.get( user__pk = user_name.pk)
        return [result_list]


##new model for profile
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="User name",
    )

    available = models.BooleanField(default = False)
    photo = models.ImageField(upload_to='profile_pics/',default  = "profile_pics/user_default.png")
    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    #Reducing picture quality to reduce load on server
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        img_path = self.photo.path
        foo = Image.open(img_path)
        foo = foo.resize((160, 300), Image.ANTIALIAS)
        foo.save(img_path, quality=95)



