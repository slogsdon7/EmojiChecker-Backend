import factory
from factory import Faker

from api.models import User, SendLog


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('free_email')
    email = Faker('free_email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    birth_date = Faker('date_of_birth')
    is_staff = False

    @factory.sequence
    def phone_number(n):
        a = n // 10000
        b = n % 10000
        return '+1%03d555%04d' % (a, b)


class SendLogFactory(factory.DjangoModelFactory):
    class Meta:
        model = SendLog
