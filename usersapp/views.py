from rest_framework import generics, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError


# Create your views here.

# auth u-n ----------------------------------------->
class CreateUserView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]  # hechqanday imkoniyatlarni cheklamaslik u-n


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

    # tasdiqlash kodini togri va yaroqliligini tekshiradi------------>
    @staticmethod
    def check_verify(user, code):  # 12:03 -> 12:05 => expiration_time=12:05   12:04
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        print(verifies)
        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        else:
            verifies.update(
                is_confirmed=True)  # is_confirmed Truega ozgaradi (shu codni yana tasdiqlamoqchi bolsak check_verify ruhsat bermasligi u-n)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


# tasdiqlash kodini qayta olish uchun -------------->
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
            send_phone_code(user.phone_number, code)
        else:
            data = {
                "message": "Email yoki telefon raqami noto'g'ri"
            }
            raise ValidationError(data)

        return Response(
            {
                "success": True,
                "message": "Tasdiqlash kodingiz qaytadan yuborildi"
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
        },
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):  # patch requesti u-n ishlatiladi
        super(ChangeUserInfoView, self).partial_update(request, *args, **kwargs)
        data = {
            "success": True,
            "message": "User muvofaqiyatli yangilandi",
            "auth_status": self.request.user.auth_status,
        },
        return Response(data, status=status.HTTP_200_OK)


# Rasm update qilish uchun
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
