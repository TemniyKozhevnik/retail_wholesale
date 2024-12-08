from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser

# Регистрируем модель в админке:
admin.site.register(MyUser, UserAdmin) 
