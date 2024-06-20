from typing import Iterable
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from config.constants import MAX_LEN_NAME_CATEGORY


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
    qwwq = models.Choices

    class MPTTMeta:
        """Конфигурация модели категории."""
        order_insertion_by = ("name",)
        verbose_name = _("категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        """Строковое представление категории."""
        return self.name


class Advertisement(models.Model):
    title = models.CharField(_("Название"),max_length=175)
    description = models.CharField(_("Описание"), max_length=2000)
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    category = models.ForeignKey("ad.Category", on_delete=models.CASCADE, **NULLABLE)
    created = models.DateTimeField(auto_now=True)
    changed = models.DateTimeField(auto_now_add=True)
    moderation = models.BooleanField(_("Модерация"), default=False)


from django.db.models.signals import post_save

class IP(models.Model):
    ip = models.CharField(max_length=100)
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    advertisement = models.ForeignKey("ad.Advertisement", on_delete=models.CASCADE, **NULLABLE)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        print('======================instance.id', instance.profile_id)
        queryset = IP.objects.all().filter(profile_id=instance.profile_id)
        # print('--------------------------------------------------', instance.__dict__, sender, queryset)
      
        if len(queryset)>2:
            # print('--------------------------------------------------', sender, instance, queryset)
            queryset.exclude(pk__in=queryset.values_list("pk")[:2]).delete()
        return

post_save.connect(IP.post_create, sender=IP)


class Images(models.Model):
    title = models.CharField(max_length=150)
    image = models.FileField(_("Фотография"), upload_to="media/images")
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    advertisement = models.ForeignKey("ad.Advertisement", on_delete=models.CASCADE, **NULLABLE)
    created = models.DateTimeField(auto_now=True)
    changed = models.DateTimeField(auto_now_add=True)


class Documents(models.Model):
    title = models.CharField(max_length=150)
    document = models.FileField(_("Документ"), upload_to="media/documents")
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    advertisement = models.ForeignKey("ad.Advertisement", on_delete=models.CASCADE, **NULLABLE)
    created = models.DateTimeField(auto_now=True)
