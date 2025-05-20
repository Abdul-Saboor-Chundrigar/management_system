from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Asset
from .forms import AssetForm

class AssetListView(ListView):
    model = Asset
    ordering = ['id']  # or any field, e.g., ['name', '-created_at']
    template_name = 'asset_management/asset_list.html'
    context_object_name = 'assets'
    paginate_by = 20

class AssetCreateView(CreateView):
    model = Asset
    ordering = ['id']  # or any field, e.g., ['name', '-created_at']
    form_class = AssetForm
    template_name = 'asset_management/asset_form.html'
    
    def get_success_url(self):
        return reverse_lazy('asset_management:asset_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context

class AssetUpdateView(UpdateView):
    model = Asset
    ordering = ['id']  # or any field, e.g., ['name', '-created_at']
    form_class = AssetForm
    template_name = 'asset_management/asset_form.html'
    success_url = reverse_lazy('asset_management:asset_list')

class AssetDetailView(DetailView):
    model = Asset
    ordering = ['id']  # or any field, e.g., ['name', '-created_at']
    template_name = 'asset_management/asset_detail.html'

class AssetDeleteView(DeleteView):
    model = Asset
    ordering = ['id']  # or any field, e.g., ['name', '-created_at']
    template_name = 'asset_management/asset_confirm_delete.html'
    success_url = reverse_lazy('asset_management:asset_list')

