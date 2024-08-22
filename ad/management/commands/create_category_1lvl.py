from django.core.management import BaseCommand
from ad.models import Category
from users.models import Profile

 
def ff():
    category_list = ["Купить", "Продать", "Сдать", "Снять", "Услуги"]
    for i in category_list:
        get_category = Category.objects.get_or_create(name=i)
  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()