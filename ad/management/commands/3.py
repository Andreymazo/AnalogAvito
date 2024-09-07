# import datetime
import json
from django.utils import timezone
from django.core.management import BaseCommand
from ad.models import Car
from users.models import Profile

 
def ff():
    with open("db1.json", "r") as jsonFile:
        ata = json.load(jsonFile)
    print(ata)

   
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()
