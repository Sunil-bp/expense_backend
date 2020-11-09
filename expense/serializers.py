from rest_framework import serializers
from expense.models import Bank, CreditCard

from rest_framework.serializers import (
EmailField,
CharField,
HyperlinkedIdentityField,
ModelSerializer,
SerializerMethodField,
ValidationError
)
from django.contrib.auth.models import User


class BankSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")

    class Meta:
        model = Bank
        # fields = "__all__"
        exclude = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context['request'].user
        return Bank.objects.create(**validated_data)


class CreditCardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")

    def create(self, validated_data):
        validated_data["user"] = self.context['request'].user
        return CreditCard.objects.create(**validated_data)

    class Meta:
        model = CreditCard
        # fields = "__all__"
        exclude = ["user"]


