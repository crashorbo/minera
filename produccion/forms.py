from django import forms

from .models import Produccion


class ProduccionCreateForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ('minima_ley', 'maxima_ley',
                  'destino', 'tms', 'cargas')
        widgets = {
            'minima_ley': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'maxima_ley': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'tms': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'cargas': forms.Textarea(attrs={'class': 'd-none'})
        }
