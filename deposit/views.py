from django.shortcuts import render

# Create your views here.
# import django_filters
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import permissions

from .models import (
    Tm_DepositGroup, 
    Tm_MoneyType,
    Tm_DepositItem,
    Tt_Savings,
    Tt_Deposit
)
from .serializers import (
    Tm_DepositGroupSerializer,
    Tm_MoneyTypeSerializer,
    Tm_DepositItemSerializer,
    Tt_SavingsSerializer,
    Tt_DepositSerializer,
)


#預金項目グループ
class Tm_DepositGroupViewSet(viewsets.ModelViewSet):
    queryset = Tm_DepositGroup.objects.all()
    serializer_class = Tm_DepositGroupSerializer
#金種
class Tm_MoneyTypeViewSet(viewsets.ModelViewSet):
    queryset = Tm_MoneyType.objects.all()
    serializer_class = Tm_MoneyTypeSerializer
#預金項目
class Tm_DepositItemViewSet(viewsets.ModelViewSet):
    queryset = Tm_DepositItem.objects.all()
    serializer_class = Tm_DepositItemSerializer
#貯金設定
class Tt_SavingsViewSet(viewsets.ModelViewSet):
    queryset = Tt_Savings.objects.all()
    serializer_class = Tt_SavingsSerializer
#預金トラン
class Tt_DepositViewSet(viewsets.ModelViewSet):
    queryset = Tt_Deposit.objects.all()
    serializer_class = Tt_DepositSerializer
