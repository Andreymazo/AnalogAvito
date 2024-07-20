from rest_framework import generics
from ad.models import Category, Car, Images, Like
from ad.serializers import LikeSerializer, LikeSerializerCreate
from bulletin.serializers import CarSerializer, CategorySerializer, ImagesSerializer
from rest_framework import status
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
from rest_framework import serializers

from users.models import CustomUser

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
    

    
class UploadViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


"""Функция для проверки сколько запросов в базу через релейтед нейм"""
@extend_schema(
     
        
        request=ImagesSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Вывод фоток автомобиля",
                response=ImagesSerializer,
            ),
        },
         
    )
@api_view(["GET"])
def check_car_images_db_requests(request):# Пробросить черерз тулбар, увидим 2 запроса в базу 89 и 94 строчки, а не 1+3 по количеству фоток (их там хоть сколько)
    car_obj = Car.objects.get(id=5)
    if request.method == "GET":
        serializer= ImagesSerializer(car_obj.images.all(), many=True)
        return Response(serializer.data)
        

"""Функция возвращает лайки по объекту (объявлению)"""
@extend_schema(
     
        description="Лайки объявления",
        request=LikeSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Вывод лайков по объявлению",
                response=LikeSerializer,
            ),
        },
         
    )
@api_view(["GET"])
def like_list_obj(request, ContentType_id=16, obj_id=6):
    content_type = ContentType.objects.get_for_id(ContentType_id)
    obj = content_type.get_object_for_this_type(pk=obj_id)
    if request.method == "GET":
        like_queryset_obj = Like.objects.all().filter(object_id=obj.id)
        serializer= LikeSerializer(like_queryset_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""Функция возвращает лайки по пользователю залогиненному""" 
@extend_schema(
     
        description="Лайки объявления",
        request=LikeSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Вывод лайков по пользователю-залогиненному",
                response=LikeSerializer,
            ),
        },
         
    )
@api_view(["GET"])
def like_list_user(request):
    if request.user.is_anonymous:
        return redirect(reverse("bulletin:sign_in_email"))
    user_instance = request.user
    if request.method == "GET":
        like_queryset_user = Like.objects.all().filter(user_id=user_instance.id)
        serializer= LikeSerializer(like_queryset_user, many=True)
        return Response(serializer.data)
    
"""Функция возвращает лайки по пользователю, может смотреть любой залогиненный, по дефлоту выведет для первого""" 
@extend_schema(
     
        description="Лайки объявления",
        request=LikeSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Вывод лайков по пользователю",
                response=LikeSerializer,
            ),
        },
         
    )
@api_view(["GET"])
def like_list_user(request, user_id=1):
    if request.user.is_anonymous:
        return redirect(reverse("bulletin:sign_in_email"))
    user_instance = CustomUser.objects.get(id=user_id)
    if request.method == "GET":
        like_queryset_user = Like.objects.all().filter(user_id=user_instance.id)
        serializer= LikeSerializer(like_queryset_user, many=True)
        return Response(serializer.data)
    

"""Функция добавляет лайк текущего пользователя к объявлению"""
@extend_schema(
     
        description="Лайки объявления",
        request=LikeSerializerCreate,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Добавление лайка пользователя",
                response=LikeSerializerCreate,
            ),
            status.HTTP_200_OK: OpenApiResponse(
                description=(
                    "Лайк у пользователя уже существует"
                ),
                response=LikeSerializerCreate,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description=(
                    "Ввели неправильные данные"
                ),
                response=inline_serializer(
                    name="ValidationErrorInConfirmCode",
                    fields={"email": serializers.ListField(
                        child=serializers.CharField()
                    )}
                ),
            )
        }, 
    )
@api_view(['POST'])
def like_add(request):# is_liked=False, ContentType_id=16, obj_id=6):
    print('request.user', request.user)
    if request.user.is_anonymous:
        return redirect(reverse("bulletin:sign_in_email"))
    # content_type = ContentType.objects.get_for_id(ContentType_id)
    # obj = content_type.get_object_for_this_type(pk=obj_id)
    user_instance = request.user
    if request.method == "POST":
        serializer = LikeSerializerCreate(data=request.data)
        if serializer.is_valid():
            print('serializer.data', serializer.data)
            content_type = serializer.validated_data.get("content_type")
            object_id = serializer.validated_data.get('object_id')
            is_liked = serializer.validated_data.get('is_liked')
            try:
                print('1111111111111111111111111')
                like_instance = Like.objects.get(user=user_instance, content_type=content_type, object_id=object_id,is_liked=is_liked)
                return Response([{"message" : "Лайки уже существуют"},serializer.data], status=status.HTTP_200_OK)
            except Like.DoesNotExist:
                # obj.votes.create(user=request.user, vote=self.vote_type)
                # result = True
                print('22222222222222222222222222')
                like_instance = Like.objects.create(user=user_instance, content_type=content_type, object_id=object_id,is_liked=is_liked)
                like_instance.save()
            # serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.views.decorators.csrf import csrf_exempt 
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http import HttpResponse, JsonResponse 
from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.parsers import JSONParser
from django.contrib.contenttypes.models import ContentType


class LikeForm(forms.Form):
    queryset = Car.objects.all()
    choices = [(f"{i}", i) for i in queryset]
    choose_car = forms.ChoiceField(choices=choices)


# """Функция для тестирования лайков: на входе юзер и карточку, надо ввести, для этого форма (с ней миграции не проходят), после тестирования уберем,
#  на выходе добавляем лайк от пользователя карточке"""
# # @csrf_exempt
# @api_view(['GET', 'POST'])
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def like_list_create(request):
#     if request.user.is_anonymous:
#         return redirect(reverse("bulletin:sign_in_email"))
#     user_instance = request.user
#     car_queryset = Car.objects.all()
#     obj=car_queryset.get(id=5)#Для проверки вставим 1 объявление авто
#     print('user_instance', user_instance)
    
#     form = LikeForm()
#     if request.method == 'GET':
#         like_queryset = Like.objects.all().filter(object_id=obj.id)
#         serializer = LikeSerializer(like_queryset, many=True) 
#         # return JsonResponse(serializer.data, safe=False) 
#         print('serializer.data', type(serializer.data), serializer.data)
        
#         print('like_queryset', like_queryset)
#         print('data_for_template ================', serializer.data)
#         total_likes = obj.likes.count()
#         tottal_likes_user = Like.objects.filter(user_id = request.user.id).count()
#         print('==========total_likes===========', total_likes)
#         print('==========total_likes_usr===========', tottal_likes_user)
#         return Response({"form": form, "data": request.data, "like_queryset":serializer.data, "tottal_likes_user": tottal_likes_user, "card_instance":obj, "total_likes":total_likes}, template_name="ad/templates/ad/template_for_like.html", status=status.HTTP_200_OK)
#     form = LikeForm(request.POST)
#     if request.method == 'POST':
        
#         if form.is_valid():
           
#             print('------------1---------------')
#             form_value = form.cleaned_data.get("choose_car")
#             obj = car_queryset.get(id=form_value)
#             print("form_value", form_value)
#             context = {"form_value":form_value}
#         # Response(data, status=None, template_name=None, headers=None, content_type=None)
#             print('user_instance====================', user_instance, "-----------form_value", form_value)#user_instance==================== andreymazo3@mail.ru -----------form_value Card object (2)
#             Like.objects.get_or_create(user=user_instance, content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,is_liked=False)
#             print(f"like added to car object {obj} from {user_instance} _______________________")
#             return Response(context, template_name="ad/templates/ad/template_for_like.html", status=status.HTTP_201_CREATED)
#         else:
#             print(form.errors.as_data())
#             return Response(template_name="ad/templates/ad/template_for_like.html", status=status.HTTP_204_NO_CONTENT)
#   kill -9 $(lsof -t -i:8080)
