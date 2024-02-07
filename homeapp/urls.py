from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomeView.as_view()),
    path('homeall/<int:pk>', HomeViewALL.as_view()),
    path('pic/', PictureView.as_view()),
    path('picall/<int:pk>', PictureViewALL.as_view()),
    path('type/', TypeView.as_view()),
    path('typeall/<int:pk>', TypeViewALL.as_view()),
    path('hometype/', HomeTypeView.as_view()),
    path('hometypeall/<int:pk>', HomeTypeViewALL.as_view()),
    path('api/v1/search/', HomeModelSearchView.as_view()),
]
