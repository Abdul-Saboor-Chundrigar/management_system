from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Attachment
from employee_management.models import Employee
from asset_management.models import Asset
from warehouse_management.models import Warehouse
from vendorescalation_management.models import VendorEscalationManagement
from django.http import HttpResponse
import io
from django.db.models import Q

def attachment_list(request):
    # Handle attachment search
    attachment_query = request.GET.get('attachment_query', '')
    attachments = Attachment.objects.select_related('employee').all()
    if attachment_query:
        attachments = attachments.filter(
            Q(filename__icontains=attachment_query) |
            Q(description__icontains=attachment_query) |
            Q(employee__emp_number__icontains=attachment_query)
        )

    record_details = []
    for attachment in attachments:
        if attachment.employee:
            employee_records = Employee.objects.filter(emp_number=attachment.employee.emp_number)
            assets = Asset.objects.filter(employee=attachment.employee)
            warehouses = Warehouse.objects.filter(employee=attachment.employee)
            vendors = VendorEscalationManagement.objects.filter(employee=attachment.employee)
            
            employee_data = []
            for emp in employee_records:
                fields = {field.verbose_name: getattr(emp, field.name) for field in emp._meta.fields if field.name not in ['id']}
                employee_data.append(fields)
            
            asset_data = []
            for asset in assets:
                fields = {field.verbose_name: getattr(asset, field.name) for field in asset._meta.fields if field.name not in ['id', 'employee']}
                asset_data.append(fields)
            
            warehouse_data = []
            for wh in warehouses:
                fields = {field.verbose_name: getattr(wh, field.name) for field in wh._meta.fields if field.name not in ['id', 'employee']}
                warehouse_data.append(fields)
            
            vendor_data = []
            for vendor in vendors:
                fields = {field.verbose_name: getattr(vendor, field.name) for field in vendor._meta.fields if field.name not in ['id', 'employee']}
                vendor_data.append(fields)
            
            record_details.append({
                'attachment': attachment,
                'employee': attachment.employee,
                'employee_data': employee_data,
                'asset_data': asset_data,
                'warehouse_data': warehouse_data,
                'vendor_data': vendor_data,
            })
        else:
            record_details.append({
                'attachment': attachment,
                'employee': None,
                'employee_data': [],
                'asset_data': [],
                'warehouse_data': [],
                'vendor_data': [],
            })

    # Handle employee search
    search_query = request.GET.get('search_query', '')
    search_results = []
    if search_query:
        search_results = Employee.objects.filter(
            Q(emp_number__icontains=search_query) | Q(name__icontains=search_query)
        )

    return render(request, 'file_attachment/list.html', {
        'record_details': record_details,
        'search_query': search_query,
        'search_results': search_results,
        'attachment_query': attachment_query,
    })

def add_attachment(request, emp_number):
    try:
        employee = Employee.objects.get(emp_number=emp_number)
    except Employee.DoesNotExist:
        messages.error(request, f'Employee with emp_number {emp_number} does not exist.')
        return redirect('file_attachment:attachment_list')
    
    if request.method == 'POST':
        description = request.POST.get('description')
        file = request.FILES.get('file')
        
        if not description or not file:
            messages.error(request, 'Description and file are required.')
            return render(request, 'file_attachment/form.html', {'mode': 'Add', 'employee': employee})
        
        # Check for duplicate attachment
        if Attachment.objects.filter(filename=file.name, employee=employee).exists():
            messages.error(request, f'An attachment with filename "{file.name}" already exists for this employee.')
            return render(request, 'file_attachment/form.html', {'mode': 'Add', 'employee': employee})
        
        try:
            attachment = Attachment(
                filename=file.name,
                description=description,
                file_data=file.read(),
                employee=employee
            )
            attachment.full_clean()
            attachment.save()
            messages.success(request, 'Attachment added successfully!')
            return redirect('file_attachment:attachment_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'file_attachment/form.html', {'mode': 'Add', 'employee': employee})
    
    return render(request, 'file_attachment/form.html', {'mode': 'Add', 'employee': employee})

def edit_attachment(request, id):
    attachment = get_object_or_404(Attachment, id=id)
    
    if request.method == 'POST':
        description = request.POST.get('description')
        file = request.FILES.get('file')
        
        if not description:
            messages.error(request, 'Description is required.')
            return render(request, 'file_attachment/form.html', {'mode': 'Edit', 'attachment': attachment})
        
        attachment.description = description
        if file:
            # Check for duplicate filename with same employee
            if Attachment.objects.filter(filename=file.name, employee=attachment.employee).exclude(id=attachment.id).exists():
                messages.error(request, f'An attachment with filename "{file.name}" already exists for this employee.')
                return render(request, 'file_attachment/form.html', {'mode': 'Edit', 'attachment': attachment})
            attachment.filename = file.name
            attachment.file_data = file.read()
        
        try:
            attachment.full_clean()
            attachment.save()
            messages.success(request, 'Attachment updated successfully!')
            return redirect('file_attachment:attachment_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'file_attachment/form.html', {'mode': 'Edit', 'attachment': attachment})
    
    return render(request, 'file_attachment/form.html', {'mode': 'Edit', 'attachment': attachment})

def download_attachment(request, id):
    attachment = get_object_or_404(Attachment, id=id)
    response = HttpResponse(attachment.file_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{attachment.filename}"'
    return response

def delete_attachment(request, id):
    attachment = get_object_or_404(Attachment, id=id)
    attachment.delete()
    messages.success(request, 'Attachment deleted successfully!')
    return redirect('file_attachment:attachment_list')
