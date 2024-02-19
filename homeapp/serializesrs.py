from rest_framework import serializers, request
from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework.exceptions import ValidationError


class SearchSerializer(ModelSerializer):
    class Meta:
        model = SearchModel
        fields = '__all__'


class HomeSerializer(ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault())  # user mizni yashirib unga aktiv bo'lgan foydalanuvchini o'rnatish uchun

    class Meta:
        model = HomeModel
        fields = ['type', 'home_type', 'location', 'count_rooms', 'area', 'floor', 'building_floor', 'repair',
                  'building_material', 'price', 'description', 'comforts', 'owner', 'created',
                  'updated']


class PictureSerializer(ModelSerializer):
    pic = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=[
        'jpg', 'jpeg', 'png', 'heic', 'heif'
    ])])

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

# coment u-n ---------------------------->
# class CommentListSerializers(ModelSerializer):
#     Replies = serializers.SerializerMethodField()
#     Author = serializers.HiddenField(
#         default=serializers.CurrentUserDefault())
#
#     # Author = serializers.ReadOnlyField(
#     #     source='Author.username')
#
#     def get_Replies(self, obj):
#         if obj.any_children:
#             return CommentListSerializers(obj.children(), many=True).data
#
#     # def get_Author(self, obj):
#     #     return obj.Author.username
#
#     class Meta:
#         model = CommentModel
#         fields = ("Author", "CreatedDate", "ModifiedDate", "Post", "Parent", "CommentText", "Replies")
