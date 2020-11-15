from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)

from rest_framework.response import Response
from rest_framework import status

from expense.serializers import BankSerializer, CreditCardSerializer, CreditCardRecordSerializer
from expense.models import Subcategory, Category, Bank, CreditCard, \
    AccountCategory, AccountSubcategory, ExpenseRecord, ExpenseTransfer, CreditCardRecord
from users.models import Profile
from users.serializers import ProfileList
from expense.serializers import SubcategorySerializer, CategorySerializer, \
    AccountCategorySerializer, AccountSubcategorySerializer, \
    ExpenseRecordSerializer, ExpenseTransferSerializer, CreditCardRecordSerializer

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class BankList(generics.ListCreateAPIView):
    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)

    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            bank = Bank.objects.filter(user=request.user, bank_name=serializer['bank_name'].value)
            if bank.count() > 0:
                return Response({"message": "Bank with same name already there  "},
                                status=status.HTTP_208_ALREADY_REPORTED)
            else:
                bank = Bank(user=request.user, bank_name=serializer['bank_name'].value,
                            balance=serializer['balance'].value)
                bank.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)

    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]


class CreditCardList(generics.ListCreateAPIView):
    def get_queryset(self):
        return CreditCard.objects.filter(user=self.request.user)

    serializer_class = CreditCardSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = CreditCardSerializer(data=request.data)
        if serializer.is_valid():
            cc = CreditCard.objects.filter(user=request.user, credit_name=serializer['credit_name'].value)
            if cc.count() > 0:
                return Response({"message": "Data with same name already there  "},
                                status=status.HTTP_208_ALREADY_REPORTED)
            else:
                cc = CreditCard(user=request.user,
                                credit_name=serializer['credit_name'].value,
                                balance=serializer['balance'].value,
                                limit=serializer['limit'].value,
                                due=serializer['due'].value,
                                billing_date=serializer['billing_date'].value
                                )
                cc.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreditCardDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return CreditCard.objects.filter(user=self.request.user)

    serializer_class = CreditCardSerializer
    permission_classes = [IsAuthenticated]


class ProfileImage(generics.ListAPIView):
    def get_queryset(self):
        return Profile.objects.get_images(user_name=self.request.user)

    serializer_class = ProfileList
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ExpenseList(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        return ExpenseRecord.objects.filter(user=user)

    serializer_class = ExpenseRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'create_on': ['gte', 'lte', 'exact'],
                        "amount": ['gte', 'lte', 'exact'],
                        'account': ['exact'],
                        'category': ['exact'],
                        'sub_category': ['exact'],
                        }
    search_fields = ['note', ]
    ordering_fields = '__all__'
    ordering = ['-create_on']
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        return ExpenseRecord.objects.filter(user=user)

    queryset = ExpenseRecord.objects.all()
    serializer_class = ExpenseRecordSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]



class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class SubcategoryList(generics.ListCreateAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAuthenticated]

class SubcategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAuthenticated]

class SubcategoryAccountList(generics.ListCreateAPIView):
    serializer_class = AccountSubcategorySerializer

    def get_queryset(self):
        user = self.request.user
        return AccountSubcategory.objects.filter(user=user)
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class SubcategoryAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        return AccountSubcategory.objects.filter(user=user)
    serializer_class = AccountSubcategorySerializer
    permission_classes = [IsAuthenticated]



class CategoryAccountList(generics.ListCreateAPIView):
    serializer_class = AccountCategorySerializer

    def get_queryset(self):
        user = self.request.user
        return AccountCategory.objects.filter(user=user)

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class CategoryAccountdetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        return AccountCategory.objects.filter(user=user)
    serializer_class = AccountCategorySerializer
    permission_classes = [IsAuthenticated]


class ExpenseTransferList(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        return ExpenseTransfer.objects.filter(user=user)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'create_on': ['gte', 'lte', 'exact'],
                        "amount": ['gte', 'lte', 'exact'],

                        }
    search_fields = ['note', ]
    ordering_fields = '__all__'
    ordering = ['-create_on']
    serializer_class = ExpenseTransferSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ExpenseTransferDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        return ExpenseTransfer.objects.filter(user=user)

    serializer_class = ExpenseTransferSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class CreditCardExpenseList(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        return CreditCardRecord.objects.filter(user=user)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'created_on': ['gte', 'lte', 'exact'],
                        "amount": ['gte', 'lte', 'exact'],
                        }
    search_fields = ['note', ]
    ordering_fields = '__all__'
    ordering = ['-created_on']
    serializer_class = CreditCardRecordSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer: CreditCardRecordSerializer = CreditCardRecordSerializer(data=request.data)
        if serializer.is_valid():
            if serializer['type'].value == 'expense':
                ac = CreditCard.objects.get(pk=serializer['account'].value)
                if ac.balance < serializer['amount'].value:
                    return Response({"message": "balance is less "}, status=status.HTTP_204_NO_CONTENT)
                CC = CreditCardRecord.objects.add_record(user=request.user,
                                                         account=serializer['account'].value,
                                                         type="expense",
                                                         created_on=serializer['created_on'].value,
                                                         amount=serializer['amount'].value,
                                                         category=serializer['category'].value,
                                                         sub_category=serializer['sub_category'].value,
                                                         note=serializer['note'].value,
                                                         emi_total=serializer['emi_total'].value,
                                                         balance_remaning=serializer['account'].value
                                                         )
            else:
                CC = CreditCardRecord.objects.add_payment(user=request.user,
                                                          account=serializer['account'].value,
                                                          type="payment",
                                                          created_on=serializer['created_on'].value,
                                                          amount=serializer['amount'].value,
                                                          category=serializer['category'].value,
                                                          sub_category=serializer['sub_category'].value,
                                                          note=serializer['note'].value,
                                                          emi_total=0,
                                                          balance_remaning=0
                                                          )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreditCardExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        return CreditCardRecord.objects.filter(user=user)

    serializer_class = CreditCardRecordSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
