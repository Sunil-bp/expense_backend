from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta


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


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_name = models.CharField(max_length=30, null=False, blank=False)
    limit = models.IntegerField(null=False, blank=False)
    balance = models.IntegerField(null=False, blank=False)
    due = models.IntegerField(null=False, blank=False)
    create_on = models.DateField(default=datetime.date.today)
    billing_date = models.DateField(null=False, blank=False)
    excess = models.IntegerField(null=False, blank=False, default=0)

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
    account = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)
    create_on = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=7, choices=record_type)
    amount = models.IntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f'{self.account}  : {self.amount} :  {self.note}'


class ExpenseTransfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_on = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField(null=False, blank=False)
    from_account = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, related_name='from_account')
    to_account = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, related_name='to_account')
    note = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f'{self.user} :  {self.amount} :   {self.from_account}  {self.to_account}'


class CreditCardRecordManager(models.Manager):

    def add_record(self, user, account, created_on, type, amount, category, sub_category, \
                   note, emi_total, balance_remaning):
        print(f"Calling custom model to add user  credit card expense  ")
        ac = CreditCard.objects.get(pk=account)
        ac.balance -= amount
        ac.save()
        account = CreditCard.objects.get(pk=account)
        category = Category.objects.get(pk=category)
        sub_category = Subcategory.objects.get(pk=sub_category)

        if emi_total and emi_total > 1:
            print("Emi is enabled for this record  ")
            if not created_on:
                set_month = datetime.datetime.now()
            else:
                #2020-08-14T00:53:00Z
                set_month = datetime.datetime.strptime(created_on,'%Y-%m-%dT%H:%M:%SZ')
            for each_emi in range(emi_total):
                # print(type(set_month))
                print(set_month)
                month = set_month + relativedelta(months=each_emi)
                print(f"Creating emi for month {each_emi + 1} and date  {month}")
                new_note = note + " : EMI  " + str(emi_total) + "/" + str((each_emi + 1))
                self.create(user=user,
                            account=account,
                            type=type,
                            created_on=month,
                            amount=amount,
                            category=category,
                            sub_category=sub_category,
                            note=new_note,
                            emi_total=0,
                            balance_remaning=amount / emi_total)
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

    def add_payment(self, user, account, created_on, type, amount, category, sub_category, \
                    note, emi_total, balance_remaning):
        print("Custom model to add credit card payment  ")
        account = CreditCard.objects.get(pk=account)
        category = Category.objects.get(pk=category)
        sub_category = Subcategory.objects.get(pk=sub_category)
        print(f"Saving expense data for this payment  ")
        self.create(user=user,
                    account=account,
                    type="payment",
                    amount=amount,
                    category=category,
                    sub_category=sub_category,
                    note=note,
                    payed=True,
                    emi_total=0,
                    balance_remaning=0)
        print(f"getting Credit card data ")
        ac = CreditCard.objects.get(pk=account.pk)
        payed = 0
        amount += ac.excess
        print(f"Total amount to be used  {amount}")
        billing_date = ac.billing_date
        total_amonut = amount

        print(f"Billing date  is {billing_date}")
        today = datetime.datetime.today()
        current_billing_date = datetime.datetime(today.year, today.month - 1, billing_date.day)
        print(f"\nCurrent billing date is  {current_billing_date}\n")
        # get all payments  noot payed
        old_data = CreditCardRecord.objects.filter(user=user,
                                                   account=account,
                                                   type="expense",
                                                   payed=False,
                                                   created_on__lte=current_billing_date).order_by('created_on')
        print(f"Number of records  {old_data.count()}")
        for data in old_data:
            print(f"Paying for data {data}")
            if data.balance_remaning > total_amonut:
                print(f"Paying {total_amonut} to data {data.note} ")
                data.balance_remaning -= total_amonut
                total_amonut = 0
                data.save()
                break
            else:
                print(f"Paying {data.balance_remaning} to data {data.note}  and setting data as payed")
                total_amonut -= data.balance_remaning
                data.balance_remaning = 0
                data.payed = True
                data.save()
        print(f"payed  is  : {payed}\n remaining amount  : {amount}")
        payed = amount - total_amonut
        ac.balance += payed
        ac.excess = 0
        if total_amonut > 0:
            print('payed more than the required or no paymant to be made storing to access')
            ac.excess = total_amonut
        print(f"Account data is  {ac}")
        ac.save()
        print("saving payment data  ")


class CreditCardRecord(models.Model):
    record_type = [
        ("payment", "payment"), ("expense", "expense"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=7, choices=record_type)
    amount = models.IntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=30, null=False, blank=False)
    payed = models.BooleanField(default=False)
    emi_total = models.IntegerField(null=False, blank=False, default=0)
    balance_remaning = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.account}  : {self.amount} :  {self.note}'

    objects = CreditCardRecordManager()
