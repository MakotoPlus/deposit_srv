from django.shortcuts import render

# Create your views here.
# import django_filters
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import permissions

from django.contrib.auth.models import Group
from users.models import User
from users.serializers import UserSerializer, GroupSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum


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
    Tt_SavingsListSerializer,
    SavingGroupSumarySerializer,
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


#
# このプロジェクトの共通ModelViewSet拡張クラス
class DepostBaseModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
    #
    # Pageing の切替
    # URLパラメータに no_pageが設定されていたらPagingをOffにするためにNoneを返す
    def paginate_queryset(self, queryset):
        if 'no_page' in self.request.query_params :
            return None
        return super().paginate_queryset(queryset)


#
# このプロジェクトの共通ModelViewSet拡張クラス
class DepostBaseReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    #
    # Pageing の切替
    # URLパラメータに no_pageが設定されていたらPagingをOffにするためにNoneを返す
    def paginate_queryset(self, queryset):
        if 'no_page' in self.request.query_params :
            return None
        return super().paginate_queryset(queryset)



#預金項目グループ
class Tm_DepositGroupViewSet(DepostBaseModelViewSet):
    queryset = Tm_DepositGroup.objects.all()
    serializer_class = Tm_DepositGroupSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
    
#金種
class Tm_MoneyTypeViewSet(DepostBaseModelViewSet):
    queryset = Tm_MoneyType.objects.all()
    serializer_class = Tm_MoneyTypeSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
#預金項目
class Tm_DepositItemViewSet(DepostBaseModelViewSet):
    queryset = Tm_DepositItem.objects.all()
    serializer_class = Tm_DepositItemSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)

#預金項目リストボックス用
class Tm_DepositItemListViewSet(DepostBaseModelViewSet):
    queryset = Tm_DepositItem.objects.all()
    serializer_class = Tm_DepositItemListSerializer


#貯金設定
class Tt_SavingsViewSet(DepostBaseModelViewSet):
    queryset = Tt_Savings.objects.all()
    serializer_class = Tt_SavingsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
#預金トラン
class Tt_DepositViewSet(DepostBaseModelViewSet):
    queryset = Tt_Deposit.objects.all()
    serializer_class = Tt_DepositSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)

#預金トランリスト
class Tt_DepositListViewSet(DepostBaseReadOnlyModelViewSet):
    queryset = Tt_Deposit.objects.all()
    serializer_class = Tt_DepositListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Tt_Deposit.objects.all()
        return queryset
    # def perform_create(self, serializer):
    #    serializer.save(u_user=self.request.user)

#貯金トランリスト
class Tt_SavingsListViewSet(DepostBaseReadOnlyModelViewSet):
    queryset = Tt_Savings.objects.all()
    serializer_class = Tt_SavingsListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Tt_Savings.objects.all()
        return queryset
    # def perform_create(self, serializer):
    #    serializer.save(u_user=self.request.user)

#貯金グループサマリーリスト
@api_view(['GET'])
def saving_group_samary_list(request, format=None):
    if request.method == 'GET':
        queryset = Tm_DepositGroup.objects.annotate(
            sum_value=Sum(
                'deposititem_deposit_group_key__savings_deposititem_key__deposit_value')
        ).filter(sum_value__isnull=False)
        serializer = SavingGroupSumarySerializer(queryset, many=True)
        return Response(serializer.data)
