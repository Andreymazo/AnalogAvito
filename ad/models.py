from typing import Iterable
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save
from config.constants import MAX_LEN_NAME_CATEGORY, MIN_YEAR_AUTO_CREATED
from config import settings
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


NULLABLE = {'blank': True, 'null': True}


class Category(MPTTModel):
    """Модель категории."""
    name = models.CharField(
        _("Название"),
        max_length=MAX_LEN_NAME_CATEGORY,
        unique=True
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        **NULLABLE,
        related_name="children",
        verbose_name=_("Родитель")
    )

    class MPTTMeta:
        """Конфигурация модели категории."""
        order_insertion_by = ("name",)
        verbose_name = _("категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        """Строковое представление категории."""
        return self.name

"""Модель объявление (абстрактная) поля, которой будут у всех объявлений"""
class Advertisement(models.Model):
    # category = TreeForeignKey('ad.Category', on_delete=models.CASCADE, related_name='advertisement')
    # profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    title = models.CharField(_("Document'stitle"), max_length=150, **NULLABLE)
    created = models.DateTimeField(auto_now=True)
    changed = models.DateTimeField(auto_now_add=True)
    moderation = models.BooleanField(_("Модерация"), default=False)
    archived = models.BooleanField(_("Архивное"), default=False)
    price = models.CharField(_("price"), max_length=100)
    description = models.CharField(_("Description"), max_length=2000)
    # marker = models.OneToOneField('map.Marker', on_delete=models.CASCADE, related_name="card")
    
    

    class Meta:
        abstract = True

    
    # likes = GenericRelation(Like)
    
    def __str__(self):
        return str(self.id)

BY_MILEAGE = [("ALL", "ALL"), ("NEW", "NEW"), ("WM", "With Mileage"),]

BY_TRANSMISSION = [("A", "AUTO"), ("R", "ROBOT"), ("V", "VARIATOR"), ("M", "MECHANICAL"),]

BY_DRIVE = [("FWD", "FRONT_WHEEL_DRIVE"), ("RWD", "REAR_WHEEL_DRIVE"), ("4WD", "VARIATOR"),]

BY_TYPE = [("SD", "SEDAN"), ("UN", "UNIVERSAL"), ("OR", "OFF_ROAD"), ("HTB", "HATCHBACK")]

BY_COLOUR = [("BLACK", "BLACK"), ("WHITE", "WHITE"), ("GREEN", "GREEN"), ("GREY", "GREY"), ("RED", "RED"), ("ORANGE", "ORANGE"), ("BEIGE", "BEIGE"), ("BROWN", "BROWN")]

BY_FUEL = [("PTR", "PETROL"), ("GAS", "GAS"), ("HYBRID", "HYBRID"), ("ELECTRIC", "ELECTRIC"), ("DIESEL", "DIESEL")]

MEN_SIZES = [("XS—40/42", "особо маленький - extra small"), ("S — 44/46", "маленький - small") , ("(M—48/50", "средний - medium"), \
    ("L— 52/54", "большой - large" ), ("XL—56/58", "особо большой — extra large"), ("XXL— 60/62", " особо особо большой— extra-extra large" ),\
          ("3XL—64/66", "особо особо особо большой— extra-extra-extra large" ),
]
def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Like(models.Model):
    is_liked = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    # card = models.ForeignKey("ad.Card", on_delete=models.CASCADE, related_name="likes")# Удалили, вместо нее Advertisement
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')#Как я понял вместотого, чтобы было понятно все написано с форейн кеями к каждой модели, можно так написать через content_type
    
    def __str__(self):
        """Строковое представление объекта Лайк."""
        return f"{self.user}"
    

class Favorite(models.Model):
    is_favorited = models.BooleanField()
    user = GenericRelation("users.CustomUser", related_query_name='fovorite')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          related_name='favorites',
    #                          on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        """Строковое представление объекта Избранное."""
        return f"{self.user}"


    # @property
    # def total_likes_user(self):
    #     return self.likes.count()  
class Car(Advertisement):
    category = TreeForeignKey('ad.Category', on_delete=models.CASCADE, related_name='car')
    # profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name='cars', **NULLABLE)
    by_mileage = models.CharField(_("Differ by mileage"), choices=BY_MILEAGE)
    brand = models.CharField(_("brand"), max_length=100)
    model = models.CharField(_("model"), max_length=100)
    price = models.CharField(_("price"), max_length=100)
    year = models.IntegerField(_('year'), default=current_year(), validators=[MinValueValidator(MIN_YEAR_AUTO_CREATED), 
                                                                                    max_value_current_year])
    mileage = models.IntegerField()
    transmission = models.CharField(_("Differ by transmission"), choices=BY_TRANSMISSION, **NULLABLE)
    by_wheel_drive = models.CharField(_("Differ by wheel drive"), choices=BY_DRIVE, **NULLABLE)
    engine_capacity = models.IntegerField(_("engine capacity"), validators=[MinValueValidator(0), MaxValueValidator(10000)], **NULLABLE)
    engine_power = models.IntegerField(_("engine power in horse power"), validators=[MinValueValidator(0), MaxValueValidator(900)], **NULLABLE) 
    fuel_consumption = models.IntegerField(_("fuel consumption per 100 km"), validators=[MinValueValidator(1), MaxValueValidator(40)], **NULLABLE)
    location = models.CharField(_("location"), max_length=160, **NULLABLE)
    type = models.CharField(_("Differ by type"), choices=BY_TYPE, **NULLABLE)
    colour = models.CharField(_("Differ by colour"), choices=BY_COLOUR, **NULLABLE)
    fuel = models.CharField(_("Differ by fuel"), choices=BY_FUEL, **NULLABLE)
    add_parametres =  models.CharField(_("additional"), max_length=150, **NULLABLE)
    description = models.CharField(_("Description"), max_length=2000)
    likes = GenericRelation("ad.Like", related_query_name='cars')
    images = GenericRelation("ad.Images", related_query_name='cars')
    promotions = GenericRelation("ad.Promotion", related_query_name='cars')
    views = GenericRelation("ad.Views", related_query_name='cars')
    mssg = GenericRelation("chat.Mssg", related_query_name='cars')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()    
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _("Automobile")
        verbose_name_plural = _("Automobiles")

    def __str__(self) -> str:
        return str(self.id)
    
"""This model is a profile's IP, more then two IPs will be deleted when created"""
class IP(models.Model):
    ip = models.CharField(max_length=100)
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    auto = models.ForeignKey("ad.Car", on_delete=models.CASCADE, **NULLABLE)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        queryset = IP.objects.all().filter(profile_id=instance.profile_id)
      
        if len(queryset)>2:
            queryset.exclude(pk__in=queryset.values_list("pk")[:2]).delete()
        return

post_save.connect(IP.post_create, sender=IP)
# from django.core.files.storage import FileSystemStorage
# import os
# class OverwriteStorage(FileSystemStorage):

#     def get_available_name(self, name, max_length=None):
#         pass
#         """Returns a filename that's free on the target storage system, and
#         available for new content to be written to.

#         Found at http://djangosnippets.org/snippets/976/

#         This file storage solves overwrite on upload problem. Another
#         proposed solution was to override the save method on the model
#         like so (from https://code.djangoproject.com/ticket/11663):

#         def save(self, *args, **kwargs):
#             try:
#                 this = MyModelName.objects.get(id=self.id)
#                 if this.MyImageFieldName != self.MyImageFieldName:
#                     this.MyImageFieldName.delete()
#             except: pass
#             super(MyModelName, self).save(*args, **kwargs)
#         """
#         # If the filename already exists, remove it as if it was a true file system
#         # if self.exists(name):
#         #     os.remove(os.path.join(settings.MEDIA_ROOT, name))
#         # return name
"""This model related to Car and other ad models, using content_type model"""
class Images(models.Model):
    title = models.CharField(_("Photoe's title"), max_length=150, **NULLABLE)
    image = models.ImageField(_("Photo"),  upload_to="images")#storage= OverwriteStorage()
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="images", **NULLABLE)
    created = models.DateTimeField(auto_now=True)
    changed = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


"""This model - profile's documents"""
class Documents(models.Model):
    title = models.CharField(_("Document'stitle"), max_length=150, **NULLABLE)
    document = models.FileField(_("Document's title"), upload_to="media/documents")
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    auto = models.ForeignKey("ad.Car", on_delete=models.CASCADE, **NULLABLE)
    created = models.DateTimeField(auto_now=True)


"""This model for promotion: will be highlighted and up in filtering. Related to other ad models by content_type model"""
class Promotion(models.Model):
    created = models.DateTimeField(auto_now=True)
    changed = models.DateTimeField(auto_now_add=True)
    time_paied = models.DateTimeField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()    
    content_object = GenericForeignKey('content_type', 'object_id')


"""This model views related by FK to ad.IP by content_type model to ad models"""
class Views(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()    
    content_object = GenericForeignKey('content_type', 'object_id')
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="view", **NULLABLE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def total_viwes_profile(self):
        return Views.objects.all().filter(profile=self.profile).count()
    
    @property
    def total_viwes_object(self):
        return Views.objects.all().filter(object_id=self.object_id).count()

class MenClothes(Advertisement):
    category = TreeForeignKey('ad.Category', on_delete=models.CASCADE, related_name='menclothes')
    size = models.CharField(choices=MEN_SIZES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()    
    content_object = GenericForeignKey('content_type', 'object_id')
    likes = GenericRelation("ad.Like", related_query_name='men_clothes')
    images = GenericRelation("ad.Images", related_query_name='men_clothes')
    promotions = GenericRelation("ad.Promotion", related_query_name='men_clothes')
    views = GenericRelation("ad.Views", related_query_name='men_clothes')
    mssg = GenericRelation("chat.Mssg", related_query_name='men_clothes')
    class Meta:
        verbose_name = _("Men Clothes")
        verbose_name_plural = _("Men Clothes")

    def __str__(self) -> str:
        return str(self.id)
    
class WemenClothes(Advertisement):
    category = TreeForeignKey('ad.Category', on_delete=models.CASCADE, related_name='wemenclothes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()    
    content_object = GenericForeignKey('content_type', 'object_id')
    likes = GenericRelation("ad.Like", related_query_name='women_clothes')
    images = GenericRelation("ad.Images", related_query_name='women_clothes')
    promotions = GenericRelation("ad.Promotion", related_query_name='women_clothes')
    views = GenericRelation("ad.Views", related_query_name='women_clothes')
    mssg = GenericRelation("chat.Mssg", related_query_name='women_clothes')
    class Meta:
        verbose_name = _("Women Shoes")
        verbose_name_plural = _("Women Shoes")

    def __str__(self) -> str:
        return str(self.id)

class MenShoes(Advertisement):
    category = TreeForeignKey('ad.Category', on_delete=models.CASCADE, related_name='menshoes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()    
    content_object = GenericForeignKey('content_type', 'object_id')
    likes = GenericRelation("ad.Like", related_query_name='men_shoes')
    images = GenericRelation("ad.Images", related_query_name='men_shoes')
    promotions = GenericRelation("ad.Promotion", related_query_name='men_shoes')
    views = GenericRelation("ad.Views", related_query_name='men_shoes')
    mssg = GenericRelation("chat.Mssg", related_query_name='men_shoes')
    class Meta:
        verbose_name = _("Men Shoes")
        verbose_name_plural = _("Men Shoes")

    def __str__(self) -> str:
        return str(self.id)

class WemenShoes(Advertisement):
    category = TreeForeignKey('ad.Category', on_delete=models.CASCADE, related_name='wemenshoes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()    
    content_object = GenericForeignKey('content_type', 'object_id')
    likes = GenericRelation("ad.Like", related_query_name='women_shoes')
    images = GenericRelation("ad.Images", related_query_name='women_shoes')
    promotions = GenericRelation("ad.Promotion", related_query_name='women_shoes')
    views = GenericRelation("ad.Views", related_query_name='women_shoes')
    mssg = GenericRelation("chat.Mssg", related_query_name='women_shoes')
    class Meta:
        verbose_name = _("Wemen Shoes")
        verbose_name_plural = _("Wemen Shoes")

    def __str__(self) -> str:
        return str(self.id)

class ChildClothesShoes(Advertisement):
    category = TreeForeignKey('ad.Category', on_delete=models.CASCADE, related_name='childclothesshoes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()    
    content_object = GenericForeignKey('content_type', 'object_id')
    likes = GenericRelation("ad.Like", related_query_name='child_clothes_shoes')
    images = GenericRelation("ad.Images", related_query_name='child_clothes_shoes')
    promotions = GenericRelation("ad.Promotion", related_query_name='child_clothes_shoes')
    views = GenericRelation("ad.Views", related_query_name='child_clothes_shoes')
    mssg = GenericRelation("chat.Mssg", related_query_name='child_clothes_shoes')
    class Meta:
        verbose_name = _("Child's Clothes&Shoes")
        verbose_name_plural = _("Child's Clothes&Shoes")

    def __str__(self) -> str:
        return str(self.id)

class BagsKnapsacks(Advertisement):
    category = TreeForeignKey('ad.Category', on_delete=models.CASCADE, related_name='bagsknapsacks')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()    
    content_object = GenericForeignKey('content_type', 'object_id')
    class Meta:
        verbose_name = _("Bags&Knapsacks")
        verbose_name_plural = _("Bags&Knapsacks")
    def __str__(self) -> str:
        return str(self.id)


"""This is changed by model Advertisement, must be deleted after testing"""
# class Card(models.Model):
#     title = models.CharField(_("Document'stitle"), max_length=150, **NULLABLE)
#     price = models.CharField(_("price"), max_length=100)
#     description = models.CharField(_("Description"), max_length=2000)
#     marker = models.OneToOneField('map.Marker', on_delete=models.CASCADE, related_name="card")
#     profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="card", **NULLABLE)
#     created = models.DateTimeField(auto_now=True)
#     # likes = GenericRelation(Like)
    
#     def __str__(self):
#         return str(self.id)
    
    # @property
    # def total_likes(self):
    #     return self.likes.count()
    
#   promo: '2024-08-03T14:00:00.000Z',
#   userName: 'Андрей',
#   createAdDate: '2024-07-03T14:00:00.000Z',
#   userCreate: '2022-03-22T14:00:00.000Z',
#   adCounter: '10',
#   image: ['/cardMockImage.png'],