from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage as DjangoEmail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmailMessage, EmailStorageQuota, EmailAttachment
from .forms import EmailForm, TestEmailForm
from posteio_integration.models import PosteIOConfig
from vendorescalation_management.models import VendorEscalationManagement
from warehouse_management.models import Warehouse
from asset_management.models import Asset
from employee_management.models import Employee
import imaplib
import email
from email.header import decode_header
from django.utils import timezone
from django.core.exceptions import ValidationError
import logging
import ssl
from django.contrib import messages
from email.mime.text import MIMEText
import smtplib
import logging


@login_required
def email_list(request):
    emails = EmailMessage.objects.filter(user=request.user).order_by('-sent_at', '-received_at')
    return render(request, 'custom_email_client/email_list.html', {'emails': emails})

@login_required
def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            recipient = form.cleaned_data['recipient']
            app_name = form.cleaned_data['app_name']
            vendor = form.cleaned_data['vendor']
            size_mb = (len(subject.encode()) + len(body.encode())) / (1024 * 1024)
            config = PosteIOConfig.objects.first()
            if not config:
                messages.error(request, "Poste.io configuration is missing. Please contact an admin.")
                return redirect('custom_email_client:email_list')
            email_message = EmailMessage(
                user=request.user,
                subject=subject,
                body=body,
                sender=config.default_from_email,
                recipient=recipient,
                size_mb=size_mb,
                app_name=app_name,
                vendor=vendor,
                is_sent=True
            )
            try:
                email_message.clean()
                django_email = DjangoEmail(
                    subject=subject,
                    body=body,
                    from_email=config.default_from_email,
                    to=[recipient]
                )
                for file in request.FILES.getlist('attachments'):
                    size_mb = file.size / (1024 * 1024)
                    email_message.size_mb += size_mb
                    email_message.clean()
                    django_email.attach(file.name, file.read(), file.content_type)
                django_email.send()
                email_message.save()
                for file in request.FILES.getlist('attachments'):
                    attachment = EmailAttachment(email=email_message, file=file)
                    attachment.save()
                messages.success(request, "Email sent successfully.")
                return redirect('custom_email_client:email_list')
            except Exception as e:
                messages.error(request, f"Failed to send email: {str(e)}")
    else:
        form = EmailForm()
    return render(request, 'custom_email_client/send_email.html', {'form': form})

@login_required
def receive_emails(request):
    config = PosteIOConfig.objects.first()
    if not config:
        messages.error(request, "Poste.io configuration is missing. Please contact an admin.")
        return redirect('custom_email_client:email_list')
    try:
        mail = imaplib.IMAP4_SSL(config.imap_host, config.imap_port)
        mail.login(config.imap_username or request.user.email, config.imap_password or '')
        mail.select('INBOX')
        _, data = mail.search(None, 'ALL')
        for num in data[0].split()[:10]:
            _, msg_data = mail.fetch(num, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(msg['subject'])[0]
            subject = subject.decode(encoding or 'utf-8') if isinstance(subject, bytes) else subject
            sender = msg['from']
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()
            size_mb = len(raw_email) / (1024 * 1024)
            email_message = EmailMessage(
                user=request.user,
                subject=subject,
                body=body,
                sender=sender,
                recipient=request.user.email,
                size_mb=size_mb,
                received_at=timezone.now(),
            )
            try:
                email_message.clean()
                email_message.save()
            except ValidationError:
                messages.warning(request, f"Skipped email '{subject}' due to storage limit.")
        mail.logout()
        messages.success(request, "Emails fetched successfully.")
    except Exception as e:
        messages.error(request, f"Failed to fetch emails: {str(e)}")
    return redirect('custom_email_client:email_list')


logger = logging.getLogger(__name__)

def test_email(request):
    logger.error("Entering test_email view")
    config = PosteIOConfig.objects.first()
    logger.error(f"PosteIOConfig: {config}")
    if not config:
        logger.error("No PosteIOConfig found")
        messages.error(request, "Poste.io configuration is missing. Please contact an admin.")
        return redirect('custom_email_client:email_list')
    
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        logger.error(f"POST data: recipient={recipient}, subject={subject}, body={body}")
        
        # Validate inputs
        if not all([recipient, subject, body]):
            logger.error("Missing required fields")
            messages.error(request, "All fields (recipient, subject, body) are required.")
            return render(request, 'custom_email_client/test_email.html', {})
        
        try:
            # Create unverified SSL context
            context = ssl._create_unverified_context()
            # Manual SMTP connection
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = config.default_from_email
            msg['To'] = recipient
            with smtplib.SMTP(config.smtp_host, config.smtp_port, context=context) as server:
                server.starttls(context=context)
                server.login(config.imap_username, config.imap_password)
                server.send_message(msg)
            # Log email in database
            EmailMessage.objects.create(
                sender=config.default_from_email,
                recipient=recipient,
                subject=subject,
                body=body,
                is_test=True
            )
            logger.error("Email sent successfully")
            messages.success(request, "Test email sent successfully")
            return redirect('custom_email_client:email_list')
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            messages.error(request, f"Failed to send email: {str(e)}")
    return render(request, 'custom_email_client/test_email.html', {})

@receiver(post_save, sender=Employee)
def send_employee_email(sender, instance, created, **kwargs):
    if created:
        config = PosteIOConfig.objects.first()
        if not config:
            return
        user = instance.created_by or User.objects.first()
        subject = f"New Employee: {instance.name}"
        body = f"Employee {instance.name} added."
        email_message = EmailMessage(
            user=user,
            subject=subject,
            body=body,
            sender=config.default_from_email,
            recipient=user.email,
            size_mb=(len(subject.encode()) + len(body.encode())) / (1024 * 1024),
            app_name='employee_management',
            is_sent=True
        )
        try:
            email_message.clean()
            send_mail(subject, body, config.default_from_email, [user.email])
            email_message.save()
        except Exception:
            pass
