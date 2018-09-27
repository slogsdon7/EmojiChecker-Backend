from django.core.management.base import BaseCommand, CommandError
from api.models import Schedule, Message, User

class Command(BaseCommand):


    def handle(self, *args, **options):
        scheduled = Schedule.objects.check_schedule()
        if scheduled.exists():
            results = scheduled[0].send_scheduled_message()
            print(results)



