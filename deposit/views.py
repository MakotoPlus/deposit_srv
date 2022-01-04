from django.shortcuts import render
import datetime
# Create your views here.
# import django_filters
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import permissions
from django.http import Http404
from django.contrib.auth.models import Group
from users.models import User
from users.serializers import UserSerializer, GroupSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from django.db.models import F

from deposit.models import (
    Tm_DepositGroup, 
    Tm_MoneyType,
    Tm_DepositItem,
    Tt_Savings,
    Tt_Deposit
)
from deposit.serializers import (
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
    SavingsTotalSerializer,
    Tt_SavingsBatchSerializer,
    DepositBatchSerializer,
    DepositTotalSerializer,
    DepositGroupSumarySerializer,
    DepositSumarySerializer,
    DepositDateSumarySerializer,
)

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters 
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status

import logging

logger = logging.getLogger(__name__)

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
class DepositBaseReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
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

#預金フィルタークラス
class Tt_DepositListFilter(filters.FilterSet):
    delete_flag = filters.BooleanFilter(field_name="delete_flag")
    depositItem_key = filters.ModelMultipleChoiceFilter(
        queryset=Tm_DepositItem.objects.all()
    )
    class Meta:
        model = Tt_Deposit
        fields = {
            'insert_yyyymmdd' : ['lte','gte']
        }

#預金トラン
class Tt_DepositViewSet(DepostBaseModelViewSet):
    queryset = Tt_Deposit.objects.all()
    serializer_class = Tt_DepositSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = Tt_DepositListFilter
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)

'''
# Filterはモデルが無いと実装厳しそうなので諦める
# 預金グループ単位サマリーフィルタークラス
#class DepositSumaryViewFilter(filters.FilterSet):
    #delete_flag = filters.BooleanFilter(field_name="delete_flag")
    depositItem_key = filters.ModelMultipleChoiceFilter(
        queryset=Tm_DepositItem.objects.all()
    )
    #class Meta:
    #    model = Tt_Deposit
    #    fields = {
    #        'insert_yyyymm' : ['lte','gte']
    #    }
'''

class DepositDateSumaryViewSet(DepositBaseReadOnlyModelViewSet):
    '''
    預金日付単位サマリーView
    '''
    records = Tm_DepositItem.objects.filter(
        deposit_deposititem_key__delete_flag=False).select_related(
        'deposit_group_key').values('depositItem_key', 'depositItem_name', 
        insert_yyyymm=F('deposit_deposititem_key__insert_yyyymm')
        ).annotate(value=Sum(F('deposit_deposititem_key__deposit_value') * 
        F('deposit_deposititem_key__deposit_type'))).filter(
        value__isnull=False).order_by('depositItem_key', 'deposit_deposititem_key__insert_yyyymm')

    # Order by句は depositItem_key, insert_yyyymmとなっているので
    # それに従い加算処理をしてqueryset の dict として生成する    
    queryset =[]
    now_sum_value = 0
    now_depositkey = None
    for record in records:
        if ((now_depositkey == None) or (now_depositkey != record['depositItem_key'])):
            now_depositkey = record['depositItem_key']
            now_sum_value = record['value']
        else :
            now_sum_value += record['value']
            record['value'] = now_sum_value
        queryset.append(record)

    # Filterはモデルが無いと実装厳しそうなので諦める
    # filterset_class = DepositSumaryViewFilter
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ['depositItem_key', 'insert_yyyymm']
    serializer_class = DepositDateSumarySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)




class DepositSumaryViewSet(DepositBaseReadOnlyModelViewSet):
    '''
    預金グループ単位サマリー

    {'sql': 'SELECT "Tm_DepositItem"."depositItem_key", 
    "Tm_DepositItem"."depositItem_name", "Tm_DepositItem"."deposit_group_key_id"
    , "Tm_DepositItem"."moneyType_key_id", "Tm_DepositItem"."savings_flag"
    , "Tm_DepositItem"."order_dsp", "Tm_DepositItem"."delete_flag", "Tm_DepositItem"."update_date"
    , "Tm_DepositItem"."u_user_id", SUM(("Tt_Deposit"."deposit_value" * "Tt_Deposit"."deposit_type")) 
    AS "sum_value", "Tm_DepositGroup"."deposit_group_key", "Tm_DepositGroup"."deposit_group_name"
    , "Tm_DepositGroup"."order_dsp", "Tm_DepositGroup"."delete_flag", "Tm_DepositGroup"."update_date"
    , "Tm_DepositGroup"."u_user_id" FROM "Tm_DepositItem" INNER JOIN "Tt_Deposit" 
    ON ("Tm_DepositItem"."depositItem_key" = "Tt_Deposit"."depositItem_key_id") 
    INNER JOIN "Tm_DepositGroup" ON (
    "Tm_DepositItem"."deposit_group_key_id" = "Tm_DepositGroup"."deposit_group_key") 
    WHERE "Tt_Deposit"."delete_flag" = 0 GROUP BY "Tm_DepositItem"."depositItem_key", 
    "Tm_DepositItem"."depositItem_name", "Tm_DepositItem"."deposit_group_key_id", 
    "Tm_DepositItem"."moneyType_key_id", "Tm_DepositItem"."savings_flag", 
    "Tm_DepositItem"."order_dsp", "Tm_DepositItem"."delete_flag", "Tm_DepositItem"."update_date", 
    "Tm_DepositItem"."u_user_id", "Tm_DepositGroup"."deposit_group_key", 
    "Tm_DepositGroup"."deposit_group_name", "Tm_DepositGroup"."order_dsp", 
    "Tm_DepositGroup"."delete_flag", "Tm_DepositGroup"."update_date", 
    "Tm_DepositGroup"."u_user_id" 
    HAVING SUM(("Tt_Deposit"."deposit_value" * "Tt_Deposit"."deposit_type")) 
    IS NOT NULL ORDER BY "Tm_DepositItem"."order_dsp" ASC LIMIT 21', 'time': '0.001'}
    '''
    serializer_class = DepositSumarySerializer
    #filterset_class = Tt_DepositListFilter

    # ページネーション
    pagination_class = LimitOffsetPagination
    # Sort項目限定設定
    ordering_fields = ['deposit_group_key', 'depositItem_key']
    ordering = ['deposit_group_key', 'depositItem_key']   
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Tm_DepositItem.objects.filter(
        deposit_deposititem_key__delete_flag=False).select_related(
        'deposit_group_key').annotate(sum_value=Sum(F('deposit_deposititem_key__deposit_value') * 
        F('deposit_deposititem_key__deposit_type'))).filter(
        sum_value__isnull=False).order_by('deposit_group_key','depositItem_key')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


#預金トランリスト
class Tt_DepositListViewSet(DepositBaseReadOnlyModelViewSet):
    serializer_class = Tt_DepositListSerializer
    filterset_class = Tt_DepositListFilter
    # ページネーション
    pagination_class = LimitOffsetPagination
    # Sort項目限定設定
    ordering_fields = ['insert_yyyymmdd', 'depositItem_key']
    ordering = ['insert_yyyymmdd', 'depositItem_key']
    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Tt_Deposit.objects.all().order_by('-insert_yyyymmdd','depositItem_key')
        return queryset


#貯金トランリスト
class Tt_SavingsListViewSet(DepositBaseReadOnlyModelViewSet):
    queryset = Tt_Savings.objects.all()
    serializer_class = Tt_SavingsListSerializer
    # ページネーション
    pagination_class = LimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Tt_Savings.objects.all()
        return queryset
    # def perform_create(self, serializer):
    #    serializer.save(u_user=self.request.user)

class DepositGroupSumaryList(DepositBaseReadOnlyModelViewSet):
    '''
    #預金グループサマリーリスト

    削除フラグデータ除外

    {'sql': 'SELECT "Tm_DepositGroup"."deposit_group_key", 
        "Tm_DepositGroup"."deposit_group_name", "Tm_DepositGroup"."order_dsp", 
        "Tm_DepositGroup"."delete_flag", "Tm_DepositGroup"."update_date", 
        "Tm_DepositGroup"."u_user_id", SUM(("Tt_Deposit"."deposit_value" 
        * "Tt_Deposit"."deposit_type")) AS "sum_value" FROM "Tm_DepositGroup" 
        INNER JOIN "Tm_DepositItem" ON ("Tm_DepositGroup"."deposit_group_key" = 
        "Tm_DepositItem"."deposit_group_key_id") INNER JOIN "Tt_Deposit" ON 
        ("Tm_DepositItem"."depositItem_key" = "Tt_Deposit"."depositItem_key_id") 
        WHERE "Tt_Deposit"."delete_flag" = 0 GROUP BY "Tm_DepositGroup".
        "deposit_group_key", "Tm_DepositGroup"."deposit_group_name", 
        "Tm_DepositGroup"."order_dsp", "Tm_DepositGroup"."delete_flag", 
        "Tm_DepositGroup"."update_date", "Tm_DepositGroup"."u_user_id" 
        HAVING SUM(("Tt_Deposit"."deposit_value" * "Tt_Deposit"."deposit_type")) 
        IS NOT NULL ORDER BY "Tm_DepositGroup"."order_dsp" ASC LIMIT 21'
        , 'time': '0.000'}
    '''
    queryset = Tm_DepositGroup.objects.filter(
        deposititem_deposit_group_key__deposit_deposititem_key__delete_flag=False
        ).annotate(sum_value=Sum(F('deposititem_deposit_group_key__deposit_deposititem_key__deposit_value') * 
        F('deposititem_deposit_group_key__deposit_deposititem_key__deposit_type'))
        ).filter(sum_value__isnull=False)
    serializer_class = DepositGroupSumarySerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class SavingGroupSumaryList(DepositBaseReadOnlyModelViewSet):
    '''
    #貯金グループサマリーリスト

    削除フラグデータ除外
    SELECT "Tm_DepositGroup"."deposit_group_key", "Tm_DepositGroup"."deposit_group_name", "Tm_DepositGroup"."order_dsp", "Tm_DepositGroup"."delete_flag", "Tm_DepositGroup"."update_date", "Tm_DepositGroup"."u_user_id", SUM(("Tt_Savings"."deposit_value" * "Tt_Savings"."deposit_type")) AS "sum_value" FROM "Tm_DepositGroup" INNER JOIN "Tm_DepositItem" ON ("Tm_DepositGroup"."deposit_group_key" = "Tm_DepositItem"."deposit_group_key_id") INNER JOIN "Tt_Savings" ON ("Tm_DepositItem"."depositItem_key" = "Tt_Savings"."depositItem_key_id") WHERE "Tt_Savings"."delete_flag" = 0 GROUP BY "Tm_DepositGroup"."deposit_group_key", "Tm_DepositGroup"."deposit_group_name", "Tm_DepositGroup"."order_dsp", "Tm_DepositGroup"."delete_flag", "Tm_DepositGroup"."update_date", "Tm_DepositGroup"."u_user_id" HAVING SUM(("Tt_Savings"."deposit_value" * "Tt_Savings"."deposit_type")) IS NOT NULL ORDER BY "Tm_DepositGroup"."order_dsp" 

    '''
    # permission_classes = [permissions.IsAuthenticated]
    #queryset = Tm_DepositGroup.objects.annotate(
    #    sum_value=Sum(F('deposititem_deposit_group_key__savings_deposititem_key__deposit_value') 
    #    * F('deposititem_deposit_group_key__savings_deposititem_key__deposit_type'))).filter(
    #    sum_value__isnull=False
    #)
    queryset = Tm_DepositGroup.objects.filter(
        deposititem_deposit_group_key__savings_deposititem_key__delete_flag=False
        ).annotate(sum_value=Sum(F('deposititem_deposit_group_key__savings_deposititem_key__deposit_value') * 
        F('deposititem_deposit_group_key__savings_deposititem_key__deposit_type'))
        ).filter(sum_value__isnull=False)

    serializer_class = SavingGroupSumarySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class SavingsTotal(viewsets.ViewSet):
    '''
    貯金総合計値

    削除フラグデータ除外

    '''
    #queryset = Tt_Savings.objects.aggregate(value=Sum(F('deposit_type')*F('deposit_value')))
    #serializer_class = SavingsTotalSerializer
    #def get(self, request, *args, **kwargs):
    #    return self.list(request, *args, **kwargs)
    #def get(self, request, format=None):
    def list(self, request):
        #queryset = Tt_Savings.objects.aggregate(value=Sum(F('deposit_type')*F('deposit_value')))
        queryset = Tt_Savings.objects.filter(delete_flag=False).aggregate(value=Sum(F('deposit_type')*F('deposit_value')))
        serializer = SavingsTotalSerializer(queryset)
        return Response(serializer.data)

