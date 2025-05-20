from django.core.management.base import BaseCommand
from email_management.views import send_vendor_emails

class Command(BaseCommand):
    help = 'Send daily vendor escalation email'

    def handle(self, *args, **options):
        send_vendor_emails()
        self.stdout.write(self.style.SUCCESS('Daily vendor email sent successfully'))
