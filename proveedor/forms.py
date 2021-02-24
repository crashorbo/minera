from django import forms

from .models import Proveedor


class ProovedorCreateForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ('nombres', 'apellidos', 'numero_documento',
                  'direccion', 'telefono')
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control form-control-sm'})
        }
