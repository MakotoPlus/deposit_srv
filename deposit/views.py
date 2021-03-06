
from django.shortcuts import render
import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from pyparsing import Or

# Create your views here.
# import django_filters
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import permissions
from django.core.exceptions import ValidationError
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
    Tt_Deposit,
    Tt_Assets
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
    DepositItemDateSumarySerializer,
    Tt_AssetsSerializer,
    Tt_AssetsListSerializer,
    Tt_AssetsPandasSerializer,
    Tt_AssetsUpdateSerializer,
    AssetsGroupSumarySerializer,
)

from rest_pandas import PandasViewSet, PandasUnstackedSerializer
#from django_pivot.pivot import pivot

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


#預金項目リストボックス用フィルタークラス
class Tm_DepositItemListFilter(filters.FilterSet):
    delete_flag = filters.BooleanFilter(field_name="delete_flag")
    deposit_flag = filters.BooleanFilter(field_name="deposit_flag")

#預金項目リストボックス用
class Tm_DepositItemListViewSet(DepostBaseModelViewSet):
    queryset = Tm_DepositItem.objects.all()
    filterset_class = Tm_DepositItemListFilter
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

#資産トランフィルタークラス
class Tt_AssetsListFilter(filters.FilterSet):
    delete_flag = filters.BooleanFilter(field_name="delete_flag")
    class Meta:
        model = Tt_Assets
        fields = {
            'insert_yyyymm' : ['lte','gte']
        }

#資産トラン
class Tt_AssetsViewSet(DepostBaseModelViewSet):
    queryset = Tt_Assets.objects.all()
    serializer_class = Tt_AssetsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = Tt_AssetsListFilter
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)

#
#資産トラン一括登録
#
# https://docs.djangoproject.com/en/4.0/ref/models/querysets/#bulk-create
# https://qiita.com/Utena-lotus/items/c7bde7f663cfc4aabff1
class Tt_AssetsBulkViewSet(generics.CreateAPIView):
    serializer_class = Tt_AssetsSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            #
            # 新規作成のため既に同じ年月データが１件でも存在した場合はNoneを返すエラーしてしまう
            # Serialize.is_Validだとー出来そうにないのでここで記述
            kwargs["many"] = True
            records = kwargs.get("data")
            insert_yyyymm = records[0]['insert_yyyymm']
            logger.debug( f'insert_yyyymm=[{insert_yyyymm}]')
            assets_dataset_count = Tt_Assets.objects.filter(insert_yyyymm=insert_yyyymm).count()
            logger.debug( f'assets_dataset_count=[{assets_dataset_count}]')
            if assets_dataset_count > 0 :
                logger.info( f'assets_dataset_count=[{assets_dataset_count}]')
                logger.error( f'既に存在する年月({insert_yyyymm})の資産データを登録しようとしたため処理をエラーにします')
                return None
            # u_user の値を設定する
            for record in records:
                record["u_user"] = self.request.user.uuid
        return super(Tt_AssetsBulkViewSet, self).get_serializer(*args, **kwargs)

class AssetsPandasViewSet(PandasViewSet):
    '''
    資産トランのPivotデータ取得    
    insert_yyyymm_from, insert_yyyymm_toが設定されている場合は絞込も行う    
    '''
    queryset = Tt_Assets.objects.all().order_by('insert_yyyymm').reverse()
    serializer_class = Tt_AssetsPandasSerializer
    pandas_serializer_class = PandasUnstackedSerializer

    def get_queryset(self):
        #return super().get_queryset()
        insert_yyyymm_from = None
        insert_yyyymm_to = None
        if 'insert_yyyymm_from' in self.request.GET:
            insert_yyyymm_from = self.request.GET.get('insert_yyyymm_from')
        if 'insert_yyyymm_to' in self.request.GET:
            insert_yyyymm_to = self.request.GET.get('insert_yyyymm_to')
        records = Tt_Assets.objects.all().order_by('insert_yyyymm').reverse()
        if insert_yyyymm_from :
            records = records.filter(insert_yyyymm__gte=insert_yyyymm_from)
        if insert_yyyymm_to :
            records = records.filter(insert_yyyymm__lte=insert_yyyymm_to)
        return records;

class Tt_AssetsGroupSumaryViewSet(DepositBaseReadOnlyModelViewSet):
    '''
    資産グループ・日付単位のサマリーレコードを返すView

    イメージSQL:
    SELECT 
        "Tt_Assets"."insert_yyyymm"
        , "Tm_DepositItem"."deposit_group_key_id"
        , "Tm_DepositGroup"."deposit_group_name"
        , SUM(("Tt_Assets"."deposit_value" * "Tt_Assets"."deposit_type")) AS "sum_value" 
    FROM 
        "Tt_Assets" 
        INNER JOIN "Tm_DepositItem" ON ("Tt_Assets"."depositItem_key_id" = "Tm_DepositItem"."depositItem_key") 
        INNER JOIN "Tm_DepositGroup" ON ("Tm_DepositItem"."deposit_group_key_id" = "Tm_DepositGroup"."deposit_group_key") 
    GROUP BY 
        "Tt_Assets"."insert_yyyymm", "Tm_DepositItem"."deposit_group_key_id", "Tm_DepositGroup"."deposit_group_name"

    '''
    serializer_class = AssetsGroupSumarySerializer

    def get_queryset(self):
        # 処理概要
        # 1. パラメータ取得
        # 2. 資産トランから資産グループ・月単位のデータを取得する
        # 3. シリアライズ項目に合わせてい結果を格納する
        
        #-------------------------------------------------
        # 1. パラメータ取得
        #-------------------------------------------------
        insert_yyyymm_from = None
        insert_yyyymm_to = None
        if 'insert_yyyymm_from' in self.request.GET:
            insert_yyyymm_from = self.request.GET.get('insert_yyyymm_from')
        if 'insert_yyyymm_to' in self.request.GET:
            insert_yyyymm_to = self.request.GET.get('insert_yyyymm_to')

        #-------------------------------------------------
        # 2. 資産トランから資産グループ・月単位のデータを取得する
        # 参考サイト
        # https://note.crohaco.net/2014/django-aggregate/
        #-------------------------------------------------
        records = Tt_Assets.objects.prefetch_related(
                'depositItem_key__deposit_group_key__deposit_group_name',
                'depositItem_key__deposit_group_key'
            ).values(
                'insert_yyyymm'
                ,'depositItem_key__deposit_group_key'
                ,'depositItem_key__deposit_group_key__deposit_group_name'
            ).annotate(
                sum_value=Sum(
                    F('deposit_value') * 
                    F('deposit_type')
                )
            ).order_by('insert_yyyymm', 'depositItem_key__deposit_group_key')
        #
        # FROM、TO 絞込実施
        if insert_yyyymm_from :
            records = records.filter(insert_yyyymm__gte=insert_yyyymm_from)
        if insert_yyyymm_to :
            records = records.filter(insert_yyyymm__lte=insert_yyyymm_to)


        #-------------------------------------------------
        # 3. シリアライズ項目に合わせてい結果を格納する
        #    deposit_group_key
        #    deposit_group_name
        #    insert_yyyymm
        #    value
        #-------------------------------------------------
        results = []
        for record in records:
            results.append(
                {
                    'deposit_group_key': record['depositItem_key__deposit_group_key'],
                    'deposit_group_name' : record['depositItem_key__deposit_group_key__deposit_group_name'],
                    'insert_yyyymm' : record['insert_yyyymm'],
                    'value' : record['sum_value']
                }
            )
        return results

class DepositItemDateSumaryViewSet(DepositBaseReadOnlyModelViewSet):
    '''
    預金項目・日付単位サマリーView
    '''
    # Filterはモデルが無いと実装厳しそうなので諦める
    # filterset_class = DepositSumaryViewFilter
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ['depositItem_key', 'insert_yyyymm']
    serializer_class = DepositItemDateSumarySerializer

    def get_queryset(self):
        # 処理概要
        # 1. パラメータ取得
        # 2. 全ての預金トランを年月単位のデータを取得する
        # 3. 月毎に加算して行く
        
        #-------------------------------------------------
        # 1. パラメータ取得
        #-------------------------------------------------
        depositItem_keys = None
        insert_yyyymm_from = None
        insert_yyyymm_to = None
        if 'depositItem_key' in self.request.GET:
            depositItem_keys = self.request.GET.getlist('depositItem_key', None)
        if 'insert_yyyymm_from' in self.request.GET:
            insert_yyyymm_from = self.request.GET.get('insert_yyyymm_from')
        if 'insert_yyyymm_to' in self.request.GET:
            insert_yyyymm_to = self.request.GET.get('insert_yyyymm_to')

        #-------------------------------------------------
        # 2. 全ての預金トランを年月単位のデータを取得する
        # 
        #    Filterが利用できないのでここで絞込条件の設定を行う
        #-------------------------------------------------
        records = Tm_DepositItem.objects.filter(
            deposit_deposititem_key__delete_flag=False).select_related(
            'deposit_group_key').values('depositItem_key', 'depositItem_name', 
            insert_yyyymm=F('deposit_deposititem_key__insert_yyyymm')
            ).annotate(value=Sum(F('deposit_deposititem_key__deposit_value') * 
            F('deposit_deposititem_key__deposit_type'))).filter(
            value__isnull=False).order_by('depositItem_key','deposit_deposititem_key__insert_yyyymm')

        # 項目キー、年月が指定されていた場合更に絞込み
        if depositItem_keys :
            records = records.filter(depositItem_key__in=depositItem_keys)
        #
        # FROM は結果的に加算処理が必要なため絞込条件は後程実施する
        #if insert_yyyymm_from :
        #    records = records.filter(insert_yyyymm__gte=insert_yyyymm_from)
        if insert_yyyymm_to :
            records = records.filter(insert_yyyymm__lte=insert_yyyymm_to)

        # Order by句は depositItem_key, insert_yyyymmとなっているので
        # それに従い加算処理をしてqueryset の dict として生成する

        #-------------------------------------------------
        # 3. 月毎に加算して行く
        #-------------------------------------------------
        results = []
        # 開始日付と最大の日付を取得する
        str_start_yyyymm = None
        for record in records:
            if (str_start_yyyymm == None) or (str_start_yyyymm > record['insert_yyyymm']):
                str_start_yyyymm = record['insert_yyyymm']
        # 開始日の日付取得
        start_date = dt.strptime(str_start_yyyymm + '/01', '%Y/%m/%d')
        now_sum_value = 0
        now_depositkey = None
        for record in records:
            if ((now_depositkey == None) or (now_depositkey != record['depositItem_key'])):
                now_depositkey = record['depositItem_key']
                now_depositItem_name = record['depositItem_name']
                now_sum_value = 0
                now_date = start_date
            #-----------------------------------------------------------------
            # 現在の追加レコードの日付が now_dateと差があった場合は、差の期間は前の金額と同じデータを作成する
            # あーめんどう
            #-----------------------------------------------------------------
            insert_yyyymm_date = dt.strptime(record['insert_yyyymm'] + '/01', '%Y/%m/%d')
            while (now_date < insert_yyyymm_date) :
                # 年月の差分に同じ値を設定処理
                d = now_date.strftime('%Y/%m')
                results.append({
                    'depositItem_key' : now_depositkey,
                    'depositItem_name': now_depositItem_name,
                    'insert_yyyymm': d,
                    'value' : now_sum_value
                });
                now_date = now_date + relativedelta(months=1)
            # 金額加算
            now_sum_value += record['value']
            results.append({
                'depositItem_key' : now_depositkey,
                'depositItem_name': now_depositItem_name,
                'insert_yyyymm': record['insert_yyyymm'],
                'value' : now_sum_value
            })
            # 次のために年月加算
            now_date = insert_yyyymm_date + relativedelta(months=1)
        
        if insert_yyyymm_from :
            result_filter = [];
            for result in results:
                if result['insert_yyyymm'] >= insert_yyyymm_from:
                    result_filter.append(result)
            results = result_filter;
        return results




class DepositDateSumaryViewSet(DepositBaseReadOnlyModelViewSet):
    '''
    預金日付単位サマリーView
    records = Tt_Deposit.objects.values('insert_yyyymm').annotate(value=
    Sum(F('deposit_value') * F('deposit_type'))).filter(
    value__isnull=False).order_by('insert_yyyymm')
    '''
    # Filterはモデルが無いと実装厳しそうなので諦める
    # filterset_class = DepositSumaryViewFilter
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ['depositItem_key', 'insert_yyyymm']
    serializer_class = DepositDateSumarySerializer

    # Order by句は insert_yyyymmとなっているので
    # それに従い加算処理をしてqueryset の dict として生成する    
    # queryset =[]
    def get_queryset(self):
        queryset =[]
        now_sum_value = 0
        now_depositkey = None
        records = Tt_Deposit.objects.values('insert_yyyymm').annotate(value=
        Sum(F('deposit_value') * F('deposit_type'))).filter(
        value__isnull=False).order_by('insert_yyyymm')
        for record in records:
            now_sum_value += record['value']
            record['value'] = now_sum_value
            queryset.append(record)
        self.queryset = queryset
        return queryset
        #return super().get_queryset()

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

    def get_queryset(self):
        queryset = Tm_DepositItem.objects.filter(
            deposit_deposititem_key__delete_flag=False).select_related(
            'deposit_group_key').annotate(sum_value=Sum(F('deposit_deposititem_key__deposit_value') * 
            F('deposit_deposititem_key__deposit_type'))).filter(
            sum_value__isnull=False).order_by('deposit_group_key','depositItem_key')
        self.queryset = queryset
        return self.queryset
  
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
    serializer_class = DepositGroupSumarySerializer

    def get_queryset(self):
        queryset = Tm_DepositGroup.objects.filter(
            deposititem_deposit_group_key__deposit_deposititem_key__delete_flag=False
            ).annotate(sum_value=Sum(F('deposititem_deposit_group_key__deposit_deposititem_key__deposit_value') * 
            F('deposititem_deposit_group_key__deposit_deposititem_key__deposit_type'))
            ).filter(sum_value__isnull=False)
        self.queryset = queryset
        return self.queryset

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
    serializer_class = SavingGroupSumarySerializer

    def get_queryset(self):
        self.queryset = Tm_DepositGroup.objects.filter(
            deposititem_deposit_group_key__savings_deposititem_key__delete_flag=False
            ).annotate(sum_value=Sum(F('deposititem_deposit_group_key__savings_deposititem_key__deposit_value') * 
            F('deposititem_deposit_group_key__savings_deposititem_key__deposit_type'))
            ).filter(sum_value__isnull=False)
        return self.queryset
  
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
            logger.debug('DepositBatch_post::Start')
            logger.debug('request')
            logger.debug(request.data)
            # これ要るんか？
            batchSerializer = DepositBatchSerializer(data=request.data)
            if batchSerializer.is_valid() :
                logger.debug('is_valid::True')
                # 預金データ複数取得
                # serializer = Tt_SavingsBatchSerializer(records, many=True)
                insert_yyyymmdd = batchSerializer.data['insert_yyyymmdd']
                insert_yyyymm = batchSerializer.data['insert_yyyymm']
                memo = batchSerializer.data['memo']
                logger.debug('insert_yyyymmdd={0}'.format(insert_yyyymmdd))
                logger.debug('memo={0}'.format(memo))
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
                    logger.debug('Create Deposit')
                    deposit = Tt_Deposit.objects.create(**deposit_record)
                    logger.debug('Create Deposit.Save')
                    deposit.save()
                return Response(batchSerializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.debug('is_valid::False')
            return Response(batchSerializer.data, status=status.HTTP_400_BAD_REQUEST)
        except :
            import traceback
            logger.error('DepositBatch::例外発生')
            logger.error(traceback.print_exc())            
            return Http404



#
# 資産トラン一括更新処理
class Tt_AssetsBulkUpdatesViewSet(generics.UpdateAPIView):

    serializer_class = Tt_AssetsUpdateSerializer
    lookup_field = "assets_key"
    records = []
    def get_queryset(self, request_data):
        #return Tt_Assets.objects.all()
        logger.info('get_serializer')
        logger.info('data')
        logger.info(request_data)
        #return Tt_Assets.objects.filter(insert_yyyymm=insert_yyyymm)
        return Tt_Assets.objects.filter(insert_yyyymm=request_data[0]['insert_yyyymm'])

    def get_serializer(self, *args, **kwargs):
        logger.info( 'get_serializer')
        logger.info('data')
        logger.info(kwargs.get("data"))
        if isinstance(kwargs.get("data", {}), list):
            logger.info( 'isinstance')
            kwargs["many"] = True
            #
            # Clientからのデータは、PK値が設定されてこないのでここで設定する
            # self.records = kwargs.get("data")
            #logger.info('record')
            #logger.info(self.records)
            for record in self.records:
                dataSet = Tt_Assets.objects.filter(
                    insert_yyyymm=record['insert_yyyymm']
                ).filter(
                    depositItem_key=record['depositItem_key']
                )
                record['assets_key'] = dataSet[0].assets_key
                record["u_user"] = self.request.user.uuid
                logger.info('record')
                logger.info(record)
        return super(Tt_AssetsBulkUpdatesViewSet, self).get_serializer(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        # ids = self.validate_ids(request.data)
        # logger.info('request.data')
        # logger.info(request.data)
        logger.info('request.records')
        logger.info(self.records)

        self.records = request.data
        instances = self.get_queryset(request.data)
        serializer = self.get_serializer(
            instances, data=self.records, partial=False, many=True
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)
        

    def validate_ids(data, field="id", unique=True):
        if isinstance(data, list):
            id_list = [int(x[field]) for x in data]
            if unique and len(id_list) != len(set(id_list)):
                raise ValidationError("Multiple updates to a single {} found".format(field))
            return id_list
        return [data]

    ''''
    def get_queryset(self):
        # 更新対象のデータを全て抽出するデータセットを返す
        return Tt_Assets.objects.filter(
            insert_yyyymm=self.kwargs['insert_yyyymm'])

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        logger.debug('Tt_AssetsBulkUpdatesViewSet_post::Start')
        logger.debug('request')
        logger.debug(request.data)
    '''