from django.db import IntegrityError
from rest_framework import generics
from ad.models import Category, Car, Like, Images, Views
from users.models import Notification
from ad.serializers import CarCreateSerializer, LikeSerializer, LikeSerializerCreate, NotificationSerializer
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


@extend_schema(
    tags=["Категории/Categories"],
    summary="Список всех категорий",
    request=CarCreateSerializer,
)
class CategoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = "Category list"
    filter_fields = (
        '-created',
    )


@extend_schema(
    tags=["Автомобили/Cars"],
    summary=" Car list and car creation",
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
    # name = "Car list"
    # filter_fields = ( 
    #     '-created', 
    # )
    # def list(self, request, *args, **kwargs):
    #     print('ggggggggggggggggg', request.user, self.request.user)
    #     # print('cache================', cache._connections.__dict__)
    #     # print("req session ===============", request.session["user_id"])
    #     # print(cache.get('access_token'))
    #     # print(cache.get('refresh_token'))
    #     return super().list(request, *args, **kwargs)
    # """This func was necessary if serializer.data after serializer.save() called, since we commented serializer.save() in perform_create no need this"""
    # """Костыль конечно, но пока не знаю как пройти ошибку, вроде при тестировании в сваггере ее нет, была в браузере и при 1 фото сериализаторе"""
    # def change_image_to_string(self, obj):
    #     if type(obj) == InMemoryUploadedFile:
    #         return f"images/{obj}"
    #     if type(obj) == TemporaryUploadedFile:
    #         return f"images/{obj}"
    #     if type(obj) == Profile:
    #         return str(obj)
    #     else:
    #         return obj

    # def create(self, request, *args, **kwargs):#, ContentType_id=16, obj_id=6
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     # print('serializer.data', serializer.data)
    #     # content_type = ContentType.objects.get_for_id(ContentType_id)
    #     # obj = content_type.get_object_for_this_type(pk=obj_id)
    #     # print('77777777777777777777777777', content_type, obj)
    #     s = OrderedDict([(k, self.change_image_to_string(v)) for k,v  in serializer.validated_data.items()])
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(s)
    #     print('headers----------------', headers)
    #     return Response([s, {"message": "Uploaded"}], status=status.HTTP_201_CREATED, headers=headers)
    #     # car_instance, created = Car.objects.get_or_create(
    #     #         by_mileage=serializer.validated_data.get('by_mileage', None),
    #     #         year=serializer.validated_data.get('year', None), 
    #     #         brand=serializer.validated_data.get('brand',None), 
    #     #         model=serializer.validated_data.get('model', None), 
    #     #         mileage=serializer.validated_data.get('mileage', None),
    #     #         price=serializer.validated_data.get('price',None), 
    #     #         category_id=Category.objects.get(name='Транспорт',).id,
    #     #         profile = Profile.objects.get(user=request.user)
    #     #         )#category_id=validated_data.get('category_id', None).id # Can choose

    #     # try:
    #     #     #Photoes anyway will be loaded even the same
    #     #     image_instance, created = Images.objects.get_or_create(
    #     #             content_type = ContentType.objects.get_for_model(type(car_instance)),object_id = car_instance.id,
    #     #             title=serializer.validated_data.get('title'),image = serializer.validated_data.get('image'),
    #     #             )
    #     #     # return Response( [serializer.data, {"message": "This photo already uploaded"}], status=status.HTTP_206_PARTIAL_CONTENT)
    #     # except Images.MultipleObjectsReturned:
    #     #     image = Images.objects.filter(content_type = ContentType.objects.get_for_model(type(car_instance)),
    #     #             object_id = car_instance.id,title=serializer.validated_data.get('title'),).order_by('id').first()  

    # #     # try:
    # #     #     print('type image', type(serializer.validated_data.get('image')))
    # #     #     obj = Images.objects.get(content_type = ContentType.objects.get_for_model(type(car_instance)),object_id = car_instance.id,
    # #     #             title=serializer.validated_data.get('title'),image = serializer.validated_data.get('image'),)
    # #     #     print('444444444444444444444', obj)
    # #     #     return Response( [serializer.data, {"message": "This photo already uploaded"}], status=status.HTTP_206_PARTIAL_CONTENT)
    # #     # except Images.DoesNotExist:
    # #     #     obj = Images.objects.create(content_type = ContentType.objects.get_for_model(type(car_instance)),object_id = car_instance.id,
    # #     #                         title=serializer.validated_data.get('title'),image = serializer.validated_data.get('image'),)
    # #     #     return Response( [serializer.data, {"message": "Uploaded"}], status=status.HTTP_201_CREATED)

    #     # self.perform_create(serializer)
    #     # headers = self.get_success_headers(s)
    #     # return Response([s, {"message": "Uploaded"}], status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


@extend_schema(
    tags=["Автомобили/Cars"],
    summary="Создание объявления авто несколько фото подгружаются / Car multyple image creation",
    responses={
            201: OpenApiResponse(response=CarCreateSerializer,
                                 description='Created. New car in response'),
            400: OpenApiResponse(description='Bad request (something invalid)'),
        },
)

class CarCreate(generics.CreateAPIView, generics.ListAPIView):
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CarCreateSerializer

    # def get(self, request, *args, **kwargs):
    #     print('request.user', request.user)
    #     serializer = CarCreateSerializer(Car.objects.all(), many=True)
    #     # print("serializer.data ==", serializer.data)
    #     return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     serializer = CarCreateSerializer(request.data)
    #     print("serializer.data ==", serializer.data)
    #     return Response(serializer.data)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


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
@api_view(["GET"])  # Здесь лучше с фронта получать объект объявлений obj - объявление и сувать его в
# content_type = ContentType.objects.get_for_model(obj).
# Фронт не знает к какой модели какое число и потом номер инстанса надо брать. По obj фильтровать проще

def like_list_obj(request, obj):  # ContentType_id=16, obj_id=6):
    # content_type = ContentType.objects.get_for_id(ContentType_id)
    # obj = content_type.get_object_for_this_type(pk=obj_id)
    content_type = ContentType.objects.get_for_model(obj)
    if request.method == "GET":
        like_queryset_obj = Like.objects.all().filter(content_type=content_type).filter(object_id=obj.id)
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


"""Function add like from requested user"""


@extend_schema(
    tags=["Лайки / Likes"],
    description="Добавление лайков пользователем / Likes for the instance",
    summary="Add like by request user",
    parameters=[
        OpenApiParameter("content_type", OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=True,),
        OpenApiParameter("object_id", OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=True,),
        OpenApiParameter("is_liked", OpenApiTypes.BOOL, location=OpenApiParameter.QUERY, required=True,)
        ],
    request=LikeSerializerCreate,
    responses={
            201: OpenApiResponse(response=LikeSerializerCreate,
                                 description='Created. New like in response'),
            200: OpenApiResponse(description=("Like from the user already exists")),
            400: OpenApiResponse(description='Bad request (something invalid)'),
        },
)
@api_view(['POST'])
def like_add(request):  # is_liked=False, ContentType_id=16, obj_id=6):
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
                like_instance = Like.objects.get(user=user_instance, content_type=content_type, object_id=object_id,
                                                 is_liked=is_liked)
                return Response([{"message": "Лайки уже существуют"}, serializer.data], status=status.HTTP_200_OK)
            except Like.DoesNotExist:
                print('22222222222222222222222222')
                like_instance = Like.objects.create(user=user_instance, content_type=content_type, object_id=object_id,
                                                    is_liked=is_liked)
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
    serializer = NotificationSerializer(data=request.data)
    notifications = Notification.objects.all().filter(
        key_to_recepient=request.user.email) | Notification.objects.all().filter(key_to_recepient=request.user.id)
    num_mssgs = notifications.count()

    if not notifications:
        return Response([serializer.data, {"message": f"Дорогой {request.user.email}у вас нет сообщений"}],
                        status=status.HTTP_200_OK)
    return Response([serializer.data, {"message": f'Дорогой {request.user.email}, у вас {num_mssgs} сообщений'}],
                    status=status.HTTP_200_OK)
