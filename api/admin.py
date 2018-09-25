from django.contrib import admin
from api.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.register(User, UserAdmin)