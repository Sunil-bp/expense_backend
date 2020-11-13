from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone
import datetime
from django.db import IntegrityError
from dateutil.relativedelta import relativedelta

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

    # ok so save.super  but check for first time
    # def save(self, *args, **kwargs):
    #     if self.id == None:
    #         old_data = Bank.objects.filter(user= self.user,bank_name =self.bank_name ).count()
    #         if old_data>0:
    #             print(f"Already data exists  {old_data}")
    #             # raise IntegrityError
    #             return "data already there "
    #
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
    eccess = models.IntegerField(null=False, blank=False,default=0)

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



class CreditCardRecordManager(models.Manager):

    def add_record(self,user,account,created_on,type,amount,category,sub_category,\
                   note,emi_total,balance_remaning):
        print("custom model to add user  credit card expense  ")
        print(f"self is  {self}")
        ac = CreditCard.objects.get(pk = account)
        ac.balance -= amount
        ac.save()
        account = CreditCard.objects.get(pk = account)
        category = Category.objects.get(pk = category)
        sub_category = Subcategory.objects.get(pk = sub_category)


        if emi_total and emi_total > 1:
            print("Emi is enabled for this record  ")
            if not created_on:
                set_month = datetime.datetime.now()
            else:
                set_month = created_on
            for each_emi in range(emi_total):
                month = set_month + relativedelta(months=each_emi)
                print(f"Crating emi for month {each_emi+1} and date  {month}")
                new_note = note + " : EMI  "+ str(emi_total) +"/"+str((each_emi+1))
                self.create(user=user,
                            account=account,
                            type=type,
                            created_on=month,
                            amount=amount,
                            category=category,
                            sub_category=sub_category,
                            note=new_note,
                            emi_total=0,
                            balance_remaning=amount/emi_total)
            print("saving final data  ")
            self.create(user=user,
                        account=account,
                        type=type,
                        created_on=set_month,
                        amount=amount,
                        category=category,
                        sub_category=sub_category,
                        note=note,
                        payed=True,
                        emi_total=emi_total,
                        balance_remaning=0)
        else:
            print("no emi on this one ")
            if not created_on:
                self.create(user=user,
                            account=account,
                            type=type,
                            amount=amount,
                            category=category,
                            sub_category=sub_category,
                            note=note,
                            emi_total=0,
                            balance_remaning=amount)
            else:
                self.create(user=user,
                            account=account,
                            created_on=created_on,
                            type=type,
                            amount=amount,
                            category=category,
                            sub_category=sub_category,
                            note=note,
                            emi_total=0,
                            balance_remaning=amount)

    def add_payment(self,user,account,created_on,type,amount,category,sub_category,\
                   note,emi_total,balance_remaning):
        print("custom model to add user  credit card payment  ")
        print(f"self is  {self}")
        ac = CreditCard.objects.get(pk = account)
        if ac.eccess > 0:
            print("SOme money from last payment stored in bank ")
            amount += ac.eccess
        total_amonut  = amount

        if ac.due > 0 :

            print("paying old due ")
            if ac.due > amount:
                ac.due -= amount
            else:
                amount -= ac.due
                ac.due = 0
        print("Adding amout into balance  ")
        ac.balance += amount
        billing_date = ac.billing_date
        ac.save()
        account = CreditCard.objects.get(pk = account)
        category = Category.objects.get(pk = category)
        sub_category = Subcategory.objects.get(pk = sub_category)
        print(f"billing date  is {billing_date}")
        today = datetime.datetime.today()
        current_billing_date = datetime.datetime(today.year,today.month-1,billing_date.day)
        print(f"Currnt billing date is  {current_billing_date}")
        #get all payments  noot payed
        old_data  = CreditCardRecord.objects.filter(user=user,
                                                    account=account,
                                                    type="expense",
                                                    payed=False,
                                                    created_on__lte=current_billing_date).order_by('created_on')
        print(f"number of records  {old_data.count()}")
        for data in old_data:
            print(f"Paying for data {data}")
            if data.balance_remaning > total_amonut:
                data.balance_remaning -= total_amonut
                data.save()
                break
            else:
                total_amonut -= data.balance_remaning
                data.balance_remaning = 0
                data.payed = True
                data.save()
        if balance_remaning >0 :
            print('payed more than the required  storng to access')
            ac = CreditCard.objects.get(pk=account)
            ac.eccess = balance_remaning
            ac.save()
        print("saving payment data  ")
        self.create(user=user,
                    account=account,
                    type="payment",
                    amount=amount,
                    category=category,
                    sub_category=sub_category,
                    note=note,
                    payed= True,
                    emi_total=0,
                    balance_remaning=0)





class CreditCardRecord(models.Model):
    record_type = [
        ("payment", "payment"), ("expense", "expense"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account =  models.ForeignKey(CreditCard, on_delete=models.SET_NULL,null=True)
    created_on = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=7, choices=record_type)
    amount = models.IntegerField(null=False, blank=False)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=30, null=False, blank=False)
    payed = models.BooleanField(default=False)
    emi_total  =  models.IntegerField(null=False, blank=False,default=0)
    balance_remaning = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.account}  : {self.amount} :  {self.note}'


    objects  = CreditCardRecordManager()
    ##first time m  odel save  ,,, amount  = balance_remoening
    # def save(self, *args, **kwargs):
    #     if self.pk == None:
    #         if self.type =="expense":
    #             #the data is added for the first time
    #             self.balance_remaning = self.amount
    #             if self.emi_total > 0 :
    #                 self.balance_remaning = self.amount / self.emi_total
    #         else:
    #             distribute_amount  = self.amount
    #             #makiing a payment
    #             all_unpaid = CreditCardRecord.objects.filter(user=self.user,account=self.account,type="expense", payed=False).order_by('create_on')
    #             for record in all_unpaid:
    #                 print(f"Data is {record}")
    #                 #check if emi is due for this month
    #                 d1  = datetime.datetime.now()
    #                 d2  = record.create_on
    #                 print(d1,d2,d1.month,d2.month)
    #                 mon = (d1.year - d2.year) * 12 + d1.month - d2.month
    #                 print(f" months diff  {mon}" )
    #
    #                 # if record.emi_remaining > 0:
    #                 #     ##the amount payable is not amount but amount/ total emi
    #                 #     payabe  = record.amount / record.emi_total
    #                 # else :
    #                 #     payabe = record.amount
    #                 if record.balance_remaning > distribute_amount:
    #                     print("balance is greter than amont being paid ")
    #                     record.balance_remaning -= distribute_amount
    #                     print(record.balance_remaning)
    #                     record.save()
    #                     break
    #                 else:
    #                     distribute_amount  -= record.balance_remaning
    #                     if record.emi_remaining <= 1:
    #                         print("emi conpleted  ")
    #                         record.balance_remaning = 0
    #                         record.emi_remaining  = 0
    #                         record.payed = True
    #                     else:
    #                         print("emi remians ")
    #                         record.balance_remaning = record.amount / record.emi_total
    #                         record.emi_remaining -= 1
    #                 record.save()
    #         self.payed = True
    #     super().save(*args, **kwargs)  # Call the "real" save() method.

