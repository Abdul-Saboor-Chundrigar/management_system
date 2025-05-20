from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import VendorEscalationManagement
from vendorescalation_management.models import VendorEscalationManagement
from .forms import VendorEscalationManagementForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class VendorEscalationManagementListView(LoginRequiredMixin, ListView):
    model = VendorEscalationManagement
    template_name = 'vendorescalation_management/vendor_list.html'
    context_object_name = 'escalations'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-date_created')

class VendorEscalationManagementDetailView(LoginRequiredMixin, DetailView):
    model = VendorEscalationManagement
    template_name = 'vendorescalation_management/vendor_detail.html'
    context_object_name = 'vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Context data:", context)
        return context

class VendorEscalationManagementCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = VendorEscalationManagement
    form_class = VendorEscalationManagementForm
    template_name = 'vendorescalation_management/vendor_form.html'
    success_url = reverse_lazy('vendorescalation_management:vendor_list')
    permission_required = 'vendorescalation_management.add_vendorescalation'

class VendorEscalationManagementUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = VendorEscalationManagement
    form_class = VendorEscalationManagementForm
    template_name = 'vendorescalation_management/vendor_form.html'
    success_url = reverse_lazy('vendorescalation_management:vendor_list')
    permission_required = 'vendorescalation_management.change_vendorescalation'

class VendorEscalationManagementDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = VendorEscalationManagement
    template_name = 'vendorescalation_management/vendor_confirm_delete.html'
    success_url = reverse_lazy('vendorescalation_management:vendor_list')
    context_object_name = 'vendor'
    permission_required = 'vendorescalation_management.delete_vendorescalation'
