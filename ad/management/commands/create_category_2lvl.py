from django.core.management import BaseCommand
from ad.models import Category

 
def ff():
    # category_list = ["Транспорт", "Услуги", "Личные вещи", "Электроника"]
    parent_id = Category.objects.get(name="Услуги").id
    Category.objects.get_or_create(name="Грузоперевозки", parent_id=parent_id)
    # for i in category_list:
    #     get_category = Category.objects.get_or_create(name=i)
  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()