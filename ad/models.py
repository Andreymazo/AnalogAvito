from typing import Iterable
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save
from config.constants import MAX_LEN_NAME_CATEGORY, MIN_YEAR_AUTO_CREATED
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

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


class Advertisement(models.Model):
    category = TreeForeignKey('ad.Category', on_delete=models.CASCADE, related_name='advertisement')
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    created = models.DateTimeField(auto_now=True)
    changed = models.DateTimeField(auto_now_add=True)
    moderation = models.BooleanField(_("Модерация"), default=False)

    class Meta:
        abstract = True

BY_MILEAGE = [("ALL", "ALL"), ("NEW", "NEW"), ("WM", "With Mileage"),]

BY_TRANSMISSION = [("A", "AUTO"), ("R", "ROBOT"), ("V", "VARIATOR"), ("M", "MECHANICAL"),]

BY_DRIVE = [("FWD", "FRONT_WHEEL_DRIVE"), ("RWD", "REAR_WHEEL_DRIVE"), ("4WD", "VARIATOR"),]

BY_TYPE = [("SD", "SEDAN"), ("UN", "UNIVERSAL"), ("OR", "OFF_ROAD"), ("HTB", "HATCHBACK")]

BY_COLOUR = [("BLACK", "BLACK"), ("WHITE", "WHITE"), ("GREEN", "GREEN"), ("GREY", "GREY"), ("RED", "RED"), ("ORANGE", "ORANGE"), ("BEIGE", "BEIGE"), ("BROWN", "BROWN")]

BY_FUEL = [("PTR", "PETROL"), ("GAS", "GAS"), ("HYBRID", "HYBRID"), ("ELECTRIC", "ELECTRIC"), ("DIESEL", "DIESEL")]

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)
   
class Car(Advertisement):
    by_mileage = models.CharField(_("Differ by mileage"), choices=BY_MILEAGE)
    brand = models.CharField(_("brand"), max_length=100)
    model = models.CharField(_("model"), max_length=100)
    price = models.CharField(_("price"), max_length=100)
    year = models.PositiveSmallIntegerField(_('year'), default=current_year(), validators=[MinValueValidator(MIN_YEAR_AUTO_CREATED), 
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

    class Meta:
        verbose_name = _("Automobile")
        verbose_name_plural = _("Automobiles")

    def __str__(self) -> str:
        return str(self.model)
    

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


class Images(models.Model):
    title = models.CharField(_("Photoe's title"), max_length=150, **NULLABLE)
    image = models.FileField(_("Photo"), upload_to="media/images")
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    auto = models.ForeignKey("ad.Car", on_delete=models.CASCADE, **NULLABLE)
    created = models.DateTimeField(auto_now=True)
    changed = models.DateTimeField(auto_now_add=True)


class Documents(models.Model):
    title = models.CharField(_("Document'stitle"), max_length=150, **NULLABLE)
    document = models.FileField(_("Document's title"), upload_to="media/documents")
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    auto = models.ForeignKey("ad.Car", on_delete=models.CASCADE, **NULLABLE)
    created = models.DateTimeField(auto_now=True)
