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
]