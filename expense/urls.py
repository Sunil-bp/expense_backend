from django.urls import path, include
from . import views

urlpatterns = [
    path('bank/', views.BankList.as_view(), name='bank-list'),
    path('bank/<int:pk>/', views.BankDetail.as_view(), name='bank-detail'),
    path('creditcard/', views.CreditCardList.as_view(), name='CreditCard-list'),
    path('creditcard/<int:pk>/', views.CreditCardDetail.as_view(), name='CreditCard-detail'),
    path('category/', views.CategoryList.as_view(), name='expense-tracker-category'),
    path('subcategory/', views.SubcategoryList.as_view(), name='expense-tracker-subcategory'),
    path('categoryaccount/', views.CategoryAccountList.as_view(), name='expense-tracker-category-account'),
    path('subcategoryaccount/', views.SubcategoryAccountList.as_view(), name='expense-tracker-subcategory-account'),
    path('expensetransfer/', views.ExpenseTransferList.as_view(), name='expense-tracker-tansfer'),
    path('expensetransfer/<int:pk>/', views.ExpenseTransferDetail.as_view(), name='expense-tracker-transfer-details'),
    path('user-image/', views.ProfileImage.as_view(), name='expense-tracker-user-image'),
    path('expense/', views.ExpenseList.as_view(), name='expense-tracker-list'),
    path('expense/<int:pk>/', views.ExpenseDetail.as_view(), name='expense-tracker-detail'),
    path('creditrecord/', views.CreditCardExpenseList.as_view(), name='CreditCardRecord-list'),
    path('creditrecord/<int:pk>/', views.CreditCardExpenseDetail.as_view(), name='CreditCardRecord-details'),

]
