from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Vehicle, Driver
from .forms import VehicleForm, DriverForm

# ==========================================
# VEHICLE REGISTRY MANAGEMENT VIEWS
# ==========================================

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'core/vehicle_list.html'
    context_object_name = 'vehicles'
    # Orders by registration number naturally
    ordering = ['reg_no'] 


class VehicleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm  # Wire up Member A's secure form validation rules
    template_name = 'core/vehicle_form.html'  # Use Member B's Tailwind layout shell
    success_url = reverse_lazy('core:vehicle_list')  # Redirect back to the inventory list
    
    # RBAC: Requires user to have the core database 'add_vehicle' standard permission
    permission_required = 'core.add_vehicle' 


class VehicleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm  # Uses same validation rules for safely processing asset updates
    template_name = 'core/vehicle_form.html'  # Reuses Member B's form view structural layout
    success_url = reverse_lazy('core:vehicle_list')
    
    # RBAC: Requires user to have the core database 'change_vehicle' standard permission
    permission_required = 'core.change_vehicle'


# ==========================================
# DRIVER REGISTRY MANAGEMENT VIEWS
# ==========================================

class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    template_name = 'core/driver_list.html'
    context_object_name = 'drivers'
    ordering = ['name']


class DriverCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Driver
    form_class = DriverForm
    template_name = 'core/driver_form.html'  # Member B can copy vehicle_form structure for this
    success_url = reverse_lazy('core:driver_list')
    
    permission_required = 'core.add_driver'


class DriverUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Driver
    form_class = DriverForm
    template_name = 'core/driver_form.html'
    success_url = reverse_lazy('core:driver_list')
    
    permission_required = 'core.change_driver'