from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from expense.models import Category, Subcategory, AccountSubcategory, AccountCategory


def add_default_cate(modeladmin, request, queryset):
    category_querry = Category.objects.filter(pre_add=True)

    for each_user in queryset:
        print("Each user is  %s", each_user)
        for category in category_querry:
            ac = AccountCategory.objects.get_or_create(user=each_user, category=category)
        sub_category_querry = Subcategory.objects.filter(pre_add=True)
        for sub_category in sub_category_querry:
            sac = AccountSubcategory.get_or_create.create(user=each_user, subcategory=sub_category)


add_default_cate.short_description = "Add all default categories "


class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        UserAdmin.list_display = list(UserAdmin.list_display) + ['date_joined']

    actions = [add_default_cate]

    # Function to count objects of each user from another Model (where user is FK)
    # def some_function(self, obj):
    #     return obj.another_model_set.count()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


def make_aviable(modeladmin, request, queryset):
    queryset.update(available=True)


make_aviable.short_description = "Mark selected users as avialble"


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo']
    ordering = ['user']
    actions = [make_aviable]


admin.site.register(Profile, ProfileAdmin)
