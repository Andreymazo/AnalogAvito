from django.core.management import BaseCommand
from ad.models import Category
from users.models import Profile
# Avito:
# Личные вещи --> Одежда, обувь, акссессуары --> Личные вещи --> Женская одежда
#  https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/svadebnye_platya_podgotovka_i_himchistka_2054834952
def ff():
    pass
    # MenClothes
    # WemenClothes
    # MenShoes
    # WemenShoes
    # ChildClothesShoes
    # BagsKnapsacks
    # parent_id  = Category.objects.get(name="Личные вещи").id
    # lst_of_smth = ["Мужская одежда", "Мужская обувь",  "Женская одежда", "Женская обувь", "Детская одежда и обувь" ,"Сумки, рюкзаки, чемоданы", "Остальное"]
    # [Category.objects.get_or_create(name=i, parent_id=parent_id)  for i in lst_of_smth]


class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()