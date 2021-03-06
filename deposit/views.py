
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
# ?????????????????????????????????ModelViewSet???????????????
class DepostBaseModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
    #
    # Pageing ?????????
    # URL?????????????????? no_page???????????????????????????Paging???Off??????????????????None?????????
    def paginate_queryset(self, queryset):
        if 'no_page' in self.request.query_params :
            return None
        return super().paginate_queryset(queryset)


#
# ?????????????????????????????????ModelViewSet???????????????
class DepositBaseReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    #
    # Pageing ?????????
    # URL?????????????????? no_page???????????????????????????Paging???Off??????????????????None?????????
    def paginate_queryset(self, queryset):
        if 'no_page' in self.request.query_params :
            return None
        return super().paginate_queryset(queryset)



#????????????????????????
class Tm_DepositGroupViewSet(DepostBaseModelViewSet):
    queryset = Tm_DepositGroup.objects.all()
    serializer_class = Tm_DepositGroupSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
    
#??????
class Tm_MoneyTypeViewSet(DepostBaseModelViewSet):
    queryset = Tm_MoneyType.objects.all()
    serializer_class = Tm_MoneyTypeSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)
#????????????
class Tm_DepositItemViewSet(DepostBaseModelViewSet):
    queryset = Tm_DepositItem.objects.all()
    serializer_class = Tm_DepositItemSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)


#????????????????????????????????????????????????????????????
class Tm_DepositItemListFilter(filters.FilterSet):
    delete_flag = filters.BooleanFilter(field_name="delete_flag")
    deposit_flag = filters.BooleanFilter(field_name="deposit_flag")

#????????????????????????????????????
class Tm_DepositItemListViewSet(DepostBaseModelViewSet):
    queryset = Tm_DepositItem.objects.all()
    filterset_class = Tm_DepositItemListFilter
    serializer_class = Tm_DepositItemListSerializer


#????????????
class Tt_SavingsViewSet(DepostBaseModelViewSet):
    queryset = Tt_Savings.objects.all()
    serializer_class = Tt_SavingsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)

#??????????????????????????????
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

#???????????????
class Tt_DepositViewSet(DepostBaseModelViewSet):
    queryset = Tt_Deposit.objects.all()
    serializer_class = Tt_DepositSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = Tt_DepositListFilter
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)

#???????????????????????????????????????
class Tt_AssetsListFilter(filters.FilterSet):
    delete_flag = filters.BooleanFilter(field_name="delete_flag")
    class Meta:
        model = Tt_Assets
        fields = {
            'insert_yyyymm' : ['lte','gte']
        }

#???????????????
class Tt_AssetsViewSet(DepostBaseModelViewSet):
    queryset = Tt_Assets.objects.all()
    serializer_class = Tt_AssetsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = Tt_AssetsListFilter
    def perform_create(self, serializer):
        serializer.save(u_user=self.request.user)

#
#???????????????????????????
#
# https://docs.djangoproject.com/en/4.0/ref/models/querysets/#bulk-create
# https://qiita.com/Utena-lotus/items/c7bde7f663cfc4aabff1
class Tt_AssetsBulkViewSet(generics.CreateAPIView):
    serializer_class = Tt_AssetsSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            #
            # ????????????????????????????????????????????????????????????????????????????????????None?????????????????????????????????
            # Serialize.is_Valid???????????????????????????????????????????????????
            kwargs["many"] = True
            records = kwargs.get("data")
            insert_yyyymm = records[0]['insert_yyyymm']
            logger.debug( f'insert_yyyymm=[{insert_yyyymm}]')
            assets_dataset_count = Tt_Assets.objects.filter(insert_yyyymm=insert_yyyymm).count()
            logger.debug( f'assets_dataset_count=[{assets_dataset_count}]')
            if assets_dataset_count > 0 :
                logger.info( f'assets_dataset_count=[{assets_dataset_count}]')
                logger.error( f'????????????????????????({insert_yyyymm})?????????????????????????????????????????????????????????????????????????????????')
                return None
            # u_user ?????????????????????
            for record in records:
                record["u_user"] = self.request.user.uuid
        return super(Tt_AssetsBulkViewSet, self).get_serializer(*args, **kwargs)

