from rest_framework import serializers
from django.contrib.auth.models import Group
from users.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'url', 'username', 'email', 'groups', 'last_name', 'first_name', 'is_staff', 'is_active']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
