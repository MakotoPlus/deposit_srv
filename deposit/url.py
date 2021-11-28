from rest_framework import routers
from .views import (Tm_DepositGroupViewSet,
    Tm_MoneyTypeViewSet, Tm_DepositItemViewSet,
    Tt_SavingsViewSet, Tt_DepositViewSet)


router = routers.DefaultRouter()
router.register(r'deposit_group', Tm_DepositGroupViewSet)
router.register(r'money_type', Tm_MoneyTypeViewSet)
router.register(r'deposit_item', Tm_DepositItemViewSet)
router.register(r'savings', Tt_SavingsViewSet)
router.register(r'deposit', Tt_DepositViewSet)
