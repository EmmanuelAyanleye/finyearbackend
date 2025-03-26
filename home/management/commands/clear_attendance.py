from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import Attendance, Course

class Command(BaseCommand):
    help = 'Delete all attendance records or clean up orphaned records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--orphaned',
            action='store_true',
            help='Delete only orphaned attendance records (where course no longer exists)',
        )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                if options['orphaned']:
                    # Delete only orphaned records
                    deleted_count = Attendance.objects.filter(course__isnull=True).delete()[0]
                    message = f'Successfully deleted {deleted_count} orphaned attendance records'
                else:
                    # Delete all records
                    count = Attendance.objects.all().count()
                    confirm = input(f'Found {count} attendance records. Delete all? (yes/no): ')
                    
                    if confirm.lower() == 'yes':
                        deleted_count = Attendance.objects.all().delete()[0]
                        message = f'Successfully deleted {deleted_count} attendance records'
                    else:
                        message = 'Operation cancelled'
                        return self.stdout.write(self.style.WARNING(message))

                self.stdout.write(self.style.SUCCESS(message))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )