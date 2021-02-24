from django import forms
from dal import autocomplete

from .models import Carga
from proveedor.models import Proveedor
from conductor.models import Vehiculo


class CargaForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label="Seleccionar Paciente", widget=autocomplete.ModelSelect2(
        url='proveedor-autocomplete', attrs={'class': 'form-control form-control-sm'}))
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Vehiculo", widget=autocomplete.ModelSelect2(
        url='vehiculo-autocomplete', attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = Carga
        fields = ('proveedor', 'vehiculo', 'peso_bruto',
                  'peso_neto', 'peso_tara', 'destino')
        widgets = {
            'destino': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'peso_bruto': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'peso_tara': forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
        }
