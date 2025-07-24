from django.urls import path
from . import views

urlpatterns = [
    path('auth_code/',views.SendAuthCodeView.as_view(), name='auth_code'),
]
