from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password']

class ProfileList(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")
    email = serializers.CharField(source="user.email")
    first_name =  serializers.CharField(source="user.first_name")
    last_name =  serializers.CharField(source="user.last_name")
    last_login =  serializers.CharField(source="user.last_login")
    class Meta:
        model = Profile
        fields = ['username','pk','email','photo','first_name','last_name','last_login']
        # fields = ['username']

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)