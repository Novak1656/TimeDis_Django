from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('pass_recovery/', pass_recovery, name='pass_recovery'),
    path('user_settings/', user_settings, name='user_settings'),
]
