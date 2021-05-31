from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.


class ProduccionIndexView(TemplateView):
    template_name = 'produccion/index.html'


class ProduccionNuevoView(TemplateView):
    template_name = 'produccion/nuevo.html'
