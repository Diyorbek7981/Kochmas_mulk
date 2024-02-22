from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomeView.as_view()),
    path('homeall/<int:pk>', HomeViewALL.as_view()),
    path('pic/', PictureView.as_view()),
    path('picall/<int:pk>', PictureViewALL.as_view()),
    path('adm/type/', TypeView.as_view()),
    path('adm/typeall/<int:pk>', TypeViewALL.as_view()),
    path('adm/hometype/', HomeTypeView.as_view()),
    path('adm/hometypeall/<int:pk>', HomeTypeViewALL.as_view()),
    path('api/v1/search/', HomeModelSearchView.as_view()),
    path('like_list/', HomeLikeListView.as_view()),
    path('create_delete_like/<int:pk>', HomeLikeApiView.as_view()),
]
