from django.core.exceptions import FieldError
import django_filters
from django.apps import apps
from django_filters.rest_framework import DjangoFilterBackend
from redis.exceptions import ConnectionError
from rest_framework import pagination, filters
from rest_framework.exceptions import APIException
from django.core.cache import cache
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError, ProgrammingError
from rest_framework import generics
from ad.filters import BagsKnapsacksFilter, CarFilter, CategoryFilter, ChildClothesShoesFilter, CustomFilterSet, CategoryFilterByName, MenClothesFilter, MenShoesFilter, WemenClothesFilter, WemenShoesFilter
# from ad.func_for_help import choose_serializer
from ad.models import BagsKnapsacks, Category, Car, ChildClothesShoes, Like, Images, MenClothes, MenShoes, Views, WemenClothes, WemenShoes
from ad.pagination import OrdinaryListPagination
from config.backends import CustomFilterQueryset, MyFilterBackend
from users.models import Notification
from ad.serializers import CarCreateSerializer, CarNameSerializer, DefaultSerializer, LikeSerializer, \
    LikeSerializerCreate, NotificationSerializer, CategoryFilterSerializer, ViewsSerializer
from bulletin.serializers import CarListSerializer, CarSerializer, CategorySerializer, ImagesSerializer
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
    OpenApiTypes,
    inline_serializer, extend_schema_view
)
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from rest_framework.decorators import api_view
from collections import OrderedDict
from rest_framework import serializers
from users.models import CustomUser, Profile
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from rest_framework.parsers import MultiPartParser, FormParser
from map.models import Marker
from django.db import transaction
from django.contrib import messages
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from ad.serializers import BagsKnapsacksSerialiser, ChildClothesShoesSerialiser, MenClothesSerialiser, MenShoesSerialiser, WemenClothesSerialiser, WemenShoesSerialiser


# @extend_schema(
#     tags=["Категории/Categories"],
#     summary="Список всех категорий",
#     request=CategorySerializer,
# )
# class CategoryList(generics.ListAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     name = "Category list"
#     filter_fields = (
#         '-created',
#     )

from django.core.signing import BadSignature, Signer
from django.urls import reverse
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    inline_serializer, extend_schema_view
)
from rest_framework import viewsets
from ad.models import Category
from bulletin.serializers import (
    CategorySerializer,

)


