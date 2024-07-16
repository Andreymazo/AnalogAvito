from django.core.management import BaseCommand
from ad.models import Auto, Category
from users.models import Profile

 
def ff():
    category_list = ["Транспорт", "Услуги", "Личные вещи", "Электроника"]
    for i in category_list:
        get_category = Category.objects.get_or_create(name=i)
  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()