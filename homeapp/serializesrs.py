from rest_framework import serializers, request
from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import exceptions
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from .utils import check_email_or_phone
from .utils import send_email,send_phone_code


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)

    class Meta:
        model = Users
        fields = (
            'id',
            'auth_type',
            'auth_status'
        )
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}
        }

    # yaratilgan codni email yoki phonega yuboradi utildagi funksialar orqali
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_phone_code(user.phone_number, code)
            # send_phone_code(user.phone_number, code)
        user.save()
        return user

    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    # kiritilgan malumotni email yoki phone ekanligini tekshiradi
    @staticmethod
    def auth_validate(data):
        print(data)
        user_input = str(data.get('email_phone_number')).lower()
        input_type = check_email_or_phone(user_input)  # email or phone
        if input_type == "email":
            data = {
                "email": user_input,
                "auth_type": VIA_EMAIL
            }
        elif input_type == "phone":
            data = {
                "phone_number": user_input,
                "auth_type": VIA_PHONE
            }
        else:
            data = {
                'success': False,
                'message': "You must send email or phone number"
            }
            raise ValidationError(data)

        return data

    # email va phone takrorlanmasligi uchun validation
    def validate_email_phone_number(self, value):
        value = value.lower()
        if value and Users.objects.filter(email=value).exists():
            data = {
                "success": False,
                "message": "Bu email allaqachon ma'lumotlar bazasida bor"
            }
            raise ValidationError(data)
        elif value and Users.objects.filter(phone_number=value).exists():
            data = {
                "success": False,
                "message": "Bu telefon raqami allaqachon ma'lumotlar bazasida bor"
            }
            raise ValidationError(data)

        return value

    # malumot userga borishidan oldin uni ushlab qolib tokenni ham qoshib beradi
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())

        return data


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
