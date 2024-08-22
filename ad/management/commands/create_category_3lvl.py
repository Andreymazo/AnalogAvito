from django.core.management import BaseCommand
from ad.models import Category

 
def ff():
    parent_id = Category.objects.get(name="Транспорт").id
    Category.objects.get_or_create(name="Автомобили (продажа)", parent_id=parent_id)
    Category.objects.get_or_create(name="Мотоциклы, мопеды (продажа)", parent_id=parent_id)
    Category.objects.get_or_create(name="Лодки,катера (продажа)", parent_id=parent_id)
   

  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()