from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


NULLABLE = {'blank': True, 'null': True}

MAX_LEN_CODE = 5
COUNT_SEND_CODE = 3

phone_validator = RegexValidator(
    r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?"
    r"(\(?\d{4}\)?)?$",
    "The phone number provided is invalid"
)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    # username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        **NULLABLE
    )
    info = models.TextField(
        _("Информация"),
        blank=True,
        null=True,
        help_text=_("Введите дополнительную информацию")
    )
    email = models.EmailField(
        _("Почта"),
        max_length=254,
        unique=True,
        help_text=_("Введите email, не более 254 символов"),
    )
    # profile = models.OneToOneField(
    #     Profile,
    #     on_delete=models.CASCADE,
    #     verbose_name="user"
    # )
    is_first = models.BooleanField(_("Первый вход"), default=True)
    is_banned = models.BooleanField(_("Бан"), default=False)
    banned_at = models.DateTimeField(
        _("Время начала бана"),
        **NULLABLE
    )
    changed_at = models.DateTimeField(_("Время изменения"), auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        """Конфигурация модели пользователя."""
        ordering = ("id",)
        verbose_name = _("пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        """Строковое представление объекта пользователя."""
        return str(self.username)


class Profile(models.Model):
    """Модель профайла."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="profile"
    )
    phone_number = models.CharField(
        _("Номер телефона"),
        max_length=12,
        unique=True,
        validators=[phone_validator]
    )
    name = models.CharField(_("Имя пользователя"), max_length=150)


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
