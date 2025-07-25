import random
import string
import time
from django.core.cache import cache

from users.models import User


def create_auth_code(phone):
    code = '{:04d}'.format(random.randint(0, 9999))
    cache.set(f'auth_code_{phone}', code, timeout=120)
    time.sleep(2)
    return code

def get_cache_code(phone):
    code_cache = cache.get(f'auth_code_{phone}')
    return code_cache

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def user_create(phone):
    user, created = User.objects.get_or_create(phone_number=phone)
    return user, created
