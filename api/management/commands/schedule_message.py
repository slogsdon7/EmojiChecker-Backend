from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from api.models import Schedule


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Creates a scheduled event for every minute for the next 10000 minutes.
         Be very sure that SMS is not actually enabled when using this."""

        dt = datetime.now()
        td = timedelta(minutes=1)
        for i in range(10000):
            dt = dt + td
            s = Schedule(send_at=dt, message_id=1)
            s.save()
