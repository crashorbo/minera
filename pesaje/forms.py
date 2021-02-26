from django import forms
from dal import autocomplete

from .models import Carga
from proveedor.models import Proveedor
from conductor.models import Vehiculo


class CargaForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label="Seleccionar Proveedor", widget=autocomplete.ModelSelect2(
        url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Vehiculo", widget=autocomplete.ModelSelect2(
        url='vehiculo-autocomplete', attrs={'class': 'form-control'}))
    carguio = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Carguio", widget=autocomplete.ModelSelect2(
        url='carguio-autocomplete', attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Carga
        fields = ('proveedor', 'vehiculo', 'carguio', 'peso_bruto',
                  'peso_neto', 'peso_tara', 'peso_neto_tn', 'origen', 'destino')
        widgets = {
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
            'peso_bruto': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso_tara': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_neto_tn': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }


class CargaTaraForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label="Seleccionar Proveedor", widget=autocomplete.ModelSelect2(
        url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Vehiculo", widget=autocomplete.ModelSelect2(
        url='vehiculo-autocomplete', attrs={'class': 'form-control'}))
    carguio = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Carguio", widget=autocomplete.ModelSelect2(
        url='carguio-autocomplete', attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Carga
        fields = ('proveedor', 'vehiculo', 'carguio', 'peso_bruto',
                  'peso_neto', 'peso_tara', 'peso_neto_tn', 'origen', 'destino')
        widgets = {
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
            'peso_bruto': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_tara': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_neto_tn': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }
