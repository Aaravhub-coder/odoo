# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Vehicle Registry Paths
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/add/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_edit'),
    # Driver Registry Paths
    path('drivers/', views.DriverListView.as_view(), name='driver_list'),
    path('drivers/add/', views.DriverCreateView.as_view(), name='driver_create'),
    path('drivers/<int:pk>/edit/', views.DriverUpdateView.as_view(), name='driver_edit'),
    # Assets
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/add/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('drivers/', views.DriverListView.as_view(), name='driver_list'),
    path('drivers/add/', views.DriverCreateView.as_view(), name='driver_create'),
    path('drivers/<int:pk>/edit/', views.DriverUpdateView.as_view(), name='driver_edit'),
    # Trips
    path('trips/', views.TripListView.as_view(), name='trip_list'),
    path('trips/add/', views.TripCreateView.as_view(), name='trip_create'),
    path('trips/<int:pk>/<str:action>/', views.TripStatusTransitionView.as_view(), name='trip_action'),
    # Maintenance, Fuel, & Logs
    path('maintenance/add/', views.MaintenanceLogCreateView.as_view(), name='maintenance_create'),
    path('maintenance/<int:pk>/close/', views.CloseMaintenanceView.as_view(), name='maintenance_close'),
    path('fuel/add/', views.FuelLogCreateView.as_view(), name='fuel_create'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='expense_create'),
]