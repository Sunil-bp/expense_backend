from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone
import datetime


# Create your models here.

class BankManager(models.Manager):
    def with_counts(self):
        result_list = self.filter(user__username__contains="sunil")
        return result_list

    def with_counts_test(self):
        result_list = self.filter(user__username__contains="te")
        return result_list


class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=30, null=False, blank=False)
    balance = models.IntegerField(null=False, blank=False)
    create_on = models.DateField(default=datetime.date.today)

    # objects = BankManager()

    def __str__(self):
        return f'{self.user.username} account  {self.bank_name} : balance {self.balance}'

    # no need can have multiple account with save name
    # def save(self, *args, **kwargs):
    #     self.bank_name += "-" + self.user.username
    #     super().save(*args, **kwargs)  # Call the "real" save() method.


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_name = models.CharField(max_length=30, null=False, blank=False)
    limit = models.IntegerField(null=False, blank=False)
    expenditure = models.IntegerField(null=False, blank=False)
    create_on = models.DateField(default=datetime.date.today)
    billing_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return f'{self.user.username} name : {self.credit_name} : balance {self.expenditure}'


class Category(models.Model):
    category = [
        ("income", "income"), ("expense", "expense"),
    ]
    category_name = models.CharField(max_length=30, null=False, blank=False)
    type = models.CharField(max_length=9, choices=category)
    pre_add = models.BooleanField(default=False)
    icon = models.CharField(max_length=20, default="home")

    def __str__(self):
        return str(self.category_name) + " : " + str(self.pre_add)


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=30, null=False, blank=False)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)
    pre_add = models.BooleanField(default=False)

    def __str__(self):
        return str(self.subcategory_name) + " : " + str(self.parent.category_name) + " : " + str(self.pre_add)


class AccountCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}   {self.category} '


class AccountSubcategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}  {self.subcategory} '
