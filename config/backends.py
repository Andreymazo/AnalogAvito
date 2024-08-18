# from django.conf import settings
# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User


# class SettingsBackend(BaseBackend):
#     """
#     Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

#     Use the login name and a hash of the password. For example:

#     ADMIN_LOGIN = 'admin'
#     ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
#     """

#     # def authenticate(self, request, username=None, password=None):
#     #     login_valid = settings.ADMIN_LOGIN == username
#     #     pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
#     #     if login_valid and pwd_valid:
#     #         try:
#     #             user = User.objects.get(username=username)
#     #         except User.DoesNotExist:
#     #             # Create a new user. There's no need to set a password
#     #             # because only the password from settings.py is checked.
#     #             user = User(username=username)
#     #             user.is_staff = True
#     #             user.is_superuser = True
#     #             user.save()
#     #         return user
#     #     return None

#     def get_user(self, email):
#         try:
#             return User.objects.get(email=email)
#         except User.DoesNotExist:
#             return None
# from django.contrib.auth.models import User

###############################################
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from config.settings import BACKEND_SESSION_KEY
from django.db.utils import load_backend
class SettingsBackend:
    """
    Custom authentication backend.

    Allows users to log in using their email address.
    """
    
    def authenticate(request, email=None):
        """
        Overrides the authenticate method to allow users to log in using their email address.
        """
        User = get_user_model()
        print("--------req email  ffffffffffff  ---------------", request, email)
       
        # try:
        #     user = User.objects.get(email=email)
        #     user_id = request.session[user.id]
        #     backend_path = request.session[BACKEND_SESSION_KEY]
        #     backend = load_backend(backend_path)
        #     # user = backend.get_user(user_id) or AnonymousUser()
        # except KeyError:
        #     user = AnonymousUser()
        # return user
        try:
            user = User.objects.get(email=email)
            user.is_active=True
            user.save()
            request.session["user_id"]=user.id
            return user
            
            # if user.check_password(password):
            #     return user
            # return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Overrides the get_user method to allow users to log in using their email address.
        """
        
        User = get_user_model()
        print('user_id================', user_id)
        try:
            print('User.objects.get(pk=id_)', User.objects.get(pk=user_id))
            user = User.objects.get(pk=user_id)
            user.is_active=True
            user.save()
            return user
        except User.DoesNotExist:
            return None
    # @staticmethod
    # def get_user(id_):
    #     User = get_user_model()
    #     print('user_id================', id_, 'self===============', User)
    #     try:
    #         print('User.objects.get(pk=id_)', User.objects.get(pk=id_))
    #         user = User.objects.get(pk=id_)
    #         user.is_active=True
    #         user.save()
    #         return user # <-- tried to get by email here
    #     except User.DoesNotExist:
    #         return None
####################################
# class SettingsBackend(object):
#     User = get_user_model()
#     @staticmethod
#     def authenticate(request, email=None):
#         print('email =========', email)
#         User = get_user_model()
#         try:
#             return User.objects.get(email=email)
#             # if user.check_password(password):
#             #     return user
#         except User.DoesNotExist:
#             return None

#     @staticmethod
#     def get_user(id_):
#         User = get_user_model()
#         print('user_id================', id_, 'self===============', User)
#         try:
#             print('User.objects.get(pk=id_)', User.objects.get(pk=id_))
#             return User.objects.get(pk=id_) # <-- tried to get by email here
#         except User.DoesNotExist:
#             return None