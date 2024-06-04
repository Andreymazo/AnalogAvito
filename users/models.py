from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

MAX_LEN_CODE = 5
COUNT_ATTEMPTS = 3


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
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
    is_first = models.BooleanField(_("Первый вход"), default=True)
    is_banned = models.BooleanField(_("Бан"), default=False)
    banned_at = models.DateTimeField(_("Время бана"), auto_now_add=True)

    class Meta:
        """Конфигурация модели пользователя."""
        ordering = ("id",)
        verbose_name = _("пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        """Строковое представление объекта пользователя."""
        return self.username


class OneTimeCode(models.Model):
    """Модель одноразового кода."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="otc",
        verbose_name=_("Пользователь")
    )
    code = models.CharField(
        _("Одноразовый код"),
        max_length=MAX_LEN_CODE
    )
    remaining_attempts = models.PositiveSmallIntegerField(
        _("Оставшиеся попытки"),
        default=COUNT_ATTEMPTS
    )
    # is_verified = models.BooleanField(
    #     _("Код подтвержден"),
    #     default=False
    # )
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
        return f"Код для {self.user}"


# class SessionCustomuser(models.Model):
#     """Модель сессии пользователя."""
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
