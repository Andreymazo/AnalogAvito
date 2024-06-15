from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}


MAX_LEN_CODE = 5
COUNT_ATTEMPTS = 3
COUNT_SEND_CODE = 3


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    info = models.TextField(
        _("Информация"),
        blank=True,
        null=True,
        help_text=_("Введите дополнительную информацию")
    )
# name = models.CharField(_("Имя пользователя"), max_length=150, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        **NULLABLE
    )
    email = models.EmailField(
        _("Почта"),
        max_length=254,
        unique=True,
        help_text=_("Введите email, не более 254 символов"),
    )
    # phone_number = PhoneNumberField()
    phone_number = models.CharField(
        _("Номер телефона"),
        max_length=12,
        # unique=True,
        blank=True,
    )
    is_first = models.BooleanField(_("Первый вход"), default=True)
    is_banned = models.BooleanField(_("Бан"), default=False)
    changed_at = models.DateTimeField(_("Время изменения"), auto_now_add=True)

    class Meta:
        """Конфигурация модели пользователя."""
        ordering = ("id",)
        verbose_name = _("пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        """Строковое представление объекта пользователя."""
        return str(self.username)


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
        default=COUNT_ATTEMPTS
    )
    # is_verified = models.BooleanField(
    #     _("Код подтвержден"),
    #     default=False
    # )
    count_send_code = models.PositiveSmallIntegerField(
        _("Количество повторных отправок кода"),
        default=COUNT_SEND_CODE
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


# class SessionCustomuser(models.Model):
#     """Модель сессии пользователя."""
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
