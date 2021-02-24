from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.urls import reverse
from django.db.models import Q
from django.http.response import JsonResponse

from .models import Vehiculo
from .forms import VehiculoCreateForm
# Create your views here.


class VehiculoTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'conductor/index.html'


class VehiculoListJson(LoginRequiredMixin, BaseDatatableView):
    model = Vehiculo
    columns = ['tipo', 'nombres', 'apellidos',
               'numero_documento', 'telefono', 'marca', 'modelo', 'placa']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['tipo', 'nombres', 'apellidos',
                     'numero_documento', 'telefono', 'marca', 'modelo', 'placa']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'nombre':
            # escape HTML for security reasons
            return escape('{0} {1}'.format(row.nombres, row.apellidos))
        else:
            return super(VehiculoListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            q_search = Q(nombres__contains=search) | Q(apellidos__contains=search) | Q(
                numero_documento__contains=search) | Q(telefono__contains=search) | Q(placa__contains=search)
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
                item.tipo,
                item.placa,
                item.marca,
                item.modelo,
                '{} {}'.format(item.apellidos, item.nombres),
                item.numero_documento,
                # escape HTML for security reasons
                escape(item.telefono),
                '<div class="text-end cotizacion-options"><i data-url="{}" class="bi bi-pencil-square"></i><i data-url="{}" class="bi bi-trash ms-2"></i></div>'.format(
                    reverse('vehiculo-edit', kwargs={'pk': item.id}), 'test2')
            ])
        return json_data


class VehiculoCreateView(LoginRequiredMixin, FormView):
    form_class = VehiculoCreateForm
    template_name = 'conductor/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Vehiculo registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class VehiculoEditView(LoginRequiredMixin, UpdateView):
    model = Vehiculo
    form_class = VehiculoCreateForm
    template_name = 'conductor/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Datos del Vehiculo editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)
