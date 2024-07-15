from django.core.management import BaseCommand
from ad.models import Card
from users.models import Profile
from map.models import Marker

 
def ff():
    """Создаем две карты, сделает по наименьшему количеству уникального параметра, например локация уникальна и если их 2 всего, то и карт две"""
    profile_queryset = Profile.objects.all()
    profile1 = profile_queryset.get(id=6)
    profile2 = profile_queryset.get(id=5)
    profile_list = [profile1, profile2]
    marker_queryset=Marker.objects.all()
    marker1 = marker_queryset.get(id=1)
    marker2 = marker_queryset.get(id=2)
    marker_list= [marker1, marker2]
    price_list=[100, 200]
    description_list = ["Very well card", "Much joy card"]
    for i,m,t,d in zip(profile_list, marker_list, price_list, description_list):
        card_instance, created = Card.objects.get_or_create(profile = i, marker = m, price = t, description = d)
class Command(BaseCommand):
# kill -9 $(lsof -t -i:8000)
    def handle(self, *args, **options):
        ff()