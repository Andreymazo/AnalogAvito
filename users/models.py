import re

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from ad.models import Car, Promotion
from config.constants import (
    MAX_LEN_CODE,
    MAX_LEN_EMAIL,
    MAX_LEN_PHONE_NUMBER,
    MAX_LEN_NAME_PROFILE,
    MAX_LEN_USERNAME, MIN_LEN_USERNAME, MIN_LEN_NAME_PROFILE,
)
from users.managers import CustomUserManager
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db.models import PointField
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from ad.models import Images
from django.contrib.contenttypes.fields import GenericForeignKey


NULLABLE = {'blank': True, 'null': True}

phone_validator = RegexValidator(
    r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?"
    r"(\(?\d{4}\)?)?$",
    "The phone number provided is invalid"
)

def validate_name(value):
    # Проверка на наличие только букв или букв и цифр
    if not re.match(r'^[a-zA-Zа-яА-Я0-9]+$', value):
        raise ValidationError(_("Имя пользователя должно содержать только буквы или буквы и цифры"))

    # Проверка на отсутствие имени пользователя, состоящего только из цифр
    if re.match(r'^\d+$', value):
        raise ValidationError(_("Имя пользователя не может состоять только из цифр"))

"""If moer flexable auth model needed comment CustomUser (makemigrations) and uncomment the code below (makemigrations)"""
class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    # username = None
    username = models.CharField(_("username"),
                                validators=[MinLengthValidator(MIN_LEN_USERNAME), validate_name],
                                max_length=MAX_LEN_USERNAME,
                                **NULLABLE
                                )
    info = models.TextField(_("Информация"), **NULLABLE, help_text=_("Введите дополнительную информацию"))
    email = models.EmailField(_("Почта"),
                              max_length=MAX_LEN_EMAIL,
                              unique=True,
                              validators=[validate_email_length],
                              help_text=_("Введите email, не более 50 символов"),
                              )
    is_banned = models.BooleanField(_("Бан"), default=False)
    banned_at = models.DateTimeField(_("Время начала бана"), **NULLABLE)
    changed_at = models.DateTimeField(_("Время изменения"), auto_now_add=True)
    promotion = GenericRelation("ad.Promotion", related_query_name='users')
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
    REQUIRED_FIELDS = ["username"]

# class CustomUser(AbstractBaseUser):  # , PermissionsMixin):
#     email = models.EmailField(max_length=100, unique=True)
#     # VERIFICATION_TYPE = [
#     #     ('sms', 'SMS'),
#     # ]
#     # phone_number = PhoneNumberField(unique = True)
#     # verification_method = models.CharField(max_length=10,choices= VERIFICATION_TYPE)
#     # phone_number = models.CharField(max_length=16, validators=[phone_validator], unique=True)
#     first_name = models.CharField(_("first name"), max_length=150, blank=True)
#     last_name = models.CharField(_("last name"), max_length=150, blank=True)
#     is_staff = models.BooleanField(
#         _("staff status"),
#         default=False,
#         help_text=_("Designates whether the user can log into this admin site."),
#     )
#     is_active = models.BooleanField(
#         _("active"),
#         default=True,
#         help_text=_(
#             "Designates whether this user should be treated as active. "
#             "Unselect this instead of deleting accounts."
#         ),
#     )
#     date_joined = models.DateTimeField(_("date joined"), auto_now_add=True, default=timezone.now)

#     objects = UserManager()

#     EMAIL_FIELD = "email"
#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["email"]
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     # is_superuser = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     objects = CustomUserManager()

#     def __str__(self):
#         return f"{self.id}: {self.email}"

#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#         # permissions = [("worktime.add_customuser", "Can add customuser"),
#         #                ("worktime.change_customuser", "Can change customuser"),
#         #                ("worktime.delete_customuser", "Can delete customuser"),
#         #                ("worktime.view_customuser", "Can view customuser")]


    class Meta:
        """Конфигурация модели пользователя."""
        ordering = ("id",)
        verbose_name = _("пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        """Строковое представление объекта пользователя."""
        return str(self.email)


receiver(user_logged_in)
def create_notification_for_logged_in(sender, user, request, **kwargs):
    print('user', user)
    print('sender', sender)
    print('type(user), user.id', type(user), user.id)
    print('ContentType.objects.get_for_model(user)', ContentType.objects.get_for_model(user))
    car_quryset = Car.objects.prefetch_related('promotions') #  Car by Promotions
    try:
        promotions_user = Promotion.objects.prefetch_related('users')# Promotions by User
    except Promotion.DoesNotExist:
        return Response({"message":"Teres no promotion for the user"})

    print('car_quryset', car_quryset)
    print('promotions_user', promotions_user)

    promotion_qeryset = Promotion.objects.prefetch_related('cars').all()#.filter(content_type=ContentType.objects.get_for_model(user), object_id=object.id)#Выберем промоушены зарегистрировавшегося юзера
    # У Промоушена ключ на Профиль, у Профиля ключ на Юзера, Юзер входит, тут проверяется вся его подписка на подход к концу. CustomUser id = 32
    # ContentType

    content_object = ContentType.objects.get_for_model(user)#get_for_id(content_type).get_object_for_this_type(pk=object_id)
    print('-----------------content_object', content_object)
    # print('promotion_qeryset', len(promotion_qeryset), type(promotion_qeryset))
    for i in promotions_user:
        print('  content_object  ', i.content_object)
        if (i.time_paied - timezone.now()).days < 1:
            Notification.objects.create(text = f"less 1 day left for {i.content_object} promotion", key_to_recepient=user.email,\
                                         user=CustomUser.objects.get(email="andreymazo@mail.ru"))  #user от кого пришло, ставим суперюзера
            print('Notification created')

user_logged_in.connect(create_notification_for_logged_in)

class Profile(models.Model):
    """Модель профайла"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name="profile",)
    phone_number = models.CharField(_("Номер телефона"), max_length=MAX_LEN_PHONE_NUMBER, unique=True, validators=[phone_validator])
    name = models.CharField(_("Имя пользователя"),
                            max_length=MAX_LEN_NAME_PROFILE,
                            validators=[MinLengthValidator(MIN_LEN_NAME_PROFILE), validate_name]
                            )
    view = GenericRelation("ad.Views", related_query_name='profilee')
    images = GenericRelation("ad.Images",  related_query_name='profile')#object_id_field='profile_id',
    car = GenericRelation("ad.Car", related_query_name='profilee')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    bagsknapsacks = GenericRelation("ad.BagsKnapsacks", related_query_name='profilee')
    menclothes = GenericRelation("ad.MenClothes", related_query_name='profilee')
    menshoes = GenericRelation("ad.MenShoes", related_query_name='profilee')
    wemenclothes = GenericRelation("ad.WemenClothes", related_query_name='profilee')
    wemenshoes = GenericRelation("ad.WemenShoes", related_query_name='profilee')
    childclothesshoes = GenericRelation("ad.ChildClothesShoes", related_query_name='profilee')


    # location =  PointField()
    # views = GenericRelation("ad.Views", related_query_name='profile')

    def __str__(self):
        """Строковое представление объекта пользователя."""
        return str(self.user.email)

class OneTimeCode(models.Model):
    """Модель одноразового кода."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="onetimecodes", verbose_name=_("Пользователь"))
    code = models.CharField(_("Одноразовый код"), max_length=MAX_LEN_CODE)
    count_attempts = models.PositiveSmallIntegerField(_("Попытки"), default=0)
    count_send_code = models.PositiveSmallIntegerField(_("Количество повторных отправок кода"), default=0)
    updated_at = models.DateTimeField(_("Время обновления кода"), auto_now=True)
    created_at = models.DateTimeField(_("Время создания кода"), auto_now_add=True)

    class Meta:
        """Конфигурация модели одноразового кода."""
        ordering = ("id",)
        verbose_name = _("одноразовый код")
        verbose_name_plural = _("Одноразовые коды")

    def __str__(self):
        """Строковое представление одноразового кода."""
        return str(f"Код для {self.user.email}")

"""THis Notification model"""
class Notification(models.Model):
    text = models.CharField(max_length=400, **NULLABLE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='notification', **NULLABLE)
    key_to_recepient = models.CharField(max_length=50, verbose_name='Enter id or email of the user', **NULLABLE)
    promotion = GenericRelation("ad.Promotion", related_query_name='notifications')
    viewed = models.BooleanField(default=False, verbose_name='Прочитано/Не прочитано')


receiver(user_logged_in)
def count_notification(sender, user, request, **kwargs):
    """Получение количества непрочитанных уведомлений"""

    try:
        count = Notification.objects.filter(user=user, viewed=False).count()
        request.user_notification_count = count

        # Определение правильного имени на основе количества (сделал пока на первую десятку потом можно и на более расширить)
        match count:
            case 1:
                correct_name = 'новое сообщение'
            case 2 | 3 | 4:
                correct_name = 'новых сообщения'
            case _:
                correct_name = 'новых сообщений'
        request.correct_name = correct_name

    except Exception:
        request.user_notification_count = 0

user_logged_in.connect(count_notification)