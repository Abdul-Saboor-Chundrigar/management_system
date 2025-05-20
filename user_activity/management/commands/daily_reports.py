from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from user_activity.models import LoginLogoutActivity

class Command(BaseCommand):
    help = 'Sends daily activity report'

    def handle(self, *args, **options):
        yesterday = timezone.now() - timedelta(days=1)
        
        stats = {
            'logins': LoginLogoutActivity.objects.filter(
                login_time__gte=yesterday
            ).count(),
            'unique_users': LoginLogoutActivity.objects.filter(
                login_time__gte=yesterday
            ).values('user').distinct().count(),
        }
        
        message = f"""
        Daily Activity Report:
        - Total logins: {stats['logins']}
        - Unique users: {stats['unique_users']}
        """
        
        send_mail(
            'Daily Activity Report',
            message,
            'asabooraiy@gmail.com',
            ['asaboorc@gmail.com'],
            fail_silently=False,
        )
        self.stdout.write("Report sent successfully")
