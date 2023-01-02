from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.sign_up, name='sign_up'),
    path('otp_validation', views.otp_validator, name='otp_validation'),
    path('login', views.login, name='login')
]