from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

from .views import (
    UserViewSet, GroupViewSet,
    Tm_DepositGroupViewSet, Tm_MoneyTypeViewSet, 
    Tm_DepositItemViewSet,  Tt_SavingsViewSet, 
    Tt_DepositViewSet, Tm_DepositItemListViewSet,
    Tt_DepositListViewSet,
    Tt_SavingsListViewSet,
    SavingGroupSumaryList,
    SavingsTotal,
    DepositBatch,
    DepositTotal,
    DepositGroupSumaryList,
    DepositSumaryViewSet,
    DepositDateSumaryViewSet,
    DepositItemDateSumaryViewSet,
    Tt_AssetsViewSet,
    Tt_AssetsBulkViewSet,
    AssetsPandasViewSet,
    Tt_AssetsBulkUpdatesViewSet,
    Tt_AssetsGroupSumaryViewSet,
    )

#from django.urls import path
#from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'deposit_item_list', Tm_DepositItemListViewSet, basename="deposit_item_list")
router.register(r'deposit_group', Tm_DepositGroupViewSet)
router.register(r'money_type', Tm_MoneyTypeViewSet)
router.register(r'deposit_item', Tm_DepositItemViewSet)
router.register(r'savings', Tt_SavingsViewSet)
router.register(r'deposit', Tt_DepositViewSet)
router.register(r'deposit_list', Tt_DepositListViewSet, basename="deposit_list")
router.register(r'savings_list', Tt_SavingsListViewSet, basename="savings_list")
router.register(r'saving_sumary_list', SavingGroupSumaryList, basename="saving_sumary_list")
router.register(r'deposit_groupsumary_list', DepositGroupSumaryList, basename="deposit_groupsumary_list")
router.register(r'deposit_sumary_list', DepositSumaryViewSet, basename="deposit_sumary_list")
router.register(r'savings_total', SavingsTotal, basename="savings_total")
router.register(r'deposit_total', DepositTotal, basename="deposit_total")
router.register(r'deposit_date_sumary_list', DepositDateSumaryViewSet, basename="deposit_date_sumary_list")
router.register(r'deposit_item_date_sumary_list', DepositItemDateSumaryViewSet, basename="deposit_item_date_sumary_list")
router.register(r'assets', Tt_AssetsViewSet, basename="assets")
router.register(r'assets_pandas', AssetsPandasViewSet, basename="assets_pandas")
router.register(r'assets_group_sumary_list', Tt_AssetsGroupSumaryViewSet, basename="assets_group_sumary_list")



urlpatterns = [
    #url(r'^savings_total', SavingsTotal.as_view(), name='savings_total'),
    url(r'^deposit_batch', DepositBatch.as_view(), name='deposit_batch'),
    url(r'^assets_bulk_update', Tt_AssetsBulkUpdatesViewSet.as_view(), name='assets_bulk_update'),   
    url(r'^assets_bulk', Tt_AssetsBulkViewSet.as_view(), name='assets_bulk'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
