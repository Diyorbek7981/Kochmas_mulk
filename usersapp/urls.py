from django.urls import path
from .views import *

urlpatterns = [
    # signup u-n
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
]