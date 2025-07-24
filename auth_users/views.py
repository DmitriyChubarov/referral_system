from django.shortcuts import render
from ref_sys_project.services import create_auth_code
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#API
class SendAuthCodeView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        if not phone:
            return Response({'detail': 'Не отправлен номер'}, status=status.HTTP_400_BAD_REQUEST)
        code = create_auth_code(phone)
        return Response({'auth_code': code}, status=status.HTTP_200_OK)

#HTML
def SendAuthCodeHTML(request):
    if request.method=='POST':
        phone = request.POST['phone_number']
        code = create_auth_code(phone)
        return render(request, 'auth.html', {'code': code})
    return render(request, 'auth.html')