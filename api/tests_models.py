from django.test import TestCase
from api.models import Schedule, Message, User
from datetime import datetime
from api.sms import SMS
from api.tests import appUser


class TestSchedule(TestCase):
    def setUp(self):
        msg = Message.objects.create(text="test", name="test", description="test")
        user = User.objects.create(**appUser)
        Schedule.objects.create(message=msg, send_at=datetime.now())

    def test_check_schedule(self):
        schedule = Schedule.objects.check_schedule()
        self.assertEqual(schedule[0].message.text, 'test')

    def test_send_message(self):
        schedule = Schedule.objects.check_schedule()[0]
        result = schedule.send_scheduled_message()
        self.assertEqual(result['success_count'], 1)


class TestUser(TestCase):
    def setUp(self):
        pass

    def test_send_message(self):
        user = User.objects.create(**appUser)
        sms_obj = SMS(message="test")
        result = user.send_message(sms_obj)
        self.assertEqual(result, True)



