import json
from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from config import constants
from users.models import Profile
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    OpenApiTypes,
    
)


def MarkersMap(request):
    
    # queryset = Marker.objects.all()
    queryset = Profile.objects.all()
    # queryset={}
    context = {'queryset':queryset}
    context['queryset'] = json.loads(serialize('geojson', queryset))
    return render(request, "map/templates/map/home_map.html", context)


from django.views.generic.base import TemplateView
from map.models import Marker

# from map.models import ModelGis
# class MarkersMapView(TemplateView):
#     """Markers map view."""

#     template_name = "map/templates/map/home_map.html"
@extend_schema(
    tags=["Карта/ Map"],

)
class MarkersMapView(TemplateView):
    model = Profile
    template_name = 'map/templates/map/home_map.html'
    

    def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        modelgis = Profile.objects.all()
        context['queryset'] = json.loads(serialize('geojson', modelgis))
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    

    
# @extend_schema(
#         request=CityCreateSerializer,
#         responses={201: CityCreateSerializer},
#     )
# @api_view([ 'POST'])
# # @authentication_classes([TokenAuthentication])
# # @permission_classes((permissions.AllowAny,))
# def rus_city_request(request):
#     # """
#     # List all categories
#     # """
#     # if request.method == 'GET':
    
#     #     paginator = PageNumberPagination()
#     #     paginator.page_size = 10
#     #     paginator.last_page_strings = ('last',)
#     #     result_page = paginator.paginate_queryset(RusCity.objects.all(), request)
#     #     serializer = CitySerializer(result_page, many=True)

#     #     return paginator.get_paginated_response(serializer.data)
    
#     # if request.method == 'POST':
#     #     serializer = CityCreateSerializer(data=request.data, context={'request': request})
#     #     print('does we here?????????????????????')
#     #     if serializer.is_valid(raise_exception=True):
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Получаем ip"""
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

"""Получаем локацию по ip"""
def location(ip: str):
    ip='90.156.226.147'
    response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
    if response.status_code == 404:
        print("Oops")
    result = response.json()
    print('result ip', result)
    if result["status"] == "fail":
        return HttpResponse("Enter the correct IP address")

    # record = []
    lat=result['lat']
    lon=result['lon']
    # for key, value in result.items():
    #     record.append(value)
    #     print(f"[{key.title()}]: {value}")
    # return tuple(record)
    return lat, lon


"""Получаем по ip координаты и по ним и по ключу отправляем запрос на http://127.0.0.1:8002/ обратно получаем город"""
@csrf_exempt
@extend_schema(
    tags=["Карта/ Map"],
    responses={
        200: OpenApiTypes.ANY,
    }

)
@api_view(["GET"])
def query_rus_city(request):
    # form = RealEstForm(request.POST)
    ip = get_client_ip(request)
    lat, lon = location(ip)
    print('ip', ip)
    print('Получаем локацию по ip', location(ip))
    result = False
    url = 'http://127.0.0.1:8002/rus_cities'
    data = {
            "key_reply": constants.KEY_REPLY,
            "shirota" :lat,
            "dolgota": lon
            # "shirota": ip.get('shirota_form_value'),
            # "dolgota": ip.get('dolgota_form_value'),
            }
    response = requests.get(url, params=data)#, headers={ 'X-CSRFToken': clear_token})
    print('response.json()',response)
    data=response.json()
    return Response(data)
    return HttpResponse(response.json())
    # context = {
    #     'form':form
    # }
    # if request.method == "POST":   
    #     if form.is_valid():
    #         instance = form.save(commit=False)
    #         print('jjjjjjjjjjjjjjjjjjjjjjjjj')
    #         cad_num_form_value = form.cleaned_data['cad_num']
    #         shirota_form_value = form.cleaned_data['shirota']
    #         dolgota_form_value = form.cleaned_data['dolgota']
    #         # instance = HistoryApi.objects.create(cad_num=cad_num_form_value, shirota=shirota_form_value, dolgota=dolgota_form_value)
    #         result = False
    #         url = 'http://localhost:8002'
    #         data = {
    #         "cad_num": cad_num_form_value,
    #         "shirota": shirota_form_value,
    #         "dolgota": dolgota_form_value,
    #         }
    #         response = requests.post(url, params=data)#, headers={ 'X-CSRFToken': clear_token})


    #         # time.sleep(2)
    #         print('response.text', response.text)
    #         if response.text=='false':
    #             result=False
    #         if response.text=='true':
    #             result=True
    #         context = {
    #     'form':form,
    #     'result':response.text
    # }
    #         instance = HistoryApi.objects.create(cad_num=cad_num_form_value, shirota=shirota_form_value, dolgota=dolgota_form_value, result=result)
    #         instance.save()

    #     return render(request, 'testrestapi/templates/testrestapi/query.html', context) 
    # else:

    #     form = RealEstForm()

    # return render(request, 'testrestapi/templates/testrestapi/query.html', context) 



