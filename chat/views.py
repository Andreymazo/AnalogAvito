from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import Mssg
from chat.serializers import MssgDetailSerializer, MssgSerializer
from drf_spectacular.utils import (
    extend_schema
)
from users.models import CustomUser
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.shortcuts import redirect
from django.urls import reverse


@extend_schema(
    tags=["Чат (переписка между пользователями по поводу объявления) / Chat between users advertisement concerned"],
    summary="Синхронная переписка, модель Mssg, в методе POST можно создавать сообщение с полем text если до этого выбрали модель и само объявление / sync chat between users advertisement conserned, message can be created after model and object choosen",
    request=MssgSerializer,
    # parameters=[OpenApiParameter('limit', exclude=True), OpenApiParameter('offset', exclude=True), \
    #             OpenApiParameter('ordering', exclude=True), OpenApiParameter('page', exclude=True),]
)
@api_view(["GET", "POST"])
def message_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse("users:sign_in_email"))
    
    # content_type_dict={}
    # content_type_dict = cache.get_many(["content_type", "obj_id"])
    # content_type = content_type_dict["content_type"]
    # obj_id = content_type_dict["obj_id"]
    # print('"content_type", "obj_id"', content_type, obj_id)
    try:
        content_type_dict = cache.get_many((["content_type", "obj_id"]))
        content_type = content_type_dict["content_type"]
        obj_id = content_type_dict["obj_id"]
        print('"content_type", "obj_id"', content_type, obj_id)
        model_name=ContentType.objects.get_for_id(content_type).model
        model_name = model_name[0].upper() + model_name[1:]
        MyModel = apps.get_model(app_label='ad', model_name=model_name)
        content_object = MyModel.objects.get(id=obj_id)
        print('MyModel', MyModel)
        print('content_object.profile.user.email', content_object.profile.user.email)
    except:
        ContentType.DoesNotExist
        print("Model wasnt choosen")
        # return redirect(reverse("ad:get_model_fm_category"))
        if request.method == "GET":
            mssg_queryset = Mssg.objects.all().filter(key_to_recepient=request.user.email)| \
            Mssg.objects.all().filter(key_to_recepient=request.user.id) # in commented below - 
        # add advertisements the object concerned, maybe admin wants to see.  
        #| Mssg.objects.all().filter(content_type=content_type, object_id=obj_id)#content_object по нему не фильтрует почемуто
            serializer = MssgSerializer(mssg_queryset, many=True) 
            return Response([serializer.data, {"message":"Model wasnt choosen. Choose model, object, then message to owner"}], status=status.HTTP_200_OK)
            
    if request.method == 'GET':
        mssg_queryset = Mssg.objects.all().filter(key_to_recepient=request.user.email)| \
            Mssg.objects.all().filter(key_to_recepient=request.user.id) # in commented below - 
        # add advertisements the object concerned, maybe admin wants to see.  
        #| Mssg.objects.all().filter(content_type=content_type, object_id=obj_id)#content_object по нему не фильтрует почемуто
        serializer = MssgSerializer(mssg_queryset, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':#Создаем сообщение, привязанное к объявлению
        serializer = MssgSerializer(data=request.data)
        if serializer.is_valid():
            # print('serializer', serializer)
            message_value = serializer.validated_data.get('text')
            content_object=MyModel.objects.get(id=obj_id)
            mssg_instance = Mssg(text = message_value, user=request.user, key_to_recepient=content_object.profile.user.email, content_object=content_object)
            mssg_instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=["Чат (переписка между пользователями по поводу объявления) / Chat between users advertisement concerned"],
    summary="модель Mssg, в методе GET само объявление / object",
    request=MssgDetailSerializer,  
)
@api_view(["GET", "PUT", "DELETE"])
def message_detail(request, pk):
    try: 
        mssg_instance = Mssg.objects.get(pk=pk) 
    except Mssg.DoesNotExist: 
        return HttpResponse(status=404)
    if request.method == 'GET': 
        serializer = MssgDetailSerializer(mssg_instance)
        return Response([serializer.data, {"message":"mssg detailed"}], status=status.HTTP_200_OK) 
    elif request.method == 'PUT': 
        data = JSONParser().parse(request) 
        serializer = MssgDetailSerializer(mssg_instance, data=data) 
  
        if serializer.is_valid(): 
            serializer.save() 
            return Response([serializer.data, {"message":"mssg updated"}], status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
  
    elif request.method == 'DELETE': 
        mssg_instance.delete() 
        return Response({"message":"mssg deleted"}, status=status.HTTP_204_NO_CONTENT) 