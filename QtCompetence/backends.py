from django.conf import settings
from django.contrib.auth.backends import BaseBackend,ModelBackend
from django.contrib.auth.hashers import check_password
from QtCompetence.models import *
from django.db.models import Q

class QtCompetenceBackend(ModelBackend):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, username=None, password=None):
        login_valid = is_user.objects.filter(Q(user_name=username)&Q(password=password)).exists()
        if login_valid:
            if is_user.objects.filter(Q(user_name=username) & Q(is_admin=True)).exists():
                return is_user.objects.get(user_name=username)
            else:
                return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return is_user.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    # def _get_is_user_permissions(self, user_obj):
    #     return user_obj.user_permissions.all()
    
    
    # def get_user_permissions(self, user_obj, obj=None):
    #     """
    #     Return a set of permission strings the user `user_obj` has from their
    #     `user_permissions`.
    #     """
    #     return self._get_permissions(user_obj, obj, 'is_user')
