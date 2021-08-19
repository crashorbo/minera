from django import forms

from .models import Produccion


class ProduccionCreateForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ('minima_ley', 'maxima_ley',
                  'destino', 'tms', 'cargas', 'total_cargas')
        widgets = {
            'minima_ley': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'maxima_ley': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end'}),
            'tms': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end', 'readonly': True}),
            'total_cargas': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end', 'readonly': True}),
            'cargas': forms.Textarea(attrs={'class': 'd-none'}),
            'destino': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }
