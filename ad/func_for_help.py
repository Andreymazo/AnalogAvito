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
    
from ad.filters import CarFilter


def save_file(file, full_path):
    with open(full_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)    

# def ChooseFilterSet():
#     filters_list = [CarFilter,]
#     content_type = cache.get("content_type")
#     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++content_type', content_type)
#     for i in filters_list:
#         try:
#             if ContentType.objects.get_for_id(content_type) == ContentType.objects.get_for_model(i.Meta.model):
#                 filterset = i
#                 print('filterset' , filterset)
#                 return  filterset
#         except ContentType.DoesNotExist:
#             return None
         