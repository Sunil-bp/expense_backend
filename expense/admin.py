from django.contrib import admin
from expense.models import Bank, CreditCard, Subcategory, Category, AccountCategory, AccountSubcategory, ExpenseRecord


class BankAdmin(admin.ModelAdmin):
    list_display = ['user', 'bank_name', 'balance']


class CreditCardAdmin(admin.ModelAdmin):
    list_display = ['user', 'credit_name', 'limit', 'billing_date', 'balance', 'due']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'pre_add', 'type']


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['subcategory_name', 'parent', 'pre_add']


class AccountCategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'category']

class ExpenseRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'account','type','amount','category','sub_category']


admin.site.register(Bank, BankAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AccountCategory, AccountCategoryAdmin)
admin.site.register(AccountSubcategory)
admin.site.register(ExpenseRecord,ExpenseRecordAdmin)

