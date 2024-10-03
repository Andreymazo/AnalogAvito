# import datetime
import re
from django.core.management import BaseCommand
from django.contrib.gis.geos import Point
from map.models import Marker
import csv

'''На входе список в котором строка, на выходе список с тремя строками Имя, Шир, Долг'''
def get_three_colomns(s1):
    s1=str(s1)
    print('------------------s', s1, 'type' , type(s1))
    #Gather All names in 1st col, Lat - 2, Long -3
    first_lst=[]
    n=1
    # pattern=r"(\d+\.\d{2,4})"
    # pattern=r'(\d{2}\.\d{2,4})'
    pattern=r'^\+?1?\d{8,15}$'
    # pattern = r"^[-+]?[0-9]*\.?[0-9]+$"
    print(bool(re.fullmatch(pattern, s1)))
    # while not bool(re.search(pattern, s1)):
# https://regexr.com/86kqs
# https://www.geeksforgeeks.org/python-check-for-float-string/
def ff():
    # Marker.objects.create(name='1st', location=Point(50, 30))
    with open("result.csv","r") as source:
        
    # with open("out.csv","r") as source:
        # rdr=[line.split() for line in source]#From str to list #451819,Svoboda,Svoboda,56.96613,34.19721,P,PPL,RU,77,0,243,Europe/Moscow,2011-07-09
        # rdr= csv.reader(source)
        with open("result1.csv","w+", newline='\n') as result:
            wtr= csv.writer( result , delimiter=',')
            for r in source:
                r=r.split(',')
                # print('222222', r_new, r_new[1])
                # print('222222', get_three_colomns(r), type(get_three_colomns(r)))#['451747\tZyabrikovo\tZyabrikovo\t\t56.84665\t34.7048\tP\tPPL\tRU\t\t77\t\t\t\t0\t\t204\tEurope/Moscow\t2011-07-09'] <class 'list'>
                # wtr.writerow(r)
                # wtr.writerow( (r[2], r[3], r[4]) )
                get_three_colomns(r)

class Command(BaseCommand):

    def handle(self, *args, **options):
        # ff()
        # get_three_colomns(32.3232)
        get_three_colomns(+7852718184)
