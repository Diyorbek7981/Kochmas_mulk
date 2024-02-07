from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *


class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class SearchSerializer(ModelSerializer):
    class Meta:
        model = SearchModel
        fields = '__all__'


class HomeSerializer(ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault())  # user mizni yashirib unga aktiv bo'lgan foydalanuvchini o'rnatish uchun
    owner = serializers.ReadOnlyField(
        source='owner.username')  # avtor maydoni yaratib unga userni qiymatini beramiz get requestda ko'rib turish uchun

    class Meta:
        model = HomeModel
        fields = ['name', 'type', 'home_type', 'count_rooms', 'description', 'price', 'location', 'owner', 'created',
                  'updated']


class PictureSerializer(ModelSerializer):
    class Meta:
        model = PictureModel
        fields = '__all__'


class TypeSerializer(ModelSerializer):
    class Meta:
        model = TypeModel
        fields = '__all__'


class HomeTypeSerializer(ModelSerializer):
    class Meta:
        model = HomeTypeModel
        fields = '__all__'
