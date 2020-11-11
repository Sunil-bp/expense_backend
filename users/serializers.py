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
    class Meta:
        model = Profile
        fields = ['username','place','photo']
        # fields = ['username']

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)