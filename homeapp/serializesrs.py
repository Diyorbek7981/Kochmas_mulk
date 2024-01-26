from rest_framework.serializers import ModelSerializer
from .models import *


class HotelSerializer(ModelSerializer):
    class Meta:
        model = HomeModel
        fields = '__all__'


class PictureSerializer(ModelSerializer):
    class Meta:
        model = PictureModel
        fields = '__all__'
