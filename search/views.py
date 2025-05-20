from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UnifiedSearchForm
from .models import SearchLog
from employee_management.models import Employee
from asset_management.models import Asset
from warehouse_management.models import Warehouse
from vendorescalation_management.models import VendorEscalationManagement

@login_required
def unified_search(request):
    form = UnifiedSearchForm(request.GET or None)
    results = None
    related_data = []

    if form.is_valid():
        field = form.cleaned_data['field']
        query = form.cleaned_data['query']
        
        # Log the search
        SearchLog.objects.create(
            query=query,
            field=field,
            user=request.user
        )
        
        # Search based on selected field
        if field == 'emp_number':
            results = Employee.objects.filter(emp_number=query)
        elif field == 'alias':
            results = Employee.objects.filter(alias__icontains=query)
        elif field == 'region':
            results = Employee.objects.filter(region__icontains=query)
        elif field == 'email':
            results = Employee.objects.filter(email__icontains=query)
        elif field == 'date_joined':
            results = Employee.objects.filter(date_joined__date=query)
        
        # If results found, get related records and their fields
        if results and results.exists():
            employee = results.first()
            related_data = [
                ('Assets', Asset.objects.filter(employee=employee), [(field.name, field.verbose_name) for field in Asset._meta.fields]),
                ('Warehouse Records', Warehouse.objects.filter(employee=employee), [(field.name, field.verbose_name) for field in Warehouse._meta.fields]),
                ('Vendor Records', VendorEscalationManagement.objects.filter(employee=employee), [(field.name, field.verbose_name) for field in VendorEscalationManagement._meta.fields]),
            ]

    context = {
        'form': form,
        'results': results,
        'related_data': related_data,
    }
    return render(request, 'search/unified_search.html', context)
