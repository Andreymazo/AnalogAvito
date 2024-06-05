
from django.core.management import BaseCommand
from config.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL
from django.conf import settings

 #note settings is an object , hence you cannot import its contents

# settings.configure()

 #note LANGUAGES is a tuple of tuples



 #use lang_dict for your query.

 
def ff():
    lang_dict = dict(settings.LANGUAGES)
    # user = CustomUser.objects.all().get(pk=17)
    # print(CodeCustomuser.objects.filter(customuser_id=user.id).exists())
    # code_user = user.codecustomuser.name
    print (lang_dict)
    
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()

