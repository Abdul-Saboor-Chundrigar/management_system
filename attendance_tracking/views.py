from django.db import models  # Add this import at the top
from django.views.generic import ListView, CreateView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from .models import Attendance
from django.views.generic import TemplateView
from django.db.models import Count, Sum, F
from .models import Attendance
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from authentication.mixins import AdminRequiredMixin
from django.core.exceptions import PermissionDenied
# attendance_tracking/views.py

class AttendanceReportView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance_tracking/attendance_report.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role != 'ADMIN':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        context['records'] = Attendance.objects.filter(
            check_in__date=context['today']
        ).select_related('user').order_by('user__username', 'check_in')
        return context

class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance_tracking/attendance_list.html'
    context_object_name = 'attendance_records'
    ordering = ['-check_in']
    paginate_by = 20

class AttendanceCheckInView(CreateView):
    model = Attendance
    fields = ['location', 'auth_method']
    template_name = 'attendance_tracking/check_in.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.check_in = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('attendance_tracking:attendance_list')  # Added namespace

class AttendanceCheckOutView(View):
    def get(self, request):
        last_checkin = Attendance.objects.filter(
            user=request.user, 
            check_out__isnull=True
        ).last()
        if last_checkin:
            last_checkin.check_out = timezone.now()
            last_checkin.save()
        return redirect('attendance_list')

class AttendanceReportView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance_tracking/attendance_report.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role != 'ADMIN':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
