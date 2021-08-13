from django.forms.forms import Form
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, ListView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic.edit import DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.urls import reverse
from django.utils.crypto import get_random_string

from .forms import ColorEditForm, CotizacionForm, CustomUserCreationForm, CustomUserEditForm, CustomUserUpdateForm, DestinoCreateForm, DestinoProduccionCreateForm, FactorCreateForm, LaboratorioCreateForm, GeneradorCreateForm, OrigenCreateForm
from .models import Codigo, Cotizacion, CustomUser, DestinoProduccion, Factor, Generador, Parametro, Destino, Laboratorio, Origen
from .reportes import ReporteGenerador
# Create your views here.


class ConfiguracionView(LoginRequiredMixin, TemplateView):
    template_name = 'configuracion/index.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'user/profile.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Perfil actualizado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user/list.html'


class CreateUserView(LoginRequiredMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = 'user/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Usuario registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class UserEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'user/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Informacion de Usuario editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class ParametroView(LoginRequiredMixin, TemplateView):
    template_name = 'parametro/index.html'


class UbicacionView(LoginRequiredMixin, TemplateView):
    template_name = 'parametro/ubicacion.html'


class LaboratorioView(LoginRequiredMixin, TemplateView):
    template_name = 'parametro/laboratorio.html'


class CotizacionCreateView(LoginRequiredMixin, FormView):
    form_class = CotizacionForm
    template_name = 'cotizacion/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Cotizacion registrada con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class CotizacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizacion/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Cotizacion Editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class CotizacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Cotizacion
    template_name = 'cotizacion/delete.html'

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return JsonResponse({"message": "Cotizacion Eliminada con exito"}, status=200)


class CotizacionListJson(LoginRequiredMixin, BaseDatatableView):
    model = Cotizacion
    columns = ['fecha_inicio', 'fecha_fin', 'valor_oficial', 'valor_pagable']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['fecha_inicio', 'fecha_fin',
                     'valor', 'valor_oficial', 'valor_pagable']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'user':
            # escape HTML for security reasons
            return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
        else:
            return super(CotizacionListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(valor__icontains=search)

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
                escape(item.fecha_inicio.strftime("%d/%m/%Y")),
                # escape HTML for security reasons
                escape(item.fecha_fin.strftime("%d/%m/%Y")),
                '<div class="text-end">{}</div>'.format(item.valor_pagable),
                '<div class="text-end">{}</div>'.format(item.valor_oficial),
                '<div class="text-end cotizacion-options"><i data-url="{}" class="bi bi-pencil-square"></i><i data-url="{}" class="bi bi-trash ms-2"></i></div>'.format(
                    reverse('cotizacion-edit', kwargs={'pk': item.id}), reverse('cotizacion-delete', kwargs={'pk': item.id}))
            ])
        return json_data


class OrigenListView(LoginRequiredMixin, ListView):
    model = Origen
    template_name = 'origen/list.html'


class OrigenCreateView(LoginRequiredMixin, FormView):
    form_class = OrigenCreateForm
    template_name = 'origen/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Origen registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class OrigenUpdateView(LoginRequiredMixin, UpdateView):
    model = Origen
    form_class = OrigenCreateForm
    template_name = 'origen/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Origen editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class DestinoListView(LoginRequiredMixin, ListView):
    model = Destino
    template_name = 'destino/list.html'


class DestinoCreateView(LoginRequiredMixin, FormView):
    form_class = DestinoCreateForm
    template_name = 'destino/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Destino registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class DestinoUpdateView(LoginRequiredMixin, UpdateView):
    model = Destino
    form_class = DestinoCreateForm
    template_name = 'destino/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Destino editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class DestinoProduccionListView(LoginRequiredMixin, ListView):
    model = DestinoProduccion
    template_name = 'destinoproduccion/list.html'


class DestinoProduccionCreateView(LoginRequiredMixin, FormView):
    form_class = DestinoProduccionCreateForm
    template_name = 'destinoproduccion/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Destino Produccion registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class DestinoProduccionUpdateView(LoginRequiredMixin, UpdateView):
    model = DestinoProduccion
    form_class = DestinoProduccionCreateForm
    template_name = 'destinoproduccion/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Destino Produccion editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class LaboratorioListView(LoginRequiredMixin, ListView):
    model = Laboratorio
    template_name = 'laboratorio/list.html'


class LaboratorioCreateView(LoginRequiredMixin, FormView):
    form_class = LaboratorioCreateForm
    template_name = 'laboratorio/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Laboratorio registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class LaboratorioUpdateView(LoginRequiredMixin, UpdateView):
    model = Laboratorio
    form_class = LaboratorioCreateForm
    template_name = 'laboratorio/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Laboratorio editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class GeneradorCreateView(LoginRequiredMixin, FormView):
    form_class = GeneradorCreateForm
    template_name = 'generador/create.html'

    def form_valid(self, form):
        model = form.save()
        i = 0
        while i < model.cantidad:
            codigo = Codigo()
            codigo.numero = get_random_string(length=8).upper()
            codigo.cod_externo = get_random_string(length=8).upper()
            codigo.cod_proveedor = get_random_string(length=8).upper()
            codigo.cod_testigo = get_random_string(length=8).upper()
            codigo.cod_bolsa = get_random_string(length=8).upper()
            codigo.generador = model
            codigo.save()
            i = i + 1
        return JsonResponse({"message": "Codigos generados con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class GeneradorPrintView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        codigos = Codigo.objects.filter(generador=self.kwargs['pk'])
        return ReporteGenerador(codigos).generar_reporte_generador()


class GeneradorPrintExcel(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        codigos = Codigo.objects.filter(generador=self.kwargs['pk'])
        return ReporteGenerador(codigos).generar_codigos_excel()


class GeneradorListJson(LoginRequiredMixin, BaseDatatableView):
    model = Generador
    columns = ['created', 'cantidad']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['created', 'cantidad']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'user':
            # escape HTML for security reasons
            return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
        else:
            return super(CotizacionListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(created__icontains=search)

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
                escape(item.created.strftime("%d/%m/%Y")),
                '<div class="text-end">{}</div>'.format(item.cantidad),
                # escape HTML for security reasons
                '<div class="text-end cotizacion-options"><a href="{}"><i class="fa fa-file-excel-o ms-2"></i></a><i data-url="{}" class="bi bi-printer ms-2"></i></div>'.format(
                    reverse('generador-reporte-excel', kwargs={'pk': item.id}), reverse('generador-reporte', kwargs={'pk': item.id}))
            ])
        return json_data


class CodigoAutoComplete(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        q = self.request.GET['q']
        object_list = Codigo.objects.filter(utilizado=False)
        filtered_object_list = object_list
        if len(q) > 0:
            filtered_object_list = object_list.filter_on_search(q)
        qs = filtered_object_list
        qs = self.get_results(qs)
        return JsonResponse({
            'results': qs
        }, content_type='application/json')

    def get_results(self, results):
        return [dict(id=x.id, text='{}'.format(x.numero)) for x in results]


class FactorListView(LoginRequiredMixin, ListView):
    model = Factor
    template_name = 'factor/list.html'


class FactorCreateView(LoginRequiredMixin, FormView):
    form_class = FactorCreateForm
    template_name = 'factor/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Factor registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class FactorUpdateView(LoginRequiredMixin, UpdateView):
    model = Factor
    form_class = FactorCreateForm
    template_name = 'factor/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Factor editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)
