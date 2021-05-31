from decimal import Decimal
from user.models import Codigo, Cotizacion, Factor
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, DetailView, View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http.response import JsonResponse
from django.utils.html import escape
from django.urls import reverse_lazy
from django.db.models import Q
from django.forms import modelformset_factory
import datetime

from pesaje.models import Carga, Muestra
from pesaje.forms import CargaLaboratorioForm, MuestraForm


class LaboratorioIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'laboratorio/index.html'


class LaboratorioListJson(LoginRequiredMixin, BaseDatatableView):
    model = Carga
    columns = ['numero', 'numero_paleta' 'created']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['numero', 'numero_paleta', 'created']

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
            return super(LaboratorioListJson, self).render_column(row, column)

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
            q_search = Q(numero__contains=search) | Q(
                numero_paleta__contains=search) | Q(created__contains=search) | Q(muestra__codigo__contains=search)
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
                    reverse_lazy('laboratorio-update', kwargs={'pk': item.id}), item.numero),
                item.numero_paleta,
                item.created.strftime("%d/%m/%Y")
            ])
        return json_data


class LaboratorioUpdateView(LoginRequiredMixin, UpdateView):
    model = Carga
    form_class = CargaLaboratorioForm
    template_name = 'laboratorio/update.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        today = datetime.date.today()
        if not model.pagado:
            cotizacion = Cotizacion.objects.filter(
                fecha_inicio__lte=today, fecha_fin__gte=today)
            if cotizacion:
                model.cotizacion = cotizacion[0].valor_pagable
                model.tms = model.peso_neto_tn*(100 - model.h2o)/100
                if model.porcentaje_tamanos > 4:
                    model.tms_neta = model.tms - \
                        (model.tms * model.porcentaje_tamanos)/100
                else:
                    model.tms_neta = model.tms
                if model.cobre_soluble > 800:
                    model.tms_penalizar = model.tms_neta
                else:
                    model.tms_penalizar = 0
                model.tms_pagar = round(
                    model.tms_neta - model.tms_penalizar, 2)
                model.finos_gr = model.tms_pagar * model.au
                model.finos_oz = model.finos_gr / 31.1035
                if model.tipo_carga == 'LAMA' and model.au < 3:
                    model.finos_gr_recup = 0
                else:
                    factor = Factor.objects.filter(
                        rango_inferior__lte=model.au, rango_superior__gte=model.au)
                    if factor:
                        model.finos_gr_recup = round(factor[0].factor_recuperacion *
                                                     model.finos_gr, 2)
                model.calculo_regalia = model.finos_oz * model.cotizacion * 6.96
                if model.tipo_carga == 'LAMA' and model.au < 3:
                    model.recu_planta = 0
                else:
                    if model.tipo_carga == 'NORMAL' and model.au < 1:
                        model.recu_planta = 0
                    else:
                        factor = Factor.objects.filter(
                            rango_inferior__lte=model.au, rango_superior__gte=model.au)
                        if factor:
                            model.recu_planta = factor[0].factor_recuperacion * \
                                model.finos_oz

                model.valor_venta = round(
                    model.cotizacion * model.recu_planta * 6.96 * 0.94, 0)

                if model.au >= 10:
                    model.costo_tratamiento = round(
                        model.valor_venta * 0.52, 0)
                else:
                    model.costo_tratamiento = round(
                        model.valor_venta * 0.50, 0)
                model.total_liquidacion_prov = model.valor_venta - model.costo_tratamiento

                if model.recu_planta <= 0:
                    model.regalia = 0
                else:
                    if model.au >= 1 and model.au <= 2:
                        model.regalia = round(
                            model.calculo_regalia * 0.042 * 0.9, 0)
                    else:
                        model.regalia = round(
                            model.calculo_regalia * 0.042 * 1, 0)

                if model.cobre_soluble >= 150 and model.cobre_soluble <= 800:
                    model.penalizacion_cu_soluble = round(
                        (0.0089 * model.cobre_soluble - 1.325) * 30 * model.tms_pagar, 0)
                else:
                    model.penalizacion_cu_soluble = 0
                model.valor_reposicion = model.total_liquidacion_prov - model.regalia
                model.liquido_pagable = model.valor_reposicion - \
                    model.total_descuento - model.cobre_soluble
                model.save()
            return JsonResponse({"message": "Datos del Laboratorio editado con exito"}, status=200)
        return JsonResponse({"message": "Este laboratorio ya no puede ser modificado"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class LaboratorioGenerarView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        codigo = Codigo.objects.get(id=request.POST['codigo'])
        codigo.utilizado = True
        carga = Carga.objects.get(id=self.kwargs.get("pk"))
        muestra = Muestra(nombre="LABORATORIO EXTERNO",
                          carga=carga, codigo=codigo.cod_externo, css_class='muestra-ext')
        muestra.save()
        muestra = Muestra(nombre="PROVEEDOR", carga=carga,
                          codigo=codigo.cod_proveedor, css_class='muestra-prov')
        muestra.save()
        muestra = Muestra(nombre="TESTIGO", carga=carga,
                          codigo=codigo.cod_testigo, css_class='muestra-test')
        muestra.save()
        muestra = Muestra(nombre="BOLSA", carga=carga,
                          codigo=codigo.cod_bolsa, css_class='muestra-bol')
        muestra.save()
        return redirect('muestras-list', pk=carga.id)


class MuestrasListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        muestras = Muestra.objects.filter(carga__id=self.kwargs.get("pk"))
        return render(request, "laboratorio/muestras.html", {'muestras': muestras})


class MuestraUpdateView(LoginRequiredMixin, UpdateView):
    model = Muestra
    form_class = MuestraForm
    template_name = 'laboratorio/update-muestra.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Datos de Muestra guardado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)
