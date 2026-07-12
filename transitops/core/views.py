from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Vehicle, Driver, Trip, MaintenanceLog, FuelLog, Expense
from .forms import VehicleForm, DriverForm, TripForm


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

class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'core/trip_list.html'
    context_object_name = 'trips'

class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'core/trip_form.html'
    success_url = reverse_lazy('core:trip_list')

class TripStatusTransitionView(LoginRequiredMixin, django.views.View):
    """Handles automation logic when changing trip states"""
    def post(self, request, pk, action):
        trip = get_object_or_404(Trip, pk=pk)
        vehicle = trip.vehicle
        driver = trip.driver

        if action == 'dispatch' and trip.status == 'DRAFT':
            trip.status = 'DISPATCHED'
            vehicle.status = 'ON_TRIP'
            driver.status = 'ON_TRIP'
        elif action == 'complete' and trip.status == 'DISPATCHED':
            trip.status = 'COMPLETED'
            vehicle.status = 'AVAILABLE'
            driver.status = 'AVAILABLE'
        elif action == 'cancel' and trip.status == 'DISPATCHED':
            trip.status = 'CANCELLED'
            vehicle.status = 'AVAILABLE'
            driver.status = 'AVAILABLE'
        
        trip.save()
        vehicle.save()
        driver.save()
        return redirect('core:trip_list')
    

class MaintenanceLogCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceLog
    fields = ['vehicle', 'description', 'cost', 'start_date', 'is_active']
    template_name = 'core/maintenance_form.html'
    success_url = reverse_lazy('core:vehicle_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Automation: Set vehicle status to In Shop when active log is created
        if self.object.is_active:
            self.object.vehicle.status = 'IN_SHOP'
            self.object.vehicle.save()
        return response

class CloseMaintenanceView(LoginRequiredMixin, django.views.View):
    def post(self, request, pk):
        log = get_object_or_404(MaintenanceLog, pk=pk)
        log.is_active = False
        log.end_date = timezone.now().date()
        log.save()
        
        # Automation: Restore vehicle status to Available unless Retired
        if log.vehicle.status != 'RETIRED':
            log.vehicle.status = 'AVAILABLE'
            log.vehicle.save()
        return redirect('core:vehicle_list')
    
class FuelLogCreateView(LoginRequiredMixin, CreateView):
    model = FuelLog
    fields = ['vehicle', 'liters', 'cost', 'date']
    template_name = 'core/fuel_form.html'
    success_url = reverse_lazy('core:vehicle_list')

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['vehicle', 'trip', 'expense_type', 'amount', 'date', 'remarks']
    template_name = 'core/expense_form.html'
    success_url = reverse_lazy('core:trip_list')