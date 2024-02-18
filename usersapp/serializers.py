from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import update_last_login
from rest_framework.generics import get_object_or_404
from .models import *
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from .utility import send_email, send_phone_code, check_email_or_phone, check_user_type
from django.contrib.auth import authenticate


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

        if instance.auth_status == NEW:  # userni statusini tekshiramiz
            data = {
                "message": "Siz hali verifikatsiadan o'tmagansiz"
            }
            raise ValidationError(data)

        elif instance.auth_status == CODE_VERIFIED:  # user statusini o'zgartiradi
            instance.auth_status = DONE

        instance.save()
        return instance


# Rasm yuklash uchun ----------------------------------------------------------->
class ChangeUserPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=[
        'jpg', 'jpeg', 'png', 'heic', 'heif'
    ])])

    def update(self, instance, validated_data):
        photo = validated_data.get('photo')

        if photo and instance.auth_status in [DONE, PHOTO_DONE]:  # rasm borligini va statusi tekshiriladi
            instance.photo = photo
            instance.auth_status = PHOTO_DONE
            instance.save()

        else:
            data = {
                "message": "Siz hali o'zingiz haqingizdagi malumotlarni kiritmadingiz "
            }
            raise ValidationError(data)

        return instance


# Login qilish ucun --------------------------------------------------------------->
class LoginSerializer(TokenObtainPairSerializer):

    def __init__(self, request=None, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['userinput'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(required=False, read_only=True)

    # check_user_type orqali malumotni aniqlab olamiz va inputni user_inputga o'zlashtiramiz --------------->
    def auth_validate(self, data):
        user_input = data.get('userinput')  # username email yoki telefon raqam bilan kirish mumkun
        if check_user_type(user_input) == 'username':
            username = user_input

        elif check_user_type(user_input) == 'email':
            user = self.get_user(
                email__iexact=user_input)  # user get_user method orqali user o'zgartiruvchiga biriktirildi
            # email__iexact bu email boshqacharoq kiritilgadaham uni qabul qiladi  Anora@gmail.com   -> anOra@gmail.com
            username = user.username

        elif check_user_type(user_input) == 'phone':
            user = self.get_user(phone_number=user_input)
            username = user.username

        else:
            data = {
                'success': False,
                'message': "Siz email, username yoki telefon raqami jonatishingiz kerak"
            }
            raise ValidationError(data)

        authentication_kwargs = {
            self.username_field: username,
            'password': data['password']  # kiritilgan username va pasvordni olish u-n
        }

        # user statusi tekshiriladi --------------------------------------------->
        current_user = Users.objects.filter(
            username__iexact=username).first()  # noto'g'ri username kiritilsa filter None qiymat qaytaradi

        if current_user is not None and current_user.auth_status in [NEW, CODE_VERIFIED]:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Siz royhatdan toliq otmagansiz!"
                }
            )

        user = authenticate(**authentication_kwargs)
        if user is not None:
            self.user = user
        else:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Kiritilgan parol yoki username xato. Tekshirib qayta urinib koring "
                }
            )

    def validate(self, data):  # userni inputini va statusini tekshirib malumotga data qaytaradi
        self.auth_validate(data)
        if self.user.auth_status not in [DONE]:
            raise PermissionDenied("Siz login qila olmaysiz. Ruxsatingiz yoq")
        data = self.user.token()
        data['auth_status'] = self.user.auth_status
        data['full_name'] = self.user.full_name
        return data

    # userni aniqlab olib uni auth_validatega yuboramiz----------->
    def get_user(self, **kwargs):
        users = Users.objects.filter(**kwargs)
        if not users.exists():
            raise ValidationError(
                {
                    "message": "Active accaunt topilmadi"
                }
            )
        return users.first()


# Mobil va Frontent dasturchilar uchun kerak (Acses tokeni yangilab beradi (hali muddati bor bo'lsaham))  ------------------------------------------------------->
class LoginRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(Users, id=user_id)
        update_last_login(None, user)
        return data


# Userni Logout qilish uchun ---------------------------------------------------------------------------------->
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
