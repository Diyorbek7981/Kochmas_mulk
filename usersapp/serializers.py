from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from .utility import send_email, send_phone_code, check_email_or_phone


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

    # yaratilgan codni email yoki phonega yuboradi utildagi funksialar orqali ----------->

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_phone_code(user.phone_number, code)
        user.save()
        return user

    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    # kiritilgan malumotni email yoki phone ekanligini tekshiradi --------------------->
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

    # email va phone takrorlanmasligi uchun validation ---------------------->

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

    # malumot userga borishidan oldin uni ushlab qolib tokenni ham qoshib beradi --------------->

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())

        return data


# Bazaga saqlangan tasodifiy username va paswordni ozgartirish ----------------------------->
class ChangeUserSerializer(serializers.Serializer):  # serializers.Serializer va serializers.ModelSerializer da farq bor
    first_name = serializers.CharField(write_only=True, required=True)
    # write_only - ushbu satrni bazaga kiritish uchun read_only - faqat oqish uchun (bazaga saqlanmaydi)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        if password != confirm_password:  # parol va tasdiqlash parolni tekshiradi
            data = {
                "message": "Parol va tasdiqlash parolingiz birxil emas"
            }
            raise ValidationError(data)

        if password:
            validate_password(password)  # passwordni validatsiyadan o'tkazadi (bu tayyor metod)
            validate_password(confirm_password)

        return data

    def validate_username(self, username):  # usernamega validatsiya berish
        if len(username) < 5 or len(username) > 30:
            data = {
                "message": "Usernameda minimum 5 ta maxsimum 30 ta belgi bo'lishi kerak"
            }
            raise ValidationError(data)

        if username.isdigit():
            data = {
                "message": "User name raqmlardan tashkil topmasligi kerak"
            }
            raise ValidationError(data)
        return username

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get('first_name', instance.first_name)
        # *** bu userni kiritgan first nameni oladi agar u bolmasa instance orqali malumotlar bazasidagini oladi
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.username = validated_data.get('username', instance.username)

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
            # parol kiritilgan bolsa set_password orqali heshlab beradi
        if instance.auth_status == CODE_VERIFIED:  # userni statusini ozgartiradi
            instance.auth_status = DONE

        instance.save()
        return instance
