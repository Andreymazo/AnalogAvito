# from django.core.cache import cache
# from django.contrib.contenttypes.models import ContentType
# def handle_uploaded_file(f):#request,
#     path = 'media/'
#     with open(path + f.name, 'wb+') as destination:
#             for chunk in f.chunks():
#                 destination.write(chunk)
#     with open(path + f.name, 'rb') as ff:
#         data = ff.read()
#         # print(data[0:34])
#         zip_obj= ZipFile(path + f.name,"r")
#         content_list = zip_obj.namelist()
#         # content_list = [(index,i) for index,i in enumerate(content_list_new)]
#         # for fname in content_list:
#         #     print(fname)
#         # zip_obj.extract("content.xml")
#         # zip_obj.close()
#     # file_to_work="content.xml"
#     # with open("content.xml", 'r') as f:
#     #      data = f.read()
#         file = f
#         return zip_obj, content_list, file
from rest_framework.response import Response
from rest_framework import status
from ad.filters import CarFilter
from django.contrib.contenttypes.models import ContentType
from ad.models import Views
from ad.serializers import BagsKnapsacksSerialiser, CarCreateSerializer, ChildClothesShoesSerialiser, MenClothesSerialiser, MenShoesSerialiser, WemenClothesSerialiser, WemenShoesSerialiser
from bulletin.serializers import CarSerializer
from users.models import Profile

def save_file(file, full_path):
    with open(full_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)    
"""Неавторизированный смотрит, но просмотры не прибавляются, авторизированный с профилем, прибавляеи просмотры, без профиля - на регистрацию"""
def add_view(serializer, request, pk):
    try:

        profile = request.user.profile
    except AttributeError:
        return Response([serializer.data,{"message": "Anonymoususer, Views dont counted"}],
                        status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({"message": "У вас нет Профиля, перенаправляем на регистрацию"},
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    print('view created') #Here we create view every time we enter the object
    content_type = ContentType.objects.get(model='car').id
    view_instance = Views(profile=profile, content_type=ContentType.objects.get_for_id(content_type), object_id=pk)
    view_instance.save()


"""Проверяет авторизирован ли и есть ли профиль"""
def check_if_authorised_has_profile(request):
    try:
        profile = request.user.profile
    except AttributeError:
        return Response([{"message": "Anonymoususer, put method is not allowed"}],
            status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Profile.DoesNotExist:
        return Response({"message": "У вас нет Профиля, перенаправляем на регистрацию"},
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



"""На входе модель на выходе ее сериалайзер"""
def choose_serializer(model):
    print('model======================', model.__name__)
    model =  model.__name__
    mod_lst = ["MenClothes", "WemenClothes", "MenShoes", "WemenShoes", "ChildClothesShoes", "BagsKnapsacks", "Car"]
    # ser_dict = {"MenClothes":MenClothesSerialiser, "WemenClothes": WemenClothesSerialiser, "MenShoes":MenShoesSerialiser,\
    #             "WemenShoes" :WemenShoesSerialiser, "ChildClothesShoes":ChildClothesShoesSerialiser, "BagsKnapsacks":BagsKnapsacksSerialiser}
    ser_lst =  [MenClothesSerialiser, WemenClothesSerialiser, MenShoesSerialiser, WemenShoesSerialiser, ChildClothesShoesSerialiser, 
   BagsKnapsacksSerialiser, CarCreateSerializer]
    
    if str(model) in mod_lst:
        index = mod_lst.index(model)
        return ser_lst[index]
