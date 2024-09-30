# import datetime
import json
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.management import BaseCommand
import requests
from ad.models import BagsKnapsacks, Car, Category, ChildClothesShoes, Images, MenClothes, MenShoes, WemenClothes, WemenShoes
from config.settings import BASE_DIR, BASE_URL
from users.models import Profile


 
def ff():
    # with open('media/RU.txt', 'r') as f:
    #    data = f.readlines()
    
    # with open('out.csv', 'w') as f:
    #     fildnames=["name", "lat", "long", "time zone","date"]
    #     for i in data:
    #         f.write(fildnames)
    #         f.write(i)

   general_url='http://ipwho.is/'
   my_ip='5.188.167.243'
   akatov1_ip='90.156.226.147'
   response=requests.get(f'{general_url}{akatov1_ip}')
   print(response.json())
# {'ip': '5.188.167.243', 'success': True, 'type': 'IPv4', 'continent': 'Europe', 'continent_code': 'EU', 'country': 'Russia', 'country_code': 'RU', 'region': 'Saint Petersburg', 'region_code': '', 'city': 'Saint Petersburg', 'latitude': 59.9342802, 'longitude': 30.3350986, 'is_eu': False, 'postal': '191186', 'calling_code': '7', 'capital': 'Moscow', 'borders': 'AZ,BY,CN,EE,FI,GE,KP,KZ,LT,LV,MN,NO,PL,UA', 'flag': {'img': 'https://cdn.ipwhois.io/flags/ru.svg', 'emoji': '🇷🇺', 'emoji_unicode': 'U+1F1F7 U+1F1FA'}, 'connection': {'asn': 205553, 'org': 'LTD Magistral Telecom', 'isp': 'LTD Magistral Telecom', 'domain': 'magistral-telecom.com'}, 'timezone': {'id': 'Europe/Moscow', 'abbr': 'MSK', 'is_dst': False, 'offset': 10800, 'utc': '+03:00', 'current_time': '2024-09-29T12:03:06+03:00'}}
#{'ip': '90.156.226.147', 'success': True, 'type': 'IPv4', 'continent': 'Europe', 'continent_code': 'EU', 'country': 'Russia', 'country_code': 'RU', 'region': 'Saint Petersburg', 'region_code': '', 'city': 'Saint Petersburg', 'latitude': 59.9342802, 'longitude': 30.3350986, 'is_eu': False, 'postal': '191186', 'calling_code': '7', 'capital': 'Moscow', 'borders': 'AZ,BY,CN,EE,FI,GE,KP,KZ,LT,LV,MN,NO,PL,UA', 'flag': {'img': 'https://cdn.ipwhois.io/flags/ru.svg', 'emoji': '🇷🇺', 'emoji_unicode': 'U+1F1F7 U+1F1FA'}, 'connection': {'asn': 9123, 'org': 'TW VDS', 'isp': 'Timeweb Ltd.', 'domain': 'timeweb.ru'}, 'timezone': {'id': 'Europe/Moscow', 'abbr': 'MSK', 'is_dst': False, 'offset': 10800, 'utc': '+03:00', 'current_time': '2024-09-29T12:24:04+03:00'}}

# import csv 
import csv 
  
# open input CSV file as source 
# open output CSV file as result 
with open("input.csv", "r") as source: 
    reader = csv.reader(source) 
      
    with open("output.csv", "w") as result: 
        writer = csv.writer(result) 
        for r in reader: 
            
            # Use CSV Index to remove a column from CSV 
            #r[3] = r['year'] 
            writer.writerow((r[0], r[1], r[2], r[4], r[5]))
            # https://www.geeksforgeeks.org/delete-a-csv-column-in-python/
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()
