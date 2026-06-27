from django.contrib import admin

from .models import CustomUser, CustomUserManager


admin.site.register(CustomUser)
admin.site.register(CustomUserManager)
