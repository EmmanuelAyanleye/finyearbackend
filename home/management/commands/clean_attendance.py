from django.core.management.base import BaseCommand
from home.models import Attendance, Course

class Command(BaseCommand):
    help = 'Clean up orphaned attendance records'

    def handle(self, *args, **options):
        # Delete any attendance records where course doesn't exist
        deleted_count = Attendance.objects.filter(course__isnull=True).delete()[0]
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cleaned up {deleted_count} orphaned attendance records')
        )