class DepositTotal(viewsets.ViewSet):
    '''
    預金総合計値

    削除データ除外
    '''
    def list(self, request):
        queryset = Tt_Deposit.objects.filter(delete_flag=False).aggregate(value=Sum(F('deposit_type')*F('deposit_value')))
        serializer = DepositTotalSerializer(queryset)
        return Response(serializer.data)



# 預金データ一括登録
class DepositBatch(APIView):
    #貯金データで削除フラグがFlaseデータを全て取得する
    #savings_record = Tt_Savings.objects.filter(delete_flag=False).all()
    #serializer_class = Tt_SavingsBatchSerializer

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        try :
            logger.info('DepositBatch_post::Start')
            logger.info('request')
            logger.info(request.data)
            # これ要るんか？
            batchSerializer = DepositBatchSerializer(data=request.data)
            if batchSerializer.is_valid() :
                logger.info('is_valid::True')
                # 預金データ複数取得
                # serializer = Tt_SavingsBatchSerializer(records, many=True)
                insert_yyyymmdd = batchSerializer.data['insert_yyyymmdd']
                insert_yyyymm = batchSerializer.data['insert_yyyymm']
                memo = batchSerializer.data['memo']
                logger.info('insert_yyyymmdd={0}'.format(insert_yyyymmdd))
                logger.info('memo={0}'.format(memo))
                savings_records = Tt_Savings.objects.filter(delete_flag=False).all()
                d_now = datetime.datetime.now()
                for savings_record in savings_records:
                    deposit_record = {
                        'depositItem_key' : savings_record.depositItem_key,
                        'deposit_type' : savings_record.deposit_type,
                        'deposit_value' : savings_record.deposit_value,
                        'insert_yyyymmdd' : insert_yyyymmdd,
                        'insert_yyyymm' : insert_yyyymm,
                        'delete_flag' : False,
                        'memo' : memo,
                        'update_date' : d_now,
                        'u_user_id' : request.user.uuid,
                    }   
                    logger.info('Create Deposit')
                    deposit = Tt_Deposit.objects.create(**deposit_record)
                    logger.info('Create Deposit.Save')
                    deposit.save()
                return Response(batchSerializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.info('is_valid::False')
            return Response(batchSerializer.data, status=status.HTTP_400_BAD_REQUEST)
        except :
            import traceback
            logger.error('DepositBatch::例外発生')
            logger.error(traceback.print_exc())            
            return Http404




