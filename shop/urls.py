from django.urls import path

from . import views

urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.login, name='login'),
    path('otp_verification', views.login, name='otp_verification')
]