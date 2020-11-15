from rest_framework import serializers
from expense.models import Bank, CreditCard, Subcategory, Category, AccountCategory, AccountSubcategory, ExpenseRecord, \
    ExpenseTransfer, CreditCardRecord


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['bank_name', 'pk', 'balance']

    #only place where serialiser is overriden by a model
    def create(self, validated_data):
        validated_data["user"] = self.context['request'].user
        return Bank.objects.create(**validated_data)


class CreditCardSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["user"] = self.context['request'].user
        return CreditCard.objects.create(**validated_data)

    class Meta:
        model = CreditCard
        fields = ['credit_name', 'pk', 'limit','balance',
                  'due','billing_date','excess']
        # fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AccountCategorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")
    category_name  = serializers.CharField( source="category.category_name")
    type  = serializers.CharField( source="category.type")
    pre_add  = serializers.CharField( source="category.pre_add")
    icon  = serializers.CharField( source="category.icon")

    class Meta:
        model = AccountCategory
        fields = "__all__"


class AccountSubcategorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")
    subcategory_name  = serializers.CharField(source="subcategory.subcategory_name")
    subcategory_id  = serializers.CharField( source="subcategory.pk")
    category  = serializers.CharField( source="subcategory.parent.category_name")
    category_id  = serializers.CharField( source="subcategory.parent.pk")
    pre_add  = serializers.CharField( source="subcategory.pre_add")
    class Meta:
        model = AccountSubcategory
        fields = "__all__"


class ExpenseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseRecord
        fields = "__all__"


class ExpenseTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseTransfer
        fields = "__all__"


class CreditCardRecordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")
    payed = serializers.CharField(read_only=True)
    balance_remaning = serializers.CharField(read_only=True)

    class Meta:
        model = CreditCardRecord
        exclude = ["user"]
