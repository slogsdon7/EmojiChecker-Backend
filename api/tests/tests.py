from datetime import datetime, timedelta
from unittest.mock import patch, Mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User, Schedule, Message, SendLog
from api.tests.factories import UserFactory

appUser = {
    'username' : 'app_user',
    'password': 'Pas$w0rd',
    'email' : 'test@test.com',
    'phone_number': "+16788888888",
    'first_name': 'app',
    'last_name': 'user',
    'birth_date': '1969-04-20',

}

staffUser={
    'username': 'staff_user',
    'password': appUser['password'],
    'email':    'staff@test.com',
    'phone_number': "+16789994444",
    'first_name': 'staff',
    'last_name': 'user',
    'birth_date': '1969-04-20',
    'is_staff': True}


class TestUserFactory(APITestCase):
    def test_factory(self):
        user = UserFactory()


class AppUserTestCase(APITestCase):
    """Extend this class when testing App User methods"""
    def setUp(self):
        self.user = User.objects.create_user(**appUser)
        self.client.force_authenticate(self.user)

class AdminUserTestCase(APITestCase):
    """Extend this class when testing Administration methods"""
    def setUp(self):
        user = UserFactory(is_staff=True)
        self.client.force_authenticate(user)


class ScheduleAdminTestCase(AdminUserTestCase):

    def test_list_view(self):
        url = reverse('schedule-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        user = User.objects.create(**appUser)
        msg = Message.objects.create(text='Test message', name='test')
        url = reverse('schedule-list')
        dt = datetime(2018, 11, 4, 12)
        data = {'send_at': dt.isoformat(), 'message': msg.id, 'users': [user.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        msg = Message.objects.create(text='Test message', name='test')
        schedule = Schedule.objects.create(send_at=datetime(2018, 11, 4, 12).isoformat(), message=msg)
        url = reverse('schedule-detail', args=(schedule.pk,) )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




class ScheduledUserTestCase(AppUserTestCase):


    def test_list_view(self):
        url = reverse('schedule-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class ResponseUserTestCase(AppUserTestCase):
    def setUp(self):
        super().setUp()
        self.send_log = SendLog(user=self.user, success=True, ts=datetime.now())
        self.send_log.save()

    def test_create(self):
        url = reverse('responses-list')
        data = {'emoji': 'Moon'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_expiration(self):
        user = UserFactory()
        self.client.logout()
        self.client.force_login(user)
        last_week = datetime.now() - timedelta(weeks=1)
        with patch('django.utils.timezone.now', Mock(return_value=last_week)):
            send_log = SendLog.objects.create(user=user, success=True, ts=datetime(2018, 11, 10))
        url = reverse('responses-list')
        data = {'emoji': 'Moon'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ResponseAdminTestCase(AdminUserTestCase):
    pass

class EmojiUserTestCase(AppUserTestCase):
    def test_create(self):
        url = reverse('emoji-list')
        data = {'name': 'Moon',
                'emoji': '🌚'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class EmojiAdminTestCase(AdminUserTestCase):
    def test_create(self):
        url = reverse('emoji-list')
        data = {'name': 'Moon',
                'emoji': '🌚'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
