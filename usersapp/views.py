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

    def post(self, request, *args, **kwargs):
        user = self.request.user  # user ->
        code = self.request.data.get('code')  # 4083

        self.check_verify(user, code)
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
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True
