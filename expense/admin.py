from django.contrib import admin
from expense.models import Bank, CreditCard, Subcategory, Category, AccountCategory, AccountSubcategory, ExpenseRecord, \
    ExpenseTransfer, CreditCardRecord


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
    list_display = ['user', 'account', 'type', 'amount', 'category', 'sub_category']


class ExpenseTransferAdmin(admin.ModelAdmin):
    list_display = ['user', 'create_on', 'amount', 'from_account', 'to_account']


class CreditCardRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'account','amount', 'created_on', 'type',
                    'category', 'sub_category',
                    'payed','balance_remaning'
                   ]


admin.site.register(Bank, BankAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AccountCategory, AccountCategoryAdmin)
admin.site.register(AccountSubcategory)
admin.site.register(ExpenseRecord, ExpenseRecordAdmin)
admin.site.register(ExpenseTransfer, ExpenseTransferAdmin)
admin.site.register(CreditCardRecord, CreditCardRecordAdmin)
