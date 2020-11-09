from django.contrib import admin
from expense.models import Bank, CreditCard, Subcategory, Category,AccountCategory,AccountSubcategory


admin.site.register(Bank)
admin.site.register(CreditCard)
admin.site.register(Subcategory)
admin.site.register(Category)
admin.site.register(AccountCategory)
admin.site.register(AccountSubcategory)



