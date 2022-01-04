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
            'deposititem_deposit_group_key',
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
            'delete_flag',
            'update_date',
            'u_user',
        ]


#貯金データ一括登録用
class Tt_SavingsBatchSerializer(serializers.ModelSerializer):
    # depositItem_key = Tm_DepositItemSerializer()
    #u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tt_Savings
        fields = [
            'savings_key',
            'depositItem_key',
            'deposit_type',
            'deposit_value',
            'delete_flag',
            'update_date',
            'u_user',
        ]


#預金トラン
class Tt_DepositSerializer(serializers.ModelSerializer):
    # depositItem_key = Tm_DepositItemSerializer()
    u_user = serializers.ReadOnlyField(source='u_user.username')
    # 空文字,Nullを許容する
    memo = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    class Meta:
        model = Tt_Deposit
        fields = [
            'deposit_key',
            'depositItem_key',
            'deposit_type',
            'deposit_value',
            'insert_yyyymmdd',
            'insert_yyyymm',
            'memo',
            'delete_flag',
            'update_date',
            'u_user',
        ]

# 貯金/預金トランリスト用の預金項目
class DepositItemReleatedSerializer(serializers.ModelSerializer):
    deposit_group_name = serializers.ReadOnlyField(source='deposit_group_key.deposit_group_name')
    moneyType_name = serializers.ReadOnlyField(source='moneyType_key.moneyType_name')
    # u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tm_DepositItem
        fields = [
            'depositItem_key',
            'depositItem_name',
            'deposit_group_key',
            'deposit_group_name',
            'moneyType_name',
            'savings_flag',
        ]


# 預金トランリスト
class Tt_DepositListSerializer(serializers.ModelSerializer):
    depositItem_key = DepositItemReleatedSerializer()
    u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tt_Deposit
        fields = [
            'deposit_key',
            'depositItem_key', 
            'deposit_type',
            'deposit_value',
            'insert_yyyymmdd',
            'insert_yyyymm',
            'memo',
            'delete_flag',
            'update_date',
            'u_user',
        ]

# 貯金設定リスト表示用
class Tt_SavingsListSerializer(serializers.ModelSerializer):
    u_user = serializers.ReadOnlyField(source='u_user.username')
    depositItem_key = DepositItemReleatedSerializer()
    class Meta:
        model = Tt_Savings
        fields = [
            'savings_key',
            'depositItem_key', 
            'deposit_type',
            'deposit_value',
            'delete_flag',
            'update_date',
            'u_user',
        ]

#貯金グループリスト表示用
class SavingGroupSumarySerializer(serializers.Serializer):
    deposit_group_key = serializers.IntegerField()
    deposit_group_name = serializers.CharField(required=False, allow_blank=True, max_length=40)
    #deposit_group_value = serializers.IntegerField()
    order_dsp = serializers.IntegerField()
    sum_value = serializers.IntegerField()

#預金項目グループリスト表示用
class DepositSumarySerializer(serializers.Serializer):
    deposit_group_key = Tm_DepositGroupSerializer()
    #deposit_group_name = serializers.CharField(required=False, allow_blank=True, max_length=40)
    depositItem_key = serializers.IntegerField()
    depositItem_name = serializers.CharField(required=False, allow_blank=True, max_length=40)
    order_dsp = serializers.IntegerField()
    sum_value = serializers.IntegerField()

#預金グループリスト表示用
class DepositGroupSumarySerializer(serializers.Serializer):
    deposit_group_key = serializers.IntegerField()
    deposit_group_name = serializers.CharField(required=False, allow_blank=True, max_length=40)
    #deposit_group_value = serializers.IntegerField()
    order_dsp = serializers.IntegerField()
    sum_value = serializers.IntegerField()

#貯金総合計値用
class SavingsTotalSerializer(serializers.Serializer):
    value = serializers.IntegerField()

#預金総合計値用
class DepositTotalSerializer(serializers.Serializer):
    value = serializers.IntegerField()


# 預金データ登録シリアライザー
class DepositBatchSerializer(serializers.Serializer):
    insert_yyyymmdd = serializers.CharField(required=True, max_length=10)
    insert_yyyymm = serializers.CharField(required=True, max_length=7)
    memo = serializers.CharField(max_length=1024)

#預金日付単位サマリーView
class DepositDateSumarySerializer(serializers.Serializer):
    depositItem_key = serializers.IntegerField()
    depositItem_name = serializers.CharField(required=True, max_length=10)
    insert_yyyymm = serializers.CharField(required=False, max_length=10)
    #value = serializers.CharField(required=True, max_length=10)
    value = serializers.IntegerField()
