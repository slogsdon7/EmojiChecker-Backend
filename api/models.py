from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField



class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True, help_text="Use E164 Format")
    birth_date = models.DateField()

    REQUIRED_FIELDS = ['birth_date', 'phone_number', 'first_name', 'last_name', 'email']


class Emoji(models.Model):
    name = models.CharField(max_length=30)

class Message(models.Model):
    name = models.CharField(max_length=255)
    text = models.CharField(max_length=140)

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.ForeignKey(Emoji, on_delete=models.DO_NOTHING)




