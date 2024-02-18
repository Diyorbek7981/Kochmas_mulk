from django.urls import path
from .views import *

urlpatterns = [
    # signup u-n
    path('login/', LoginView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('login_refresh/', LoginRefreshView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('new_verify/', GetNewVerification.as_view()),
    path('change_user/', ChangeUserInfoView.as_view()),
    path('change_photo/', ChangeUserPhotoView.as_view()),
]
