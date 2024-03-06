from rest_framework import generics, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.exceptions import ObjectDoesNotExist
from .utility import send_email, send_phone_code, check_email_or_phone
from homeapp.permissions import *
from homeapp.pagination import *


# Create your views here.

# Email yoki phoneni aniqlab kode jo'natadi ------------------------------------------------------------------>
class CreateUserView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]  # hechqanday imkoniyatlarni cheklamaslik u-n


# Codni Tekshirish --------------------------------------------------------------------------------------->
class VerifyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user  # user ->
        code = self.request.data.get('code')  # 4083

        self.check_verify(user, code)  # pastdagi metod orqali tekshiradi (check_verify)
        return Response(
            data={
                "success": True,  # quyidagi malumotlarni bekentga qaytaradi
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token']
            }
        )

    # tasdiqlash kodini togri va yaroqliligini tekshiradi----------------------------------->
    @staticmethod
    def check_verify(user, code):  # 12:03 -> 12:05 => expiration_time=12:05   12:04
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)

        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        else:
            verifies.update(
                is_confirmed=True)  # is_confirmed Truega ozgaradi (shu codni yana tasdiqlamoqchi bolsak check_verify ruhsat bermasligi u-n)

        if user.auth_status in [NEW, FORGET_PASS]:  # statusi o'zgartiriladi
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


# tasdiqlash kodini qayta olish uchun ----------------------------------------------------------------------------->
class GetNewVerification(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.chesck_verification(user)

        if user.auth_type == VIA_EMAIL:  # validatsiya ishlamasa yangi code yaratib userga boshqatan yuborish
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone_number, code)
            # send_phone_code(user.phone_number, code)
        else:
            data = {
                "message": "Email yoki telefon raqami noto'g'ri"
            }
            raise ValidationError(data)

        return Response(
            {
                "success": True,
                "message": "Tasdiqlash kodingiz qaytadan yuborildi",
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token']
            }
        )

    @staticmethod
    def chesck_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():  # verifikatsiya Kodi muddati tugamagan bolsa ------>
            data = {
                "message": "Kodingiz hali ishlatish uchun yaroqli. Email yoki telefon raqamingizni tekshiring"
            }
            raise ValidationError(data)


# Userni Registratsiya qilish (malumotlarini update qilish)------------------------------------------------------->
class ChangeUserInfoView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeUserSerializer
    http_method_names = ['patch', 'put']  # ushbu view uchun qanday metodlarni ishlataolishimizni belgilaymiz

    def get_object(self):
        return self.request.user  # aynan request bergan userni malumotlarini olish u-n

    # bu 2 metod UpdateAPIView da bor lekn bz o'zimiz istalgan malumotni qaytarishimiz uchun buni yozdigk (yani override boldi)--------->
    def update(self, request, *args, **kwargs):  # put requesti u-n ishlatiladi
        super(ChangeUserInfoView, self).update(request, *args, **kwargs)
        data = {
            "success": True,
            "message": "User muvofaqiyatli yangilandi",
            "auth_status": self.request.user.auth_status,
        }
        return Response(data, status=status.HTTP_200_OK)

    # Patch uchun
    # def partial_update(self, request, *args, **kwargs):  # patch requesti u-n ishlatiladi
    #     super(ChangeUserInfoView, self).partial_update(request, *args, **kwargs)
    #
    #     data = {
    #         "success": True,
    #         "message": "User muvofaqiyatli yangilandi",
    #         "auth_status": self.request.user.auth_status,
    #     }
    #     return Response(data, status=status.HTTP_200_OK)


