from celery import shared_task
from .views import send_vendor_emails

@shared_task
def schedule_vendor_emails():
    send_vendor_emails.apply_async()
