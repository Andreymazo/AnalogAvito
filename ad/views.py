from rest_framework import generics
from ad.models import Category, Car
from bulletin.serializers import CarSerializer, CategorySerializer

class CategoryList(generics.ListAPIView):#ListCreateAPIView
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = "Category list"
    filter_fields = ( 
        '-created', 
    )

class CarList(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    name = "Car list"
    filter_fields = ( 
        '-created', 
    )