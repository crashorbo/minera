from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
import datetime

from django import forms
from django.forms import widgets

from .models import Cotizacion, CustomUser, Destino, Parametro


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'rol', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'rol': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-sm'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control form-control-sm'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control form-control-sm'})


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name',
                  'email', 'photo', 'telefono')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'rol')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'rol': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ('fecha_inicio', 'fecha_fin', 'valor')
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'fecha form-control form-control-sm'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'fecha form-control form-control-sm'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
        }

    def __init__(self, *args, **kwargs):
        super(CotizacionForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].initial = datetime.datetime.now()
        self.fields['fecha_fin'].initial = datetime.datetime.now()


TIPO_MESES = (
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre'),
)


class ColorForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = ('nombre', 'valor')
        widgets = {
            'nombre': forms.Select(choices=TIPO_MESES, attrs={'class': 'form-select form-select-sm'}),
            'valor': forms.TextInput(attrs={'class': 'form-control form-control-sm color-picker'})
        }


class ColorEditForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = ('nombre', 'valor')
        widgets = {
            'nombre': forms.HiddenInput(),
            'valor': forms.TextInput(attrs={'class': 'form-control form-control-sm color-picker'})
        }


class DestinoCreateForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields = ('nombre',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm uppercase'})
        }
