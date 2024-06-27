from rest_framework import generics
from ad.func_for_help import save_file
from ad.models import Category, Car, Images
from bulletin.serializers import CarSerializer, CategorySerializer, ImagesSerializer


class CategoryList(generics.ListAPIView):#ListCreateAPIView
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = "Category list"
    filter_fields = ( 
        '-created', 
    )

class CarList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    name = "Car list"
    filter_fields = ( 
        '-created', 
    )
   
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

# class UploadFileImage(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, format='jpg'):
#         # serializer = ImagesSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data, status=status.HTTP_200_OK)
#         serializer = ImagesSerializer(request.FILES)
#         # serializer = ImagesSerializer(data=request.DATA, files=request.FILES)
#         print("request.FILES================", request.FILES.__dict__)
#         file = request.FILES['file']
#         file_save_path = "media/images"
#         full_path = file_save_path + file.name
#         save_file(file, full_path)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
class UploadViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer