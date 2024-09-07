from django.core.management import BaseCommand
from ad.models import Category
from users.models import Profile

 
def ff():
    category_list = ["Транспорт", "Недвижимость", "Личные вещи", "Электроника", "Животные", "Услуги"]
    [Category.objects.get_or_create(name=i,)  for i in category_list]
   
    parent_id = Category.objects.get(name="Услуги").id
    lst_of_smth = ["Грузоперевозки", "Строительство", "Грузчики, Складские услуги","Аренда авто", "Ремонт, отделка","Красота и здоровье",]
    [Category.objects.get_or_create(name=i, parent_id=parent_id)  for i in lst_of_smth]
    parent_id = Category.objects.get(name="Транспорт").id
    lst_of_smth = ["Автомобили", "Мотоциклы", "Водный транспорт", "Грузовая техника",]
    [Category.objects.get_or_create(name=i, parent_id=parent_id)  for i in lst_of_smth]
    lst_of_smth = ["Купить жильё", "Снять долгосрочно", "Снять посуточно", "Коммерческая недвижимость",]
    parent_id = Category.objects.get(name="Недвижимость").id
    [Category.objects.get_or_create(name=i, parent_id=parent_id)  for i in lst_of_smth]
    parent_id  = Category.objects.get(name="Купить жильё").id
    lst_of_smth = ["Квартиры", "Дома", "Комнаты", "Земельные участки", "Коммерческая недвижимость",]
    [Category.objects.get_or_create(name=i, parent_id=parent_id)  for i in lst_of_smth]
    
    parent_id  = Category.objects.get(name="Личные вещи").id
    lst_of_smth = ["Мужская одежда", "Мужская обувь",  "Женская одежда", "Женская обувь", "Детская одежда и обувь" ,"Сумки, рюкзаки, чемоданы",]
    [Category.objects.get_or_create(name=i, parent_id=parent_id)  for i in lst_of_smth]
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()