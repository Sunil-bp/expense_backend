from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )
from expense.models import Bank, CreditCard
from expense.serializers import BankSerializer, CreditCardSerializer
from django.contrib.auth.models import User
from users.models import Profile

from django_filters.rest_framework import DjangoFilterBackend


class BankList(generics.ListCreateAPIView):
    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]

class BankDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]

class CreditCardList(generics.ListCreateAPIView):
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