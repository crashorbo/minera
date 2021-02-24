from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views.generic import TemplateView, FormView
# Create your views here.

from .models import Carga
from .forms import CargaForm


class PesajeListView(LoginRequiredMixin, TemplateView):
    template_name = 'pesaje/index.html'


class PesajeCreateView(LoginRequiredMixin, FormView):
    form_class = CargaForm
    template_name = 'pesaje/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Datos de Pesaje editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)
