from django.urls import path
from . import views

urlpatterns = [
    #API
    path('auth_code/',views.SendAuthCodeView.as_view(), name='auth_code'),

    #HTML
    path('auth_code_html/',views.SendAuthCodeHTML, name='auth_code_html'),

]
