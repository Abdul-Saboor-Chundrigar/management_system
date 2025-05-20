from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.apps import apps
from django.db.models import Q
from .models import EmailLog
from employee_management.models import Employee
from asset_management.models import Asset
from warehouse_management.models import Warehouse
from vendorescalation_management.models import VendorEscalationManagement
import logging
import smtplib

logger = logging.getLogger(__name__)

TEST_EMAIL = 'asaboorcai@gmail.com'

def send_emails(request):
    apps_to_models = {
        'employee_management': Employee,
        'asset_management': Asset,
        'warehouse_management': Warehouse,
        'vendorescalation_management': VendorEscalationManagement,
    }
    email_fields = {
        'employee_management': ['email'],
        'asset_management': [],  # Uses Employee.email via ForeignKey
        'warehouse_management': ['recepient_email', 'IT_email'],
        'vendorescalation_management': ['vendor_email', 'it_email'],
    }
    messages_templates = {
        'employee_management': "Your record, added in IT Management System",
        'asset_management': "Following hardware owned by you, in case any query contact local IT Support of your region",
        'warehouse_management': "Following hardware submitted in Warehouse, in case any query please contact local IT Support of your region",
        'vendorescalation_management': "Following complains need your immediate action, please expedite & rectify the issues at earliest",
    }
    fields_to_display = {
        'employee_management': [
            'id', 'emp_number', 'date_added', 'region', 'name', 'alias', 'email',
            'cell_phone', 'city', 'location', 'date_joined', 'comments'
        ],
        'asset_management': [
            'id', 'employee', 'device_type', 'region', 'date_assigned', 'brand', 'model',
            'serial_number', 'aims_tag', 'lcd_brand', 'lcd_model', 'lcd_serial',
            'lcd_aims_tag', 'cpu_brand', 'cpu_model', 'cpu_serial', 'cpu_aims_tag'
        ],
        'warehouse_management': [
            'id', 'employee', 'device_type', 'region', 'date_assigned', 'recepient_name',
            'recepient_email', 'recepient_cell', 'dispatcher', 'IT_email', 'IT_cell',
            'brand', 'model', 'serial_number', 'aims_tag', 'lcd_brand', 'lcd_model',
            'lcd_serial', 'lcd_aims_tag', 'cpu_brand', 'cpu_model', 'cpu_serial', 'cpu_aims_tag'
        ],
        'vendorescalation_management': [
            'id', 'date_created', 'vendor_name', 'vendor_email', 'employee', 'device_type',
            'brand', 'model', 'serial_number', 'aims_tag', 'lcd_brand', 'lcd_model',
            'lcd_serial', 'lcd_aims_tag', 'cpu_brand', 'cpu_model', 'cpu_serial',
            'cpu_aims_tag', 'issue_details', 'poc_name', 'it_email', 'poc_cell',
            'status', 'closure_date', 'closure_remarks'
        ],
    }
    headers = {
        'employee_management': [
            'ID', 'Employee Number', 'Date Added', 'Region', 'Name', 'Alias', 'Email',
            'Cell Phone', 'City', 'Location', 'Date Joined', 'Comments'
        ],
        'asset_management': [
            'ID', 'Employee Email', 'Device Type', 'Region', 'Date Assigned', 'Brand', 'Model',
            'Serial Number', 'AIMS Tag', 'LCD Brand', 'LCD Model', 'LCD Serial',
            'LCD AIMS Tag', 'CPU Brand', 'CPU Model', 'CPU Serial', 'CPU AIMS Tag'
        ],
        'warehouse_management': [
            'ID', 'Employee Email', 'Device Type', 'Region', 'Date Assigned', 'Recipient Name',
            'Recipient Email', 'Recipient Cell', 'Dispatcher', 'IT Email', 'IT Cell',
            'Brand', 'Model', 'Serial Number', 'AIMS Tag', 'LCD Brand', 'LCD Model',
            'LCD Serial', 'LCD AIMS Tag', 'CPU Brand', 'CPU Model', 'CPU Serial', 'CPU AIMS Tag'
        ],
        'vendorescalation_management': [
            'ID', 'Date Created', 'Vendor Name', 'Vendor Email', 'Employee Email', 'Device Type',
            'Brand', 'Model', 'Serial Number', 'AIMS Tag', 'LCD Brand', 'LCD Model',
            'LCD Serial', 'LCD AIMS Tag', 'CPU Brand', 'CPU Model', 'CPU Serial',
            'CPU AIMS Tag', 'Issue Details', 'POC Name', 'IT Email', 'POC Cell',
            'Status', 'Closure Date', 'Closure Remarks'
        ],
    }

    for app_name, model in apps_to_models.items():
        if app_name == 'vendorescalation_management':
            continue
        records = []
        if app_name == 'asset_management':
            records = model.objects.filter(employee__isnull=False).distinct()
        else:
            for field in email_fields[app_name]:
                records.extend(model.objects.exclude(**{field: ''}).exclude(**{field: None}).distinct())
        
        for record in records:
            email = TEST_EMAIL
            record_id = getattr(record, model._meta.pk.name)
            table_rows = ""
            for field in fields_to_display[app_name]:
                if field == 'employee':
                    value = record.employee.email if record.employee else 'N/A'
                else:
                    value = getattr(record, field) or 'N/A'
                table_rows += f"<tr><td>{field.replace('_', ' ').title()}</td><td>{value}</td></tr>"
            
            subject = f"Notification from {app_name}"
            body = f"""
            <html>
            <body>
                <p>Dear User,</p>
                <p>{messages_templates[app_name]}</p>
                <h3>Record Details</h3>
                <table border="1" style="border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th>Field</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                <p>Best regards,<br>Management System</p>
            </body>
            </html>
            """
            try:
                send_mail(
                    subject,
                    "This email contains HTML content. Please view it in an HTML-capable email client.",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message=body,
                    fail_silently=False,
                )
                EmailLog.objects.create(
                    recipient=email,
                    subject=subject,
                    body=body,
                    app_name=app_name,
                    record_id=str(record_id),
                )
                if hasattr(request, '_messages'):
                    messages.success(request, f"Email sent to {email} from {app_name}")
            except smtplib.SMTPException as e:
                logger.error(f"SMTP error sending email to {email} from {app_name}: {str(e)}")
                if hasattr(request, '_messages'):
                    messages.error(request, f"Failed to send email to {email} from {app_name}: SMTP error")
            except Exception as e:
                logger.error(f"Failed to send email to {email} from {app_name}: {str(e)}")
                if hasattr(request, '_messages'):
                    messages.error(request, f"Failed to send email to {email} from {app_name}")

    send_vendor_emails()
    if hasattr(request, '_messages'):
        messages.info(request, "Daily email for vendorescalation_management sent.")
    return redirect('email_management:email_log_list')

