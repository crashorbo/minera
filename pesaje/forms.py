from django import forms
from dal import autocomplete
from django.forms import widgets

from .models import Carga, Muestra
from proveedor.models import Proveedor
from conductor.models import Vehiculo, Conductor


class CargaForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label="Seleccionar Proveedor", widget=autocomplete.ModelSelect2(
        url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    conductor_vehiculo = forms.ModelChoiceField(queryset=Conductor.objects.all(), empty_label="Seleccionar Conductor",
                                                widget=autocomplete.ModelSelect2(url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Vehiculo", widget=autocomplete.ModelSelect2(
        url='vehiculo-autocomplete', attrs={'class': 'form-control'}))
    carguio = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Carguio", widget=autocomplete.ModelSelect2(
        url='carguio-autocomplete', attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Carga
        fields = ('proveedor', 'vehiculo', 'equipo_carguio', 'peso_bruto', 'conductor_vehiculo',
                  'peso_neto', 'peso_tara', 'peso_neto_tn', 'origen', 'destino', 'pesaje_bruto', 'pesaje_tara')
        widgets = {
            'pesaje_bruto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pesaje_tara': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'origen': forms.Select(attrs={'class': 'form-control'}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
            'peso_bruto': forms.NumberInput(attrs={'class': 'form-control input-selected', 'readonly': True}),
            'peso_tara': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_neto_tn': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }


class CargaTaraForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label="Seleccionar Proveedor", widget=autocomplete.ModelSelect2(
        url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    conductor_vehiculo = forms.ModelChoiceField(queryset=Conductor.objects.all(), empty_label="Seleccionar Conductor",
                                                widget=autocomplete.ModelSelect2(url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Vehiculo", widget=autocomplete.ModelSelect2(
        url='vehiculo-autocomplete', attrs={'class': 'form-control'}))
    carguio = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Carguio", widget=autocomplete.ModelSelect2(
        url='carguio-autocomplete', attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Carga
        fields = ('proveedor', 'vehiculo', 'equipo_carguio', 'peso_bruto', 'conductor_vehiculo',
                  'peso_neto', 'peso_tara', 'peso_neto_tn', 'origen', 'destino')
        widgets = {
            'pesaje_bruto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pesaje_tara': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'origen': forms.Select(attrs={'class': 'form-control'}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
            'peso_bruto': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_tara': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_neto_tn': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }


class CargaPaletaForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = ('numero_paleta', 'color')
        widgets = {
            'numero_paleta': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'color': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
        }


class CargaLaboratorioForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = ('au', 'h2o', 'porcentaje_tamanos',
                  'cobre_soluble', 'tipo_carga')
        widgets = {
            'au': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'h2o': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'porcentaje_tamanos': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'cobre_soluble': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'tipo_carga': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }


class CargaContabilidadForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = ('anticipo', 'equipo_pesado', 'balanza', 'volqueta',
                  'analisis_laboratorio', 'otros_descuentos')
        widgets = {
            'anticipo': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end descuento'}),
            'equipo_pesado': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end descuento'}),
            'balanza': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end descuento'}),
            'volqueta': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end descuento'}),
            'analisis_laboratorio': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end descuento'}),
            'otros_descuentos': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end descuento'}),
        }


class CargaPagarForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = ('pagado',)
        widgets = {
            'pagado': forms.HiddenInput(),
        }


class MuestraForm(forms.ModelForm):
    class Meta:
        model = Muestra
        exclude = ('carga', 'codigo', 'nombre', 'css_class',
                   'deleted', 'created', 'updated')
        widgets = {
            'malla_mas': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'malla_menos': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'ley_ponderada': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'nro_certif': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
            'laboratorio': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }
