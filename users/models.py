from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    bio = models.TextField(
        _("Биография"),
        blank=True,
        null=True,
        help_text=_("Введите личную информацию")
    )
    email = models.EmailField(
        _("Почта"),
        max_length=254,
        unique=True,
        help_text=_("Введите email, не более 254 символов"),
    )

    class Meta:
        """Конфигурация модели пользователя."""
        ordering = ("id",)
        verbose_name = _("пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        """Строковое представление объекта пользователя."""
        return self.username
