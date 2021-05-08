from conductor.models import Vehiculo
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.views.generic import TemplateView, FormView, ListView, View, DetailView, UpdateView, DeleteView
# Create your views here.
from user.utils import get_numeracion
from .models import Carga, Destare
from .forms import CargaForm, CargaTaraForm, DestareForm
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
        model.peso_neto = model.peso_bruto - model.peso_tara
        model.peso_neto_tn = model.peso_neto/1000
        if model.peso_bruto > 0:
            model.pesaje_bruto = True
        if model.peso_tara > 0:
            model.pesaje_tara = True
        if model.pesaje_bruto and model.pesaje_tara:
            model.pesaje = True
        model.save()
        return JsonResponse({"message": "Datos de Pesaje registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class PesajeEditView(LoginRequiredMixin, UpdateView):
    model = Carga
    form_class = CargaTaraForm
    template_name = 'pesaje/edit.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.peso_neto = model.peso_bruto - model.peso_tara
        model.peso_neto_tn = model.peso_neto/1000
        if model.peso_bruto > 0:
            model.pesaje_bruto = True
        if model.peso_tara > 0:
            model.pesaje_tara = True
        if model.pesaje_bruto and model.pesaje_tara:
            model.pesaje = True
        model.save()
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
            'fi', today)
        fecha_fin = self.request.GET.get(
            'ff', today)
        return Carga.objects.filter(created__date__range=(fecha_inicio, fecha_fin)).order_by('-created')


class PesajeSearchListView(LoginRequiredMixin, ListView):
    model = Carga
    template_name = 'pesaje/list.html'

    def get_queryset(self):
        search = self.request.GET.get(
            'search', '')

        return Carga.objects.filter(Q(proveedor__nombres__icontains=search) | Q(proveedor__apellidos__icontains=search) | Q(proveedor__numero_documento__icontains=search) | Q(numero__icontains=search)).order_by('-created')


class PesajeReporteBrutoView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        carga = Carga.objects.get(id=self.kwargs['pk'])
        return ReporteCarga(carga).reporte_peso_bruto()


class PesajeReporteNetoView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        carga = Carga.objects.get(id=self.kwargs['pk'])
        return ReporteCarga(carga).reporte_peso_neto()


class PesajeBuscarTara(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        today = datetime.date.today()
        try:
            destare = Destare.objects.get(
                created__date=today, vehiculo=self.request.GET.get('id', ''))
            tara = destare.peso
        except Destare.DoesNotExist:
            tara = 0
        return JsonResponse({"message": "Datos de Pesaje editado con exito", "tara": tara}, status=200)


class PesajeDeleteView(DeleteView):
    model = Carga
    template_name = 'pesaje/delete.html'

    def post(self, *args, **kwargs):
        carga = Carga.objects.get(id=self.kwargs['pk'])
        carga.delete()
        print(self.kwargs['pk'])
        return JsonResponse({"message": "Se ha eliminado la carga con exito"}, status=200)


class DestareView(LoginRequiredMixin, FormView):
    form_class = DestareForm
    template_name = 'pesaje/destare.html'

    def form_valid(self, form):
        today = datetime.date.today()
        model = form.save(commit=False)
        try:
            destare = Destare.objects.get(
                created__date=today, vehiculo=model.vehiculo)
            destare.peso = model.peso
            destare.save()
            print(destare.peso)
        except model.DoesNotExist:
            destare = None
            model.save()
        return JsonResponse({"message": "Datos de Destare guardado con exito"}, status=200)
