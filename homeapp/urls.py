from django.urls import path
from .views import *

urlpatterns = [
    path('home_list/', HomeListView.as_view()),
    path('home_create/', HomeCreateView.as_view()),
    path('home_detail/<int:pk>', HomeDetailView.as_view()),
    path('home_retrive_update_delete/<int:pk>', HomeViewAll.as_view()),
    path('pic_create/', PictureCreateView.as_view()),
    path('my_home/', MyHomeView.as_view()),
    path('like_list/', HomeLikeListView.as_view()),
    path('like_create_delete/<int:pk>', HomeLikeApiView.as_view()),
    path('api/v1/search/', HomeModelSearchView.as_view()),
    path('search/', SearchView.as_view()),
    # admin panel u-n
    path('adm/type/', TypeView.as_view()),
    path('adm/type_all/<int:pk>', TypeViewALL.as_view()),
    path('adm/home_type/', HomeTypeView.as_view()),
    path('adm/home_type_all/<int:pk>', HomeTypeViewALL.as_view()),
    path('adm/confort_type/', HomeTypeView.as_view()),
    path('adm/confort_type_all/<int:pk>', HomeTypeViewALL.as_view()),
]
