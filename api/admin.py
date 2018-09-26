from django.contrib import admin
from api.models import User, Emoji, Schedule, Message
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Emoji)
admin.site.register(Schedule)
admin.site.register(Message)