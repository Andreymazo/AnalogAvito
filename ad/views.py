import json
from rest_framework import generics
from ad.func_for_help import save_file
from ad.models import Category, Car, Images
from bulletin.serializers import CarSerializer, CategorySerializer, ImagesSerializer
from rest_framework import status
# from rest_framework.views import APIView #Почему то обычный не видит и не грузит файл, либо Генерик, либо МоделВьюсет грузят файл
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    inline_serializer
)
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile

from collections import OrderedDict

class CategoryList(generics.ListAPIView):#ListCreateAPIView
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = "Category list"
    filter_fields = ( 
        '-created', 
    )


@extend_schema(
    parameters=[
        CarSerializer,  # serializer fields are converted to parameters  
        ],
    request=CarSerializer,
    responses={status.HTTP_201_CREATED: OpenApiResponse(
                description="Объявление автомобиль создано",
                response=CarSerializer,
            ),}
)
# @extend_schema_field({'type':"string",'format':'binary',
#     'example':{
#              "image":{"url":"string","name":"string"},
            
#     }
# })


class CarList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    name = "Car list"
    filter_fields = ( 
        '-created', 
    )
    
    def change_image_to_string(self, obj):
        if type(obj) == InMemoryUploadedFile:
            return f"images/{obj}"
        if type(obj) == TemporaryUploadedFile:
            return f"images/{obj}"
        else:
            return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        s = OrderedDict([(k, self.change_image_to_string(v)) for k,v  in serializer.validated_data.items()])
        self.perform_create(serializer)
        headers = self.get_success_headers(s)
        return Response(s, status=status.HTTP_201_CREATED, headers=headers)
    

class UploadFileImage(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Images.objects.all()
    serializer_class=ImagesSerializer
    # parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# class UploadFileSimple(views.APIView):

    # def post(self, request, format='jpg'):

    #     serializer = ImagesSerializerSimple(request.FILES)
        
    #     # serializer = ImagesSerializer(data=request.DATA, files=request.FILES)
    #     print("request.FILES================", request.FILES.__dict__)
    #     file = request.FILES['file']
    #     file_save_path = "media/images"
    #     full_path = file_save_path + file.name
    #     save_file(file, full_path)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
class UploadViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer