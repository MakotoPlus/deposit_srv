from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models

##########################################################
# ModelBaseクラス
# 全テーブルに登録されている更新日と更新者を設定する
#
# 更新日は、インスタンスプロパティに「u_date」が存在すれば設定する
# 更新者は、パラメータにセッションのユーザクラスをキーに「user」を指定すれば設定する
#           キーuserに指定されたオブジェクトの「username」プロパティを設定する
#
#           詳細動作確認の場合は、パラメータに'debug'キー（値はなんでもＯＫ）を設定すればコンソールに出力されます
#
# 使用例： a = ModelBase()
#          a.save( user=request.user)
##########################################################
class ModelBase(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # debug フラグ設定
        # パラメータに指定されている場合コンソールに情報出力
        self.debug = False
        if 'debug' in kwargs.keys():
            self.debug = True
        # 更新日設定処理
        self._set_udate( *args, **kwargs)
        # 更新者設定処理
        self._set_u_user( *args, **kwargs)
        # Call the "real" save() method.s
        #super(ModelBase, self).save(kwargs)
        super().save()



    #################################################################
    # 更新日設定処理
    # 自クラスのインスタンスメソッドに'u_date'が存在した場合はシステム日付を設定する
    # 
    # 更新日プロパティ(u_date)を持ってればシステム日付を設定する
    #################################################################
    def _set_udate(self, *args, **kwargs):
        if 'u_date' in self.__dict__.keys():
            if self.debug :
                print( 'u_date がクラスメソッドに定義されているのでシステム日時を設定')
            self.u_date = timezone.now()
        else:
            if self.debug :
                print( 'u_date がクラスメソッドに定義されていないのでシステム日時は未設定')



    #################################################################
    # 更新者設定処理
    # パラメータで指定された情報から更新者(u_user_id)を設定する
    # パラメータには、'User'で設定されていた場合にUser.uuid値を設定する
    #################################################################
    def _set_u_user(self, *args, **kwargs):
        # u_userが自プロパティに存在しない場合は終了
        selfKey = 'u_user_id'
        paramKey = 'User'
        primaryKeyID = 'uuid'
        
        #print( self.__dict__.keys())
        if selfKey not in self.__dict__.keys():
            if self.debug :
                print( '%s がクラスメソッドに定義されていない' % selfKey )
            return
        if self.debug :
            print( '%s がクラスメソッドに定義されている' % selfKey)

        # パラメータにセッション情報のユーザ情報が設定されているか確認する
        if paramKey not in kwargs.keys():
            if self.debug :
                print( 'パラメータにユーザ情報[%s]が設定されていない' % paramKey)
            return
        if self.debug :
            print( 'パラメータにユーザ情報[%s]が設定されている' % paramKey)
        user = kwargs[paramKey]
        if primaryKeyID not in user.__dict__.keys():
            if self.debug :
                print( 'パラメータ.ユーザ情報に[%s]プロパティが設定されていない' % primaryKeyID)
                return
        if self.debug :
            print( 'パラメータ.ユーザ情報に[%s]プロパティが設定されている' % primaryKeyID)
        # ユーザ情報にユーザ名プロパティがあれば設定
        self.u_user_id = user.uuid


#
# 以降テスト用
class TestModel(ModelBase):
    def __init__(self, *args, **kwargs):
        self.u_date = '初期値 日付'
        self.u_user = '初期値 ユーザ'


class RequestDmy():
    def __init__(self, *args, **kwargs):
        self.user = user_dmy()
        pass

class user_dmy():
    def __init__(self, *args, **kwargs):
        self.username = 'user_dmy USER TEST'
        #pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('test command')

        session_obj = RequestDmy()
        testmodel_record = TestModel()

        print( 'save()呼出し前情報' )
        if 'u_date' in testmodel_record.__dict__.keys():
            print( 'u_date=[%s]' % ( testmodel_record.u_date))
        if 'u_user' in testmodel_record.__dict__.keys():
            print( 'u_user[%s]' % ( testmodel_record.u_user))

        testmodel_record.save(user=session_obj.user, debug='true')

        print( 'save()呼出し後情報' )
        if 'u_date' in testmodel_record.__dict__.keys():
            print( 'u_date=[%s]' % ( testmodel_record.u_date))
        if 'u_user' in testmodel_record.__dict__.keys():
            print( 'u_user[%s]' % ( testmodel_record.u_user))
        print('test command end')

