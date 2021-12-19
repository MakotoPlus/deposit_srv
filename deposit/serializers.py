from rest_framework import serializers
from .models import (Tm_DepositGroup, 
                Tm_MoneyType, Tm_DepositItem, Tt_Savings, Tt_Deposit)


#預金項目グループ
class Tm_DepositGroupSerializer(serializers.ModelSerializer):
    u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tm_DepositGroup
        fields = [
            'deposit_group_key',
            'deposit_group_name',
            'order_dsp',
            'delete_flag',
            'update_date',
            'u_user',
        ]

#金種
class Tm_MoneyTypeSerializer(serializers.ModelSerializer):
    u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tm_MoneyType
        fields = [
            'moneyType_key',
            'moneyType_name',
            'delete_flag',
            'update_date',
            'u_user',
        ]

#預金項目
class Tm_DepositItemSerializer(serializers.ModelSerializer):
    #monyType_key = serializers.ReadOnlyField(source='moneyType_key.moneyType_name')
    #monyType_key = serializers.ReadOnlyField(source='moneyType_key.moneyType_name')
    u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tm_DepositItem
        fields = [
            'depositItem_key',
            'depositItem_name',
            'deposit_group_key',
            'moneyType_key',
            'savings_flag',
            'order_dsp',
            'delete_flag',
            'update_date',
            'u_user',
        ]
#預金項目リストボックス用        
class Tm_DepositItemListSerializer(serializers.ModelSerializer):
    deposit_group_key = Tm_DepositGroupSerializer()
    moneyType_key = Tm_MoneyTypeSerializer()
    u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tm_DepositItem
        fields = [
            'depositItem_key',
            'depositItem_name',
            'deposit_group_key',
            'moneyType_key',
            'savings_flag',
            'order_dsp',
            'delete_flag',
            'update_date',
            'u_user',
        ]

#貯金設定
class Tt_SavingsSerializer(serializers.ModelSerializer):
    # depositItem_key = Tm_DepositItemSerializer()
    u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tt_Savings
        fields = [
            'savings_key',
            'depositItem_key',
            'deposit_type',
            'deposit_value',
            'order_dsp',
            'delete_flag',
            'update_date',
            'u_user',
        ]

#預金トラン
class Tt_DepositSerializer(serializers.ModelSerializer):
    # depositItem_key = Tm_DepositItemSerializer()
    u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tt_Deposit
        fields = [
            'deposit_key',
            'depositItem_key',
            'deposit_type',
            'deposit_value',
            'insert_yyyymmdd',
            'memo',
            'delete_flag',
            'update_date',
            'u_user',
        ]
