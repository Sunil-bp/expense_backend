from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone
import datetime
from django.db import IntegrityError

# Create your models here.

class BankManager(models.Manager):
    def with_counts(self):
        result_list = self.filter(user__username__contains="sunil")
        return result_list

    def with_counts_test(self):
        result_list = self.filter(user__username__contains="te")
        return result_list


class Bank(models.Model):
    # typegiven = [
    #     ("bank", "bank"), ("credit", "credit"),
    # ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=30, null=False, blank=False)
    balance = models.IntegerField(null=False, blank=False)
    create_on = models.DateField(default=datetime.date.today)
    # type = models.CharField(max_length=9, choices=typegiven,default="bank")

    # objects = BankManager()

    def __str__(self):
        return f'{self.user.username} account  {self.bank_name} : balance {self.balance}'

    # no need can have multiple account with save name
    # def save(self, *args, **kwargs):
    #     self.bank_name += "-" + self.user.username
    #     super().save(*args, **kwargs)  # Call the "real" save() method.

    ## problem with two sbi account
    ##o this has to be done in view or the model set as unique
    # def save(self, *args, **kwargs):
    #     old_data = Bank.objects.filter(user= self.user,bank_name =self.bank_name ).count()
    #     if old_data>0:
    #         print(f"Already data exists  {old_data}")
    #         # raise IntegrityError
    #         return "data already there "
    #     # self.bank_name += "-" + self.user.username
    #     super().save(*args, **kwargs)  # Call the "real" save() method.


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_name = models.CharField(max_length=30, null=False, blank=False)
    limit = models.IntegerField(null=False, blank=False)
    balance = models.IntegerField(null=False, blank=False)
    due = models.IntegerField(null=False, blank=False)
    create_on = models.DateField(default=datetime.date.today)
    billing_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return f'{self.user.username} name : {self.credit_name} : balance {self.balance}'


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


class ExpenseRecord(models.Model):
    record_type = [
        ("income", "income"), ("expense", "expense"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account =  models.ForeignKey(Bank, on_delete=models.SET_NULL,null=True)
    create_on = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=7, choices=record_type)
    amount = models.IntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f'{self.account}  : {self.amount} :  {self.note}'


class ExpenseTransfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_on = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField(null=False, blank=False)
    from_account = models.ForeignKey(Bank, on_delete=models.SET_NULL,null=True,related_name='from_account')
    to_account = models.ForeignKey(Bank, on_delete=models.SET_NULL,null=True,related_name='to_account')
    note = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f'{self.user} :  {self.amount} :   {self.from_account}  {self.to_account}'


class CreditCardRecord(models.Model):
    record_type = [
        ("payment", "payment"), ("expense", "expense"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account =  models.ForeignKey(CreditCard, on_delete=models.SET_NULL,null=True)
    create_on = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=7, choices=record_type)
    amount = models.IntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=30, null=False, blank=False)
    payed = models.BooleanField(default=False)
    emi_remaining  =  models.IntegerField(null=False, blank=False,default=0)
    emi_total  =  models.IntegerField(null=False, blank=False,default=0)
    balance_remaning = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.account}  : {self.amount} :  {self.note}'

    ##first time model save  ,,, amount  = balance_remoening
    def save(self, *args, **kwargs):
        if self.pk == None:
            if self.type =="expense":
                #the data is added for the first time
                self.balance_remaning = self.amount
                if self.emi_total > 0 :
                    self.balance_remaning = self.amount / self.emi_total
            else:
                distribute_amount  = self.amount
                #makiing a payment
                all_unpaid = CreditCardRecord.objects.filter(user=self.user,account=self.account,type="expense", payed=False).order_by('create_on')
                for record in all_unpaid:
                    print(f"Data is {record}")
                    #check if emi is due for this month
                    d1  = datetime.datetime.now()
                    d2  = record.create_on
                    print(d1,d2,d1.month,d2.month)
                    mon = (d1.year - d2.year) * 12 + d1.month - d2.month
                    print(f" months diff  {mon}" )

                    # if record.emi_remaining > 0:
                    #     ##the amount payable is not amount but amount/ total emi
                    #     payabe  = record.amount / record.emi_total
                    # else :
                    #     payabe = record.amount
                    if record.balance_remaning > distribute_amount:
                        print("balance is greter than amont being paid ")
                        record.balance_remaning -= distribute_amount
                        print(record.balance_remaning)
                        record.save()
                        break
                    else:
                        distribute_amount  -= record.balance_remaning
                        if record.emi_remaining <= 1:
                            print("emi conpleted  ")
                            record.balance_remaning = 0
                            record.emi_remaining  = 0
                            record.payed = True
                        else:
                            print("emi remians ")
                            record.balance_remaning = record.amount / record.emi_total
                            record.emi_remaining -= 1
                    record.save()
            self.payed = True
        super().save(*args, **kwargs)  # Call the "real" save() method.
