from rest_framework import serializers, request
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

    # coments = serializers.SerializerMethodField(
    #     method_name="get_coments")
    #
    # def get_coments(self, obj):
    #     coments = obj.comments.filter(Parent=None)
    #     serializer = CommentListSerializers(coments, many=True)
    #     if serializer.data == []:
    #         return None
    #     return serializer.data

    class Meta:
        model = HomeModel
        fields = ['name', 'type', 'home_type', 'count_rooms', 'description', 'price', 'location', 'owner', 'created',
                  'updated']


class PictureSerializer(ModelSerializer):
    class Meta:
        model = PictureModel
        fields = ['pic', 'home', 'created', 'updated']


class TypeSerializer(ModelSerializer):
    class Meta:
        model = TypeModel
        fields = ['name', 'created', 'updated']


class HomeTypeSerializer(ModelSerializer):
    class Meta:
        model = HomeTypeModel
        fields = ['name', 'created', 'updated']


# coment u-n
class CommentListSerializers(ModelSerializer):
    Replies = serializers.SerializerMethodField()
    Author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    # Author = serializers.ReadOnlyField(
    #     source='Author.username')

    def get_Replies(self, obj):
        if obj.any_children:
            return CommentListSerializers(obj.children(), many=True).data

    # def get_Author(self, obj):
    #     return obj.Author.username

    class Meta:
        model = CommentModel
        fields = ("Author", "CreatedDate", "ModifiedDate", "Post", "Parent", "CommentText", "Replies")
