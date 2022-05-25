from genericpath import exists
from datetime import datetime, timezone
from rest_framework import serializers
from .models import (Tm_DepositGroup, 
    Tm_MoneyType, Tm_DepositItem, Tt_Savings, Tt_Deposit, Tt_Assets)
from django.core.exceptions import ValidationError
from django.db import IntegrityError

import logging

logger = logging.getLogger(__name__)

#from drf_dynamic_fields import DynamicFieldsMixin

#預金項目グループ
class Tm_DepositGroupSerializer(serializers.ModelSerializer):
    u_user = serializers.ReadOnlyField(source='u_user.username')
    class Meta:
        model = Tm_DepositGroup
        fields = [
            'deposit_group_key',
            'deposit_group_name',
            'deposit_flag',
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
            'deposit_flag',
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

#預金項目・日付単位サマリーView
class DepositItemDateSumarySerializer(serializers.Serializer):
    depositItem_key = serializers.IntegerField()
    depositItem_name = serializers.CharField(required=True, max_length=10)
    insert_yyyymm = serializers.CharField(required=False, max_length=10)
    #value = serializers.CharField(required=True, max_length=10)
    value = serializers.IntegerField()

#預金日付単位サマリーView
class DepositDateSumarySerializer(serializers.Serializer):
    insert_yyyymm = serializers.CharField(required=False, max_length=10)
    value = serializers.IntegerField()

# 資産トラン一括登録用シリアライザー
# https://qiita.com/Utena-lotus/items/c7bde7f663cfc4aabff1
class Tt_AssetsListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        tt_assets = [Tt_Assets(**item) for item in validated_data]
        Tt_Assets.objects.bulk_create(tt_assets)
        return tt_assets
        

# 資産トランシリアライザー
class Tt_AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tt_Assets
        fields = '__all__'
        list_serializer_class = Tt_AssetsListSerializer

# 資産トラン一括更新用シリアライザー
# https://levelup.gitconnected.com/really-fast-bulk-updates-with-django-rest-framework-43594b18bd75
class Tt_BulkAssetsUpdateListSerializer(serializers.ListSerializer):
    #def to_representation(self, instances):
    #    logger.info('to_representation--------')
    #    #logger.info(instances)
    #    #value = instances[0].value
    #    rep_list = []
    #    for instance in instances:
    #        rep_list.append(
    #            dict(
    #                assets_key=instance.pk,
    #                deposit_value=instance.deposit_value,
    #            )
    #        )
    #    return rep_list
    def update(self, instances, validated_data):
        #
        # instance を１つにずつ分解し処理する
        # Tt_AssetsUpdateSerializerのupdateメソッドを呼出して更新処理を行う。
        # 
        #logger.info('ListSerializer::update')
        #logger.info('validated_data')
        #logger.info(validated_data)
        #logger.info('ListSerializer::instance')
        #logger.info(instances)
        instance_hash = {index: instance for index, instance in enumerate(instances)}
        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)
        ]
        return result


# 資産トラン更新用シリアライザー
class Tt_AssetsUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):  
        '''
        1レコード分の資産トランの更新処理


        Parameters
        ----------------------------------------------
        instance : DataSet 更新対象の1レコード
        validated_data : 変更したいパラメータ内容(1レコード)

        Return
        ----------------------------------------------
        DataSet : 更新インスタンス
        '''
        logger.info('UpdateSerializer::update')
        #logger.info(validated_data)
        #logger.info(self._kwargs["data"])
        #logger.info(instance.depositItem_key)
        # レコードに更新値を設定
        instance.deposit_value = validated_data["deposit_value"]
        instance.u_user = validated_data["u_user"]
        instance.update_date = validated_data["update_date"]
        #logger.info(instance)
        instance.save()
        return instance

    class Meta:
        model = Tt_Assets
        fields = '__all__'
        read_only_fields = ('assets_key','depositItem_key', 'deposit_type', 'insert_yyyymmdd'
            , 'insert_yyyymm', 'delete_flag', 'memo')
        list_serializer_class = Tt_BulkAssetsUpdateListSerializer


# 資産 Pivotテーブルシリアライザー
#class Tt_AssetsAllPivotSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
class Tt_AssetsAllPivotSerializer(serializers.ModelSerializer):
    # insert_yyyymm 以外は動的な列なんだなこれ    
    def __init__(self, *args, **kwargs):
        # fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        self.filds.pop('insert_yyyymm')
        records = Tm_DepositItem.objects.all()
        for record in records:
            self.fields.pop(record.depositItem_key.toString())

class Tt_AssetsPandasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tt_Assets
        fields = ['depositItem_key', 'deposit_value', 'insert_yyyymm']
        pandas_index = ['insert_yyyymm']
        pandas_unstacked_header = ['depositItem_key']