@extend_schema(
    tags=["Категории/Categories"],
    request=CategorySerializer,
    parameters=[OpenApiParameter('limit', exclude=True), OpenApiParameter('offset', exclude=True), OpenApiParameter('ordering', exclude=True),]
)
@extend_schema_view(
    list=extend_schema(summary="Список всех категорий"),
    retrieve=extend_schema(summary="Получение информации о категории")
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для категорий."""
    http_method_names = ("get",)
    queryset = Category.objects.prefetch_related('children').all()
    serializer_class = CategorySerializer

@extend_schema(
    tags=["Категории/Categories"],
    summary="Список всех категорий/Фильтрация категорий",
    )

class CategoriesFilter(generics.ListAPIView):
    """Эндпоинт для проверки работы фильтрации категорий."""

    # Получаем queryset только для нулевого уровня, потомки будут получены в сериализаторе
    queryset = Category.objects.filter(level=0)
    serializer_class = CategoryFilterSerializer
    pagination_class = OrdinaryListPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilterByName



@extend_schema(
    tags=["Автомобили/Cars"],
    # summary=" Car list and car creation",
    request=CarCreateSerializer,
    responses={status.HTTP_201_CREATED: OpenApiResponse(
        description="Объявление автомобиль создано",
        response=CarSerializer,
    ), }

)

class CarList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CarCreateSerializer


    @extend_schema(
    summary="Список автомобилей / Car list",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    @extend_schema(
    summary="Создание автомобиля / Car list create",
    # parameters=[OpenApiParameter(name='category', description='Category Id', type=int)],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    tags=["Автомобили/Cars"],
    # summary="Создание объявления авто несколько фото подгружаются / Car multyple image creation",
    # responses={
    #         201: OpenApiResponse(response=CarCreateSerializer,
    #                              description='Created. New car in response'),
    #         400: OpenApiResponse(description='Bad request (something invalid)'),
    #     },
    # parameters=[OpenApiParameter('limit', exclude=True), OpenApiParameter('offset', exclude=True), OpenApiParameter('ordering', exclude=True),]
)


# class CarCreate(generics.CreateAPIView, generics.ListAPIView):
#     queryset = Car.objects.all()
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = CarCreateSerializer

#     @extend_schema(
#     summary="Список всех автомобилей",
#     )
#     def get(self, request, *args, **kwargs):
#         serializer = CarCreateSerializer(Car.objects.all(), many=True)
#         return Response([serializer.data, {"message": "Список объявлений автомобилей / List of cars"}])

#     @extend_schema(
#     tags=["Автомобили/Cars"],
#     summary="Создание объявления авто несколько фото подгружаются / Car multyple image creation",
#     responses={
#             201: OpenApiResponse(response=CarCreateSerializer,
#                                  description='Created. New car in response'),
#             400: OpenApiResponse(description='Bad request (something invalid)'),
#         },
#     parameters=[OpenApiParameter('limit', exclude=True), OpenApiParameter('offset', exclude=True), OpenApiParameter('ordering', exclude=True),]
#     )
#     def post(self, request, *args, **kwargs):
#         serializer = CarCreateSerializer(request.data)
#         print("serializer.data ==", serializer.data)
#         return Response(serializer.data)

#     # def perform_create(self, serializer):
#     #     serializer.save(user=self.request.user)


@extend_schema(
    tags=["Автомобили/Cars"],
)
class CarDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    ## Под капотом три метода ниже, если что-то надо их меняем:
    # class ItemDetail(APIView):

    @extend_schema(
        methods=['GET'],
        summary='Получение информации об автомобиле',
    )
    def get(self, request, pk, format=None):
        # Add new model instance Views get_or_creation

        item = get_object_or_404(Car.objects.all(), pk=pk)
        serializer = CarSerializer(item)
        try:
            profile = request.user.profile
        except AttributeError:
            print('---------------------', request.user, '4444444444', self.request.user)
            return Response([serializer.data, {"message": "Anonymoususer, Views dont counted"}],
                            status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"message": "У вас нет Профиля, перенаправляем на регистрацию"},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        view_instance = Views.objects.get_or_create(profile=profile,
                                                    content_type=ContentType.objects.get_for_model(item),
                                                    object_id=item.id)

        return Response(serializer.data)

    @extend_schema(
        methods=['PUT'],
        summary="Обновление данных об автомобиле",
        description="Метод позволяет полностью обновить информацию об автомобиле. "
                    "Тело запроса должно содержать полную информацию об автомобиле, "
                    "включая все обязательные поля."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)  # Дла реализации доки

    #     def put(self, request, pk, format=None):
    #         item = get_object_or_404(Item.objects.all(), pk=pk)
    #         serializer = ItemSerializer(item, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(
        methods=['PATCH'],
        summary="Частичное обновление информации об автомобиле",
        description="Метод позволяет частично обновить информацию об автомобиле."
    )
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)  # Дла реализации доки

    @extend_schema(
        methods=['DELETE'],
        summary="Удаление объекта"
    )
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)  # Дла реализации доки


#     def delete(self, request, pk, format=None):
#         item = get_object_or_404(Item.objects.all(), pk=pk)
#         item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    tags=["Изображения/Images"],
)
@extend_schema_view(
    list=extend_schema(summary="Получение списка всех изображений"),
    create=extend_schema(summary="Загрузка нового изображения пользователем"),
    retrieve=extend_schema(summary="Получение информации о изображении"),
    update=extend_schema(summary="Обновление изображения"),
    partial_update=extend_schema(summary="Обновление изображения"),
    destroy=extend_schema(summary="Удаление изображения")
)
class UploadViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


"""Func returns likes by obj (ad)"""
@extend_schema(

    tags=["Лайки / Likes"],
    summary="Лайки объявления / List of likes the advertisement concerned, returns likes by obj (ad)",
    description="Лайки объявления",
    request=LikeSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Likes by advertisement",
            response=LikeSerializer,
        ),
    },
)
@api_view(["GET"])  # Здесь в кэше уже должны быть модель и ноер объекта
def like_list_obj(request):  # ContentType_id=16, obj_id=6):
    try:
        dict_of_cache = cache.get_many(["content_type", "obj_id"])
        content_type = dict_of_cache['content_type']
        obj_id = dict_of_cache['obj_id']
    except KeyError as e:
        print(e)
        return redirect(reverse("ad:get_model_fm_category"))
    # content_type = ContentType.objects.get_for_id(ContentType_id)
    # obj = content_type.get_object_for_this_type(pk=obj_id)
    # content_type = ContentType.objects.get_for_model(obj)
    if request.method == "GET":
        like_queryset_obj = Like.objects.all().filter(content_type=content_type).filter(object_id=obj_id)
        serializer = LikeSerializer(like_queryset_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""Function returns likes for requested user"""
@extend_schema(
    tags=["Лайки / Likes "],
    summary="Лайки пользователя / List of likes request user concerned",
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
        serializer = LikeSerializer(like_queryset_user, many=True)
        return Response(serializer.data)


"""Function returns likes for user instance, for 1st by default"""
@extend_schema(

    tags=["Лайки / Likes"],
    summary="Лайки кастомного пользователя / List of likes by custom user",
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
        serializer = LikeSerializer(like_queryset_user, many=True)
        return Response(serializer.data)

# class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    # def get_object(self):
    #     print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    #     queryset = self.get_queryset()             # Get the base queryset
    #     queryset = self.filter_queryset(queryset)  # Apply any filter backends
    #     filter = {}
    #     for field in self.lookup_fields:
    #         if self.kwargs.get(field): # Ignore empty fields.
    #             filter[field] = self.kwargs[field]
    #     obj = get_object_or_404(queryset, **filter)  # Lookup the object
    #     self.check_object_permissions(self.request, obj)
    #     return obj


# from rest_framework import filters
# import django_filters

from django_filters import filters
# class CategoryFilter(filters.FilterSet):
#     """
#         Filter of crop name
#     """
#     name = filters.ModelMultipleChoiceFilter
#     # name = filters.CharFilter(field_name='name', lookup_expr='contains')

#     class Meta:
#         model = Crop
#         fields = ['name']

def get_ad_forcategory(self_model_category):
    lst_mdls =  [ChildClothesShoes, WemenShoes, MenShoes, WemenClothes, MenClothes, BagsKnapsacks, Car]
    for i in lst_mdls:
      
        # print(i.category.field._related_name)
        # print(str((type(self_model_category.bagsknapsacks.all().first()).__name__)).lower())
        if i.category.field._related_name==str((type(self_model_category.childclothesshoes.all().first()).__name__)).lower():
            return i
        if i.category.field._related_name==str((type(self_model_category.wemenshoes.all().first()).__name__)).lower():
            return i
        if i.category.field._related_name==str((type(self_model_category.menshoes.all().first()).__name__)).lower():
            return i
        if i.category.field._related_name==str((type(self_model_category.wemenclothes.all().first()).__name__)).lower():
            return i
        if i.category.field._related_name==str((type(self_model_category.menclothes.all().first()).__name__)).lower():
            return i
        if i.category.field._related_name==str((type(self_model_category.bagsknapsacks.all().first()).__name__)).lower():
            return i
        if i.category.field._related_name==str((type(self_model_category.car.all().first()).__name__)).lower():
            return i
       
class StandardSetPagination(pagination.PageNumberPagination):
       page_size = 3
@extend_schema(
    tags=["Общая логика (Контент Тайп) / ContentType concerned"],
    summary="По категориям получаем модель объявлений",
    request=CategorySerializer,
    # parameters=[OpenApiParameter('limit', exclude=True), OpenApiParameter('offset', exclude=True), \
    #             OpenApiParameter('ordering', exclude=True), OpenApiParameter('page', exclude=True),]
)
class GetModelFmCategoryView(generics.ListAPIView, generics.RetrieveAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)#  IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardSetPagination
    filterset_class = CategoryFilter

    def get(self, request, *args, **kwargs):# This is for retrieve
        ctype_id=""
        queryset = self.filter_queryset(self.get_queryset())
        print('queryset', queryset.first())
        print('queryset', type(queryset.first()))
        serializer = CategorySerializer(queryset, many=True)
        
        try:
            self_model=queryset.first()
            print('self_model 1', self_model)
            self_model_returned = get_ad_forcategory(self_model)
            print('self_model 2', self_model_returned)
            # print('11111111111111', type(queryset.first().ad_for_category.all().first()))
            ctype = ContentType.objects.get_for_model(self_model_returned)
            # ctype = ContentType.objects.get_for_model(model=type(queryset.first().advertisement.all().first()))
            print('Number by contenttype', ctype.id)
            ctype_id=ctype.id
        except:
            self_model.DoesNotExist
        try:
            cache.set("content_type", ctype.id, 60)
        except UnboundLocalError as e:
            print(e)
        return Response([serializer.data, {"Number by contenttype (blank if None)":f"{ctype_id}"}, \
                         {"message": "Selected Category and number by ContentType advertisement concerned"}], status=status.HTTP_200_OK)
    def get_object(self):#This is for retrieveupdate
        queryset = self.filter_queryset(self.get_queryset())
        print('queryset', queryset)
        obj = queryset.get(pk=self.request.data['parent'])
        # print('self ======= ====== ======', self.request.data['parent'])
        print('obj', obj)
        return obj


def ChooseFilterSet():
    filters_list = [CarFilter,]
    
    for i in filters_list:
        try:
            content_type = cache.get("content_type")
            if ContentType.objects.get_for_id(content_type) == ContentType.objects.get_for_model(i.Meta.model):
                filterset = i
                print('filterset' , filterset)
                return  filterset
        except ContentType.DoesNotExist:
            return None
        except ProgrammingError as e:
            print(e, 'строка 524')
        except ConnectionError as e:
            print(e, 'строка 455')


@extend_schema(
    tags=["Общая логика (Контент Тайп) / ContentType concerned"],
    summary="По модели получаем объект - объявление",
    parameters=[OpenApiParameter(name='id', description='Object Id', type=int)],
    # request=inline_serializer(name=), Не понимаю как подхватить сериализатор из списка в схему
    # responses=inline_serializer(),
)
class GetObjFmModelView(generics.ListAPIView, generics.RetrieveAPIView):
    filterset_class = ChooseFilterSet()
    pagination_class = StandardSetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id']
    # lookup_field=['id']
    # serializer_class = CarNameSerializer
    # queryset = Car.objects.all()

    def get_queryset(self):
        try:
            content_type = cache.get('content_type')
        except AttributeError as e:
            print(e, '- ad/views.py 470str')
        except TypeError as e:
            print(e, '- ad/views.py 472str')
        try:
            model_name=ContentType.objects.get_for_id(content_type).model
            model_name = model_name[0].upper() + model_name[1:]
            MyModel = apps.get_model(app_label='ad', model_name=model_name)
            queryset = MyModel.objects.all()

            return queryset
        except UnboundLocalError as e:
            print(e, ' - ad/views.py 549str')
        except TypeError as e:
            print(e, '- ad/views.py 551str')
        except ContentType.DoesNotExist:
            queryset = None#{"ContentType is None":"ContentType is None"}
        return queryset


    def get_serializer_class(self):
        serializer = DefaultSerializer
        serializer_list = [CarNameSerializer, MenClothesSerialiser, MenShoesSerialiser, WemenClothesSerialiser, WemenShoesSerialiser, \
            ChildClothesShoesSerialiser, BagsKnapsacksSerialiser]# Будем добавлять сериализаторы по мере наполнения моделями

        try:
            content_type = cache.get('content_type')
            for i in serializer_list:

                if ContentType.objects.get_for_id(content_type) == ContentType.objects.get_for_model(i.Meta.model):
                    serializer = i
                    return serializer
                    return [j for j in serializer_list if ContentType.objects.get_for_id(content_type) == ContentType.objects.get_for_model(i.Meta.model)]
                else:
                    return serializer
        except AttributeError as e:
            print(' - ad/views.py 572str - ', e)
        except UnboundLocalError as e:
            print(' - ad/views.py 574str - ', e)
        except TypeError as e:
            print(' - ad/views.py 576str - ', e)

        print('error occured swagger serializer' , serializer)
        return serializer


    def get(self, request):

        obj_id = ""
        queryset = self.filter_queryset(self.get_queryset())
        print("queryset in class", queryset)
        if not queryset:
            return redirect(reverse("ad:get_model_fm_category")) 
        serializer=self.get_serializer_class()
        print('iiiiiiiiiiiiiii ==== serializer', serializer)
        serializer = serializer(queryset, many=True)
        content_type = cache.get('content_type')
        print('serialiser', serializer)
        obj_id = serializer.data[0]['id']
        cache.set_many({"obj_id": obj_id, "content_type":content_type}, 60)
        print(' ============ serializer.data', serializer.data)
        return Response([serializer.data, {"content_type":content_type, "obj_id":obj_id, "message":"Got content_type and obj_id and pass it in cache at endpoin: like_add "}], status=status.HTTP_200_OK)


    serializer_class = (CarNameSerializer,)
    queryset = get_queryset




"""Func has content_type on enter in cache from GetModelFmCategoryView, request.user choose objct with LikeSerializerCreate, Like adds"""
@extend_schema(
    tags=["Лайки / Likes"],
    description="Добавление лайков пользователем / Likes for the instance",
    summary="Добавление лайков пользователем / Add like by request user",
    # parameters=[
        # OpenApiParameter("content_type", OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=True,),
    #     OpenApiParameter("object_id", OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=True,),
    #     OpenApiParameter("is_liked", OpenApiTypes.BOOL, location=OpenApiParameter.QUERY, required=True,)
        # ],
    request=LikeSerializerCreate,
    responses={
            201: OpenApiResponse(response=LikeSerializerCreate,
                                 description='Created. New like in response'),
            200: OpenApiResponse(description=("Like from the user already exists")),
            400: OpenApiResponse(description='Bad request (something invalid)'),
        },
)
@api_view(['POST'])
def like_add(request, is_liked=False):#, ContentType_id=8, obj_id=2, **kwargs):
    print('request.user', request.user)
    if request.user.is_anonymous:
        return redirect(reverse("users:sign_in_email"))
    dict_of_cache = cache.get_many(["content_type", "obj_id"])
    content_type = dict_of_cache['content_type']
    obj_id = dict_of_cache['obj_id']
    print('content_type, obj_id', content_type, obj_id)

    user_instance = request.user
    if request.method == "POST":
        serializer = LikeSerializerCreate(data=request.data)
        if serializer.is_valid():

            print('serializer.data', serializer.data)
            is_liked = serializer.validated_data.get('is_liked')

            try:
                print('11111111111111')
                like_instance = Like.objects.get(user=user_instance, content_type=ContentType.objects.get_for_id(content_type), object_id=obj_id, is_liked=is_liked)
                like_instance.save()
                # return Response(serializer.data)
                # like_instance = Like.objects.get(user=user_instance, content_type=content_type, object_id=object_id,
                #                                  is_liked=is_liked)
                # return Response([{"message": "Лайки уже существуют"}, serializer.data], status=status.HTTP_200_OK)
            except Like.DoesNotExist:
                print('22222222222222222222222222')
                like_instance = Like.objects.create(user=user_instance, content_type=ContentType.objects.get_for_id(content_type), object_id=obj_id,
                                                    is_liked=is_liked)
                # like_instance = Like(user=user_instance, content_object=like_instance, is_liked=is_liked)
                like_instance.save()
                # serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""Function for test likes: In: user and car_object (form for this, must be commented if migrations needed), all must be deleted after testing,
  Out: like added from user to car object"""

# from django.views.decorators.csrf import csrf_exempt 
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# from django.http import HttpResponse, JsonResponse 
# from django import forms
# from django.shortcuts import redirect
# from django.urls import reverse
# from rest_framework.parsers import JSONParser
# from django.contrib.contenttypes.models import ContentType

# class LikeForm(forms.Form):
#     queryset = Car.objects.all()
#     choices = [(f"{i}", i) for i in queryset]
#     choose_car = forms.ChoiceField(choices=choices)

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

####################################
"""Func returns notifications requested user reffered"""


@extend_schema(
    tags=["Уведомления / Notifications"],
    summary=["Уведомляем при входе пользователя о его новых сообщениях / Notification by user's enter notifies about new messages"],
    description=["Notifications by user"],
    request=NotificationSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description=(
                    "Like from the user already exists"
            ),
            response=NotificationSerializer,
        ),
    },
)
@api_view(["GET"])
def notifications_by_enter(
        request):  # If requestuser authentificated and if there mssgs for request user return numb of mssgs
    if not request.user.is_authenticated:
        # login_url = reverse_lazy('bulletin:sign_in_email')
        # return redirect(login_url)
        return Response({"message": "Вы неавторизированы. Перенаправляем на авторизацию"},
                        status=status.HTTP_400_BAD_REQUEST)
    notifications = Notification.objects.all().filter(
        key_to_recepient=request.user.email) | Notification.objects.all().filter(key_to_recepient=request.user.id)
    num_mssgs = notifications.count()
    serializer = NotificationSerializer(notifications)
    if not notifications:
        return Response([serializer.data, {"message": f"Дорогой {request.user.email}у вас нет сообщений"}],
                        status=status.HTTP_200_OK)
    return Response([serializer.data, {"message": f'Дорогой {request.user.email}, у вас {num_mssgs} сообщений'}],
                    status=status.HTTP_200_OK)
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = CategoryFilter  # Use the custom filter class

    # def get_queryset(self):
    #     user = self.request.user 
    #     req_serializer = CategorySerializer(data=self.request.GET.dict())
    #     if req_serializer.is_valid():  
    #         # if 'page_size' in self.request.GET:
    #         #     self.pagination_class = PaginationSetup.custom_standard_pagination(page_size=self.request.GET['page_size'])
    #         if 'crop_type_id' in self.request.GET:
    #             return Category.objects.filter(crop_type=self.request.GET['crop_type_id'], country=self.request.GET['country_id'])

    #         return Category.objects.filter(
    #             category=self.request.GET['category_id']
    #         ) 
    #     raise APIException(req_serializer.errors)

# class RetrieveCategoryView(generics.ListAPIView, generics.RetrieveUpdateAPIView,filters.SearchFilter):# MultipleFieldLookupMixin,  ):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     # filter_backends = [filters.SearchFilter]
#     # search_fields = ['name',]
#     lookup_fields = ['id']
#     # ordering_fields = ['name', ]

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data)
#         # return super().list(request, *args, **kwargs)

#     def get_queryset(self):
#         # return super().get_queryset()
#         queryset = Category.objects.all()
#         category = self.request.query_params.get('name')
#         if category is not None:
#             queryset = queryset.filter(category__name=category)
#         print('1111111111111111111')
#         return queryset

#     def get_object(self):
#         print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
#         queryset = self.get_queryset()             # Get the base queryset
#         queryset = self.filter_queryset(queryset)  # Apply any filter backends
#         filter = {}
#         for field in self.lookup_fields:
#             print('field', field)
#             if self.kwargs.get(field): # Ignore empty fields.
#                 filter[field] = self.kwargs[field]
#         print('filter', filter, TypeError(filter))
#         obj = get_object_or_404(queryset, **filter)  # Lookup the object
#         self.check_object_permissions(self.request, obj)
#         return obj
    # def get_object(self):
    #     queryset = self.get_queryset()
    #     filter = {}
    #     for field in self.multiple_lookup_fields:
    #         filter[field] = self.kwargs[field]

    #     obj = get_object_or_404(queryset, **filter)
    #     self.check_object_permissions(self.request, obj)
    #     print('000000000000000000000000000000000000000000000')
    #     return obj

    #     # print('6666666666666666666666666', self.get_object())
    #     # return ContentType.objects.get_for_model()
    # def get_search_fields(self, view, request):
    #     if request.query_params.get('name_only'):
    #         return ['name']
    #     return super(RetrieveCategoryView, self).get_search_fields(view, request)
        # return super().get_search_fields(view, request)

# """Function add like from requested user"""
# class GetCategorySerializer(serializers.Serializer):
#     queryset = Category.objects.all()
#     choices = [(f"{i}", i) for i in queryset]
#     choose_category = serializers.ChoiceField(choices=choices)
# category = CategorySerializer(Category.objects.all, many=True)

# @extend_schema(
# methods=['GET', 'POST'],
# request=CategorySerializer,
# responses={
# status.HTTP_200_OK: OpenApiResponse(
# description="В",
# response=CategorySerializer,
# ),
# },
# examples=[{OpenApiExample(
# "Example",
# value={
# "name":"Category Example",
# "category":"category_id",
# },
# request_only=True
# )

# }],
# # components=[{
# # 'schemas':{'Category':{
# # 'type':'string',
# # 'enum':[i for i in Category.objects.all()],
# # 'description': 'Category ID',
# # }}
# # }],
# )
# @api_view(["GET", "POST"])
# def get_model_fm_category(request):
#     serializer=CategorySerializer(data=Category.objects.all(), many=True)#data=request.data)
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = GetCategorySerializer(data=request.data)
#         if serializer.is_valid():
#             category = Category.objects.get(name=serializer.validated_data['choose_category'])
#             print(category)
#             print(type(category.advertisement.all().first()))
#             ctype = ContentType.objects.get_for_model(model=type(category.advertisement.all().first()))
#             print(ctype.id)
# # serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def choose_serializer(model):
    print('model======================', model.__name__)
    model =  model.__name__
    mod_lst = ["MenClothes", "WemenClothes", "MenShoes", "WemenShoes", "ChildClothesShoes", "BagsKnapsacks", "Car"]
    # ser_dict = {"MenClothes":MenClothesSerialiser, "WemenClothes": WemenClothesSerialiser, "MenShoes":MenShoesSerialiser,\
    #             "WemenShoes" :WemenShoesSerialiser, "ChildClothesShoes":ChildClothesShoesSerialiser, "BagsKnapsacks":BagsKnapsacksSerialiser}
    ser_lst =  [MenClothesSerialiser, WemenClothesSerialiser, MenShoesSerialiser, WemenShoesSerialiser, ChildClothesShoesSerialiser, 
   BagsKnapsacksSerialiser, CarSerializer]
    
    if str(model) in mod_lst:
        index = mod_lst.index(model)
        return ser_lst[index]
Car

@extend_schema(
    tags=["Личные вещи/ Personal items"],
    # summary=" Car list and car creation",
    request=MenClothesSerialiser,
    responses={status.HTTP_200_OK: OpenApiResponse(
        description="Объявление создано",
        response=MenClothesSerialiser,
    ), }

)
class MenClothesList(generics.ListCreateAPIView):# Пока без криейта, чтобы сделать криейт, нужны криейтовские сериалайзеры, по аналогии с CarCreateSerializer
    queryset = MenClothes.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = MenClothesSerialiser
    pagination_class =  OrdinaryListPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenClothesFilter
    filter_backends = [DjangoFilterBackend]

@extend_schema(
    tags=["Личные вещи/ Personal items"],
    # summary=" Car list and car creation",
    request=MenShoesSerialiser,
    responses={status.HTTP_200_OK: OpenApiResponse(
        description="---------------------",
        response=MenShoesSerialiser,
    ), }

)
class MenShoesList(generics.ListCreateAPIView):# Пока без криейта, чтобы сделать криейт, нужны криейтовские сериалайзеры, по аналогии с CarCreateSerializer
    queryset = MenShoes.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = MenShoesSerialiser
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenShoesFilter
    filter_backends = [DjangoFilterBackend]


@extend_schema(
    tags=["Личные вещи/ Personal items"],
    # summary=" Car list and car creation",
    request=BagsKnapsacksSerialiser,
    responses={status.HTTP_200_OK: OpenApiResponse(
        description="--------------------------",
        response=BagsKnapsacksSerialiser,
    ), }

)
class BagsKnapsacksList(generics.ListCreateAPIView):# Пока без криейта, чтобы сделать криейт, нужны криейтовские сериалайзеры, по аналогии с CarCreateSerializer
    queryset = BagsKnapsacks.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = BagsKnapsacksSerialiser
    filter_backends = [DjangoFilterBackend]
    filterset_class = BagsKnapsacksFilter
    filter_backends = [DjangoFilterBackend]

@extend_schema(
    tags=["Личные вещи/ Personal items"],
    # summary=" Car list and car creation",
    request=ChildClothesShoesSerialiser,
    responses={status.HTTP_200_OK: OpenApiResponse(
        description="-----------------------",
        response=ChildClothesShoesSerialiser,
    ), }

)
class ChildClothesShoesList(generics.ListCreateAPIView):# Пока без криейта, чтобы сделать криейт, нужны криейтовские сериалайзеры, по аналогии с CarCreateSerializer
    queryset = ChildClothesShoes.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = ChildClothesShoesSerialiser
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChildClothesShoesFilter
    filter_backends = [DjangoFilterBackend]

@extend_schema(
    tags=["Личные вещи/ Personal items"],
    # summary=" Car list and car creation",
    request=WemenClothesSerialiser,
    responses={status.HTTP_200_OK: OpenApiResponse(
        description="---------------",
        response=WemenClothesSerialiser,
    ), }

)
class WemenClothesList(generics.ListCreateAPIView):# Пока без криейта, чтобы сделать криейт, нужны криейтовские сериалайзеры, по аналогии с CarCreateSerializer
    queryset = WemenClothes.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = WemenClothesSerialiser
    filter_backends = [DjangoFilterBackend]
    filterset_class = WemenClothesFilter
    filter_backends = [DjangoFilterBackend]

@extend_schema(
    tags=["Личные вещи/ Personal items"],
    # summary=" Car list and car creation",
    request=WemenShoesSerialiser,
    responses={status.HTTP_200_OK: OpenApiResponse(
        description="О-------------",
        response=WemenShoesSerialiser,
    ), }

)
class WemenShoesList(generics.ListCreateAPIView):# Пока без криейта, чтобы сделать криейт, нужны криейтовские сериалайзеры, по аналогии с CarCreateSerializer
    queryset = WemenShoes.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = WemenShoesSerialiser
    filter_backends = [DjangoFilterBackend]
    filterset_class = WemenShoesFilter
    filter_backends = [DjangoFilterBackend]

"""Получение объявлений по польльзователю"""
@api_view(["GET"])
def get_ads_fm_user(request):
    user = request.user
    app_models = apps.get_app_config('ad').get_models()
    if request.method == "GET":
        lst_data =[]
        for i in app_models:
            try:
                instance = i.objects.all().filter(profilee=user.profile)
                serializer=choose_serializer(i)
                lst_data.append(serializer(instance, many=True).data)
                
            except AttributeError as e:
                print(e)
            except FieldError as e:
                print(e)
        return Response(lst_data, status=status.HTTP_200_OK)
    
    
"""Func add view and returns views by obj (ad)"""
@extend_schema(
    tags=["Просмотры. На входе категория-модель, номер объявления, на выходе список просмотрров объявления с добавлением одного просмотра (сейчас добавляет п-любому), \
          этого опльзователя / Views. Number of model and number of object by enter, list of views with adding (adds anyway) the current by exit"],
    summary="Просмотры объявления, добавляется по Профилю / List of views the advertisement concerned, returns likes by obj (ad)",
    request=ViewsSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Views by advertisement",
            response=ViewsSerializer,
        ),
    },
)
@api_view(["GET"])  # Здесь в кэше уже должны быть модель и ноер объекта
def views_list_obj(request):
    try:
        dict_of_cache = cache.get_many(["content_type", "obj_id"])
        content_type = dict_of_cache['content_type']
        obj_id = dict_of_cache['obj_id']
    except KeyError as e:
        print(e)
        return redirect(reverse("ad:get_model_fm_category"))# Если в кэше нет обджекта, редиректим
    # content_type = ContentType.objects.get_for_id(ContentType_id)
    # obj = content_type.get_object_for_this_type(pk=obj_id)
    # content_type = ContentType.objects.get_for_model(obj)
    profile_instance = request.user.profile
    if request.method == "GET":
        view_instance = Views(profile=profile_instance, content_type=ContentType.objects.get_for_id(content_type), object_id=obj_id)
        view_instance.save()
        views_queryset_obj = Views.objects.all().filter(content_type=content_type).filter(object_id=obj_id)
        serializer = ViewsSerializer(views_queryset_obj, many=True)
        print('view_instance.total_viwes_profile, view_instance.total_viwes_object', view_instance.total_viwes_profile, view_instance.total_viwes_object)#Views.objects.get(id=obj_id)
        return Response(serializer.data, status=status.HTTP_200_OK)
