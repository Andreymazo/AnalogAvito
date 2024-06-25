from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.constants import (
    MAX_LEN_CODE,
    MAX_LEN_EMAIL,
    MAX_LEN_PHONE_NUMBER,
    MAX_LEN_NAME_PROFILE,
)
from users.managers import CustomUserManager


NULLABLE = {'blank': True, 'null': True}

phone_validator = RegexValidator(
    r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?"
    r"(\(?\d{4}\)?)?$",
    "The phone number provided is invalid"
)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    username = None
    info = models.TextField(
        _("Информация"),
        **NULLABLE,
        help_text=_("Введите дополнительную информацию")
    )
    email = models.EmailField(
        _("Почта"),
        max_length=MAX_LEN_EMAIL,
        unique=True,
        help_text=_("Введите email, не более 254 символов"),
    )
    is_banned = models.BooleanField(_("Бан"), default=False)
    banned_at = models.DateTimeField(
        _("Время начала бана"),
        **NULLABLE
    )
    changed_at = models.DateTimeField(_("Время изменения"), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Конфигурация модели пользователя."""
        ordering = ("id",)
        verbose_name = _("пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        """Строковое представление объекта пользователя."""
        return str(self.email)


class Profile(models.Model):
    """Модель профайла."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="profile"
    )
    phone_number = models.CharField(
        _("Номер телефона"),
        max_length=MAX_LEN_PHONE_NUMBER,
        unique=True,
        validators=[phone_validator]
    )
    name = models.CharField(
        _("Имя пользователя"),
        max_length=MAX_LEN_NAME_PROFILE
    )
    def __str__(self):
        """Строковое представление объекта пользователя."""
        return str(self.user.email)

class OneTimeCode(models.Model):
    """Модель одноразового кода."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="onetimecodes",
        verbose_name=_("Пользователь")
    )
    code = models.CharField(
        _("Одноразовый код"),
        max_length=MAX_LEN_CODE
    )
    count_attempts = models.PositiveSmallIntegerField(
        _("Попытки"),
        default=0
    )
    count_send_code = models.PositiveSmallIntegerField(
        _("Количество повторных отправок кода"),
        default=0
    )
    updated_at = models.DateTimeField(
        _("Время обновления кода"),
        auto_now=True
    )
    created_at = models.DateTimeField(
        _("Время создания кода"),
        auto_now_add=True
    )

    class Meta:
        """Конфигурация модели одноразового кода."""
        ordering = ("id",)
        verbose_name = _("одноразовый код")
        verbose_name_plural = _("Одноразовые коды")

    def __str__(self):
        """Строковое представление одноразового кода."""
        return str(f"Код для {self.user.email}")
