from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    ordering = ['id']  # or any field, e.g., ['name', '-created_at']
    template_name = 'employee_management/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20

class EmployeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Employee
    ordering = ['id']  # or any field, e.g., ['name', '-created_at']
    form_class = EmployeeForm
    template_name = 'employee_management/employee_form.html'
    #success_url = reverse_lazy('employee_list')
    success_url = reverse_lazy('employee_management:employee_list')
    permission_required = 'employee_management.add_employee'

class EmployeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Employee
    ordering = ['id']  # or any field, e.g., ['name', '-created_at']
    form_class = EmployeeForm
    template_name = 'employee_management/employee_form.html'
    #success_url = reverse_lazy('employee_list')
    success_url = reverse_lazy('employee_management:employee_list')
    permission_required = 'employee_management.change_employee'

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    ordering = ['id']  # or any field, e.g., ['name', '-created_at']
    template_name = 'employee_management/employee_detail.html'
    context_object_name = 'employee'

class EmployeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee_management/employee_confirm_delete.html'
    #success_url = reverse_lazy('employee_list')
    success_url = reverse_lazy('employee_management:employee_list')
    permission_required = 'employee_management.delete_employee'
