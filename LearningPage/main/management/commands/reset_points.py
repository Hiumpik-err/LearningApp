from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Uzytkownik

class Command(BaseCommand):
    #Resets Daily points every day and Weekly points every Monday
    def handle(self, *args, **options):
        now = timezone.now()
        Uzytkownik.objects.update(daily_points = 0)
        self.stdout.write(self.style.SUCCESS(f'Daily points reset at {now}'))

        if now.weekday() == 0:
            Uzytkownik.objects.update(weekly_points = 0)
            self.stdout.write(self.style.SUCCESS("Monday detected: Weekly points reset!"))