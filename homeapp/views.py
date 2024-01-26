from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializesrs import *


# Create your views here.

class HomeView(generics.ListAPIView):
    queryset = HomeModel.objects.all()
    serializer_class = HotelSerializer


class PictureView(generics.ListAPIView):
    queryset = PictureModel.objects.all()
    serializer_class = PictureSerializer
