from django.shortcuts import render

# Create your views here.
# import django_filters
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import permissions

from django.contrib.auth.models import Group
from users.models import User
from users.serializers import UserSerializer, GroupSerializer

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
    Tm_DepositItemListSerializer,
    Tt_SavingsSerializer,
    Tt_DepositSerializer,
    Tt_DepositListSerializer,
    DepositItemReleatedSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



#預金項目グループ
class Tm_DepositGroupViewSet(viewsets.ModelViewSet):
    queryset = Tm_DepositGroup.objects.all()
    serializer_class = Tm_DepositGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
    
#金種
class Tm_MoneyTypeViewSet(viewsets.ModelViewSet):
    queryset = Tm_MoneyType.objects.all()
    serializer_class = Tm_MoneyTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
#預金項目
class Tm_DepositItemViewSet(viewsets.ModelViewSet):
    queryset = Tm_DepositItem.objects.all()
    serializer_class = Tm_DepositItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)

#預金項目リストボックス用
class Tm_DepositItemListViewSet(viewsets.ModelViewSet):
    queryset = Tm_DepositItem.objects.all()
    serializer_class = Tm_DepositItemListSerializer
    permission_classes = [permissions.IsAuthenticated]



#貯金設定
class Tt_SavingsViewSet(viewsets.ModelViewSet):
    queryset = Tt_Savings.objects.all()
    serializer_class = Tt_SavingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
#預金トラン
class Tt_DepositViewSet(viewsets.ModelViewSet):
    queryset = Tt_Deposit.objects.all()
    serializer_class = Tt_DepositSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)

#預金トランリスト
class Tt_DepositListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tt_Deposit.objects.all()
    serializer_class = Tt_DepositListSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Tt_Deposit.objects.all()
        return queryset
    # def perform_create(self, serializer):
    #    serializer.save(u_user=self.request.user)
