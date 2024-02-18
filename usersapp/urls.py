from django.urls import path
from .views import *

urlpatterns = [
    # signup u-n
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('new_verify/', GetNewVerification.as_view()),
    path('change_user/', ChangeUserInfoView.as_view()),
]
