import random
import time
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SendAuthCodeView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        if not phone:
            return Response({'detail': 'Не отправлен номер'}, status=status.HTTP_400_BAD_REQUEST)
        code = '{:04d}'.format(random.randint(0, 9999))
        cache.set(f'auth_code_{phone}', code, timeout=120)
        time.sleep(2)
        return Response({'detail': f'auth_code-{code}'}, status=status.HTTP_200_OK)
