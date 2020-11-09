from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User
from users.models import Profile
from django.dispatch import receiver
from expense.models import Subcategory,Category\
    ,AccountCategory,AccountSubcategory


@receiver(post_save, sender=Profile)
def update_user_set_up(sender, instance, **kwargs):
    if kwargs['created']:
        print(f"Running signal to add default categories for user {instance.user}")
        category_querry = Category.objects.filter(pre_add=True)
        for category in category_querry:
            ac = AccountCategory.objects.create(user= instance.user,category=category)
            ac.save()
        sub_category_querry = Subcategory.objects.filter(pre_add=True)
        for sub_category in sub_category_querry:
            sac = AccountSubcategory.objects.create(user=instance.user, subcategory=sub_category)
            sac.save()