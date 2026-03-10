from django import forms
from django.contrib.auth.models import User
from .models import Farm, Crop, DiseaseReport

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'latitude', 'longitude', 'size_acres', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Farm Name'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': '41.8781'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': '-87.6298'}),
            'size_acres': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': '100'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
        }

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_type', 'planting_date', 'expected_harvest', 'area_acres', 'notes']
        widgets = {
            'crop_type': forms.Select(attrs={'class': 'form-control'}),
            'planting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_harvest': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'area_acres': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DiseaseReportForm(forms.ModelForm):
    class Meta:
        model = DiseaseReport
        fields = ['farm', 'crop', 'disease_name', 'description', 'severity', 'photo', 'latitude', 'longitude', 'affected_area']
        widgets = {
            'farm': forms.Select(attrs={'class': 'form-control'}),
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'disease_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Late Blight'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe symptoms and affected areas'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'affected_area': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Square meters'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter farms and crops to user's only
            self.fields['farm'].queryset = Farm.objects.filter(farmer=user)
            self.fields['crop'].queryset = Crop.objects.filter(farm__farmer=user)