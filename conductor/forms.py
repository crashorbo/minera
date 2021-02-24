from django import forms

from .models import Vehiculo


class VehiculoCreateForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ('nombres', 'apellidos', 'numero_documento',
                  'telefono', 'placa', 'marca', 'modelo', 'descripcion', 'tipo')
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'placa': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
            'marca': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
            'tipo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }
