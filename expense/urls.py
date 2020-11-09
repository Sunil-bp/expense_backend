from django.urls import path, include
from . import views

urlpatterns = [
    path('bank/', views.BankList.as_view(), name='bank-list'),
    path('bank/<int:pk>/', views.BankDetail.as_view(), name='bank-detail'),
    path('creditcard/', views.CreditCardList.as_view(), name='CreditCard-list'),
    path('creditcard/<int:pk>/', views.CreditCardDetail.as_view(), name='CreditCard-detail'),
]
