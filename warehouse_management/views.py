from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Warehouse
from .forms import WarehouseForm

class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'warehouse_management/warehouse_list.html'
    context_object_name = 'warehouse_items'
    paginate_by = 20

class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehouse_management/warehouse_form.html'
    success_url = reverse_lazy('warehouse_management:warehouse_list')

class WarehouseUpdateView(UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehouse_management/warehouse_form.html'
    success_url = reverse_lazy('warehouse_management:warehouse_list')

class WarehouseDetailView(DetailView):
    model = Warehouse
    template_name = 'warehouse_management/warehouse_detail.html'
    context_object_name = 'warehouse'

class WarehouseDeleteView(DeleteView):
    model = Warehouse
    template_name = 'warehouse_management/warehouse_confirm_delete.html'
    success_url = reverse_lazy('warehouse_management:warehouse_list')
