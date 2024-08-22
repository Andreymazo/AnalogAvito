from django.core.management import BaseCommand
from ad.models import Category

 
def ff():
    # category_list = ["Транспорт", "Услуги", "Личные вещи", "Электроника"]
    parent_id = Category.objects.get(name="Услуги").id
    Category.objects.get_or_create(name="Грузоперевозки", parent_id=parent_id)
    parent_id = Category.objects.get(name="Купить").id
    Category.objects.get_or_create(name="Транспорт", parent_id=parent_id)
    Category.objects.get_or_create(name="Недвижимость", parent_id=parent_id)
    Category.objects.get_or_create(name="Личные вещи", parent_id=parent_id)
    Category.objects.get_or_create(name="Животные", parent_id=parent_id)
    parent_id = Category.objects.get(name="Сдать").id
    Category.objects.get_or_create(name="Транспорт (аренда)", parent_id=parent_id)
    Category.objects.get_or_create(name="Недвижимость (аренда)", parent_id=parent_id)
    Category.objects.get_or_create(name="Личные вещи (аренда)", parent_id=parent_id)
    Category.objects.get_or_create(name="Животные (аренда)", parent_id=parent_id)
    # for i in category_list:
    #     get_category = Category.objects.get_or_create(name=i)
  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()