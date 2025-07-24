import random
import time
from django.core.cache import cache


def create_auth_code(phone):
    code = '{:04d}'.format(random.randint(0, 9999))
    cache.set(f'auth_code_{phone}', code, timeout=120)
    time.sleep(2)
    return code