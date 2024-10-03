# import datetime
import json
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.management import BaseCommand
from ad.models import BagsKnapsacks, Car, Category, ChildClothesShoes, Images, MenClothes, MenShoes, WemenClothes, WemenShoes
from config.settings import BASE_DIR, BASE_URL
from users.models import Profile


 
def ff():
    # lst_mdls =  [ChildClothesShoes, WemenShoes, MenShoes, WemenClothes, MenClothes, BagsKnapsacks]
    # p1 = Category.objects.get(id=30)
    # print(str((type(p1.childclothesshoes.all().first()).__name__)).lower())
    # print(ChildClothesShoes.category.field._related_name)
    # # {'_related_name': 'childclothesshoes', '_related_query_name': None, '_limit_choices_to': None, 'name': 'category', 'verbose_name': 'category', '_verbose_name': None, 'primary_key': False, 'max_length': None, '_unique': False, 'blank': False, 'null': False, 'remote_field': <ManyToOneRel: ad.childclothesshoes>, 'is_relation': True, 'default': <class 'django.db.models.fields.NOT_PROVIDED'>, 'db_default': <class 'django.db.models.fields.NOT_PROVIDED'>, 'editable': True, 'serialize': True, 'unique_for_date': None, 'unique_for_month': None, 'unique_for_year': None, '_choices': None, 'help_text': '', 'db_index': True, 'db_column': None, 'db_comment': None, '_db_tablespace': None, 'auto_created': False, 'creation_counter': 193, '_validators': [], '_error_messages': None, 'from_fields': ['self'], 'to_fields': [None], 'swappable': True, 'db_constraint': True, 'attname': 'category_id', 'column': 'category_id', 'concrete': True, 'model': <class 'ad.models.ChildClothesShoes'>, 'opts': <Options for ChildClothesShoes>, 'related_model': <class 'ad.models.Category'>, 'validators': [], 'related_fields': [(<mptt.fields.TreeForeignKey: category>, <django.db.models.fields.BigAutoField: id>)], 'foreign_related_fields': (<django.db.models.fields.BigAutoField: id>,)}
    # for i in lst_mdls:
    #     if i.category.field._related_name==str((type(p1.childclothesshoes.all().first()).__name__)).lower():
    #         print('here')
    #         return str(i.__name__)
    # content_type = ContentType.objects.get(model='car')

    print(ContentType.objects.get(id=20).model_class().objects.get(id=2).profilee.all().first()) # чьи объявления

   
    # print(content_type.id)
    # car=Car.objects.get(id=6)
    # content_type =  ContentType.objects.get(model='car')
    # print(BASE_DIR, BASE_URL, )
    # instance = MenClothes.objects.get(id=8)
    #car.images.all())
    # print(Images.objects.filter(content_type).filter(object_id=car.id))
    # Images
    
#  prefetch = GenericPrefetch(
# ...     "content_object", [Bookmark.objects.all(), Animal.objects.only("name")]
# ... )
# >>> TaggedItem.objects.prefetch_related(prefetch).all()
# <QuerySet [<TaggedItem: Great>, <TaggedItem: Awesome>]>

    # p2 = Category.objects.get(id=31)
#    print(Category.objects.get(id=30))
    # lst_p = [p1,p2]
    # for i in lst_p:
    #     i.childclothesshoes.all()
    #     i.bagknapsacks.all()
        # try:
        # except:

    # print(p1.childclothesshoes.all())
    # print(p2.bagknapsacks.all())
    # print(ChildClothesShoes.category.__dict__)
   
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()
