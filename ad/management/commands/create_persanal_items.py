from django.core.management import BaseCommand
from ad.models import BagsKnapsacks, Category, ChildClothesShoes, MenClothes, MenShoes, WemenClothes, WemenShoes
from users.models import Profile
# Avito:
# Личные вещи --> Одежда, обувь, акссессуары --> Личные вещи --> Женская одежда
#  https://www.avito.ru/sankt-peterburg/odezhda_obuv_aksessuary/svadebnye_platya_podgotovka_i_himchistka_2054834952
def ff():
    profile_lst = [Profile.objects.first(), Profile.objects.last()]
    price_lst = [2000, 3000]
                    
    # lst_categ = [Category.objects.get(name="Мужская одежда"), Category.objects.get(name="Мужская обувь"), Category.objects.get(name="Женская одежда"),\
    #               Category.objects.get(name="Женская обувь"),  Category.objects.get(name="Детская одежда и обувь"),  \
    #                 Category.objects.get(name="Сумки, рюкзаки, чемоданы"), ]
    # dict_of_categories = ["Мужская одежда", "Мужская обувь",  "Женская одежда", "Женская обувь", "Детская одежда и обувь" ,"Сумки, рюкзаки, чемоданы",]
    menclothes_category = Category.objects.get(name="Мужская одежда")
    mensh_category = Category.objects.get(name="Мужская обувь")
    wemenclothes_category = Category.objects.get(name="Женская одежда")
    wemsh_category = Category.objects.get(name="Женская обувь")
    childcloth_category = Category.objects.get(name="Детская одежда и обувь")
    bagssnacks_category = Category.objects.get(name="Сумки, рюкзаки, чемоданы")

    for i,ii in zip(profile_lst, price_lst):
    # [MenClothes(price=ii, content_object = i) for i,ii in zip(profile_lst, price_lst)]
        menclothes = MenClothes(price=ii, content_object = i, category=menclothes_category)
        menclothes.save()
        wemenclothes = WemenClothes(price=ii, content_object = i, category=wemenclothes_category)
        wemenclothes.save()
        mensh = MenShoes(price=ii, content_object = i,category=mensh_category)
        mensh.save()
        wemsh = WemenShoes(price=ii, content_object = i,category=wemsh_category)
        wemsh.save()
        childcloth = ChildClothesShoes(price=ii, content_object = i, category=childcloth_category)
        childcloth.save()
        bagssnacks = BagsKnapsacks(price=ii, content_object = i, category=bagssnacks_category)
        bagssnacks.save()

    # parent_id  = Category.objects.get(name="Личные вещи").id
    # lst_of_smth = ["Мужская одежда", "Мужская обувь",  "Женская одежда", "Женская обувь", "Детская одежда и обувь" ,"Сумки, рюкзаки, чемоданы", "Остальное"]
    # [Category.objects.get_or_create(name=i, parent_id=parent_id)  for i in lst_of_smth]


class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()