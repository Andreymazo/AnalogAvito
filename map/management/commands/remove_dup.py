from shapely.geometry import Point, linestring
import csv
from django.core.management import BaseCommand

from users.models import Profile


"""Remove duplicates"""
def ff(lst_in):
    check_lst=[]
    n=0
    while len(lst_in)-1>=n:
        while lst_in[n] not in check_lst:
            check_lst.append(lst_in[n])
            n += 1
        n += 1
    # print(check_lst)
    return check_lst


"""Найдем расстояние между двумя точками"""
def dist_between():
    ppto_a = Profile.objects.last().location
    ppto_b = Profile.objects.first().location
    # print(ppto_a)
    dist = ppto_a.distance(ppto_b)*100
    print('distance in km', dist)

"""Проверяем на дистанцию от введенных координат и расстояния, возвращаем True или False"""
# https://stackoverflow.com/questions/32092584/geodjango-how-can-i-get-the-distance-between-two-points
# https://zach.se/geodesic-distance-between-points-in-geodjango/
def check_city(str_fm_csv, d,x,y):
    lat=str_fm_csv[:-2]
    long=str_fm_csv[:-1]
  

"""Выведем города в радиусе d км от заданных координат x,y. path - путь к нашим городам static/russian_cities/result7.csv"""
def f(d,x,y):
    lst_cities=[]
    with open('static/russian_cities/result7.csv', 'r') as f:
        with open('result.csv' , 'w+') as ff:
            wrt=csv.writer(ff)
            for i in f:
                print(i)#Ozero  ,Kyubozero  ,60.56859  ,36.43079
                if check_city(i):
                    lst_cities.append(i[1])
                else:
                    pass

class Command(BaseCommand):

    def handle(self, *args, **options):
        # ff([1,2,"3","rt","u",2,"rt","y",1])
        # f(100, 50.2423, 49.4923)
        dist_between()