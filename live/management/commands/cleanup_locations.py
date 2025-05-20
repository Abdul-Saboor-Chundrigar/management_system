# live/management/commands/cleanup_locations.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from live.models import UserLocation
from datetime import timedelta

class Command(BaseCommand):
    help = 'Cleans up old location records'

    def handle(self, *args, **options):
        # Delete records older than 30 days
        cutoff = timezone.now() - timedelta(days=30)
        count, _ = UserLocation.objects.filter(timestamp__lt=cutoff).delete()
        
        # Keep only latest record per user per day
        from django.db.models import Max
        latest_ids = UserLocation.objects.values(
            'user_id',
            timestamp_date=models.functions.TruncDate('timestamp')
        ).annotate(max_id=Max('id')).values_list('max_id', flat=True)
        
        extra_count, _ = UserLocation.objects.exclude(id__in=latest_ids).delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Deleted {count} old records and {extra_count} duplicates'
            )
        )
