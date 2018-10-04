from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from api.sms import SMS


class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True, help_text="Use E164 Format")
    birth_date = models.DateField()
    is_current_subject = models.BooleanField(default=True)
    REQUIRED_FIELDS = ['birth_date', 'phone_number', 'first_name', 'last_name', 'email']

    def send_message(self, sms_obj):
        sent = sms_obj.send(self.phone_number)
        return sent


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



class ScheduleManager(models.Manager):
    def check_schedule(self):
        now = datetime.now()
        return self.model.objects.filter(sent=False).filter(send_at__lte=now)


class Schedule(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    send_at = models.DateTimeField(help_text="Use ISO 8601 format")
    sent = models.BooleanField(default=False)
    objects = ScheduleManager()

    def send_scheduled_message(self):
        users = User.objects.filter(is_current_subject=True).filter(is_staff=False)
        sms_obj = SMS(message=self.message.text)
        success_count = 0
        error_count = 0
        for user in users:
            sent = user.send_message(sms_obj)
            if sent:
                success_count+=1
                self.sendlog_set.create(user=user, success=True)
            else:
                error_count+=1
                self.sendlog_set.create(user=user,success=False, log_message="Error")

        return {'success_count': success_count,
                    'error_count': error_count}


class SendLog(models.Model):
    response = models.OneToOneField(Response, on_delete=models.CASCADE, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ts = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    log_message = models.TextField(null=True)









