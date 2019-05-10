from workers import task

from api.models import Schedule


@task(schedule=60)
def poll_schedule():
    scheduled = Schedule.objects.check_schedule()
    if scheduled.exists():
        scheduled[0].send_scheduled_message()
