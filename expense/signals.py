from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from users.models import Profile
from django.dispatch import receiver
from expense.models import Subcategory, Category \
    , AccountCategory, AccountSubcategory, Bank, CreditCard, ExpenseRecord, ExpenseTransfer


@receiver(post_save, sender=Profile)
def update_user_set_up(sender, instance, **kwargs):
    if kwargs['created']:
        print(f"Running signal to add default categories for user {instance.user}")
        category_querry = Category.objects.filter(pre_add=True)
        for category in category_querry:
            ac = AccountCategory.objects.create(user=instance.user, category=category)
            ac.save()
        sub_category_querry = Subcategory.objects.filter(pre_add=True)
        for sub_category in sub_category_querry:
            sac = AccountSubcategory.objects.create(user=instance.user, subcategory=sub_category)
            sac.save()


# use two table for storing expense records
# @receiver(post_save, sender=CreditCard)
# def update_user_set_up(sender, instance, **kwargs):
#     if kwargs['created']:
#         print(f"Running signal to add new bank  data for {instance.user}")
#         sac = Bank.objects.create(
#             user=instance.user,
#             bank_name = instance.credit_name + "__" + instance.user
#             balance =
#             create_on
#             type = mo
#             subcategory=sub_category)
#         # sac.save()


@receiver(pre_save, sender=ExpenseRecord)
def add_expense(sender, instance, **kwargs):
    print(f"signal foor expense record  ")
    ar = ExpenseRecord.objects.get(pk = instance.pk)
    ac = Bank.objects.get(user=instance.user, bank_name=instance.account.bank_name)

    amount  = 0
    if ar:
        if instance.type == "income":
            ac.balance += (instance.amount -amount )
        else:
            ac.balance -= ( instance.amount - amount) 
    else:
        if instance.type == "income":
            ac.balance +=  instance.amount
        else:
            ac.balance -= instance.amount
    ac.save()


@receiver(post_save, sender=ExpenseTransfer)
def expense_transfer(sender, instance, **kwargs):

    ac = Bank.objects.get(user=instance.user, bank_name=instance.from_account.bank_name)
    ac.balance -= instance.amount
    ac.save()
    ac = Bank.objects.get(user=instance.user, bank_name=instance.to_account.bank_name)
    ac.balance += instance.amount
    ac.save()


@receiver(post_delete, sender=ExpenseRecord)
def expense_deleted(sender, instance, **kwargs):

    ##if bank is not existing  then just delete
    if not instance.account:
        print("Bank doesn't exists  exists ")
        return
    ac = Bank.objects.get(user=instance.user, bank_name=instance.account.bank_name)
    if instance.type == "income":
        ac.balance -= instance.amount
    else:
        ac.balance += instance.amount
    ac.save()
