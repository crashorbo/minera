import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views.generic import TemplateView, FormView, ListView, View, DetailView, UpdateView
# Create your views here.
from user.utils import get_numeracion
from .models import Carga
from .forms import CargaForm, CargaTaraForm
from .reportes import ReporteCarga


class PesajeIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'pesaje/index.html'


class PesajeDetailView(DetailView):
    model = Carga
    template_name = 'pesaje/detalle.html'


class PesajeCreateView(LoginRequiredMixin, FormView):
    form_class = CargaForm
    template_name = 'pesaje/create.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.numero = get_numeracion(1)
        model.usuario = self.request.user
        model.save()
        return JsonResponse({"message": "Datos de Pesaje registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class PesajeTaraView(LoginRequiredMixin, UpdateView):
    model = Carga
    form_class = CargaTaraForm
    template_name = 'pesaje/tara.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.pesaje = True
        model.peso_neto = model.peso_bruto - model.peso_tara
        model.peso_neto_tn = model.peso_neto/1000
        model.save()
        return JsonResponse({"message": "Datos de Pesaje editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class PesajeEditView(LoginRequiredMixin, FormView):
    model = Carga
    form_class = CargaForm
    template_name = 'pesaje/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Datos de Pesaje editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class PesajeListView(LoginRequiredMixin, ListView):
    model = Carga
    template_name = 'pesaje/list.html'

    def get_queryset(self):
        today = datetime.date.today()
        fecha_inicio = self.request.GET.get(
            'fecha_inicio', today)
        fecha_fin = self.request.GET.get(
            'fecha_fin', today)
        return Carga.objects.filter(created__date__range=(fecha_inicio, fecha_fin))


class PesajeReporteView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        carga = Carga.objects.get(id=self.kwargs['pk'])
        if carga.pesaje:
            return ReporteCarga(carga).reporte_peso_neto()
        return ReporteCarga(carga).reporte_peso_bruto()
