from django.urls import path, include
from . import views

urlpatterns = [
    path('user/', views.Usercreate.as_view(), name='user-create'),
    path('userlist/', views.Profilelist.as_view(), name='user-create'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('email/', views.sending_mail, name='user-list'),

]
