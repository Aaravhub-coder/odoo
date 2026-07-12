from django.contrib import admin

# Register your models here.
# core/admin.py
from django.contrib import admin
from .models import Vehicle, Driver, Trip, MaintenanceLog, FuelLog, Expense

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'name', 'vehicle_type', 'max_load', 'odometer', 'status')
    list_filter = ('status', 'vehicle_type')
    search_fields = ('reg_no', 'name')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_no', 'license_category', 'expiry_date', 'safety_score', 'status')
    list_filter = ('status', 'license_category')
    search_fields = ('name', 'license_no')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'destination', 'vehicle', 'driver', 'cargo_weight', 'status')
    list_filter = ('status',)
    search_fields = ('source', 'destination', 'vehicle__reg_no', 'driver__name')

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'cost', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('vehicle__reg_no', 'description')

@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'liters', 'cost', 'date')
    list_filter = ('date',)
    search_fields = ('vehicle__reg_no',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'expense_type', 'amount', 'date')
    list_filter = ('expense_type', 'date')
    search_fields = ('vehicle__reg_no', 'remarks')