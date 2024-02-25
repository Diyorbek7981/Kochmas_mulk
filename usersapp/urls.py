from django.urls import path
from .views import LoginView, LogOutView, LoginRefreshView, CreateUserView, VerifyAPIView, GetNewVerification, \
    ChangeUserInfoView, ChangeUserPhotoView, ForgotPasswordView, ResetPasswordView, UserCreateListView, \
    UserALLView, SuperUserUserALLView, SuperUserUserCreateListView, UserUpdateApiView, UserMessageCreate, \
    NewPhoneNumberView, CodesView, VerifyCodeAndUpdatePhoneNumber

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
    path('forgot_pass/', ForgotPasswordView.as_view()),
    path('reset_pass/', ResetPasswordView.as_view()),
    path('user_update/', UserUpdateApiView.as_view()),
    path('user_message/', UserMessageCreate.as_view()),
    path('new_phone/', NewPhoneNumberView.as_view()),
    path('verif_new_phone/', VerifyCodeAndUpdatePhoneNumber.as_view()),
    path('codes/', CodesView.as_view()),
    # admin panel u-n
    path('adm/creat_list_user/', UserCreateListView.as_view()),
    path('adm/user_all/<uuid:pk>', UserALLView.as_view()),
    path('adm/superuser_user_all/', UserALLView.as_view()),
    path('adm/supperuser_user_all/<uuid:pk>', SuperUserUserALLView.as_view()),
]
