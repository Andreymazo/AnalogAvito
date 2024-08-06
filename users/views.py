# import json
# from django.shortcuts import render
# from django.core.serializers import serialize
# from django.contrib.auth import get_user_model 
# from rest_framework.response import Response
# from rest_framework import status, mixins
# from ad.models import Car
# from rest_framework.decorators import api_view
# from ad.models import IP
# from users.models import Profile
# from rest_framework.generics import ListCreateAPIView#, RetrieveAPIView, GenericAPIView


# # Метод для получения айпи
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR') # В REMOTE_ADDR значение айпи пользователя
#     return ip
# """Создаем просмотры пользователя по айпи на объявления автомобиль"""
# @api_view(["POST"])
# def views_user(request):
    
#     serializer=ViewsSerialiser(data=request.data)

#     if serializer.is_valid():
#         ip = serializer.validated_data.get("ip")
#         content_object = serializer.validated_data.get("content_object")
#         # car_value = Car.objects.get(profile=profile)
#     user=get_user_model()
#     try:
#         serializer = ViewsSerialiser()
#         ip = get_client_ip(request)
#         # ip_value = IP.objects.filter(profile=profile.id).get_or_create(ip=ip)
#     except Profile.DoesNotExist:
#         return Response({"message":"Profile doesn't exists. Create profile"}, status=status.HTTP_206_PARTIAL_CONTENT)
#     return Response([serializer.data, {"massage": "Get or created view value"}], status=status.HTTP_200_OK)



# class ViewsList(ListCreateAPIView):
#     queryset = Views.objects.all()
#     serializer_class = ViewsSerialiser
   