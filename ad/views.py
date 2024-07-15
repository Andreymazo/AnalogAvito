import json
from rest_framework import generics
from ad.func_for_help import save_file
from ad.models import Card, Category, Car, Images, Like
from ad.serializers import LikeSerializer
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
from rest_framework.decorators import api_view
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

    
class UploadViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer



# from django.views.decorators.csrf import csrf_exempt 
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse 
from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.parsers import JSONParser
class LikeForm(forms.Form):
    queryset = Card.objects.all()
    choices = [(f"{i}", i) for i in queryset]
    choose_card = forms.ChoiceField(choices=choices)
"""Функция на входе юзер и карточку, надо ввести, для этого форма, после тестирования, уберем, на выходе добавляем лайк от пользователя карточке"""
# @csrf_exempt
@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def like_list_create(request):
    
    user_instance = request.user
    card_queryset = Card.objects.all()
    card_instance=card_queryset.get(id=1)#Для проверки вставим 1ую карточку
    print('user_instance', user_instance)
    if request.user.is_anonymous:
        return redirect(reverse("bulletin:sign_in_email"))
    form = LikeForm()
    if request.method == 'GET':
        like_queryset = Like.objects.all().filter(card_id=card_instance.id)
        serializer = LikeSerializer(like_queryset, many=True) 
        # return JsonResponse(serializer.data, safe=False) 
        print('serializer.data', type(serializer.data), serializer.data)
        
        print('like_queryset', like_queryset)
        print('data_for_template ================', serializer.data)
        total_likes = card_instance.likes.count()
        tottal_likes_user = Like.objects.filter(user_id = request.user.id).count()
        return Response({"form": form, "data": request.data, "like_queryset":serializer.data, "tottal_likes_user": tottal_likes_user, "card_instance":card_instance, "total_likes":total_likes}, template_name="ad/templates/ad/template_for_like.html", status=status.HTTP_200_OK)
    form = LikeForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form_value = form.cleaned_data.get("choose_card")
            card_instance = card_queryset.get(id=form_value)
            print("form_value", form_value)
            context = {"form_value":form_value}
        # Response(data, status=None, template_name=None, headers=None, content_type=None)
            print('user_instance====================', user_instance, "-----------form_value", form_value)#user_instance==================== andreymazo3@mail.ru -----------form_value Card object (2)
            Like.objects.get_or_create(user=user_instance,card=card_instance,is_liked=False)
            print(f"like added to card {card_instance} from {user_instance} _______________________")
            return Response(context, template_name="ad/templates/ad/template_for_like.html", status=status.HTTP_201_CREATED)
#   kill -9 $(lsof -t -i:8080)
