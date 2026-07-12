from django.db import models
from django.core.validators import MinValueValidator

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ON_TRIP', 'On Trip'),
        ('IN_SHOP', 'In Shop'),
        ('RETIRED', 'Retired'),
    ]
    
    reg_no = models.CharField(max_length=50, unique=True, help_text="Unique Registration Number")
    name = models.CharField(max_length=100, help_text="Vehicle Name/Model")
    vehicle_type = models.CharField(max_length=50, help_text="e.g., Van, Truck, Prime Mover")
    max_load = models.FloatField(validators=[MinValueValidator(0.0)], help_text="Maximum load capacity in kg")
    odometer = models.IntegerField(validators=[MinValueValidator(0)], help_text="Current odometer reading in km")
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2, help_text="Purchase cost of the vehicle")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return f"{self.name} ({self.reg_no}) - {self.status}"


class Driver(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ON_TRIP', 'On Trip'),
        ('OFF_DUTY', 'Off Duty'),
        ('SUSPENDED', 'Suspended'),
    ]

    name = models.CharField(max_length=100)
    license_no = models.CharField(max_length=50, unique=True)
    license_category = models.CharField(max_length=50, help_text="e.g., Heavy Commercial, Light Motor Vehicle")
    expiry_date = models.DateField(help_text="Driver's license validity expiry date")
    contact = models.CharField(max_length=20)
    safety_score = models.FloatField(default=100.0, help_text="Safety performance score out of 100")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return f"{self.name} (Lic: {self.license_no}) - {self.status}"


class Trip(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('DISPATCHED', 'Dispatched'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='trips')
    cargo_weight = models.FloatField(validators=[MinValueValidator(0.0)], help_text="Weight of cargo in kg")
    distance = models.FloatField(validators=[MinValueValidator(0.0)], help_text="Planned distance in km")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip {self.id}: {self.source} ➔ {self.destination} ({self.status})"


class MaintenanceLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_logs')
    description = models.TextField(help_text="Details of the maintenance or repair work performed")
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if maintenance is currently active")
    is_active = models.BooleanField(default=True, help_text="True means the vehicle is currently in shop")

    def __str__(self):
        status_str = "Active" if self.is_active else "Closed"
        return f"Maintenance for {self.vehicle.reg_no} ({status_str})"


class FuelLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_logs')
    liters = models.FloatField(validators=[MinValueValidator(0.0)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    date = models.DateField()

    def __str__(self):
        return f"Fuel Log {self.id}: {self.liters}L for {self.vehicle.reg_no}"


class Expense(models.Model):
    EXPENSE_TYPES = [
        ('TOLL', 'Toll'),
        ('FINE', 'Fine/Challan'),
        ('PERMIT', 'State Permit'),
        ('OTHER', 'Other Operational Cost'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='expenses')
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    date = models.DateField()
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_expense_type_display()} - {self.amount} ({self.vehicle.reg_no})"