def send_vendor_emails():
    model = VendorEscalationManagement
    in_progress_records = model.objects.filter(status='In Progress').distinct()
    
    if not in_progress_records:
        logger.info("No In Progress vendor records found.")
        return
    
    fields = [
        'id', 'date_created', 'vendor_name', 'vendor_email', 'employee', 'device_type',
        'brand', 'model', 'serial_number', 'aims_tag', 'lcd_brand', 'lcd_model',
        'lcd_serial', 'lcd_aims_tag', 'cpu_brand', 'cpu_model', 'cpu_serial',
        'cpu_aims_tag', 'issue_details', 'poc_name', 'it_email', 'poc_cell',
        'status', 'closure_date', 'closure_remarks'
    ]
    headers = [
        'ID', 'Date Created', 'Vendor Name', 'Vendor Email', 'Employee Email', 'Device Type',
        'Brand', 'Model', 'Serial Number', 'AIMS Tag', 'LCD Brand', 'LCD Model',
        'LCD Serial', 'LCD AIMS Tag', 'CPU Brand', 'CPU Model', 'CPU Serial',
        'CPU AIMS Tag', 'Issue Details', 'POC Name', 'IT Email', 'POC Cell',
        'Status', 'Closure Date', 'Closure Remarks'
    ]
    
    table_rows = ""
    for record in in_progress_records:
        table_rows += "<tr>"
        for field in fields:
            if field == 'employee':
                value = record.employee.email if record.employee else 'N/A'
            else:
                value = getattr(record, field) or 'N/A'
            table_rows += f"<td>{value}</td>"
        table_rows += "</tr>"
    
    email = TEST_EMAIL
    subject = "Daily Summary: Pending Vendor Escalations"
    body = f"""
    <html>
    <body>
        <p>Dear User,</p>
        <p>Following complains need your immediate action, please expedite & rectify the issues at earliest</p>
        <h3>In Progress Vendor Escalations</h3>
        <table border="1" style="border-collapse: collapse;">
            <thead>
                <tr>
                    {' '.join(f'<th>{header}</th>' for header in headers)}
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        <p>Best regards,<br>Management System</p>
    </body>
    </html>
    """
    try:
        send_mail(
            subject,
            "This email contains HTML content. Please view it in an HTML-capable email client.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=body,
            fail_silently=False,
        )
        EmailLog.objects.create(
            recipient=email,
            subject=subject,
            body=body,
            app_name='vendorescalation_management',
            record_id='daily_summary',
        )
        logger.info(f"Daily vendor email sent to {email}")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error sending daily vendor email to {email}: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to send daily vendor email to {email}: {str(e)}")

def email_log_list(request):
    date_query = request.GET.get('date_query', '')
    logs = EmailLog.objects.all()
    if date_query:
        try:
            from datetime import datetime
            date = datetime.strptime(date_query, '%Y-%m-%d')
            logs = logs.filter(sent_at__date=date)
        except ValueError:
            if hasattr(request, '_messages'):
                messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
    return render(request, 'email_management/log_list.html', {
        'logs': logs,
        'date_query': date_query,
    })

def delete_email_log(request, id):
    log = get_object_or_404(EmailLog, id=id)
    if request.method == 'POST':
        log.delete()
        if hasattr(request, '_messages'):
            messages.success(request, 'Email log deleted successfully!')
        return redirect('email_management:email_log_list')
    return render(request, 'email_management/confirm_delete.html', {'log': log})
