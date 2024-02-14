from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import *
from .serializesrs import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status
# search uchun
from functools import reduce
import operator


# Create your views here.

class HomeModelSearchView(generics.ListAPIView):
    queryset = HomeModel.objects.all()

    serializer_class = SearchSerializer

    def post(self, request, format=None):
        serializer = SearchSerializer(data=request.data)

        if serializer.is_valid():
            queryset = HomeModel.objects.all()
            queryset = queryset.filter(
                Q(type__name__icontains=serializer.validated_data['type'])
            )

            queryset = queryset.filter(
                Q(home_type__name__icontains=serializer.validated_data['home_type'])
            )

            rooms = serializer.validated_data['count_rooms']
            if rooms is not None:
                if rooms == 6:
                    queryset = queryset.filter(count_rooms__gte=rooms
                                               )
                else:
                    queryset = queryset.filter(
                        Q(count_rooms__icontains=rooms)
                    )

            if 'location' in serializer.validated_data:
                queryset = queryset.filter(
                    Q(location__icontains=serializer.validated_data['location'])
                )

            if 'from_price' and 'up_to_price' in serializer.validated_data:
                price = serializer.validated_data['from_price']
                price1 = serializer.validated_data['up_to_price']

                if price is not None and price1 is not None:
                    price = min(price, price1)
                    price1 = max(price, price1)

                    queryset = queryset.filter(
                        Q(price__gte=price, price__lte=price1))

                queryset = queryset.all()

                # price = serializer.validated_data['price']
                # up_lo = serializer.validated_data['up_low']
                # if up_lo == 0:
                #     queryset = queryset.filter(Q(price__lt=price))
                # elif up_lo == 1:
                #     queryset = queryset.filter(Q(price__gte=price))

                serializer = HomeSerializer(queryset, many=True)
                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_terms = self.request.query_params.getlist('q')

        if search_terms:
            queryset = queryset.filter(
                reduce(operator.and_, (
                    Q(name__icontains=term) |
                    Q(count_rooms__icontains=term) |
                    Q(location__icontains=term) |
                    Q(price__icontains=term) |
                    Q(description__icontains=term) |
                    Q(type__name__icontains=term) |
                    Q(home_type__name__icontains=term)
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

    def get_queryset(self):
        return PictureModel.objects.filter(home__owner=self.request.user)


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


# coment u-n
class CommentListAPIView(generics.ListCreateAPIView):
    queryset = CommentModel.objects.all()
    serializer_class = CommentListSerializers

    def get_queryset(self):
        queryset = CommentModel.objects.filter(Parent=None)
        return queryset
