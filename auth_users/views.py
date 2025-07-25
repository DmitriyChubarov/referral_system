
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from ref_sys_project.services import create_auth_code, get_cache_code, generate_invite_code, user_create
from users.models import User
from .serializers import ProfileSerializer


#API
class SendAuthCodeView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        if not phone:
            return Response({'detail': 'Не отправлен номер'}, status=status.HTTP_400_BAD_REQUEST)
        code = create_auth_code(phone)
        return Response({'auth_code': code}, status=status.HTTP_200_OK)
    
class ConfirmAuthCodeView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('code')
        if not phone or not code:
            return Response({'detail': 'Не отправлен номер или код'}, status=status.HTTP_400_BAD_REQUEST)
        code_cache = get_cache_code(phone)
        if not code_cache or code != code_cache:
            return Response({'detail': 'Код не подходит или закончилось время его действия'}, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = user_create(phone)

        if created:
            user.invite_code = generate_invite_code()
            user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key,
                        'invite_code': user.invite_code,
                        'created': created}, 
                        status=status.HTTP_200_OK)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
    
class InputAuthCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invited_code = request.data.get('invited_code')
        if not invited_code:
            return Response({'detail': 'Реферальный код не отправлен'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.invited_code:
            return Response({'detail': 'Вы уже вводили реферальный код'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.invite_code == invited_code:
            return Response({'detail': 'Нельзя вводить свой собственный код'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            User.objects.get(invite_code=invited_code)
        except User.DoesNotExist:
            return Response({'detail': 'Реферальный код не существует'}, status=status.HTTP_404_NOT_FOUND)
        
        request.user.invited_code = invited_code
        request.user.save()

        return Response({'detail': 'Реферальный успешно активирован'}, status=status.HTTP_200_OK)

    
#HTML
def SendAuthCodeHTML(request):
    if request.method=='POST':
        phone = request.POST['phone_number']
        if not phone:
            return render(request, 'auth.html', {'error': 'Не отправлен номер'})
        create_auth_code(phone)
        request.session['phone_number'] = phone
        return redirect('login_html')
    return render(request, 'auth.html')

def ConfirmAuthCodeHTML(request):
    phone = request.session.get('phone_number')
    code_cache = get_cache_code(phone)
    if request.method=='POST':
        code = request.POST.get('code')
        if not code:
            return render(request, 'login.html', {'code_cache': code_cache, 'error': 'Код не отправлен'})
        if not code_cache or code != code_cache:
            return render(request, 'login.html', {'code_cache': code_cache, 'error': 'Код не подходит'})
        
        user, created = user_create(phone)

        if created:
            user.invite_code = generate_invite_code()
            user.save()

        login(request, user)
        
        return redirect('profile_html')
    return render(request, 'login.html', {'code_cache': code_cache})

@login_required
def profile_view(request):
    user = request.user
    if request.method=='POST':
        invited_code = request.POST.get('invited_code')
        if not invited_code:
            return render(request, 'profile.html', {'user': user, 'error': 'Реферальный код не отправлен'})
        if user.invited_code:
            return render(request, 'profile.html', {'user': user, 'error': 'Вы уже вводили реферальный код'}) #удалить наверное
        if user.invite_code == invited_code:
            return render(request, 'profile.html', {'user': user, 'error': 'Нельзя вводить свой собственный код'}) 
        
        user.invited_code = invited_code
        user.save()
        
    users = User.objects.filter(invited_code=user.invite_code)

    return render(request, 'profile.html', {'user': user, 'users': users})



