from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    UserViewSet, GroupViewSet,
    Tm_DepositGroupViewSet, Tm_MoneyTypeViewSet, 
    Tm_DepositItemViewSet,  Tt_SavingsViewSet, 
    Tt_DepositViewSet, Tm_DepositItemListViewSet,
    Tt_DepositListViewSet)

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
