from pesaje.forms import CargaContabilidadForm, CargaPagarForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, DetailView, View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http.response import JsonResponse
from django.utils.html import escape
from django.urls import reverse_lazy
import datetime
from django.db.models import Q

from .reportes import ReporteContabilidad, ReporteExcel
from pesaje.templatetags.pesaje_tags import numero_decimal
from pesaje.models import Carga
# Create your views here.


class ContabilidadIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'contabilidad/index.html'


class ContabilidadListJson(LoginRequiredMixin, BaseDatatableView):
    model = Carga
    columns = ['numero', 'numero_paleta' 'created', 'proveedor']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['numero', 'numero_paleta',
                     'created', 'proveedor', 'pagado']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        return Carga.objects.filter(laboratorio=True)

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'nombre':
            # escape HTML for security reasons
            return escape('{0} {1}'.format(row.nombres, row.apellidos))
        else:
            return super(ContabilidadListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        try:
            search = datetime.datetime.strptime(search, '%d/%m/%Y')
            search = search.strftime("%Y-%m-%d")
        except:
            print('fecha no valida')
        if search:
            q_search = Q(numero__contains=search) | Q(numero_paleta__contains=search) | Q(created__contains=search) | Q(
                proveedor__apellidos__contains=search) | Q(proveedor__nombres__contains=search)
            qs = qs.filter(q_search)
        # more advanced example using extra parameters
        filter_customer = self.request.GET.get('customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part) | Q(
                    customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                # escape HTML for security reasons
                '<div data-url="{}" class="itemid">{}</div>'.format(
                    reverse_lazy('contabilidad-update', kwargs={'pk': item.id}), item.numero),
                item.created.strftime("%d/%m/%Y"),
                '{} {}'.format(item.proveedor.apellidos,
                               item.proveedor.nombres),
                '<div class="text-end">{}</div>'.format(item.liquido_pagable),
                '<div class="pagado text-end">PAGADO</div>' if (
                    item.pagado) else '<div class="por-pagar text-end">POR PAGAR</div>'
            ])
        return json_data


class ContabilidadUpdateView(LoginRequiredMixin, UpdateView):
    model = Carga
    form_class = CargaContabilidadForm
    template_name = 'contabilidad/update.html'

    def get(self, request, *args, **kwargs):
        carga = Carga.objects.get(id=self.kwargs['pk'])
        if carga.pagado:
            return redirect('contabilidad-carga-view', pk=carga.id)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        model = form.save(commit=False)
        model.total_descuento = model.penalizacion_cu_soluble + model.anticipo + \
            model.equipo_pesado + model.balanza + model.volqueta + \
            model.analisis_laboratorio + model.otros_descuentos
        model.liquido_pagable = model.valor_reposicion - model.total_descuento
        model.save()
        return JsonResponse({"message": "Datos de Pesaje editado con exito", "descuentos": numero_decimal(model.total_descuento), "pagable": numero_decimal(model.liquido_pagable)}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class ContabilidadPagarView(LoginRequiredMixin, UpdateView):
    model = Carga
    form_class = CargaPagarForm
    template_name = 'contabilidad/pagar.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.pagado = True
        model.save()
        return redirect('contabilidad-carga-view', pk=model.id)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class ContabilidadCargaView(LoginRequiredMixin, DetailView):
    model = Carga
    template_name = 'contabilidad/detail.html'


class ReporteBoletaView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        carga = Carga.objects.get(id=self.kwargs['pk'])
        if carga.pesaje:
            return ReporteContabilidad(carga).reporte_boleta()
        return ReporteContabilidad(carga).reporte_boleta()


class ReportePorPagar(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        carga = Carga.objects.filter(pagado=False)
        return ReporteExcel(carga).reporte_por_pagar()
