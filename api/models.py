from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField





class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True, help_text="Use E164 Format")
    birth_date = models.DateField()

    REQUIRED_FIELDS = ['birth_date', 'phone_number', 'first_name', 'last_name', 'email']


class Emoji(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.TextField(null=True, blank=True)
    emoji = models.CharField(max_length=2, help_text='The actual emoji 💩')

    def __str__(self):
        return self.emoji + ' - ' + self.name



class Message(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True)
    created = models.DateField(auto_now_add=True)
    text = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.ForeignKey(Emoji, on_delete=models.DO_NOTHING)
    ts = models.DateTimeField(auto_now_add=True)


class Schedule(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    send_at = models.DateTimeField()
    sent = models.BooleanField(default=False)


class SendLog(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ts = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    log_message = models.TextField(null=True)









