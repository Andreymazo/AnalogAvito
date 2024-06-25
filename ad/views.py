from rest_framework import generics
from ad.models import Category
from bulletin.serializers import CategorySerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = "category_list"
    filter_fields = ( 
        '-created', 
    )