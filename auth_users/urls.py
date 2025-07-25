from django.urls import path
from . import views

urlpatterns = [
    #API
    path('auth_code/',views.SendAuthCodeView.as_view(), name='auth_code'),
    path('login/',views.ConfirmAuthCodeView.as_view(), name='login'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('invited_code/',views.InputAuthCodeView.as_view(), name='invited_code'),

    #HTML
    path('auth_code_html/',views.SendAuthCodeHTML, name='auth_code_html'),
    path('login_html/',views.ConfirmAuthCodeHTML, name='login_html'),
    path('profile_html/',views.profile_view, name='profile_html'),
]
