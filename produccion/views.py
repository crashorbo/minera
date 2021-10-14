from django.contrib.auth.mixins import LoginRequiredMixin
from produccion.models import Produccion
from django.http.response import JsonResponse
from pesaje.models import Carga
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, View

from produccion.forms import ProduccionCreateForm
from produccion.reportes import reporte_produccion

# Create your views here.


class ProduccionIndexView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        objetos = Produccion.objects.all().order_by('-created')
        return render(self.request, 'produccion/index.html', {'objetos': objetos})


class ProduccionNuevoView(LoginRequiredMixin, FormView):
    form_class = ProduccionCreateForm
    template_name = 'produccion/nuevo.html'

    def form_valid(self, form):
        model = form.save()
        cargas = model.cargas.split(",")
        for carga in cargas:
            aux = Carga.objects.get(pk=carga)
            aux.produccion = model
            aux.save()
        return redirect('produccion-cargas-view', model.id)


class ProduccionView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        produccion = Produccion.objects.get(pk=self.kwargs['pk'])
        return render(self.request, 'produccion/lista-cargas-ver.html', {'produccion': produccion})


class ProduccionCargasView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        min = self.kwargs['min']
        max = self.kwargs['max']
        pag = self.kwargs['pagado']
        if pag == 1:
            cargas = Carga.objects.filter(
                laboratorio=True, pagado=True, produccion=None, au__range=(min, max))
        else:
            cargas = Carga.objects.filter(
                laboratorio=True, produccion=None, au__range=(min, max))
        return render(self.request, 'produccion/lista-cargas-ajax.html', {'cargas': cargas})


class ProduccionEntregaView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        carga = Carga.objects.get(pk=self.kwargs['pk'])
        if carga.estado_produccion:
            carga.estado_produccion = False
        else:
            carga.estado_produccion = True
        carga.save()
        return JsonResponse({"message": "Datos de Pesaje registrado con exito"}, status=200)


class ProduccionCargaRemoveView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        carga = Carga.objects.get(pk=self.kwargs['pk'])
        carga.produccion = None;
        carga.save()
        return JsonResponse({"message": "Carga Eliminada de Produccion con exito"}, status=200)
class ReporteProduccion(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        produccion = Produccion.objects.get(pk=self.kwargs['pk'])
        return reporte_produccion(produccion)
