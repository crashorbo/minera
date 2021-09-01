from django import forms
from dal import autocomplete
import datetime

from django.forms import fields, widgets

from .models import Carga, Muestra, Destare
from proveedor.models import Proveedor
from conductor.models import Vehiculo, Conductor


class CargaForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label="Seleccionar Proveedor", widget=autocomplete.ModelSelect2(
        url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    conductor_vehiculo = forms.ModelChoiceField(queryset=Conductor.objects.all(), empty_label="Seleccionar Conductor",
                                                widget=autocomplete.ModelSelect2(url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Vehiculo", widget=autocomplete.ModelSelect2(
        url='vehiculo-autocomplete', attrs={'class': 'form-control'}))
    equipo_carguio = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Carguio", widget=autocomplete.ModelSelect2(
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


class CargaEditForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = ('anticipo', 'equipo_pesado', 'balanza', 'volqueta',
                  'analisis_laboratorio', 'otros_descuentos', 'retencion_acuerdo_vol')
        widgets = {
            'anticipo': forms.NumberInput(attrs={'class': 'table-input'}),
            'equipo_pesado': forms.NumberInput(attrs={'class': 'table-input'}),
            'balanza': forms.NumberInput(attrs={'class': 'table-input'}),
            'volqueta': forms.NumberInput(attrs={'class': 'table-input'}),
            'analisis_laboratorio': forms.NumberInput(attrs={'class': 'table-input'}),
            'otros_descuentos': forms.NumberInput(attrs={'class': 'table-input'}),
            'retencion_acuerdo': forms.NumberInput(attrs={'class': 'table-input'}),
        }


class CargaTaraForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label="Seleccionar Proveedor", widget=autocomplete.ModelSelect2(
        url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    conductor_vehiculo = forms.ModelChoiceField(queryset=Conductor.objects.all(), empty_label="Seleccionar Conductor",
                                                widget=autocomplete.ModelSelect2(url='proveedor-autocomplete', attrs={'class': 'form-control'}))
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Vehiculo", widget=autocomplete.ModelSelect2(
        url='vehiculo-autocomplete', attrs={'class': 'form-control'}))
    equipo_carguio = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Carguio", widget=autocomplete.ModelSelect2(
        url='carguio-autocomplete', attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Carga
        fields = ('proveedor', 'vehiculo', 'equipo_carguio', 'peso_bruto', 'conductor_vehiculo',
                  'peso_neto', 'peso_tara', 'peso_neto_tn', 'origen', 'destino')
        widgets = {
            'origen': forms.Select(attrs={'class': 'form-control'}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
            'peso_bruto': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_tara': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'peso_neto_tn': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }


class CargaPaletaForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = ('numero_paleta', 'color', 'fecha_paleta')
        widgets = {
            'fecha_paleta': forms.DateInput(attrs={'class': 'form-control form-control-sm'}),
            'numero_paleta': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'color': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'}),
        }

        def __init__(self, *args, **kwargs):
            self.fields['fecha_paleta'].required = False
            super(CargaPaletaForm, self).__init__(*args, **kwargs)


class CargaLaboratorioForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = ('au', 'h2o', 'porcentaje_tamanos', 'fecha_muestreo',
                  'cobre_soluble', 'tipo_carga', 'observaciones', 'oro_soluble', 'ratio')
        widgets = {
            'au': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'h2o': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'porcentaje_tamanos': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'cobre_soluble': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'oro_soluble': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'ratio': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end', 'readonly': True}),
            'fecha_muestreo': forms.DateInput(attrs={'class': 'form-control form-control-sm text-center'}),
            'tipo_carga': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
        }


class CargaContabilidadForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = ('anticipo', 'equipo_pesado', 'balanza', 'volqueta',
                  'analisis_laboratorio', 'otros_descuentos', 'retencion_acuerdo_vol')
        widgets = {
            'anticipo': forms.NumberInput(attrs={'class': 'table-input'}),
            'equipo_pesado': forms.NumberInput(attrs={'class': 'table-input tooltip-box-carguio'}),
            'balanza': forms.NumberInput(attrs={'class': 'table-input'}),
            'volqueta': forms.NumberInput(attrs={'class': 'table-input tooltip-box-volqueta'}),
            'analisis_laboratorio': forms.NumberInput(attrs={'class': 'table-input'}),
            'otros_descuentos': forms.NumberInput(attrs={'class': 'table-input'}),
            'retencion_acuerdo': forms.NumberInput(attrs={'class': 'table-input'}),
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


class DestareForm(forms.ModelForm):
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Seleccionar Vehiculo", widget=autocomplete.ModelSelect2(
        url='vehiculo-autocomplete', attrs={'class': 'form-control'}))

    class Meta:
        model = Destare
        fields = ('vehiculo', 'peso')
        widgets = {
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }
