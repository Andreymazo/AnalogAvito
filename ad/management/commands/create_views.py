from django.core.management import BaseCommand
from ad.models import Car, Views, IP
from users.models import Profile
from django.contrib.contenttypes.models import ContentType



def ff():
    """Создаем просмотр на объявление автомобиль юзера по ip"""
    ip_instance = IP.objects.first()# решили пока без привязки к айпи делать
    car_instance = Car.objects.first()
    content_type = ContentType.objects.get_for_model(car_instance)
    # view_instance = Views.objects.get_or_create(content_type=content_type, object_id=car_instance.id, ip=ip_instance)
    view_instance = Views(content_object=car_instance)
    view_instance.save()
class Command(BaseCommand):
# kill -9 $(lsof -t -i:8000)
    def handle(self, *args, **options):
        ff()