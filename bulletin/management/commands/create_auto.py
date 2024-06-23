from django.core.management import BaseCommand
from ad.models import Auto
from users.models import Profile

 
def ff():
    
    profile_queryset = Profile.objects.all()
    profile1 = profile_queryset.get(id=6)
    profile2 = profile_queryset.get(id=5)
    # auto_list = [(), ()]
    profile_list = [profile1, profile2]
    mileage_list = [200000, 100000]
    transmission_list = ["AUTO", "MECHANICAL"]
    description_list = ["Very well car", "Much joy vehicle"]
    for i,m,t,d in zip(profile_list, mileage_list, transmission_list, description_list):
        Auto.objects.create(profile = i, mileage = m, transmission = t, description = d)
    
    # profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, **NULLABLE)
    # mileage = models.IntegerField()
    # transmission = models.CharField(_("Differ by transmission"), choices=BY_TRANSMISSION, **NULLABLE)
    # by_wheel_drive = models.CharField(_("Differ by wheel drive"), choices=BY_DRIVE, **NULLABLE)
    # engine_capacity = models.IntegerField(_("engine capacity"), validators=[MinValueValidator(0), MaxValueValidator(10000)], **NULLABLE)
    # engine_power = models.IntegerField(_("engine power in horse power"), validators=[MinValueValidator(0), MaxValueValidator(900)], **NULLABLE) 
    # fuel_consumption = models.IntegerField(_("fuel consumption per 100 km"), validators=[MinValueValidator(1), MaxValueValidator(40)], **NULLABLE)
    # location = models.CharField(_("location"), max_length=160, **NULLABLE)
    # type = models.CharField(_("Differ by type"), choices=BY_TYPE, **NULLABLE)
    # colour = models.CharField(_("Differ by colour"), choices=BY_COLOUR, **NULLABLE)
    # fuel = models.CharField(_("Differ by fuel"), choices=BY_FUEL, **NULLABLE)
    # add_parametres =  models.CharField(_("additional"), max_length=150, **NULLABLE)
    # description = models.CharField(_("Description"), max_length=2000)
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()