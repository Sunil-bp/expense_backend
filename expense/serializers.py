from rest_framework import serializers
from expense.models import Bank, CreditCard, Subcategory, Category, AccountCategory, AccountSubcategory, ExpenseRecord, \
    ExpenseTransfer, CreditCardRecord
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


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =Category
        fields = "__all__"



class AccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =AccountCategory
        fields = "__all__"


class AccountSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =AccountSubcategory
        fields = "__all__"

class ExpenseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model =ExpenseRecord
        fields = "__all__"


class ExpenseTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model =ExpenseTransfer
        fields = "__all__"