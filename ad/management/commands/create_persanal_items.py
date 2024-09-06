from django.core.management import BaseCommand
from ad.models import BagsKnapsacks, Category, ChildClothesShoes, MenClothes, MenShoes, WemenClothes, WemenShoes
from users.models import Profile
# Avito:
# Личные вещи --> Одежда, обувь, акссессуары --> Личные вещи --> Женская одежда
#  https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/svadebnye_platya_podgotovka_i_himchistka_2054834952
def ff():
    profile_lst = [Profile.objects.first(), Profile.objects.last()]
    price_lst = [2000, 3000]
    for i,ii in zip(profile_lst, price_lst):

        menclothes = MenClothes(price=ii, content_object = i)
        menclothes.save()
    wemenclothes = WemenClothes(price=ii, content_object = i)
    wemenclothes.save()
    mensh = MenShoes(price=ii, content_object = i)
    mensh.save()
    wemsh = WemenShoes(price=ii, content_object = i)
    wemsh.save()
    childcloth = ChildClothesShoes(price=ii, content_object = i)
    childcloth.save()
    bagssnacks = BagsKnapsacks(price=ii, content_object = i)
    bagssnacks.save()

    # parent_id  = Category.objects.get(name="Личные вещи").id
    # lst_of_smth = ["Мужская одежда", "Мужская обувь",  "Женская одежда", "Женская обувь", "Детская одежда и обувь" ,"Сумки, рюкзаки, чемоданы", "Остальное"]
    # [Category.objects.get_or_create(name=i, parent_id=parent_id)  for i in lst_of_smth]


class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()