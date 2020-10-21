from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.Usercreate.as_view(), name='user-list'),

    ]