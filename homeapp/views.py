from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import *
from .serializesrs import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
# search uchun
from functools import reduce
import operator


# Create your views here.

class HomeModelSearchView(generics.ListAPIView):
    queryset = HomeModel.objects.all()
    serializer_class = HomeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_terms = self.request.query_params.getlist('search')

        if search_terms:
            # price_search_terms = [term for term in search_terms if '-' in term]
            # other_search_terms = [term for term in search_terms if '-' not in term]
            #
            # if price_search_terms:
            #     for price_term in price_search_terms:
            #         price_threshold = float(price_term.replace('-', ''))
            #         queryset = queryset.filter(price__lt=price_threshold)

            queryset = queryset.filter(
                reduce(operator.and_, (
                    Q(name__icontains=term) |
                    Q(price__icontains=term) |
                    Q(description__icontains=term) |
                    Q(type__name__icontains=term) |
                    Q(home_type__name__icontains=term) |
                    Q(location__name__icontains=term)
                    for term in search_terms
                ))
            )

        return queryset


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


class LocationViewALL(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocationModel.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsOwnerOrReadOnly]
