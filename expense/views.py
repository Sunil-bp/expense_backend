from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

from rest_framework.response import Response
from rest_framework import status

from expense.serializers import BankSerializer, CreditCardSerializer
from django.contrib.auth.models import User
from users.models import  Profile
from expense.models import Subcategory,Category,Bank, CreditCard,\
    AccountCategory,AccountSubcategory,ExpenseRecord,ExpenseTransfer
from django.contrib.auth.models import User
from users.models import Profile
from users.serializers import  ProfileList
from expense.serializers  import SubcategorySerializer,CategorySerializer,\
    AccountCategorySerializer,AccountSubcategorySerializer,\
    ExpenseRecordSerializer,ExpenseTransferSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class BankList(generics.ListCreateAPIView):

    # def __init__(self):
    #     print("hello \n\n")
    #     return Response("gd", status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)
    # queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print(f"data is now {type(request.data)}")
        print(f"custom method to create {(self)} , {request}, {args}, {kwargs}")
        serializer = BankSerializer(data=request.data)
        print(f" serialised data  {serializer}")
        if serializer.is_valid():
            # serializer.save()
            print(serializer.data)
            bank = Bank.objects.filter(user=request.user,bank_name = serializer['bank_name'].value)
            if bank.count()>0:
                print("Data already there ")
                return Response({"message":"data already there  "}, status=status.HTTP_208_ALREADY_REPORTED)
            else:
                bank = Bank(user=request.user, bank_name=serializer['bank_name'].value,balance= serializer['balance'].value)
                bank.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class BankDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]

class CreditCardList(generics.ListCreateAPIView):
    print("Getting credit  card ")
    def get_queryset(self):
        return CreditCard.objects.filter(user=self.request.user)
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [IsAuthenticated]

class CreditCardDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return CreditCard.objects.filter(user=self.request.user)
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [IsAuthenticated]

class ProfileImage(generics.ListAPIView):
    def get_queryset(self):
        print(f" in querry set  {self} ")
        i = Profile.objects.get_images(user_name = self.request.user)
        print(i)
        return i
    # queryset = Profile.objects.all()
    serializer_class = ProfileList
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class ExpenseList(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        return ExpenseRecord.objects.filter(user = user)
    serializer_class = ExpenseRecordSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = {'create_on': ['gte', 'lte','exact'],
                        "amount":['gte', 'lte','exact'],
                        'account':['exact'],
                        'category': ['exact'],
                        'sub_category': ['exact'],
                        }
    search_fields =['note',]
    ordering_fields ='__all__'
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

class SubcategoryList(generics.ListCreateAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class SubcategoryAccountList(generics.ListCreateAPIView):
    serializer_class = AccountSubcategorySerializer
    def get_queryset(self):
        user = self.request.user
        return AccountSubcategory.objects.filter(user = user)

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class CategoryAccountList(generics.ListCreateAPIView):
    serializer_class = AccountCategorySerializer
    def get_queryset(self):
        user = self.request.user
        return AccountCategory.objects.filter(user = user)

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ExpenseTransferList(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        return ExpenseTransfer.objects.filter(user = user)

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
        return ExpenseTransfer.objects.filter(user = user)
    serializer_class = ExpenseTransferSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