class AssetsPandasViewSet(PandasViewSet):
    '''
    ??????????????????Pivot???????????????    
    insert_yyyymm_from, insert_yyyymm_to????????????????????????????????????????????????    
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
    ?????????????????????????????????????????????????????????????????????View

    ????????????SQL:
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
        # ????????????
        # 1. ?????????????????????
        # 2. ??????????????????????????????????????????????????????????????????????????????
        # 3. ???????????????????????????????????????????????????????????????
        
        #-------------------------------------------------
        # 1. ?????????????????????
        #-------------------------------------------------
        insert_yyyymm_from = None
        insert_yyyymm_to = None
        if 'insert_yyyymm_from' in self.request.GET:
            insert_yyyymm_from = self.request.GET.get('insert_yyyymm_from')
        if 'insert_yyyymm_to' in self.request.GET:
            insert_yyyymm_to = self.request.GET.get('insert_yyyymm_to')

        #-------------------------------------------------
        # 2. ??????????????????????????????????????????????????????????????????????????????
        # ???????????????
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
        # FROM???TO ????????????
        if insert_yyyymm_from :
            records = records.filter(insert_yyyymm__gte=insert_yyyymm_from)
        if insert_yyyymm_to :
            records = records.filter(insert_yyyymm__lte=insert_yyyymm_to)


        #-------------------------------------------------
        # 3. ???????????????????????????????????????????????????????????????
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
    ???????????????????????????????????????View
    '''
    # Filter????????????????????????????????????????????????????????????
    # filterset_class = DepositSumaryViewFilter
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ['depositItem_key', 'insert_yyyymm']
    serializer_class = DepositItemDateSumarySerializer

    def get_queryset(self):
        # ????????????
        # 1. ?????????????????????
        # 2. ??????????????????????????????????????????????????????????????????
        # 3. ???????????????????????????
        
        #-------------------------------------------------
        # 1. ?????????????????????
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
        # 2. ??????????????????????????????????????????????????????????????????
        # 
        #    Filter??????????????????????????????????????????????????????????????????
        #-------------------------------------------------
        records = Tm_DepositItem.objects.filter(
            deposit_deposititem_key__delete_flag=False).select_related(
            'deposit_group_key').values('depositItem_key', 'depositItem_name', 
            insert_yyyymm=F('deposit_deposititem_key__insert_yyyymm')
            ).annotate(value=Sum(F('deposit_deposititem_key__deposit_value') * 
            F('deposit_deposititem_key__deposit_type'))).filter(
            value__isnull=False).order_by('depositItem_key','deposit_deposititem_key__insert_yyyymm')

        # ??????????????????????????????????????????????????????????????????
        if depositItem_keys :
            records = records.filter(depositItem_key__in=depositItem_keys)
        #
        # FROM ??????????????????????????????????????????????????????????????????????????????
        #if insert_yyyymm_from :
        #    records = records.filter(insert_yyyymm__gte=insert_yyyymm_from)
        if insert_yyyymm_to :
            records = records.filter(insert_yyyymm__lte=insert_yyyymm_to)

        # Order by?????? depositItem_key, insert_yyyymm????????????????????????
        # ????????????????????????????????????queryset ??? dict ?????????????????????

        #-------------------------------------------------
        # 3. ???????????????????????????
        #-------------------------------------------------
        results = []
        # ?????????????????????????????????????????????
        str_start_yyyymm = None
        for record in records:
            if (str_start_yyyymm == None) or (str_start_yyyymm > record['insert_yyyymm']):
                str_start_yyyymm = record['insert_yyyymm']
        # ????????????????????????
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
            # ??????????????????????????????????????? now_date??????????????????????????????????????????????????????????????????????????????????????????
            # ??????????????????
            #-----------------------------------------------------------------
            insert_yyyymm_date = dt.strptime(record['insert_yyyymm'] + '/01', '%Y/%m/%d')
            while (now_date < insert_yyyymm_date) :
                # ??????????????????????????????????????????
                d = now_date.strftime('%Y/%m')
                results.append({
                    'depositItem_key' : now_depositkey,
                    'depositItem_name': now_depositItem_name,
                    'insert_yyyymm': d,
                    'value' : now_sum_value
                });
                now_date = now_date + relativedelta(months=1)
            # ????????????
            now_sum_value += record['value']
            results.append({
                'depositItem_key' : now_depositkey,
                'depositItem_name': now_depositItem_name,
                'insert_yyyymm': record['insert_yyyymm'],
                'value' : now_sum_value
            })
            # ???????????????????????????
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
    ??????????????????????????????View
    records = Tt_Deposit.objects.values('insert_yyyymm').annotate(value=
    Sum(F('deposit_value') * F('deposit_type'))).filter(
    value__isnull=False).order_by('insert_yyyymm')
    '''
    # Filter????????????????????????????????????????????????????????????
    # filterset_class = DepositSumaryViewFilter
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ['depositItem_key', 'insert_yyyymm']
    serializer_class = DepositDateSumarySerializer

    # Order by?????? insert_yyyymm????????????????????????
    # ????????????????????????????????????queryset ??? dict ?????????????????????    
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
    ????????????????????????????????????

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

    # ????????????????????????
    pagination_class = LimitOffsetPagination
    # Sort??????????????????
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


#????????????????????????
class Tt_DepositListViewSet(DepositBaseReadOnlyModelViewSet):
    serializer_class = Tt_DepositListSerializer
    filterset_class = Tt_DepositListFilter
    # ????????????????????????
    pagination_class = LimitOffsetPagination
    # Sort??????????????????
    ordering_fields = ['insert_yyyymmdd', 'depositItem_key']
    ordering = ['insert_yyyymmdd', 'depositItem_key']
    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Tt_Deposit.objects.all().order_by('-insert_yyyymmdd','depositItem_key')
        return queryset


#????????????????????????
class Tt_SavingsListViewSet(DepositBaseReadOnlyModelViewSet):
    queryset = Tt_Savings.objects.all()
    serializer_class = Tt_SavingsListSerializer
    # ????????????????????????
    pagination_class = LimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Tt_Savings.objects.all()
        return queryset
    # def perform_create(self, serializer):
    #    serializer.save(u_user=self.request.user)

class DepositGroupSumaryList(DepositBaseReadOnlyModelViewSet):
    '''
    #???????????????????????????????????????

    ??????????????????????????????

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
    #???????????????????????????????????????

    ??????????????????????????????
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
    ??????????????????

    ??????????????????????????????

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
    ??????????????????

    ?????????????????????
    '''
    def list(self, request):
        queryset = Tt_Deposit.objects.filter(delete_flag=False).aggregate(value=Sum(F('deposit_type')*F('deposit_value')))
        serializer = DepositTotalSerializer(queryset)
        return Response(serializer.data)



# ???????????????????????????
class DepositBatch(APIView):
    #????????????????????????????????????Flase??????????????????????????????
    #savings_record = Tt_Savings.objects.filter(delete_flag=False).all()
    #serializer_class = Tt_SavingsBatchSerializer

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        try :
            logger.debug('DepositBatch_post::Start')
            logger.debug('request')
            logger.debug(request.data)
            # ?????????????????????
            batchSerializer = DepositBatchSerializer(data=request.data)
            if batchSerializer.is_valid() :
                logger.debug('is_valid::True')
                # ???????????????????????????
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
            logger.error('DepositBatch::????????????')
            logger.error(traceback.print_exc())            
            return Http404



#
# ?????????????????????????????????
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
            # Client????????????????????????PK?????????????????????????????????????????????????????????
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
        # ????????????????????????????????????????????????????????????????????????
        return Tt_Assets.objects.filter(
            insert_yyyymm=self.kwargs['insert_yyyymm'])

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        logger.debug('Tt_AssetsBulkUpdatesViewSet_post::Start')
        logger.debug('request')
        logger.debug(request.data)
    '''