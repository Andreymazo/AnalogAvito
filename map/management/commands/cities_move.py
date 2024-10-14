# import datetime
import re
from django.core.management import BaseCommand
from django.contrib.gis.geos import Point
from map.models import Marker
import csv


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
                print('222222', r)
                # print('222222', get_three_colomns(r), type(get_three_colomns(r)))#['451747\tZyabrikovo\tZyabrikovo\t\t56.84665\t34.7048\tP\tPPL\tRU\t\t77\t\t\t\t0\t\t204\tEurope/Moscow\t2011-07-09'] <class 'list'>
                wtr.writerow(r)
                # wtr.writerow( (r[2], r[3], r[4]) )
                # get_three_colomns(r)



def remove_qutes():
    ff=[]
    with open("result1.csv", "r") as f:
        for i in f:
            print('i1', i)
            i=i.replace('"', '')
            print('i2', i)
            ff.append(i)
    with open('result3.csv', 'w+') as f:
        f.writelines(ff)





def what_line():
    with open('result4.csv', 'r') as f:
        for i in f:
            print(type(i))

"""1st - from 2nd - where to"""
def fm_str_lst(path1, path2):
    with open(path1, 'r') as f:
        with open(path2, 'w+') as ff:
            wtr = csv.writer(ff, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE, lineterminator='\n')
            for i in f:
                i=i.split(',', 1)
                print('i, type(i)', i, type(i))
                wtr.writerow(i)

'''На входе список в котором строка, на выходе список с тремя строками Имя, Шир, Долг'''
def remove_first_colomn_i(s1):#451756,Zarech’ye ,Zarech'ye ,56.68265 ,34.70984 ,P ,PPL ,RU ,77 ,0 ,178 ,Europe/Moscow ,2011-07-09 
    s1=str(s1)
    # print('------------------s', s1, 'type' , type(s1))
    first_lst=[]
    n=1
    pattern0 = r'^(\d{6,8})'
    # print('what we done', re.sub(pattern=pattern0, repl='', string=s1,))
    new_s1=re.sub(pattern=pattern0, repl='', string=s1,)[1:]
    return  new_s1
    # pattern=r"(\d+\.\d{2,4})"
    # pattern=r'(\d{2}\.\d{2,4})'
    # pattern1=r'^\+?1?\d{8,15}$'
    # pattern2=r'^\+?1?\d{8,15}$'
    # # pattern = r"^[-+]?[0-9]*\.?[0-9]+$"
    # print(bool(re.fullmatch(pattern0, s1)))
    # while not bool(re.search(pattern, s1)):
# https://regexr.com/86kqs
# https://www.geeksforgeeks.org/python-check-for-float-string/
# https://www.geeksforgeeks.org/regular-expression-python-examples/
def remove_first_col(path1,path2):
    with open (path1, 'r') as f:
        with open(path2, 'w+') as ff:
            wrt=csv.writer(ff,delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE, lineterminator='\n')
            for i in f:
                i=remove_first_colomn_i(i)
                i=i.split(',')
                wrt.writerow(i)
"""Remove duplicates"""
def remove_dup(lst_in):
        check_lst=[]
        n=0
        while len(lst_in)-1>=n:
            while lst_in[n] not in check_lst:
                check_lst.append(lst_in[n])
                n += 1
            n += 1
        # print(check_lst)
        return check_lst
def gather_first_col(s1):
    new_s1=s1.split(',')
    print('new_s1, type(new_s1)', new_s1, type(new_s1))#['Zyabrikovo  ', 'Zyabrikovo  ', '56.84665  ', '34.7048  ', 'P  ', 'PPL  ', 'RU  
    #', '77  ', '0  ', '204  ', 'Europe/Moscow  ', '2011-07-09   \n'] <class 'list'>
    pattern_1=r'[^0-9]'#Всё кроме цифр
    pattern_2=r'(\d{2}\.\d{2,4})'# формат: 32.3456
    first_col_lst=[]
    n=0
    finish=[]
    # while len(new_s1)-1>=n:
    #     print('ggggggggg', n, 'new_s1', new_s1)
    #     while not bool(re.search(pattern_2, new_s1[n])):
    #         first_col_lst.append(new_s1[n])
    #         n+=1
            
    #     first_col_lst=remove_dup(first_col_lst)
    #     print('first_col_lst', first_col_lst, n, 'new_s1', new_s1)
    #     finish=first_col_lst+ new_s1[n:n+2]
    #     print('finish', finish, type(finish), len(finish), n)
    #     return finish

    while len(new_s1)-1>=n:
   
        try:
            while not bool(re.search(pattern_2, new_s1[n])):
                first_col_lst.append(new_s1[n])
                n+=1
                
            first_col_lst=remove_dup(first_col_lst)
            # print('first_col_lst', first_col_lst, n)
            finish=first_col_lst+ new_s1[n:n+2]
            # n=n-1
            # print('new_s1', new_s1, type(new_s1), len(new_s1), n)
            return finish
        except IndexError as e:
            # print(e, 'deleting emptu string finish', finish)
            return finish 
        

def fix_second_col(path1, path2):
    with open(path1, 'r') as f:
        with open(path2, 'w+') as ff:
            wtr=csv.writer(ff)
            for i in f:
                # print(i, type(i))
                i=gather_first_col(i)
                # i=i.split(',')
                wtr.writerow(i)


def remove_blank_str(path1, path2):
    ff=[]
    with open(path1, 'r') as f:
        for i in f:
            if not len(i) == 1:
                ff.append(i)

            # print(i, 'len(i)', len(i))#len(i) 1
    with open(path2, 'w') as fff:
        fff.writelines(ff)

def remove_smth(path1, path2):
    ff=[]
    with open(path1, 'r', newline='\n') as f:
        for i in f:
            i=i.replace(',','')
            i=i.split()
            # i=' '.join(i)
            # print('i, type(i', i.replace(',',''))

            # i=i.replace('\t\t',' ')
            print('i',i)

            # if not len(i) == 1:
            ff.append(i)
    # new_ff=[]
    with open(path2, 'w+', newline='\n') as fff:
        # for i in ff:
    #         i=' '.join(i)
    #         print('i', i)
            # new_ff.append(i)
        # fff.writelines(ff )
        wtr = csv.writer(fff)
        for i in ff:
        #         i=i.split(',', 1)
                print('i, type(i)', i, type(i))
                wtr.writerow(i)

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        remove_smth('cities1.csv', 'cities2.csv')
    
