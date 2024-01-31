from django.shortcuts import render
from rest_framework import generics,permissions
from .models import *
from .serializesrs import *
from .permissions import IsAdminOrReadOnly,IsOwnerOrReadOnly


# Create your views here.

class HomeView(generics.ListCreateAPIView):
    queryset = HomeModel.objects.all()
    serializer_class = HomeSerializer


class HomeViewALL(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeModel.objects.all()
    serializer_class = HomeSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PictureView(generics.ListCreateAPIView):
    queryset = PictureModel.objects.all()
    serializer_class = PictureSerializer


class PictureViewALL(generics.RetrieveUpdateDestroyAPIView):
    queryset = PictureModel.objects.all()
    serializer_class = PictureSerializer
    permission_classes = [IsOwnerOrReadOnly]

class TypeView(generics.ListCreateAPIView):
    queryset = TypeModel.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class TypeViewALL(generics.RetrieveUpdateDestroyAPIView):
    queryset = TypeModel.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class HomeTypeView(generics.ListCreateAPIView):
    queryset = HomeTypeModel.objects.all()
    serializer_class = HomeTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class HomeTypeViewALL(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeTypeModel.objects.all()
    serializer_class = HomeTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class LocationView(generics.ListCreateAPIView):
    queryset = LocationModel.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminOrReadOnly]


class LocationViewALL(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocationModel.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminOrReadOnly]
