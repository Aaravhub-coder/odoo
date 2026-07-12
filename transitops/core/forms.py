from django import forms
from .models import Vehicle, Driver

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['reg_no', 'name', 'vehicle_type', 'max_load', 'odometer', 'acquisition_cost', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_reg_no(self):
        """
        Enforces strict case-insensitive uniqueness on the vehicle registration number.
        Prevents duplicates like 'DL-1CA-1234' and 'dl-1ca-1234'.
        """
        reg_no = self.cleaned_data.get('reg_no')
        if reg_no:
            reg_no_upper = reg_no.strip().upper()
            
            # Check if another vehicle already has this registration number (excluding the current vehicle if updating)
            queryset = Vehicle.objects.filter(reg_no__iexact=reg_no_upper)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
                
            if queryset.exists():
                raise forms.ValidationError("A vehicle with this registration number already exists.")
            
            return reg_no_upper
        return reg_no


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_no', 'license_category', 'expiry_date', 'contact', 'safety_score', 'status']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_safety_score(self):
        """
        Validates that the safety score stays strictly within a bounded range of 0.0 to 100.0.
        """
        safety_score = self.cleaned_data.get('safety_score')
        if safety_score is not None:
            if safety_score < 0.0 or safety_score > 100.0:
                raise forms.ValidationError("Safety score must be a realistic rating between 0 and 100.")
        return safety_score

    def clean_license_no(self):
        """
        Sanitizes license numbers to be uppercase and stripped of accidental spaces.
        """
        license_no = self.cleaned_data.get('license_no')
        if license_no:
            license_no_upper = license_no.strip().upper()
            
            queryset = Driver.objects.filter(license_no__iexact=license_no_upper)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
                
            if queryset.exists():
                raise forms.ValidationError("A driver with this license number is already registered.")
                
            return license_no_upper
        return license_no