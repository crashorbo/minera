from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView

from produccion.forms import ProduccionCreateForm

# Create your views here.


class ProduccionIndexView(FormView):
    form_class = ProduccionCreateForm
    template_name = 'produccion/index.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        return redirect('')


class ProduccionNuevoView(TemplateView):
    template_name = 'produccion/nuevo.html'