# Rasm update qilish uchun------------------------------------------------------------------------------>
class ChangeUserPhotoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangeUserPhotoSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({
                "message": "Rasm muvoffaqyatli o'zgartirildi"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login uchun----------------------------------------------------------------------------------------->

class LoginView(TokenObtainPairView):
    # login qilayotgan userda hech qanday token bolmaydi shuning uchun TokenObtainPairView dan foydalanamiz
    serializer_class = LoginSerializer


# Refresh token (Acses tokeni yangilaydi) ------------------------------------------------------------>
class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer


# Userni Logout qilish uchun---------------------------------------------------------------------->
class LogOutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):  # post metotda refresh tokenni olib olamiz
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()  # tokendan boshqa foydalanmaslik uchun uni blacklistga kiritamiz
            data = {
                'success': True,
                'message': "Siz muvoffaqyatli logout qildingiz"
            }
            return Response(data, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Qayta parolni update qilish uchun olish uchun telefon raqam yoki emailga cod yuboradi ------------------------------>
class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny, ]  # Login qilmagan userlarham foydalana olishi uchun
    serializer_class = ForgotPasswordSerializer

    # Kiritilgan malumotni email yoki telefon ekanligini tekshirib qayta cod jo'natadi------------->
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email_or_phone = serializer.validated_data.get(
            'email_or_phone')  # email va phoneni validatsiasi(serializerdagi)
        user = serializer.validated_data.get('user')  # usernameni validatsiyasi (serializerdagi)

        if check_email_or_phone(email_or_phone) == 'phone':
            code = user.create_verify_code(VIA_PHONE)
            send_email(email_or_phone, code)
            # send_phone_code(email_or_phone, code)

        elif check_email_or_phone(email_or_phone) == 'email':
            code = user.create_verify_code(VIA_EMAIL)
            send_email(email_or_phone, code)

        user.auth_status = FORGET_PASS
        user.save()

        return Response(
            {
                "success": True,
                'message': "Tasdiqlash kodi muvaffaqiyatli yuborildi",
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token'],
                "user_status": user.auth_status,
            }, status=status.HTTP_200_OK
        )


# Esdan chiqqan parolni o'zgartirish uchun --------------------------------------------------------------------------->
class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordView, self).update(request, *args, **kwargs)

        try:
            user = Users.objects.get(id=response.data.get('id'))

        except ObjectDoesNotExist as e:
            raise NotFound(detail='User topilmadi')

        return Response(
            {
                'success': True,
                'message': "Parolingiz muvaffaqiyatli o'zgartirildi",
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token'],
                'auth_status': user.auth_status
            }
        )


# telefon raqamini yangilash uchun ----------------------------------------------------------------------------------->
class NewPhoneNumberView(generics.UpdateAPIView):
    serializer_class = UpdatePhoneNumberSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        user = self.request.user
        serializer.is_valid(raise_exception=True)
        new_phone_number = serializer.validated_data.get(
            'new_phone_number')  # email va phoneni validatsiasi(serializerdagi)

        if check_email_or_phone(new_phone_number) == 'phone':
            code = user.create_verify_code(VIA_PHONE)
            send_email(new_phone_number, code)
            # send_phone_code(new_phone_number, code)

        user.auth_status = NEW_PHONE
        user.new_phone = new_phone_number
        user.save()

        return Response(
            {
                "success": True,
                'message': "Tasdiqlash kodi muvaffaqiyatli yuborildi",
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token'],
                "user_status": user.auth_status,
            }, status=status.HTTP_200_OK
        )


# Yangi Kiritilgan raqamni saqlaymiz -------------------------------------------------------------------->
class VerifyCodeAndUpdatePhoneNumber(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user  # user ->
        code = self.request.data.get('code')  # 4083

        self.check_verify(user, code)  # pastdagi metod orqali tekshiradi (check_verify)
        return Response(
            data={
                "success": True,  # quyidagi malumotlarni bekentga qaytaradi
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token'],
                "new phone number": user.phone_number,
                "message": "Raqam yangilandi"
            }
        )

    # tasdiqlash kodini togri va yaroqliligini tekshiradi----------------------------------->
    @staticmethod
    def check_verify(user, code):  # 12:03 -> 12:05 => expiration_time=12:05   12:04
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)

        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan,Telefon raqamingizni qayta kiring"
            }
            raise ValidationError(data)
        else:
            verifies.update(
                is_confirmed=True)  # is_confirmed Truega ozgaradi (shu codni yana tasdiqlamoqchi bolsak check_verify ruhsat bermasligi u-n)

        if user.auth_status in [NEW_PHONE]:  # statusi o'zgartiriladi
            user.auth_status = DONE
            user.phone_number = user.new_phone
            user.save()
        return True


class UserCreateListView(generics.ListCreateAPIView):
    serializer_class = UserCreatListSerializer
    permission_classes = [IsAdminOrManangerOrReadOnly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Users.objects.all()
        else:
            return Users.objects.filter(is_superuser=False)


class UserALLView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserCreatListSerializer
    permission_classes = [IsAdminOrManangerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Users.objects.all()
        else:
            return Users.objects.filter(is_superuser=False)


class SuperUserUserCreateListView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserCreatListSerializer
    permission_classes = [ManangerOrReadOnly]
    pagination_class = CustomPageNumberPagination


class SuperUserUserALLView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserCreatListSerializer
    permission_classes = [ManangerOrReadOnly]


class UserUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserCreatListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomPageNumberPagination

    def get_object(self):
        return self.request.user  # token orqali request berayotgan userga tegishli malumotlar keladi


class CodesView(APIView):
    serializer_class = CodeSerializer

    def get(self, request):
        code = UserConfirmation.objects.filter(user=self.request.user).first()

        data = {
            "code": code.code,
            "verify_type": code.verify_type,
            "expiration_time": code.expiration_time,
            "is_confirmed": code.is_confirmed
        }
        return Response(data, status=status.HTTP_200_OK)
