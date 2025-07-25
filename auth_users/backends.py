from django.contrib.auth.backends import ModelBackend
from users.models import User

class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        phone = kwargs.get('phone_number') or username
        try:
            user = User.objects.get(phone_number=phone)
            return user
        except User.DoesNotExist:
            return None
