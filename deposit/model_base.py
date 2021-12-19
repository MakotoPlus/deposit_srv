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
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        super().save(*args, **kwargs)
