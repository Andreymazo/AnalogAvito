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
